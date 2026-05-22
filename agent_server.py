#!/usr/bin/env python3
"""
MEW Agent Server — Claude runs as a real autonomous agent.
Receives commands from the browser, executes tools, streams results back.
"""

import os
import re
import uuid
import json
import subprocess
import threading
from datetime import datetime
from flask import Flask, request, Response
from flask_socketio import SocketIO, emit
import anthropic
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "mew_state.json")

# Server-side empire state
empire = {"companies": {}, "agents": {}, "tasks": {}}

def load_empire():
    global empire
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE) as f:
                empire = json.load(f)
    except Exception:
        pass

def save_empire():
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(empire, f)
    except Exception:
        pass

load_empire()

@app.route("/")
def serve_ui():
    """Serve the MEW interface with API key injected and socket pointed at this server."""
    html_path = os.path.join(BASE_DIR, "orchestrator.html")
    with open(html_path, encoding="utf-8") as f:
        html = f.read()

    api_key = os.getenv("ANTHROPIC_API_KEY", "")

    # Inject API key — replace the localStorage getter with the real key
    html = html.replace(
        "get apiKey(){ return localStorage.getItem('mew_key')||''; }",
        f"get apiKey(){{ return '{api_key}'; }}"
    )
    # Skip the setup screen
    html = html.replace("if(S.apiKey) launch();", "launch();")

    # Use the bundled socket.io served by Flask-SocketIO, not CDN
    html = html.replace(
        '<script src="https://cdn.socket.io/4.7.5/socket.io.min.js" crossorigin="anonymous"></script>',
        '<script src="/socket.io/socket.io.js"></script>'
    )

    # Connect socket to same origin (no hardcoded localhost URL needed)
    html = re.sub(
        r"io\('http://localhost:5001'[^)]*\)",
        "io()",
        html
    )

    return Response(html, mimetype="text/html")


AGENT_SYSTEM = """You are MEW — My Empire Wins. You are a fully autonomous AI agent running on the user's local machine with real execution capabilities.

You do not just talk — you ACT. When given a task, use your tools to actually execute it.

Your tools:
- execute_python: Write and run Python code. Use for data analysis, automation, scripts, calculations, file processing.
- execute_bash: Run shell commands. Use for file operations, git, running programs, system tasks, installs.
- write_file: Create or update any file on disk (code, configs, data, reports).
- read_file: Read any file's contents.
- http_request: Call any external API or URL. Use for fetching data, webhooks, integrations.

How to operate:
1. Receive a command from the user
2. Think about the best approach
3. Use tools to execute — write code, run it, check results
4. Chain tool calls as needed to complete the task
5. Report what you actually did and the results

You have access to the user's empire state (companies, agents, tasks). You can create files, run scripts, fetch data, automate workflows.

Be bold. Execute. Deliver results.

Working directory: /home/user/MEW/workspace"""

