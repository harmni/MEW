"""
Configuration and constants for the Master Orchestrator.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = "claude-opus-4-7"
MAX_TOKENS = 4096
THINKING_TYPE = "adaptive"

# Orchestrator Configuration
ORCHESTRATOR_MODE = os.getenv("ORCHESTRATOR_MODE", "interactive")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Task Priorities
PRIORITY_CRITICAL = "critical"
PRIORITY_HIGH = "high"
PRIORITY_MEDIUM = "medium"
PRIORITY_LOW = "low"

# Task Statuses
STATUS_PENDING = "pending"
STATUS_IN_PROGRESS = "in_progress"
STATUS_COMPLETED = "completed"
STATUS_BLOCKED = "blocked"
STATUS_CANCELLED = "cancelled"

# Agent Specializations
SPECIALIZATIONS = [
    "product_development",
    "marketing_and_growth",
    "financial_management",
    "operations",
    "customer_success",
    "research_and_analysis",
    "technical_architecture",
    "risk_management",
]

# Common Industries
INDUSTRIES = [
    "SaaS",
    "E-Commerce",
    "Consulting",
    "Manufacturing",
    "Healthcare",
    "FinTech",
    "EdTech",
    "Media",
    "Real Estate",
    "Logistics",
]
