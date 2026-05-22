# Master Orchestrator Agent

A sovereign AI agent designed to be your strategic partner in building and managing multiple companies, automating tasks, and coordinating other AI agents across all functions of your life.

## Vision

The Master Orchestrator is your autonomous business partner - an intelligent agent that:
- **Oversees multiple companies** with different focuses and industries
- **Orchestrates complex tasks** by breaking them into executable steps
- **Coordinates sub-agents** for specialized work
- **Operates autonomously** on strategic decisions within your parameters
- **Learns and adapts** from outcomes and feedback
- **Scales your impact** through intelligent automation and delegation

## Features

### Core Capabilities
- **Strategic Planning**: Analyze opportunities and create growth strategies
- **Task Management**: Break complex goals into executable tasks with timelines
- **Company Management**: Track and oversee multiple business operations
- **Agent Coordination**: Spawn and manage specialized sub-agents
- **Autonomous Execution**: Execute decisions within defined parameters
- **Resource Optimization**: Allocate resources efficiently across ventures
- **Risk Management**: Identify and mitigate operational risks
- **Continuous Learning**: Improve strategies based on outcomes

### Technical Stack
- **Model**: Claude Opus 4.7 (latest, most capable)
- **Thinking**: Adaptive thinking enabled for complex strategic decisions
- **Language**: Python 3.8+
- **Framework**: Anthropic Python SDK

## Setup

### Prerequisites
- Python 3.8 or higher
- Anthropic API key (get one at https://console.anthropic.com)

### Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd MEW
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Usage

### Interactive Session

Start an interactive orchestrator session:
```bash
python orchestrator.py
```

You'll see a prompt where you can:
- Register companies: `add company CompanyName Industry`
- Spawn agents: `spawn agent AgentName Specialization`
- Create tasks: `create task TaskTitle`
- Check status: `status`
- Or just describe what you want to accomplish

### Example Interaction

```
You: I want to start a SaaS company for project management and a consulting firm

Orchestrator: I'll help you launch both ventures...
[Orchestrator analyzes market opportunities, creates task breakdown, spawns agents]

You: What's our timeline?

Orchestrator: Based on resources available, here's the phased approach...
[Provides strategic roadmap with milestones and agent assignments]
```

## Architecture

### Components

- **MasterOrchestrator**: Main agent that processes strategic requests
- **Companies**: Business entities under management
- **Tasks**: Atomic work units with tracking
- **Sub-Agents**: Specialized agents spawned for specific work
- **Operational Log**: Historical record of all decisions and actions

### Communication Flow

```
User Request
    ↓
Orchestrator (Claude Opus 4.7 with adaptive thinking)
    ├→ Analyzes current context
    ├→ Plans strategy
    ├→ Breaks into tasks
    ├→ Assigns to companies/agents
    └→ Executes and reports
```

## Configuration

Edit `orchestrator.py` to customize:
- Model selection (currently Opus 4.7)
- System prompt and strategic guidelines
- Task templates and workflows
- Company types and specializations

## Extending the System

### Add Custom Tools

The framework can be extended with custom tools for:
- Real-time data integration
- External API calls (CRM, accounting, etc.)
- Email and communication
- Calendar and scheduling
- Analytics and reporting

### Multi-Agent Workflows

Create specialized sub-agents for:
- Product development
- Marketing and growth
- Financial management
- Operations
- Customer success

## Best Practices

1. **Clear Goals**: Give the orchestrator specific, measurable objectives
2. **Regular Updates**: Check status and provide feedback regularly
3. **Context**: Remind the agent about strategic priorities
4. **Escalation**: Set clear rules for when decisions need your approval
5. **Iteration**: Refine strategies based on outcomes

## API Reference

### MasterOrchestrator

```python
# Initialize
orchestrator = MasterOrchestrator()

# Register a company
orchestrator.add_company("CompanyName", "Description", "Industry")

# Spawn a sub-agent
orchestrator.spawn_sub_agent("AgentName", "Specialization")

# Create a task
orchestrator.create_task(
    task_id="TASK_001",
    title="Build MVP",
    description="Create minimum viable product",
    assigned_to="product-agent",
    priority="high",
    deadline="2026-06-30"
)

# Update task status
orchestrator.update_task_status("TASK_001", "in_progress", progress=50)

# Process user request
response = orchestrator.process_user_request("Your strategic question here")
```

## Roadmap

### Phase 1: Core Agent
- ✅ Basic orchestrator structure
- ✅ Company management
- ✅ Task tracking
- ✅ Sub-agent spawning
- [ ] Database persistence

### Phase 2: Integration
- [ ] Email integration
- [ ] Calendar sync
- [ ] Slack/Discord communication
- [ ] Financial APIs

### Phase 3: Automation
- [ ] Autonomous task execution
- [ ] Scheduled operations
- [ ] Smart notifications
- [ ] Performance analytics

### Phase 4: Scale
- [ ] Multi-user support
- [ ] Team collaboration
- [ ] Advanced analytics
- [ ] Custom integrations

## Support & Feedback

For issues or feature requests, open an issue in the repository.

## License

Built with ❤️ to help you build something extraordinary.

---

**Your empire awaits. Let's build it together.**
