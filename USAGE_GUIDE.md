# Master Orchestrator - Complete Usage Guide

Your sovereign AI partner for building and managing an empire across multiple ventures.

## What You Have

### Three Levels of Orchestrator

#### 1. **Base Orchestrator** (`orchestrator.py`)
Simple, focused agent with core functionality:
```bash
python orchestrator.py
```
**Use when:** You want a clean, minimal interface to interact with Claude

#### 2. **Advanced Orchestrator** (`advanced_orchestrator.py`)
Enhanced with state persistence and metrics:
```bash
python advanced_orchestrator.py
```
**Use when:** You want to persist sessions across runs and track metrics

#### 3. **Tool-Enabled Orchestrator** (`orchestrator_with_tools.py`)
Full-featured with integrated external tools:
```bash
python orchestrator_with_tools.py
```
**Use when:** You want autonomous execution of emails, calendar, analytics, and projects

## Quick Start

### Basic Interaction

```bash
# Set up
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env

# Run the orchestrator
python orchestrator.py
```

You'll see a prompt where you can type natural language requests:

```
You: I want to launch a SaaS company focused on AI automation
Orchestrator: I'll help you create a strategic plan for your AI automation SaaS...
```

### Register Your Companies

```
You: add company MyAIProduct SaaS
✓ Company 'MyAIProduct' registered

You: add company ConsultingArm Consulting
✓ Company 'ConsultingArm' registered
```

### Create Your Team

```
You: spawn agent EngineeringTeam technical_architecture
✓ Agent 'EngineeringTeam' spawned

You: spawn agent MarketingTeam marketing_and_growth
✓ Agent 'MarketingTeam' spawned

You: spawn agent OperationsTeam operations
✓ Agent 'OperationsTeam' spawned
```

### Create and Track Tasks

```
You: create task Build MVP - Phase 1

You: What's the detailed breakdown for building the MVP?
Orchestrator: Here's a comprehensive plan...
[Agent creates subtasks and timelines]
```

## Features by Orchestrator Type

### Base Orchestrator Features
✓ Company management (register, track)
✓ Agent spawning and coordination
✓ Task creation and tracking
✓ Interactive conversation
✓ Claude Opus 4.7 with adaptive thinking
✓ Operational logging
✓ Status tracking

### Advanced Orchestrator Features
✓ **Everything from Base**
✓ **State Persistence:** Save/load sessions automatically
✓ **Session Management:** Create multiple sessions, resume old ones
✓ **Metrics Tracking:** Track requests, tasks, companies, agents
✓ **Company Summaries:** Get detailed company status
✓ **Agent Summaries:** Get detailed agent information

### Tool-Enabled Orchestrator Features
✓ **Everything from Advanced**
✓ **Email Tool:** Send emails, schedule communications
✓ **Calendar Tool:** Schedule meetings, manage availability
✓ **Data Analysis:** Generate reports, track metrics
✓ **Project Management:** Create projects, manage sprints
✓ **Tool Registry:** Extensible system for custom tools
✓ **Tool Status Monitoring:** Track tool usage

## Advanced Usage Patterns

### Pattern 1: Strategic Planning

```python
from orchestrator import MasterOrchestrator

orchestrator = MasterOrchestrator()

# Set up your ventures
orchestrator.add_company("Venture A", "SaaS platform", "SaaS")
orchestrator.add_company("Venture B", "Services", "Consulting")

# Get strategic advice
response = orchestrator.process_user_request("""
I have two ventures: a SaaS product and a consulting firm.
How should I structure them to maximize synergy while maintaining focus?
What's the optimal allocation of my time and resources?
""")

print(response)
```

### Pattern 2: Multi-Company Management

```python
from advanced_orchestrator import AdvancedOrchestrator

# Create a named session
orchestrator = AdvancedOrchestrator("my_empire_2026")

# Build your empire
companies = ["TechVentures", "DataConsulting", "AIProducts"]
for company in companies:
    orchestrator.add_company(company, f"Description of {company}", "SaaS")

# Get cross-company insights
response = orchestrator.process_user_request("""
Now that I have multiple companies, what are the key integration points?
Where can I achieve economies of scale?
What's the synergy multiplier if I align them properly?
""")

# Save your progress
orchestrator.save_session()
```

