from crewai import Agent
from llm.client import call_llm, FinalOutput


def create_verifier() -> Agent:
    return Agent(
        role="Verifier",
        goal="Validate results, fix issues, format final JSON",
        backstory="Quality assurance specialist.",
        tools=[],
        verbose=True,
        allow_delegation=False,
    )


def verify_results(task: str, execution_results: list) -> dict:
    """Verify execution results meet task requirements"""
    results_summary = "\n".join(
        [f"- {r['step']}: {r['status']}" for r in execution_results]
    )

    prompt = f"""
    Verify if these execution results successfully complete the task.
    Check if all requested information is present.
    If any data is missing, note it.
    
    Original Task: {task}
    
    Execution Results:
    {results_summary}
    
    Provide a final summary and list all sources/tools used.
    """

    return call_llm(prompt, FinalOutput)
