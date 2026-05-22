#!/usr/bin/env python3
"""
Advanced Master Orchestrator with state persistence and enhanced features.
Builds on the base orchestrator with additional capabilities.
"""

import os
from datetime import datetime
from typing import Optional, List, Dict
from anthropic import Anthropic
from orchestrator import MasterOrchestrator
from persistence import StateManager


class AdvancedOrchestrator(MasterOrchestrator):
    """Enhanced orchestrator with persistence and advanced features."""

    def __init__(self, session_name: Optional[str] = None):
        super().__init__()
        self.state_manager = StateManager()
        self.session_name = session_name or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.metrics = {
            "total_requests": 0,
            "total_tasks_created": 0,
            "total_companies": 0,
            "total_agents": 0,
        }

        # Load existing session if specified
        if session_name and session_name in [s["name"] for s in self.state_manager.list_sessions()]:
            self.load_session(session_name)

    def save_session(self):
        """Save current orchestrator state."""
        self.state_manager.save_state(self, self.session_name)
        print(f"✓ Session '{self.session_name}' saved")

    def load_session(self, session_name: str):
        """Load a previous session."""
        self.state_manager.load_state(session_name, self)
        self.session_name = session_name
        print(f"✓ Session '{session_name}' loaded")

    def add_company(self, name: str, description: str, industry: str) -> dict:
        """Add a company and update metrics."""
        company = super().add_company(name, description, industry)
        self.metrics["total_companies"] += 1
        return company

    def spawn_sub_agent(self, agent_name: str, specialization: str) -> dict:
        """Spawn an agent and update metrics."""
        agent = super().spawn_sub_agent(agent_name, specialization)
        self.metrics["total_agents"] += 1
        return agent

    def create_task(
        self,
        task_id: str,
        title: str,
        description: str,
        assigned_to: str,
        priority: str = "medium",
        deadline: Optional[str] = None,
    ) -> dict:
        """Create a task and update metrics."""
        task = super().create_task(task_id, title, description, assigned_to, priority, deadline)
        self.metrics["total_tasks_created"] += 1
        return task

    def process_user_request(self, user_message: str, verbose: bool = False) -> str:
        """Process request and track metrics."""
        self.metrics["total_requests"] += 1
        if verbose:
            print(f"[Request #{self.metrics['total_requests']}] Processing...")
        response = super().process_user_request(user_message)
        return response

    def get_metrics(self) -> dict:
        """Get orchestrator metrics."""
        return {
            **self.metrics,
            "active_companies": len(self.companies),
            "active_agents": len(self.sub_agents),
            "active_tasks": len(self.active_tasks),
            "operations_logged": len(self.operational_log),
        }

    def get_company_summary(self, company_name: str) -> Optional[dict]:
        """Get detailed summary of a company."""
        if company_name not in self.companies:
            return None

        company = self.companies[company_name]
        company_tasks = [
            task for task in self.active_tasks.values()
            if task["assigned_to"] == company_name
        ]

        return {
            "name": company["name"],
            "industry": company["industry"],
            "status": company["status"],
            "created_at": company["created_at"],
            "total_tasks": len(company_tasks),
            "tasks": company_tasks,
        }

    def get_agent_summary(self, agent_name: str) -> Optional[dict]:
        """Get detailed summary of an agent."""
        if agent_name not in self.sub_agents:
            return None

        agent = self.sub_agents[agent_name]
        assigned_tasks = [
            task for task in self.active_tasks.values()
            if task["assigned_to"] == agent_name
        ]

        return {
            "name": agent["name"],
            "specialization": agent["specialization"],
            "status": agent["status"],
            "created_at": agent["created_at"],
            "assigned_tasks": len(assigned_tasks),
            "task_details": assigned_tasks,
        }

    def interactive_session(self):
        """Enhanced interactive session with additional commands."""
        print("\n" + "=" * 60)
        print(f"MASTER ORCHESTRATOR - Session: {self.session_name}")
        print("=" * 60)
        print("\nCommands:")
        print("  'add company <name> <industry>' - Register a new company")
        print("  'spawn agent <name> <specialization>' - Create a sub-agent")
        print("  'create task <title>' - Create a task")
        print("  'status' - View operational status")
        print("  'metrics' - View orchestrator metrics")
        print("  'company <name>' - Get company summary")
        print("  'agent <name>' - Get agent summary")
        print("  'save' - Save session state")
        print("  'sessions' - List saved sessions")
        print("  'exit' - End session (with save prompt)")
        print("\nOr simply describe what you want to accomplish...\n")

        while True:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "exit":
                save_prompt = input("Save session before exit? (y/n): ").strip().lower()
                if save_prompt == "y":
                    self.save_session()
                print("Orchestrator shutting down. Empire operations remain active.")
                break

            if user_input.lower() == "save":
                self.save_session()
                continue

            if user_input.lower() == "metrics":
                metrics = self.get_metrics()
                print("\n--- METRICS ---")
                for key, value in metrics.items():
                    print(f"{key}: {value}")
                print()
                continue

            if user_input.lower() == "sessions":
                sessions = self.state_manager.list_sessions()
                if sessions:
                    print("\n--- SAVED SESSIONS ---")
                    for session in sessions:
                        print(
                            f"  {session['name']}: "
                            f"{session['companies']} companies, "
                            f"{session['tasks']} tasks, "
                            f"{session['agents']} agents"
                        )
                    print()
                else:
                    print("No saved sessions.\n")
                continue

            if user_input.lower() == "status":
                print("\n--- OPERATIONAL STATUS ---")
                print(f"Companies: {len(self.companies)}")
                print(f"Active Tasks: {len(self.active_tasks)}")
                print(f"Sub-Agents: {len(self.sub_agents)}")
                print(f"Operations Logged: {len(self.operational_log)}")
                print()
                continue

            if user_input.lower().startswith("company "):
                company_name = user_input[8:].strip()
                summary = self.get_company_summary(company_name)
                if summary:
                    print("\n--- COMPANY SUMMARY ---")
                    print(f"Name: {summary['name']}")
                    print(f"Industry: {summary['industry']}")
                    print(f"Status: {summary['status']}")
                    print(f"Total Tasks: {summary['total_tasks']}")
                    print()
                else:
                    print(f"Company '{company_name}' not found.\n")
                continue

            if user_input.lower().startswith("agent "):
                agent_name = user_input[6:].strip()
                summary = self.get_agent_summary(agent_name)
                if summary:
                    print("\n--- AGENT SUMMARY ---")
                    print(f"Name: {summary['name']}")
                    print(f"Specialization: {summary['specialization']}")
                    print(f"Status: {summary['status']}")
                    print(f"Assigned Tasks: {summary['assigned_tasks']}")
                    print()
                else:
                    print(f"Agent '{agent_name}' not found.\n")
                continue

            if user_input.lower().startswith("add company"):
                parts = user_input.split(maxsplit=3)
                if len(parts) >= 4:
                    name, industry = parts[2], parts[3]
                    self.add_company(name, f"Company {name}", industry)
                    print(f"✓ Company '{name}' registered\n")
                continue

            if user_input.lower().startswith("spawn agent"):
                parts = user_input.split(maxsplit=3)
                if len(parts) >= 4:
                    name, spec = parts[2], parts[3]
                    self.spawn_sub_agent(name, spec)
                    print(f"✓ Agent '{name}' spawned\n")
                continue

            # Regular request - process through orchestrator
            print("\nOrchestrator: Processing request...\n")
            response = self.process_user_request(user_input, verbose=True)
            print(f"Orchestrator: {response}\n")


def main():
    """Main entry point for advanced orchestrator."""
    orchestrator = AdvancedOrchestrator()
    orchestrator.interactive_session()


if __name__ == "__main__":
    main()
