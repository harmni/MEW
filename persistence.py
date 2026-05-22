"""
Persistence layer for Master Orchestrator state management.
Saves and restores orchestrator state to JSON files.
"""

import json
import os
from datetime import datetime
from pathlib import Path


class StateManager:
    """Manages persistence of orchestrator state."""

    def __init__(self, save_dir: str = "orchestrator_state"):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)

    def save_state(self, orchestrator, session_name: str = None):
        """Save orchestrator state to disk."""
        if not session_name:
            session_name = datetime.now().strftime("%Y%m%d_%H%M%S")

        state = {
            "timestamp": datetime.now().isoformat(),
            "session_name": session_name,
            "companies": orchestrator.companies,
            "active_tasks": orchestrator.active_tasks,
            "sub_agents": orchestrator.sub_agents,
            "operational_log": orchestrator.operational_log,
            "conversation_history": orchestrator.conversation_history,
        }

        filepath = self.save_dir / f"{session_name}.json"
        with open(filepath, "w") as f:
            json.dump(state, f, indent=2)

        return filepath

    def load_state(self, session_name: str, orchestrator):
        """Load orchestrator state from disk."""
        filepath = self.save_dir / f"{session_name}.json"

        if not filepath.exists():
            raise FileNotFoundError(f"Session '{session_name}' not found")

        with open(filepath, "r") as f:
            state = json.load(f)

        orchestrator.companies = state["companies"]
        orchestrator.active_tasks = state["active_tasks"]
        orchestrator.sub_agents = state["sub_agents"]
        orchestrator.operational_log = state["operational_log"]
        orchestrator.conversation_history = state["conversation_history"]

        return state

    def list_sessions(self):
        """List all saved sessions."""
        sessions = []
        for filepath in sorted(self.save_dir.glob("*.json"), reverse=True):
            with open(filepath, "r") as f:
                state = json.load(f)
            sessions.append(
                {
                    "name": filepath.stem,
                    "timestamp": state["timestamp"],
                    "companies": len(state["companies"]),
                    "tasks": len(state["active_tasks"]),
                    "agents": len(state["sub_agents"]),
                }
            )
        return sessions

    def delete_session(self, session_name: str):
        """Delete a saved session."""
        filepath = self.save_dir / f"{session_name}.json"
        if filepath.exists():
            filepath.unlink()
            return True
        return False

    def export_session(self, session_name: str, export_path: str):
        """Export session to a specified path."""
        filepath = self.save_dir / f"{session_name}.json"
        if not filepath.exists():
            raise FileNotFoundError(f"Session '{session_name}' not found")

        with open(filepath, "r") as f:
            state = json.load(f)

        with open(export_path, "w") as f:
            json.dump(state, f, indent=2)

        return export_path
