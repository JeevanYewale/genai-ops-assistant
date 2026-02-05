from crewai import Agent
from llm.client import call_llm, PlanSchema


def create_planner() -> Agent:
    return Agent(
        role="Planner",
        goal="Create step-by-step plans with tools",
        backstory="Expert strategist for AI ops.",
        tools=[],
        verbose=True,
        allow_delegation=False,
    )


def plan_task(task: str) -> dict:
    """Generate execution plan from task"""
    prompt = f"""
    Convert this task into a JSON plan with steps and tools needed.
    For each step, identify if it needs 'weather', 'github', or 'none'.
    
    Task: {task}
    
    Return JSON with 'steps' (list of action strings) and 'tools_needed' (list of tool names).
    """
    return call_llm(prompt, PlanSchema)