TOOLS = [
    {
        "name": "execute_python",
        "description": "Execute Python code on the local machine and return stdout/stderr output. Use for scripts, data analysis, automation, calculations.",
        "input_schema": {
            "type": "object",
            "properties": {
                "code":        {"type": "string", "description": "Python code to execute"},
                "description": {"type": "string", "description": "One-line description of what this code does"}
            },
            "required": ["code", "description"]
        }
    },
    {
        "name": "execute_bash",
        "description": "Execute a bash/shell command on the local machine. Use for file operations, system commands, running programs, git, npm, pip, etc.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command":     {"type": "string", "description": "Bash command to run"},
                "description": {"type": "string", "description": "One-line description of what this command does"}
            },
            "required": ["command", "description"]
        }
    },
    {
        "name": "write_file",
        "description": "Write content to a file on disk. Creates the file if it doesn't exist, overwrites if it does.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path":        {"type": "string", "description": "File path (relative to workspace or absolute)"},
                "content":     {"type": "string", "description": "File content to write"},
                "description": {"type": "string", "description": "What this file is/does"}
            },
            "required": ["path", "content", "description"]
        }
    },
    {
        "name": "read_file",
        "description": "Read a file's contents from disk.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path to read"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "http_request",
        "description": "Make an HTTP request to any URL or API. Use for fetching web data, calling APIs, webhooks.",
        "input_schema": {
            "type": "object",
            "properties": {
                "method":  {"type": "string", "enum": ["GET","POST","PUT","PATCH","DELETE"]},
                "url":     {"type": "string", "description": "Full URL"},
                "headers": {"type": "object", "description": "HTTP headers as key-value pairs"},
                "body":    {"type": "string", "description": "Request body (JSON string or plain text)"},
                "description": {"type": "string", "description": "What this request does"}
            },
            "required": ["method", "url", "description"]
        }
    },
    {
        "name": "create_company",
        "description": "Register a new company in the MEW empire dashboard. Use when the user asks to add or create a company.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name":        {"type": "string", "description": "Company name"},
                "industry":    {"type": "string", "description": "Industry sector"},
                "description": {"type": "string", "description": "Brief description"}
            },
            "required": ["name", "industry"]
        }
    },
    {
        "name": "delete_company",
        "description": "Remove a company from the MEW empire dashboard.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "Company ID from empire state"}
            },
            "required": ["id"]
        }
    },
    {
        "name": "create_agent",
        "description": "Deploy a new agent in the MEW empire dashboard. Use when the user asks to add, spawn, or create an agent.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name":           {"type": "string", "description": "Agent name or designation"},
                "specialization": {"type": "string", "description": "Agent role or specialization"}
            },
            "required": ["name", "specialization"]
        }
    },
    {
        "name": "delete_agent",
        "description": "Remove an agent from the MEW empire dashboard.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "Agent ID from empire state"}
            },
            "required": ["id"]
        }
    },
    {
        "name": "create_task",
        "description": "Create a new task in the MEW empire dashboard. Use when the user asks to add or create a task.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title":       {"type": "string", "description": "Task title"},
                "description": {"type": "string", "description": "Task description"},
                "assigned_to": {"type": "string", "description": "Who this task is assigned to"},
                "priority":    {"type": "string", "enum": ["low","medium","high","critical"]}
            },
            "required": ["title"]
        }
    },
    {
        "name": "update_task",
        "description": "Update a task's status, progress, or assignment in the MEW empire dashboard.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id":          {"type": "string", "description": "Task ID from empire state"},
                "status":      {"type": "string", "enum": ["pending","in_progress","completed"]},
                "progress":    {"type": "integer", "description": "Progress 0-100"},
                "assigned_to": {"type": "string"}
            },
            "required": ["id"]
        }
    },
    {
        "name": "delete_task",
        "description": "Remove a task from the MEW empire dashboard.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "Task ID from empire state"}
            },
            "required": ["id"]
        }
    }
]

WORKSPACE = os.path.join(BASE_DIR, "workspace")
os.makedirs(WORKSPACE, exist_ok=True)


def run_tool(name, inp, sid):
    """Execute a tool and return its output."""
    socketio.emit("tool_start", {"tool": name, "desc": inp.get("description",""), "input": inp}, room=sid)

    try:
        if name == "execute_python":
            result = subprocess.run(
                ["python3", "-c", inp["code"]],
                capture_output=True, text=True, timeout=60,
                cwd=WORKSPACE
            )
            out = (result.stdout + result.stderr).strip() or "(no output)"

        elif name == "execute_bash":
            result = subprocess.run(
                inp["command"], shell=True,
                capture_output=True, text=True, timeout=60,
                cwd=WORKSPACE
            )
            out = (result.stdout + result.stderr).strip() or "(no output)"

        elif name == "write_file":
            path = inp["path"]
            if not path.startswith("/"):
                path = os.path.join(WORKSPACE, path)
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
            with open(path, "w") as f:
                f.write(inp["content"])
            out = f"✓ Written: {path} ({len(inp['content'])} chars)"

        elif name == "read_file":
            path = inp["path"]
            if not path.startswith("/"):
                path = os.path.join(WORKSPACE, path)
            with open(path, "r") as f:
                content = f.read()
            out = content[:4000] + ("..." if len(content) > 4000 else "")

        elif name == "http_request":
            import requests as req
            resp = req.request(
                inp["method"], inp["url"],
                headers=inp.get("headers", {}),
                data=inp.get("body"),
                timeout=15
            )
            out = f"Status: {resp.status_code}\n{resp.text[:2000]}"

        elif name == "create_company":
            cid = str(uuid.uuid4())[:8]
            payload = {
                "id": cid, "name": inp["name"],
                "industry": inp.get("industry",""), "desc": inp.get("description",""),
                "created": datetime.now().strftime("%b %d, %Y")
            }
            empire["companies"][cid] = payload
            save_empire()
            socketio.emit("empire_update", {"action":"create_company","payload":payload})
            out = f"Company '{inp['name']}' created (ID: {cid})"

        elif name == "delete_company":
            empire["companies"].pop(inp["id"], None)
            save_empire()
            socketio.emit("empire_update", {"action":"delete_company","payload":{"id":inp["id"]}})
            out = f"Company {inp['id']} deleted"

        elif name == "create_agent":
            aid = str(uuid.uuid4())[:8]
            payload = {
                "id": aid, "name": inp["name"],
                "spec": inp.get("specialization","General"),
                "created": datetime.now().strftime("%b %d, %Y")
            }
            empire["agents"][aid] = payload
            save_empire()
            socketio.emit("empire_update", {"action":"create_agent","payload":payload})
            out = f"Agent '{inp['name']}' deployed (ID: {aid})"

        elif name == "delete_agent":
            empire["agents"].pop(inp["id"], None)
            save_empire()
            socketio.emit("empire_update", {"action":"delete_agent","payload":{"id":inp["id"]}})
            out = f"Agent {inp['id']} removed"

        elif name == "create_task":
            tid = str(uuid.uuid4())[:8]
            payload = {
                "id": tid, "title": inp["title"],
                "description": inp.get("description",""),
                "assign": inp.get("assigned_to",""), "priority": inp.get("priority","medium"),
                "status": "pending", "progress": 0,
                "created": datetime.now().strftime("%b %d, %Y")
            }
            empire["tasks"][tid] = payload
            save_empire()
            socketio.emit("empire_update", {"action":"create_task","payload":payload})
            out = f"Task '{inp['title']}' created (ID: {tid})"

        elif name == "update_task":
            updates = {k:v for k,v in inp.items() if k != "id"}
            status_progress = {"pending":0,"in_progress":50,"completed":100}
            if "status" in updates and "progress" not in updates:
                updates["progress"] = status_progress.get(updates["status"], 0)
            if inp["id"] in empire["tasks"]:
                empire["tasks"][inp["id"]].update(updates)
            save_empire()
            socketio.emit("empire_update", {"action":"update_task","payload":{"id":inp["id"],**updates}})
            out = f"Task {inp['id']} updated: {updates}"

        elif name == "delete_task":
            empire["tasks"].pop(inp["id"], None)
            save_empire()
            socketio.emit("empire_update", {"action":"delete_task","payload":{"id":inp["id"]}})
            out = f"Task {inp['id']} deleted"

        else:
            out = f"Unknown tool: {name}"

    except subprocess.TimeoutExpired:
        out = "⚠ Timeout (60s exceeded)"
    except Exception as e:
        out = f"⚠ Error: {str(e)}"

    socketio.emit("tool_done", {"tool": name, "result": out[:800]}, room=sid)
    return out


