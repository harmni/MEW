"""
Tool framework for Master Orchestrator.
Provides base classes and utilities for extending orchestrator with external capabilities.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime


class BaseTool(ABC):
    """Base class for orchestrator tools."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.created_at = datetime.now().isoformat()
        self.execution_count = 0
        self.last_executed = None

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool. Must be implemented by subclasses."""
        pass

    def log_execution(self, result: Dict[str, Any]):
        """Log tool execution."""
        self.execution_count += 1
        self.last_executed = datetime.now().isoformat()

    def get_schema(self) -> Dict[str, Any]:
        """Get JSON schema for this tool."""
        return {
            "name": self.name,
            "description": self.description,
            "type": self.__class__.__name__,
            "execution_count": self.execution_count,
            "last_executed": self.last_executed,
        }


class EmailTool(BaseTool):
    """Tool for sending emails and managing communications."""

    def __init__(self):
        super().__init__(
            "email",
            "Send emails, schedule communications, manage contacts"
        )
        self.sent_emails = []
        self.contacts = {}

    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute email operations."""
        if action == "send":
            result = self._send_email(**kwargs)
        elif action == "schedule":
            result = self._schedule_email(**kwargs)
        elif action == "add_contact":
            result = self._add_contact(**kwargs)
        else:
            result = {"error": f"Unknown action: {action}"}

        self.log_execution(result)
        return result

    def _send_email(self, to: str, subject: str, body: str, **kwargs) -> Dict[str, Any]:
        """Send an email."""
        email_record = {
            "to": to,
            "subject": subject,
            "body": body,
            "sent_at": datetime.now().isoformat(),
            "status": "sent",
        }
        self.sent_emails.append(email_record)
        return {
            "success": True,
            "message": f"Email sent to {to}",
            "email_id": len(self.sent_emails),
        }

    def _schedule_email(self, to: str, subject: str, body: str, send_at: str) -> Dict[str, Any]:
        """Schedule an email to be sent later."""
        return {
            "success": True,
            "message": f"Email scheduled to {to} for {send_at}",
        }

    def _add_contact(self, name: str, email: str, **kwargs) -> Dict[str, Any]:
        """Add a contact."""
        self.contacts[email] = {"name": name, "email": email, "added_at": datetime.now().isoformat()}
        return {
            "success": True,
            "message": f"Contact {name} added",
        }


class CalendarTool(BaseTool):
    """Tool for managing calendars and scheduling."""

    def __init__(self):
        super().__init__(
            "calendar",
            "Schedule meetings, manage availability, set reminders"
        )
        self.events = []
        self.availability = {}

    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute calendar operations."""
        if action == "create_event":
            result = self._create_event(**kwargs)
        elif action == "set_availability":
            result = self._set_availability(**kwargs)
        elif action == "list_events":
            result = self._list_events(**kwargs)
        else:
            result = {"error": f"Unknown action: {action}"}

        self.log_execution(result)
        return result

    def _create_event(self, title: str, start_time: str, end_time: str, **kwargs) -> Dict[str, Any]:
        """Create a calendar event."""
        event = {
            "title": title,
            "start_time": start_time,
            "end_time": end_time,
            "created_at": datetime.now().isoformat(),
            "status": "scheduled",
        }
        self.events.append(event)
        return {
            "success": True,
            "message": f"Event '{title}' scheduled",
            "event_id": len(self.events),
        }

    def _set_availability(self, available_slots: List[str]) -> Dict[str, Any]:
        """Set availability windows."""
        self.availability = {"slots": available_slots, "updated_at": datetime.now().isoformat()}
        return {
            "success": True,
            "message": "Availability updated",
        }

    def _list_events(self, **kwargs) -> Dict[str, Any]:
        """List upcoming events."""
        return {
            "success": True,
            "events": self.events,
            "count": len(self.events),
        }


class DataAnalysisTool(BaseTool):
    """Tool for analyzing data and generating reports."""

    def __init__(self):
        super().__init__(
            "data_analysis",
            "Analyze data, generate reports, track metrics"
        )
        self.reports = []
        self.data_sources = {}

    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute data analysis operations."""
        if action == "generate_report":
            result = self._generate_report(**kwargs)
        elif action == "track_metric":
            result = self._track_metric(**kwargs)
        elif action == "add_data_source":
            result = self._add_data_source(**kwargs)
        else:
            result = {"error": f"Unknown action: {action}"}

        self.log_execution(result)
        return result

    def _generate_report(self, title: str, metrics: List[str], **kwargs) -> Dict[str, Any]:
        """Generate a report."""
        report = {
            "title": title,
            "metrics": metrics,
            "generated_at": datetime.now().isoformat(),
            "status": "completed",
        }
        self.reports.append(report)
        return {
            "success": True,
            "message": f"Report '{title}' generated",
            "report_id": len(self.reports),
        }

    def _track_metric(self, metric_name: str, value: float, **kwargs) -> Dict[str, Any]:
        """Track a metric."""
        return {
            "success": True,
            "message": f"Metric '{metric_name}' tracked: {value}",
        }

    def _add_data_source(self, source_name: str, source_type: str, **kwargs) -> Dict[str, Any]:
        """Add a data source."""
        self.data_sources[source_name] = {
            "name": source_name,
            "type": source_type,
            "added_at": datetime.now().isoformat(),
        }
        return {
            "success": True,
            "message": f"Data source '{source_name}' added",
        }


