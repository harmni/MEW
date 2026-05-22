# Quick Start Guide - Master Orchestrator Agent

## 5-Minute Setup

### 1. Get Your API Key
- Go to https://console.anthropic.com
- Create your API key
- Keep it safe

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and paste your ANTHROPIC_API_KEY
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Orchestrator
```bash
python orchestrator.py
```

You'll see:
```
============================================================
MASTER ORCHESTRATOR - Ready to build your empire
============================================================

Commands:
  'add company <name> <industry>' - Register a new company
  'spawn agent <name> <specialization>' - Create a sub-agent
  'create task <title>' - Create a task
  'status' - View operational status
  'exit' - End session

Or simply describe what you want to accomplish...

You: 
```

## Example Interactions

### Scenario 1: Launch a New Startup
```
You: add company MyStartup SaaS
✓ Company 'MyStartup' registered

You: spawn agent ProductTeam product_development
✓ Agent 'ProductTeam' spawned

You: We need to build a product that helps teams collaborate.
What should our first 90 days look like?

Orchestrator: [Provides comprehensive 90-day roadmap with milestones, 
resource allocation, and risk assessment]
```

### Scenario 2: Multi-Company Management
```
You: I'm managing 3 companies now. How should I structure operations
for synergy while maintaining focus?

Orchestrator: [Analyzes cross-company opportunities, suggests shared 
resources and integrated systems]
```

### Scenario 3: Task Automation
```
You: create task Build customer portal

You: What are the sub-tasks and timeline for the customer portal?
Who should lead it?

Orchestrator: [Breaks down into detailed technical tasks, 
assigns to agents, provides estimates]
```

## Features You Have Now

✅ **Company Management**
- Register multiple companies
- Track status and operations
- Organize by industry

✅ **Agent Coordination**
- Spawn specialized agents
- Assign work to agents
- Track agent performance

✅ **Task Management**
- Create and track tasks
- Update progress
- Set priorities and deadlines

✅ **Strategic Thinking**
- Claude Opus 4.7 (most capable model)
- Adaptive thinking for complex decisions
- Long conversation context

✅ **Autonomous Operation**
- Agent operates independently
- Makes decisions within parameters
- Escalates when needed

## Advanced Usage

### Run Examples
```bash
python examples.py 1    # Startup launch
python examples.py 2    # Multi-company management
python examples.py 3    # Task automation
python examples.py 4    # Strategic decisions
```

### Check Operational Status
```
You: status

--- OPERATIONAL STATUS ---
Companies: 2
Active Tasks: 5
Sub-Agents: 3
Operations Logged: 12
```

### View Current Context
All your companies, tasks, and agents are visible to the orchestrator
in every interaction. It maintains full context of your operations.

## Tips for Success

### Give Clear Direction
```
Bad: "Do marketing stuff"
Good: "Create a growth plan for Q2 targeting enterprise customers
with $10K+ ARR. Focus on partnerships and case studies."
```

### Use Regular Check-ins
```
You: What's the status on all our current initiatives?
Orchestrator: [Comprehensive status report with metrics and recommendations]
```

### Leverage the Thinking
The agent uses adaptive thinking to reason through complex strategic
problems. Let it think deeply before responding to strategic questions.

### Organize with Tasks
```
You: create task Implement user authentication

You: Create a detailed project plan for user authentication
with timeline and team assignments.

Orchestrator: [Detailed breakdown of auth implementation]
```

## What's Next

The orchestrator is ready to:
1. Help you launch new ventures
2. Manage multiple companies
3. Coordinate complex projects
4. Make strategic decisions
5. Automate routine operations
6. Scale your business

## Need Help?

Check the README.md for:
- Detailed API reference
- Architecture overview
- Configuration options
- Roadmap and upcoming features

---

**You're all set. Tell the orchestrator what you want to build, and watch it plan and execute.**
