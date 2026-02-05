#!/usr/bin/env python3
"""
Standalone test of AI Ops Assistant - demonstrates core logic without external deps
"""

# Mock LLM response for testing
def mock_plan_task(task: str) -> dict:
    """Mock planner output"""
    return {
        "steps": [
            "Get weather for Delhi",
            "Search for MERN repositories"
        ],
        "tools_needed": ["weather", "github"]
    }


def mock_execute_plan(plan: dict) -> list:
    """Mock executor output"""
    results = []
    for i, step in enumerate(plan.get("steps", [])):
        tool = plan.get("tools_needed", [])[i] if i < len(plan.get("tools_needed", [])) else "none"
        results.append({
            "step": step,
            "tool": tool,
            "output": f"Mock result for: {step}",
            "status": "success"
        })
    return results


def mock_verify_results(task: str, execution_results: list) -> dict:
    """Mock verifier output"""
    return {
        "result": f"Successfully completed task: {task}",
        "sources": ["Open-Meteo API", "GitHub Search API"]
    }


def main():
    print("=" * 60)
    print("AI Ops Assistant - Standalone Test")
    print("=" * 60)
    
    task = "Weather in Delhi and top MERN repos"
    print(f"\n[TASK] {task}\n")
    
    # Step 1: Plan
    print("Step 1: PLANNER")
    print("-" * 60)
    plan = mock_plan_task(task)
    print(f"Plan: {plan}\n")
    
    # Step 2: Execute
    print("Step 2: EXECUTOR")
    print("-" * 60)
    execution_results = mock_execute_plan(plan)
    for result in execution_results:
        print(f"  * {result['step']}")
        print(f"    Tool: {result['tool']}")
        print(f"    Status: {result['status']}\n")
    
    # Step 3: Verify
    print("Step 3: VERIFIER")
    print("-" * 60)
    verification = mock_verify_results(task, execution_results)
    print(f"Result: {verification['result']}")
    print(f"Sources: {', '.join(verification['sources'])}\n")
    
    # Final output
    print("=" * 60)
    print("FINAL OUTPUT (JSON)")
    print("=" * 60)
    import json
    output = {
        "task": task,
        "plan": plan,
        "execution": execution_results,
        "verification": verification
    }
    print(json.dumps(output, indent=2))
    print("\n[SUCCESS] Test completed successfully!")
    print("\nTo run with FastAPI:")
    print("  1. pip install -r requirements.txt")
    print("  2. cp .env.example .env (add LLM_API_KEY)")
    print("  3. uvicorn main:app --reload")


if __name__ == "__main__":
    main()
