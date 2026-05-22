# Master Orchestrator Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│         Master Orchestrator - Strategic AI Partner          │
│                                                               │
│  Claude Opus 4.7 with Adaptive Thinking                     │
│  + Extended Context + Agentic Reasoning                     │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
        ┌──────▼──────┐  ┌────▼──────┐  ┌──▼───────┐
        │  Company    │  │   Task    │  │   Agent  │
        │ Management  │  │ Management│  │Orchestr. │
        └─────────────┘  └───────────┘  └──────────┘
                │
                └──────────┬──────────┐
                           │          │
                    ┌──────▼─────┐  ┌─▼────────────┐
                    │    Tools   │  │  Persistence │
                    │  Registry  │  │  & State Mgt │
                    └────────────┘  └───────────────┘
```

## Components

### 1. Core Agent (`orchestrator.py`)

**Responsibility:** Strategic planning and decision-making

**Key Classes:**
- `MasterOrchestrator` - Main agent with Claude integration
  - Uses Claude Opus 4.7 (most capable model)
  - Adaptive thinking enabled for complex reasoning
  - 1M token context window
  - Streaming support for long responses

**Features:**
- Company lifecycle management
- Agent spawning and coordination
- Task creation and tracking
- Conversation history management
- Operational logging
- Strategic decision-making

**Example Usage:**
```python
orchestrator = MasterOrchestrator()
orchestrator.add_company("StartupX", "AI platform", "SaaS")
response = orchestrator.process_user_request("Strategic question")
```

### 2. Advanced Orchestrator (`advanced_orchestrator.py`)

**Responsibility:** Persistence and metrics tracking

**Key Classes:**
- `AdvancedOrchestrator` - Extends base with state management
- `StateManager` - Handles session save/load

**Features:**
- Session persistence to JSON
- Metrics tracking
- Company summaries
- Agent summaries
- Multi-session management
- Session loading on startup

**Example Usage:**
```python
orchestrator = AdvancedOrchestrator("my_session")
orchestrator.save_session()  # Persist state
metrics = orchestrator.get_metrics()  # Get performance data
```

### 3. Tool-Enabled Orchestrator (`orchestrator_with_tools.py`)

**Responsibility:** Execution of external actions

**Key Classes:**
- `ToolEnabledOrchestrator` - Extends advanced with tools
- Integrates with tool registry

**Features:**
- Tool awareness in responses
- Tool execution framework
- Tool status monitoring
- Extended system prompt with tool info
- Autonomous action execution

**Example Usage:**
```python
orchestrator = ToolEnabledOrchestrator()
result = orchestrator.use_email_tool("send", to="team@example.com")
```

### 4. Tools Framework (`tools.py`)

**Responsibility:** Extensible integration system

**Key Classes:**
- `BaseTool` - Abstract base for all tools
- `EmailTool` - Email communication
- `CalendarTool` - Meeting scheduling
- `DataAnalysisTool` - Reporting and metrics
- `ProjectManagementTool` - Project workflows
- `ToolRegistry` - Tool management and execution

**Design Pattern:** Registry + Strategy
- Each tool implements BaseTool
- Tools registered in ToolRegistry
- Unified interface for tool execution
- Easy to add custom tools

**Example Custom Tool:**
```python
class CustomTool(BaseTool):
    def execute(self, **kwargs):
        # Implementation
        pass

registry.register_tool(CustomTool())
```

### 5. Persistence Layer (`persistence.py`)

**Responsibility:** State management and session lifecycle

**Key Classes:**
- `StateManager` - Saves/loads orchestrator state

**Features:**
- JSON-based persistence
- Session listing
- Session export/import
- Timestamp tracking
- Complete state capture

**Data Structure:**
```json
{
  "timestamp": "2026-05-22T10:30:00",
  "session_name": "my_session",
  "companies": {...},
  "active_tasks": {...},
  "sub_agents": {...},
  "operational_log": [...],
  "conversation_history": [...]
}
```

## Architecture Layers

### Layer 1: Agent Intelligence
```
User Input → Claude Opus 4.7 → Strategic Response
                    ↓
            Adaptive Thinking
            Extended Context
            Agentic Reasoning
```

### Layer 2: State Management
```
Companies ──┐
Tasks       ├→ MemoryModel ──→ StateManager ──→ Persistence
Agents ─────┤
Conversation┘
```

### Layer 3: Tool Execution
```
Agent Request → Tool Registry → Specific Tool → External Action
                       ↓
                  Logging & Metrics
```

## Data Models

### Company
```python
{
    "name": str,
    "description": str,
    "industry": str,
    "created_at": datetime,
    "status": str,
    "tasks": [task_id]
}
```

### Task
```python
{
    "id": str,
    "title": str,
    "description": str,
    "assigned_to": str,  # agent or company name
    "priority": str,  # critical, high, medium, low
    "deadline": datetime,
    "created_at": datetime,
    "status": str,
    "progress": int  # 0-100
}
```

### Agent
```python
{
    "name": str,
    "specialization": str,
    "created_at": datetime,
    "status": str,
    "assigned_tasks": [task_id]
}
```

### OperationalLog
```python
{
    "timestamp": datetime,
    "message": str
}
```

## Communication Flow

### Single Request Flow
```
┌─────────┐
│  User   │
│ Request │
└────┬────┘
     │
     ▼