### Pattern 3: Autonomous Task Execution

```python
from orchestrator_with_tools import ToolEnabledOrchestrator

orchestrator = ToolEnabledOrchestrator()

# Set up infrastructure
orchestrator.add_company("Startup", "My startup", "SaaS")
orchestrator.spawn_sub_agent("TeamLead", "operations")

# Create task with autonomy
orchestrator.create_task(
    task_id="Q2_KICKOFF",
    title="Q2 Team Kickoff",
    description="Launch Q2 with team alignment",
    assigned_to="TeamLead",
    priority="high"
)

# The orchestrator can:
# - Send calendar invites
# - Schedule meeting notifications
# - Generate progress reports
# - Track team availability
```

### Pattern 4: Decision Analysis

Use the orchestrator's thinking to analyze complex decisions:

```
You: I'm choosing between three growth strategies:

1. Expand our existing product to enterprise market
   - High revenue potential ($5M+ ARR)
   - Requires $500K investment
   - 6-month development timeline

2. Launch a new product line for SMBs
   - Faster path to revenue
   - Larger addressable market
   - Lower margins initially

3. Acquire 2-3 competitors
   - Consolidation play
   - 3x customer base growth
   - Integration complexity

Which should I pursue? What's the optimal phased approach?

Orchestrator: [Uses extended thinking to analyze opportunity cost,
risk/reward, timeline, and resource requirements for each option]
```

## Session Management

### Save Your Work

```
You: save
✓ Session saved
```

### Load Previous Session

```bash
python advanced_orchestrator.py
# On startup, prompts to load a previous session
```

### View All Sessions

```
You: sessions
--- SAVED SESSIONS ---
  my_empire_2026: 5 companies, 12 tasks, 3 agents
  q2_planning_2026: 3 companies, 8 tasks, 2 agents
  startup_launch: 2 companies, 15 tasks, 4 agents
```

## Tool Usage

### Email Tool

```
You: Schedule a strategic planning meeting with the team.
You should send an email to all stakeholders.

Orchestrator: [Considers the request and uses the email tool to
send strategic meeting invitations to your team]
```

### Calendar Tool

```
You: Block off time next week for uninterrupted focus work.

Orchestrator: [Uses calendar tool to set availability and send
meeting blocks to protect your focus time]
```

### Data Analysis Tool

```
You: Generate a comprehensive Q2 performance report covering:
- Revenue metrics
- Growth trends
- Team productivity
- Customer satisfaction

Orchestrator: [Uses data analysis tool to generate and structure
a professional quarterly report]
```

### Project Management Tool

```
You: create task Launch New Product

You: Break this into a detailed project plan with milestones.

Orchestrator: [Uses project management tool to create sprints,
define deliverables, and establish timeline]
```

## Extending the System

### Create Custom Tools

```python
from tools import BaseTool

class SlackTool(BaseTool):
    def __init__(self):
        super().__init__("slack", "Post messages, manage channels")
    
    def execute(self, action: str, **kwargs):
        if action == "post_message":
            return self._post_message(**kwargs)
        return {"error": f"Unknown action: {action}"}
    
    def _post_message(self, channel: str, message: str, **kwargs):
        # Implementation
        return {"success": True, "message": f"Posted to {channel}"}

# Register custom tool
orchestrator.tool_registry.register_tool(SlackTool())
```

### Create Domain-Specific Orchestrators

```python
class SalesOrchestrator(ToolEnabledOrchestrator):
    """Specialized for sales operations"""
    
    def _build_enhanced_system_prompt(self):
        prompt = super()._build_enhanced_system_prompt()
        sales_context = """
        You're optimized for sales operations including:
        - Deal tracking and pipeline management
        - Customer relationship management
        - Revenue forecasting
        - Sales team coordination
        """
        return prompt + sales_context
```

