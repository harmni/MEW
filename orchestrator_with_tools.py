#!/usr/bin/env python3
"""
Master Orchestrator with integrated tools and capabilities.
Combines strategic agent with practical execution tools.
"""

import json
from typing import Optional
from anthropic import Anthropic
from advanced_orchestrator import AdvancedOrchestrator
from tools import ToolRegistry


class ToolEnabledOrchestrator(AdvancedOrchestrator):
    """Orchestrator with external tools and integration capabilities."""

    def __init__(self, session_name: Optional[str] = None):
        super().__init__(session_name)
        self.tool_registry = ToolRegistry()
        self.tool_calls = []
        self.system_prompt = self._build_enhanced_system_prompt()

    def _build_enhanced_system_prompt(self) -> str:
        """Build system prompt that includes tool usage."""
        base_prompt = super()._build_system_prompt()

        tools_info = self._get_tools_info()
        enhanced_prompt = f"""{base_prompt}

AVAILABLE TOOLS:
{tools_info}

When you identify that you need to execute an action, you can use these tools:
- Email: Send communications, schedule follow-ups, manage contacts
- Calendar: Schedule meetings, manage team availability
- Data Analysis: Generate reports, track metrics, analyze trends
- Project Management: Create projects, manage sprints, track progress

You can request tool execution by mentioning the tool name and action needed.
I will execute the tools and provide results for you to act on."""

        return enhanced_prompt

    def _get_tools_info(self) -> str:
        """Format available tools information."""
        tools = self.tool_registry.list_tools()
        info = ""
        for tool in tools:
            info += f"\n- {tool['name'].upper()}: {tool['description']}"
        return info

    def process_user_request(self, user_message: str, verbose: bool = False) -> str:
        """Process request with tool awareness."""
        if verbose:
            print(f"[Request #{self.metrics['total_requests']}] Processing with tool awareness...")

        response = super().process_user_request(user_message, verbose)

        # Check if response mentions tool usage
        self._check_for_tool_requests(response, user_message)

        return response

    def _check_for_tool_requests(self, response: str, context: str):
        """Check if orchestrator response suggests tool usage."""
        # This is a simple heuristic - in production, you'd use proper parsing
        tool_names = ["email", "calendar", "data_analysis", "project_management"]

        for tool_name in tool_names:
            if tool_name.lower() in response.lower():
                # Log that a tool might be needed
                self.tool_calls.append({
                    "timestamp": __import__("datetime").datetime.now().isoformat(),
                    "tool": tool_name,
                    "context": context,
                })

    def use_email_tool(self, action: str, **kwargs):
        """Use the email tool."""
        return self.tool_registry.execute_tool("email", action, **kwargs)

    def use_calendar_tool(self, action: str, **kwargs):
        """Use the calendar tool."""
        return self.tool_registry.execute_tool("calendar", action, **kwargs)

    def use_data_analysis_tool(self, action: str, **kwargs):
        """Use the data analysis tool."""
        return self.tool_registry.execute_tool("data_analysis", action, **kwargs)

    def use_project_management_tool(self, action: str, **kwargs):
        """Use the project management tool."""
        return self.tool_registry.execute_tool("project_management", action, **kwargs)

    def get_tool_status(self) -> dict:
        """Get status of all available tools."""
        return {
            "available_tools": len(self.tool_registry.tools),
            "tool_list": self.tool_registry.list_tools(),
            "tool_calls_made": len(self.tool_calls),
        }

    def interactive_session(self):
        """Enhanced interactive session with tool support."""
        print("\n" + "=" * 60)
        print(f"MASTER ORCHESTRATOR WITH TOOLS - Session: {self.session_name}")
        print("=" * 60)
        print("\nCommands:")
        print("  'add company <name> <industry>' - Register a new company")
        print("  'spawn agent <name> <specialization>' - Create a sub-agent")
        print("  'create task <title>' - Create a task")
        print("  'status' - View operational status")
        print("  'metrics' - View orchestrator metrics")
        print("  'tools' - View available tools")
        print("  'company <name>' - Get company summary")
        print("  'agent <name>' - Get agent summary")
        print("  'save' - Save session state")
        print("  'sessions' - List saved sessions")
        print("  'exit' - End session (with save prompt)")
        print("\nOr describe what you want to accomplish. The orchestrator can use tools")
        print("like email, calendar, data analysis, and project management.\n")

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

            if user_input.lower() == "tools":
                status = self.get_tool_status()
                print("\n--- AVAILABLE TOOLS ---")
                print(f"Total tools: {status['available_tools']}")
                for tool in status['tool_list']:
                    print(f"  - {tool['name']}: {tool['description']}")
                print()
                continue

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
                    for session in sessions[:5]:
                        print(f"  {session['name']}: {session['companies']} companies, "
                              f"{session['tasks']} tasks, {session['agents']} agents")
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

            # Regular request - process through orchestrator with tool awareness
            print("\nOrchestrator: Processing request with available tools...\n")
            response = self.process_user_request(user_input, verbose=True)
            print(f"Orchestrator: {response}\n")


def main():
    """Main entry point for tool-enabled orchestrator."""
    orchestrator = ToolEnabledOrchestrator()
    orchestrator.interactive_session()


if __name__ == "__main__":
    main()
