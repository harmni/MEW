#!/usr/bin/env python3
"""
Example usage patterns for the Master Orchestrator Agent.
Demonstrates how to use the orchestrator programmatically.
"""

from orchestrator import MasterOrchestrator


def example_startup_launch():
    """Example: Launch a new startup with multiple initiatives."""
    print("\n=== EXAMPLE: Startup Launch ===\n")

    orchestrator = MasterOrchestrator()

    # Register the company
    orchestrator.add_company(
        name="TechVentures AI",
        description="AI-powered SaaS platform for business automation",
        industry="SaaS",
    )

    # Spawn specialized agents
    orchestrator.spawn_sub_agent("ProductAgent", "product_development")
    orchestrator.spawn_sub_agent("MarketingAgent", "marketing_and_growth")
    orchestrator.spawn_sub_agent("EngineeringAgent", "technical_architecture")

    # Create initial tasks
    orchestrator.create_task(
        task_id="TECH_001",
        title="Design MVP Architecture",
        description="Design scalable architecture for the platform",
        assigned_to="EngineeringAgent",
        priority="high",
        deadline="2026-06-15",
    )

    orchestrator.create_task(
        task_id="TECH_002",
        title="Create Product Roadmap",
        description="Define 12-month product roadmap with features",
        assigned_to="ProductAgent",
        priority="high",
        deadline="2026-06-10",
    )

    # Process a strategic request
    request = """
    We're launching a new SaaS company focused on AI automation.
    We have 3 months until demo day. What should our priorities be?
    How should we allocate our team?
    """

    print("Request to Orchestrator:")
    print(request)
    print("\n" + "=" * 50 + "\n")

    response = orchestrator.process_user_request(request)
    print("Orchestrator Response:")
    print(response)


def example_multi_company_management():
    """Example: Manage multiple companies simultaneously."""
    print("\n=== EXAMPLE: Multi-Company Management ===\n")

    orchestrator = MasterOrchestrator()

    # Set up multiple companies
    companies = [
        ("AgentAPI", "API infrastructure for multi-agent systems", "SaaS"),
        ("DataConsulting", "Data strategy and analytics consulting", "Consulting"),
        ("AIContent", "AI-powered content creation platform", "SaaS"),
    ]

    for name, description, industry in companies:
        orchestrator.add_company(name, description, industry)
        print(f"✓ Registered {name}")

    # Spawn cross-company agents
    orchestrator.spawn_sub_agent("CFO_Agent", "financial_management")
    orchestrator.spawn_sub_agent("COO_Agent", "operations")

    # Make a strategic decision
    request = """
    I now have 3 companies operating. How should I structure them for:
    1. Maximum synergy and shared resources
    2. Efficient scaling
    3. Risk management across the portfolio

    Which should I focus on first? What opportunities do you see?
    """

    print("\nStrategic Request:")
    print(request)
    print("\n" + "=" * 50 + "\n")

    response = orchestrator.process_user_request(request)
    print("Strategic Analysis:")
    print(response)


def example_task_automation():
    """Example: Automate complex tasks across agents."""
    print("\n=== EXAMPLE: Task Automation ===\n")

    orchestrator = MasterOrchestrator()

    # Set up infrastructure
    orchestrator.add_company("AutomatedOps", "Operations automation platform", "SaaS")
    orchestrator.spawn_sub_agent("OpsAgent", "operations")
    orchestrator.spawn_sub_agent("MonitoringAgent", "research_and_analysis")

    # Create a complex task with sub-tasks
    main_task = "QUARTERLY_REVIEW_001"
    orchestrator.create_task(
        task_id=main_task,
        title="Q2 2026 Quarterly Business Review",
        description="Comprehensive review of all operations, financials, and strategy",
        assigned_to="OpsAgent",
        priority="high",
        deadline="2026-06-30",
    )

    # Request analysis
    request = """
    Please conduct a comprehensive quarterly review covering:
    - Financial performance
    - Team productivity
    - Product roadmap progress
    - Customer satisfaction metrics
    - Risk assessment
    - Opportunities for the next quarter

    Format as an executive summary.
    """

    print("Quarterly Review Request:")
    print(request)
    print("\n" + "=" * 50 + "\n")

    response = orchestrator.process_user_request(request)
    print("Quarterly Review Output:")
    print(response)

    # Update task status
    orchestrator.update_task_status(main_task, "completed", progress=100)


def example_strategic_decision_making():
    """Example: Use orchestrator for complex strategic decisions."""
    print("\n=== EXAMPLE: Strategic Decision Making ===\n")

    orchestrator = MasterOrchestrator()

    # Setup
    orchestrator.add_company("Innovation Lab", "New venture creation", "SaaS")
    orchestrator.spawn_sub_agent("StrategyAgent", "research_and_analysis")

    request = """
    I'm deciding between three opportunities:

    1. OPPORTUNITY A: Expand our AI platform to enterprise market
       - High revenue potential ($5M+ ARR)
       - Requires 6-month development
       - Needs $500K initial investment
       - Medium competition

    2. OPPORTUNITY B: Launch marketplace for AI services
       - Lower entry barrier
       - Faster path to revenue
       - Network effects = long-term advantage
       - Requires community building

    3. OPPORTUNITY C: Acquire and integrate 2-3 smaller competitors
       - Increase customer base by 3x
       - Consolidation play
       - High integration risk
       - Requires capital raise

    Which should I pursue? What's the optimal strategy?
    """

    print("Strategic Decision Request:")
    print(request)
    print("\n" + "=" * 50 + "\n")

    response = orchestrator.process_user_request(request)
    print("Strategic Recommendation:")
    print(response)


if __name__ == "__main__":
    import sys

    examples = {
        "1": ("Startup Launch", example_startup_launch),
        "2": ("Multi-Company Management", example_multi_company_management),
        "3": ("Task Automation", example_task_automation),
        "4": ("Strategic Decision Making", example_strategic_decision_making),
    }

    if len(sys.argv) > 1 and sys.argv[1] in examples:
        _, example_func = examples[sys.argv[1]]
        example_func()
    else:
        print("Master Orchestrator - Example Usage Patterns\n")
        print("Usage: python examples.py <number>")
        print("\nAvailable examples:")
        for key, (title, _) in examples.items():
            print(f"  {key}: {title}")
        print("\nExample: python examples.py 1")