┌─────────────────────────────┐
│  MasterOrchestrator         │
│  - Add context              │
│  - Prepare conversation     │
│  - Add operational context  │
└────┬────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│  Claude Opus 4.7            │
│  - Analyze request          │
│  - Use adaptive thinking    │
│  - Consider context         │
│  - Generate response        │
└────┬────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│  Response Processing        │
│  - Check for tool use       │
│  - Log operation            │
│  - Update state             │
└────┬────────────────────────┘
     │
     ▼
┌─────────┐
│ Output  │
└─────────┘
```

### Multi-Turn Conversation Flow
```
Turn 1: User → Agent → Response → Log
Turn 2: User + History → Agent → Response → Log
Turn 3: User + History → Agent → Response → Log
...
SavePoint: Conversation History + State → Persistence
```

### Tool Execution Flow
```
Agent identifies tool need
        ↓
Tool Registry lookup
        ↓
Tool instantiation
        ↓
Action execution
        ↓
Result logging
        ↓
State update
        ↓
Response incorporation
```

## Design Patterns

### 1. **Registry Pattern** (Tools)
Multiple tools registered in a central registry. Clean separation of concerns.

### 2. **Strategy Pattern** (BaseTool)
Each tool implements the same interface but different strategies.

### 3. **State Pattern** (Orchestrator)
Orchestrator tracks state through lifecycle (planning → executing → reflecting).

### 4. **Observer Pattern** (Logging)
All operations observed and logged for audit trail.

### 5. **Facade Pattern** (Advanced Orchestrator)
Simplifies interaction by wrapping complex persistence logic.

## Extension Points

### Adding New Tools
```python
class MyTool(BaseTool):
    def execute(self, action: str, **kwargs):
        # Implement tool logic
        pass
```

### Custom Orchestrator Variants
```python
class SpecializedOrchestrator(ToolEnabledOrchestrator):
    def _build_enhanced_system_prompt(self):
        # Custom system prompt
        pass
```

### New Persistent Data
```python
class StateManager:
    def save_state(self, orchestrator):
        # Already captures all custom attributes
        pass
```

## Performance Characteristics

### Memory
- Conversation history: ~1-5KB per turn
- Companies/Tasks/Agents: ~100 bytes each
- Operational log: ~50 bytes per entry
- Total: Grows linearly with usage

### Processing
- Single request: 1-5 seconds (includes API call)
- Tool execution: 100-500ms per tool
- Persistence: 50-200ms per save
- Startup: 100-300ms (load session)

### Token Usage
- Base request: 500-2000 tokens
- With extended thinking: 2000-10000 tokens
- Context window: Up to 1M tokens available
- Estimated monthly cost: Depends on usage frequency

## Security Considerations

1. **API Key Management**
   - Stored in `.env` (not in code)
   - Uses environment variables
   - Never logged or exposed

2. **State Persistence**
   - Local JSON files
   - File permissions: User-owned
   - No encryption (can be added)

3. **Tool Execution**
   - Isolated tool methods
   - No shell access by default
   - Tools can be restricted by role

4. **Conversation Privacy**
   - Stored locally
   - Can be exported
   - Deletable per session

## Scalability

### Current Limits
- Single orchestrator instance
- In-memory state
- Local persistence
- Single API connection

### Future Improvements
- Database backend (PostgreSQL)
- Distributed orchestrators
- Message queues (Redis)
- Load balancing
- Caching layer

## Testing

### Test Coverage
```
test_orchestrator.py        # Basic operations
test_advanced.py            # Persistence
tools_test.py (implicit)    # Tool execution
```

### Testing Approach
- Unit tests for each component
- Integration tests for workflows
- Manual testing for agent responses

### Adding Tests
```python
def test_new_feature():
    orchestrator = MasterOrchestrator()
    # Test logic
    assert expected == actual
```

## Documentation Structure

```
README.md           - Overview and quick start
QUICKSTART.md       - 5-minute setup
USAGE_GUIDE.md      - Complete feature guide
ROADMAP.md          - Future development
ARCHITECTURE.md     - This file
config.py           - Configuration constants
```

## Deployment Options

### Local (Current)
```bash
python orchestrator.py
```

### Docker (Future)
```bash
docker run master-orchestrator
```

### Cloud (Future)
- AWS Lambda
- Google Cloud Functions
- Azure Functions
- Kubernetes

## Integration Points

### External Systems
- Anthropic Claude API (core)
- Email providers (future)
- Calendar services (future)
- Financial APIs (future)
- CRM platforms (future)

### File Formats
- JSON (session state)
- Python objects (in-memory)
- Environment variables (.env)

---

## Key Decisions

1. **Claude Opus 4.7** - Maximum capability for strategic thinking
2. **Adaptive Thinking** - No fixed token budget, model decides depth
3. **JSON Persistence** - Simple, portable, human-readable
4. **Tool Registry Pattern** - Extensible without modifying core
5. **Conversation History** - Full context for multi-turn interactions
6. **No Database Yet** - Keep initial deployment simple

---

## Future Architectural Changes

### Database Migration
- PostgreSQL for production
- SQLAlchemy ORM
- Migration scripts

### API Layer
- FastAPI for REST endpoints
- WebSocket for real-time
- GraphQL schema (optional)

### Monitoring
- Prometheus metrics
- ELK stack for logging
- Distributed tracing

### Containerization
- Docker for local dev
- Docker Compose for dependencies
- Kubernetes manifests for cloud

---

**Last Updated:** May 22, 2026
**Current Version:** 1.0.0
**Status:** Production Ready (Phase 1)
