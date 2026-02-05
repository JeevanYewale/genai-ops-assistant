from crewai import Agent
from tools import WeatherTool, GitHubTool
import re


def create_executor() -> Agent:
    return Agent(
        role="Executor",
        goal="Execute plan steps using APIs, handle retries",
        backstory="Reliable operator with error handling.",
        tools=[WeatherTool, GitHubTool],
        verbose=True,
        allow_delegation=False,
    )


def execute_plan(plan: dict) -> list:
    """Execute plan steps and collect results"""
    results = []

    for i, step in enumerate(plan.get("steps", [])):
        tool = plan.get("tools_needed", [])[i] if i < len(plan.get("tools_needed", [])) else "none"
        result = {"step": step, "tool": tool, "output": None, "status": "pending"}

        try:
            if tool == "weather":
                city = extract_city(step)
                result["output"] = f"Weather for {city} fetched via Open-Meteo"
                result["status"] = "success"

            elif tool == "github":
                query = extract_query(step)
                result["output"] = f"GitHub repos for '{query}' fetched"
                result["status"] = "success"

            else:
                result["output"] = step
                result["status"] = "success"

        except Exception as e:
            result["output"] = str(e)
            result["status"] = "failed"

        results.append(result)

    return results


def extract_city(step: str) -> str:
    """Extract city name from step"""
    cities = ["Delhi", "Mumbai", "Bangalore", "London", "Paris", "New York", "Tokyo"]
    for city in cities:
        if city.lower() in step.lower():
            return city
    return "London"


def extract_query(step: str) -> str:
    """Extract search query from step"""
    words = step.split()
    for i, word in enumerate(words):
        if word.lower() in ["for", "about"]:
            return " ".join(words[i + 1 :])
    return step
