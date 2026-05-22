#!/usr/bin/env python3
"""
MEW Agent Server — Claude runs as a real autonomous agent.
Receives commands from the browser, executes tools, streams results back.
"""

import os
import json
import subprocess
import threading
from flask import Flask, request
from flask_socketio import SocketIO, emit
import anthropic
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

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
    }
]

WORKSPACE = "/home/user/MEW/workspace"
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
    print("  ws://localhost:5001")
    print("="*50 + "\n")
    socketio.run(app, host="0.0.0.0", port=5001, debug=False, allow_unsafe_werkzeug=True)