class ProjectManagementTool(BaseTool):
    """Tool for managing projects, sprints, and team workflows."""

    def __init__(self):
        super().__init__(
            "project_management",
            "Create projects, manage sprints, track team progress"
        )
        self.projects = []
        self.sprints = []

    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute project management operations."""
        if action == "create_project":
            result = self._create_project(**kwargs)
        elif action == "start_sprint":
            result = self._start_sprint(**kwargs)
        elif action == "update_progress":
            result = self._update_progress(**kwargs)
        else:
            result = {"error": f"Unknown action: {action}"}

        self.log_execution(result)
        return result

    def _create_project(self, name: str, description: str, team_size: int) -> Dict[str, Any]:
        """Create a new project."""
        project = {
            "name": name,
            "description": description,
            "team_size": team_size,
            "created_at": datetime.now().isoformat(),
            "status": "planning",
        }
        self.projects.append(project)
        return {
            "success": True,
            "message": f"Project '{name}' created",
            "project_id": len(self.projects),
        }

    def _start_sprint(self, project_id: int, duration_days: int, goals: List[str]) -> Dict[str, Any]:
        """Start a sprint."""
        sprint = {
            "project_id": project_id,
            "duration_days": duration_days,
            "goals": goals,
            "started_at": datetime.now().isoformat(),
            "status": "active",
        }
        self.sprints.append(sprint)
        return {
            "success": True,
            "message": f"Sprint started for project {project_id}",
            "sprint_id": len(self.sprints),
        }

    def _update_progress(self, sprint_id: int, progress_percent: int) -> Dict[str, Any]:
        """Update sprint progress."""
        if 0 <= sprint_id < len(self.sprints):
            self.sprints[sprint_id]["progress"] = progress_percent
            return {
                "success": True,
                "message": f"Sprint {sprint_id} progress: {progress_percent}%",
            }
        return {"error": f"Sprint {sprint_id} not found"}


class ToolRegistry:
    """Registry for managing available tools."""

    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self._init_default_tools()

    def _init_default_tools(self):
        """Initialize default tools."""
        self.register_tool(EmailTool())
        self.register_tool(CalendarTool())
        self.register_tool(DataAnalysisTool())
        self.register_tool(ProjectManagementTool())

    def register_tool(self, tool: BaseTool):
        """Register a tool."""
        self.tools[tool.name] = tool

    def get_tool(self, tool_name: str) -> Optional[BaseTool]:
        """Get a tool by name."""
        return self.tools.get(tool_name)

    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools."""
        return [tool.get_schema() for tool in self.tools.values()]

    def execute_tool(self, tool_name: str, action: str, **kwargs) -> Dict[str, Any]:
        """Execute a tool action."""
        tool = self.get_tool(tool_name)
        if not tool:
            return {"error": f"Tool '{tool_name}' not found"}

        return tool.execute(action=action, **kwargs)

    def get_tool_description(self, tool_name: str) -> Optional[str]:
        """Get description of a tool."""
        tool = self.get_tool(tool_name)
        return tool.description if tool else None
