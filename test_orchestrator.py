#!/usr/bin/env python3
"""
Quick test of the Master Orchestrator Agent.
Tests basic functionality without requiring API interaction.
"""

from orchestrator import MasterOrchestrator


def test_basic_operations():
    """Test basic orchestrator operations."""
    print("Testing Master Orchestrator...\n")

    orchestrator = MasterOrchestrator()

    # Test 1: Add a company
    print("1. Testing company registration...")
    company = orchestrator.add_company(
        "TestCorp", "A test company", "SaaS"
    )
    assert company["name"] == "TestCorp"
    assert "TestCorp" in orchestrator.companies
    print("   ✓ Company registration works")

    # Test 2: Spawn a sub-agent
    print("2. Testing sub-agent spawning...")
    agent = orchestrator.spawn_sub_agent("TestAgent", "product_development")
    assert agent["name"] == "TestAgent"
    assert "TestAgent" in orchestrator.sub_agents
    print("   ✓ Sub-agent spawning works")

    # Test 3: Create a task
    print("3. Testing task creation...")
    task = orchestrator.create_task(
        task_id="TEST_001",
        title="Test Task",
        description="A test task",
        assigned_to="TestAgent",
    )
    assert task["title"] == "Test Task"
    assert "TEST_001" in orchestrator.active_tasks
    print("   ✓ Task creation works")

    # Test 4: Update task status
    print("4. Testing task status update...")
    updated = orchestrator.update_task_status("TEST_001", "in_progress", 50)
    assert updated["status"] == "in_progress"
    assert updated["progress"] == 50
    print("   ✓ Task status update works")

    # Test 5: Operational logging
    print("5. Testing operational logging...")
    assert len(orchestrator.operational_log) > 0
    print(f"   ✓ Operational log has {len(orchestrator.operational_log)} entries")

    print("\n✓ All basic operations test passed!")
    print("\nOrchestrator is ready for use. Next steps:")
    print("1. Set your ANTHROPIC_API_KEY in .env file")
    print("2. Run: python orchestrator.py (for interactive mode)")
    print("3. Or run: python examples.py <number> (for example usage)")


if __name__ == "__main__":
    test_basic_operations()
