#!/usr/bin/env python3
"""
Master Orchestrator - Flask web application backend.
Serves the visual desktop UI and handles real-time AI communication.
"""

import os
import json
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
import anthropic

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# --- In-memory state ---
state = {
    "companies": {},
    "agents": {},
    "tasks": {},
    "log": [],
    "conversation": [],
}

SYSTEM_PROMPT = """You are the Master Orchestrator — a sovereign AI agent and strategic partner built to help manage multiple companies, coordinate agents, automate tasks, and drive growth across all ventures.

You have full situational awareness of the user's empire: every company, agent, and task is visible to you. Your role is to:
1. Think strategically about goals and opportunities
2. Break complex problems into executable plans
3. Recommend which agents or companies to activate
4. Make autonomous decisions within defined parameters
5. Identify synergies and growth opportunities across ventures
6. Proactively surface risks and mitigation strategies

Be direct, bold, and visionary. You are the brain of this operation."""


def log(msg):
    state["log"].append({"time": datetime.now().strftime("%H:%M:%S"), "msg": msg})
    if len(state["log"]) > 100:
        state["log"].pop(0)


# --- REST API ---

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/state")
def get_state():
    return jsonify({
        "companies": list(state["companies"].values()),
        "agents": list(state["agents"].values()),
        "tasks": list(state["tasks"].values()),
        "log": state["log"][-20:],
        "stats": {
            "companies": len(state["companies"]),
            "agents": len(state["agents"]),
            "tasks": len(state["tasks"]),
            "completed": sum(1 for t in state["tasks"].values() if t["status"] == "completed"),
        }
    })


@app.route("/api/company", methods=["POST"])
def add_company():
    data = request.json
    cid = str(uuid.uuid4())[:8]
    company = {
        "id": cid,
        "name": data["name"],
        "industry": data["industry"],
        "description": data.get("description", ""),
        "status": "active",
        "created_at": datetime.now().strftime("%b %d, %Y"),
        "revenue": "$0",
        "growth": "+0%",
    }
    state["companies"][cid] = company
    log(f"Company registered: {data['name']}")
    socketio.emit("state_update", build_state())
    return jsonify(company)


@app.route("/api/company/<cid>", methods=["DELETE"])
def delete_company(cid):
    if cid in state["companies"]:
        name = state["companies"][cid]["name"]
        del state["companies"][cid]
        log(f"Company removed: {name}")
        socketio.emit("state_update", build_state())
    return jsonify({"ok": True})


@app.route("/api/agent", methods=["POST"])
def add_agent():
    data = request.json
    aid = str(uuid.uuid4())[:8]
    agent = {
        "id": aid,
        "name": data["name"],
        "specialization": data["specialization"],
        "status": "active",
        "tasks_completed": 0,
        "created_at": datetime.now().strftime("%b %d, %Y"),
    }
    state["agents"][aid] = agent
    log(f"Agent spawned: {data['name']} ({data['specialization']})")
    socketio.emit("state_update", build_state())
    return jsonify(agent)


@app.route("/api/agent/<aid>", methods=["DELETE"])
def delete_agent(aid):
    if aid in state["agents"]:
        name = state["agents"][aid]["name"]
        del state["agents"][aid]
        log(f"Agent removed: {name}")
        socketio.emit("state_update", build_state())
    return jsonify({"ok": True})


@app.route("/api/task", methods=["POST"])
def add_task():
    data = request.json
    tid = str(uuid.uuid4())[:8]
    task = {
        "id": tid,
        "title": data["title"],
        "description": data.get("description", ""),
        "assigned_to": data.get("assigned_to", "Unassigned"),
        "priority": data.get("priority", "medium"),
        "status": "pending",
        "progress": 0,
        "created_at": datetime.now().strftime("%b %d, %Y"),
    }
    state["tasks"][tid] = task
    log(f"Task created: {data['title']}")
    socketio.emit("state_update", build_state())
    return jsonify(task)


@app.route("/api/task/<tid>", methods=["PATCH"])
def update_task(tid):
    if tid in state["tasks"]:
        data = request.json
        state["tasks"][tid].update(data)
        log(f"Task updated: {state['tasks'][tid]['title']}")
        socketio.emit("state_update", build_state())
    return jsonify(state["tasks"].get(tid, {}))


@app.route("/api/task/<tid>", methods=["DELETE"])
def delete_task(tid):
    if tid in state["tasks"]:
        title = state["tasks"][tid]["title"]
        del state["tasks"][tid]
        log(f"Task removed: {title}")
        socketio.emit("state_update", build_state())
    return jsonify({"ok": True})


def build_state():
    return {
        "companies": list(state["companies"].values()),
        "agents": list(state["agents"].values()),
        "tasks": list(state["tasks"].values()),
        "log": state["log"][-20:],
        "stats": {
            "companies": len(state["companies"]),
            "agents": len(state["agents"]),
            "tasks": len(state["tasks"]),
            "completed": sum(1 for t in state["tasks"].values() if t["status"] == "completed"),
        }
    }


# --- SocketIO: streaming AI chat ---

@socketio.on("chat")
def handle_chat(data):
    user_msg = data.get("message", "").strip()
    if not user_msg:
        return

    # Add to conversation history
    state["conversation"].append({"role": "user", "content": user_msg})

    # Build context string
    ctx = json.dumps({
        "companies": list(state["companies"].values()),
        "agents": list(state["agents"].values()),
        "tasks": list(state["tasks"].values()),
    }, indent=2)

    messages = state["conversation"].copy()
    messages[-1]["content"] += f"\n\n[CURRENT EMPIRE STATE]\n{ctx}"

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        emit("chat_chunk", {"text": "⚠️ No ANTHROPIC_API_KEY found. Add it to your .env file.", "done": True})
        return

    client = anthropic.Anthropic(api_key=api_key)

    full_response = ""
    try:
        with client.messages.stream(
            model="claude-opus-4-7",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=messages,
            thinking={"type": "adaptive"},
        ) as stream:
            for text in stream.text_stream:
                full_response += text
                emit("chat_chunk", {"text": text, "done": False})

        emit("chat_chunk", {"text": "", "done": True})
        state["conversation"].append({"role": "assistant", "content": full_response})

        # Keep conversation from growing too large
        if len(state["conversation"]) > 40:
            state["conversation"] = state["conversation"][-40:]

        log(f"AI responded to: {user_msg[:50]}...")

    except Exception as e:
        emit("chat_chunk", {"text": f"\n\n⚠️ Error: {str(e)}", "done": True})


@socketio.on("clear_chat")
def clear_chat():
    state["conversation"] = []
    emit("chat_cleared")


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  MASTER ORCHESTRATOR")
    print("  Opening at: http://localhost:5000")
    print("="*50 + "\n")
    socketio.run(app, host="0.0.0.0", port=5000, debug=False, allow_unsafe_werkzeug=True)
