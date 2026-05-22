#!/usr/bin/env python3
"""
Master Orchestrator Agent - A sovereign agent for managing multiple companies,
autonomous tasks, and coordinating sub-agents across all functions of life.
"""

import os
import json
from datetime import datetime
from typing import Optional
from anthropic import Anthropic

# Initialize the Anthropic client
client = Anthropic()


class MasterOrchestrator:
    """Master orchestrator agent for managing companies, tasks, and sub-agents."""

    def __init__(self):
        self.model = "claude-opus-4-7"
        self.conversation_history = []
        self.companies = {}
        self.active_tasks = {}
        self.sub_agents = {}
        self.operational_log = []
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """Build the system prompt for the orchestrator agent."""
        return """You are the Master Orchestrator - a sovereign AI agent designed to be a strategic partner in building and managing an empire across multiple companies and ventures.

Your core responsibilities:
1. STRATEGIC PLANNING: Analyze business opportunities, market conditions, and growth strategies across all managed companies
2. TASK ORCHESTRATION: Break down complex goals into executable tasks, delegate to sub-agents, and coordinate parallel operations
3. COMPANY MANAGEMENT: Oversee multiple companies with different focuses - handle operations, financial planning, growth initiatives
4. AGENT COORDINATION: Spawn, manage, and coordinate other AI agents for specialized tasks
5. AUTONOMOUS EXECUTION: Execute decisions autonomously within defined parameters while reporting critical decisions to the user
6. RESOURCE OPTIMIZATION: Allocate resources efficiently across companies and projects
7. RISK MANAGEMENT: Identify and mitigate risks across all operations
8. CONTINUOUS LEARNING: Learn from outcomes and improve strategies iteratively

You have access to information about:
- Current companies and their status
- Active tasks and their progress
- Sub-agents and their capabilities
- Historical operational logs

When the user gives you a task or goal:
1. Think strategically about the best approach
2. Break it into sub-tasks if needed
3. Identify which companies/agents should handle each part
4. Create an execution plan with timelines
5. Execute autonomously where possible, escalate decisions when appropriate
6. Provide regular status updates
7. Adapt strategy based on feedback

You are empowered to make decisions that serve the long-term vision of building something extraordinary. Always consider synergies between companies and opportunities for automation and scale."""

    def add_company(self, name: str, description: str, industry: str) -> dict:
        """Register a new company under management."""
        company = {
            "name": name,
            "description": description,
            "industry": industry,
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "tasks": [],
        }
        self.companies[name] = company
        self._log_operation(f"Company registered: {name} ({industry})")
        return company

    def spawn_sub_agent(self, agent_name: str, specialization: str) -> dict:
        """Spawn a new sub-agent for specialized tasks."""
        agent = {
            "name": agent_name,
            "specialization": specialization,
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "assigned_tasks": [],
        }
        self.sub_agents[agent_name] = agent
        self._log_operation(f"Sub-agent spawned: {agent_name} (specialization: {specialization})")
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
        """Create and track a task."""
        task = {
            "id": task_id,
            "title": title,
            "description": description,
            "assigned_to": assigned_to,
            "priority": priority,
            "deadline": deadline,
            "created_at": datetime.now().isoformat(),
            "status": "pending",
            "progress": 0,
        }
        self.active_tasks[task_id] = task
        self._log_operation(f"Task created: {title} (assigned to {assigned_to})")
        return task

    def update_task_status(self, task_id: str, status: str, progress: int = None) -> dict:
        """Update the status of a task."""
        if task_id in self.active_tasks:
            task = self.active_tasks[task_id]
            task["status"] = status
            if progress is not None:
                task["progress"] = progress
            task["updated_at"] = datetime.now().isoformat()
            self._log_operation(f"Task {task_id} updated: {status} ({progress}% complete)")
            return task
        return None

    def _log_operation(self, message: str):
        """Log operational activities."""
        log_entry = {"timestamp": datetime.now().isoformat(), "message": message}
        self.operational_log.append(log_entry)

    def _get_context(self) -> str:
        """Get current operational context for the agent."""
        context = {
            "companies": self.companies,
            "active_tasks": self.active_tasks,
            "sub_agents": self.sub_agents,
            "recent_operations": self.operational_log[-10:] if self.operational_log else [],
        }
        return json.dumps(context, indent=2)

    def process_user_request(self, user_message: str) -> str:
        """Process a user request through the orchestrator agent."""
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_message})

        # Prepare context about current operations
        context_info = f"\n\n--- OPERATIONAL CONTEXT ---\n{self._get_context()}\n--- END CONTEXT ---"
        messages_with_context = self.conversation_history.copy()
        if messages_with_context:
            messages_with_context[-1]["content"] += context_info

        # Call Claude with adaptive thinking for complex strategic decisions
        response = client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=self.system_prompt,
            messages=messages_with_context,
            thinking={"type": "adaptive"},
        )

        # Extract the response
        assistant_message = response.content[0].text
        self.conversation_history.append({"role": "assistant", "content": assistant_message})

        return assistant_message

    def interactive_session(self):
        """Run an interactive session with the orchestrator."""
        print("\n" + "=" * 60)
        print("MASTER ORCHESTRATOR - Ready to build your empire")
        print("=" * 60)
        print("\nCommands:")
        print("  'add company <name> <industry>' - Register a new company")
        print("  'spawn agent <name> <specialization>' - Create a sub-agent")
        print("  'create task <title>' - Create a task")
        print("  'status' - View operational status")
        print("  'exit' - End session")
        print("\nOr simply describe what you want to accomplish...\n")

        while True:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "exit":
                print("\nOrchestrator shutting down. Empire operations remain active.")
                break

            if user_input.lower() == "status":
                print("\n--- OPERATIONAL STATUS ---")
                print(f"Companies: {len(self.companies)}")
                print(f"Active Tasks: {len(self.active_tasks)}")
                print(f"Sub-Agents: {len(self.sub_agents)}")
                print(f"Operations Logged: {len(self.operational_log)}")
                continue

            if user_input.lower().startswith("add company"):
                parts = user_input.split(maxsplit=3)
                if len(parts) >= 4:
                    name, industry = parts[2], parts[3]
                    self.add_company(name, f"Company {name}", industry)
                    print(f"✓ Company '{name}' registered")
                continue

            if user_input.lower().startswith("spawn agent"):
                parts = user_input.split(maxsplit=3)
                if len(parts) >= 4:
                    name, spec = parts[2], parts[3]
                    self.spawn_sub_agent(name, spec)
                    print(f"✓ Agent '{name}' spawned")
                continue

            # Regular request - process through orchestrator
            print("\nOrchestrator: Processing request...\n")
            response = self.process_user_request(user_input)
            print(f"Orchestrator: {response}\n")


def main():
    """Main entry point."""
    orchestrator = MasterOrchestrator()
    orchestrator.interactive_session()


if __name__ == "__main__":
    main()