## Best Practices

### 1. **Clear Intent Communication**
```
Bad: "Do marketing stuff"
Good: "Create a growth strategy for enterprise customers targeting
       $10K+ ARR with focus on partnerships and case studies"
```

### 2. **Regular Checkpoints**
```
You: Give me a comprehensive status update on all current initiatives
     including metrics, blockers, and recommendations

Orchestrator: [Provides strategic overview with actionable insights]
```

### 3. **Task Organization**
```
You: create task [Major Initiative Name]

You: What's the 90-day plan to execute [Major Initiative]?

Orchestrator: [Breaks into phases with milestones, resource needs,
              success metrics, risk mitigation]
```

### 4. **Leverage the Thinking**
Ask for deep analysis on strategic decisions. The agent uses adaptive
thinking to reason through complex problems:

```
You: Should I raise a Series A now or bootstrap for one more year?

Orchestrator: [Uses extended thinking to analyze runway, growth rates,
              market conditions, investor landscape, and options]
```

### 5. **Session Persistence**
Always name your sessions meaningfully:

```python
orchestrator = AdvancedOrchestrator("ventures_2026_q2")
```

## Command Reference

### Session Commands
- `save` - Save current session
- `sessions` - List all saved sessions
- `exit` - End session (with save prompt)

### Information Commands
- `status` - View operational status
- `metrics` - View orchestrator metrics
- `tools` - View available tools
- `company <name>` - Get company summary
- `agent <name>` - Get agent summary

### Setup Commands
- `add company <name> <industry>` - Register a company
- `spawn agent <name> <specialization>` - Create an agent
- `create task <title>` - Create a task

## Examples

### Example 1: Startup Launch
```bash
python examples.py 1
```
Shows how to launch a startup with team coordination

### Example 2: Multi-Company Management
```bash
python examples.py 2
```
Shows how to manage multiple ventures simultaneously

### Example 3: Task Automation
```bash
python examples.py 3
```
Shows how to automate complex task workflows

### Example 4: Strategic Decision Making
```bash
python examples.py 4
```
Shows how to use the orchestrator for complex decisions

## API Reference

### MasterOrchestrator Methods

```python
orchestrator.add_company(name, description, industry)
orchestrator.spawn_sub_agent(name, specialization)
orchestrator.create_task(task_id, title, description, assigned_to, priority, deadline)
orchestrator.update_task_status(task_id, status, progress)
orchestrator.process_user_request(message)
```

### AdvancedOrchestrator Methods
```python
orchestrator.save_session()
orchestrator.load_session(name)
orchestrator.get_metrics()
orchestrator.get_company_summary(name)
orchestrator.get_agent_summary(name)
```

### ToolEnabledOrchestrator Methods
```python
orchestrator.use_email_tool(action, **kwargs)
orchestrator.use_calendar_tool(action, **kwargs)
orchestrator.use_data_analysis_tool(action, **kwargs)
orchestrator.use_project_management_tool(action, **kwargs)
orchestrator.get_tool_status()
```

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
- Create `.env` file with your API key
- Check file permissions
- Verify API key is valid

### Session not loading
- Check session name spelling
- List sessions with `sessions` command
- Ensure session file exists in `orchestrator_state/`

### Tool execution issues
- Verify tool is registered: `metrics` then `tools`
- Check tool action spelling
- Refer to tool documentation

## Next Steps

1. **Set your ANTHROPIC_API_KEY** in `.env`
2. **Run the orchestrator** with `python orchestrator.py`
3. **Register your companies** and agents
4. **Start giving strategic direction** to your orchestrator
5. **Save your sessions** as you build
6. **Expand with custom tools** as needs grow

---

## Your Empire Awaits

You now have a sovereign AI partner that can:
- Manage multiple business ventures
- Coordinate complex projects
- Execute autonomous tasks
- Make strategic decisions
- Scale your operations
- Learn from outcomes

**Tell it what to build, and watch it plan and execute.**