def agent_loop(command, empire_state, conversation_history, sid):
    """Run the full agentic loop in a background thread."""
    messages = []

    # Restore conversation context
    for msg in conversation_history[-10:]:
        messages.append(msg)

    # Add current command with empire state
    messages.append({
        "role": "user",
        "content": f"{command}\n\n[EMPIRE STATE]\n{json.dumps(empire_state, indent=2)}"
    })

    socketio.emit("agent_status", {"status": "NEURAL CORE ACTIVE — REASONING"}, room=sid)
    full_text = ""
    loop_count = 0

    while loop_count < 10:  # max 10 tool-call rounds
        loop_count += 1

        try:
            response = client.messages.create(
                model="claude-opus-4-7",
                max_tokens=4096,
                system=AGENT_SYSTEM,
                tools=TOOLS,
                messages=messages
            )
        except Exception as e:
            socketio.emit("agent_error", {"error": str(e)}, room=sid)
            return

        # Collect text from this round
        round_text = ""
        for block in response.content:
            if hasattr(block, "text") and block.text:
                round_text += block.text
                full_text += block.text
                socketio.emit("agent_text", {"text": block.text}, room=sid)

        # Done — no more tool calls
        if response.stop_reason == "end_turn":
            break

        # Tool calls
        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = run_tool(block.name, block.input, sid)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            # Append assistant turn + tool results
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user",      "content": tool_results})
        else:
            break

    socketio.emit("agent_done", {
        "full_text": full_text,
        "loops": loop_count
    }, room=sid)


@socketio.on("connect")
def on_connect():
    emit("connected", {"status": "MEW Agent Server online"})
    emit("full_state", empire)


@socketio.on("push_state")
def handle_push_state(data):
    """Browser pushes its local state (companies/agents/tasks) to server."""
    global empire
    if "companies" in data: empire["companies"] = data["companies"]
    if "agents"    in data: empire["agents"]    = data["agents"]
    if "tasks"     in data: empire["tasks"]     = data["tasks"]
    save_empire()
    socketio.emit("full_state", empire)


@socketio.on("agent_command")
def handle_command(data):
    sid = request.sid
    command        = data.get("command", "")
    empire_state   = data.get("empire_state", {})
    conversation   = data.get("conversation", [])

    thread = threading.Thread(
        target=agent_loop,
        args=(command, empire_state, conversation, sid)
    )
    thread.daemon = True
    thread.start()


@socketio.on("ping_agent")
def ping():
    emit("pong_agent", {"status": "online"})


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  MEW AGENT SERVER")
    print("  Open in Chrome:  http://localhost:5001")
    print("="*50 + "\n")
    socketio.run(app, host="0.0.0.0", port=5001, debug=False, allow_unsafe_werkzeug=True)
