from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from agents.planner import plan_task
from agents.executor import execute_plan
from agents.verifier import verify_results

load_dotenv()

app = FastAPI(title="AI Ops Assistant")


class TaskRequest(BaseModel):
    task: str


@app.post("/task")
async def run_task(request: TaskRequest):
    """Execute task: Plan -> Execute -> Verify"""
    try:
        # Step 1: Plan
        plan = plan_task(request.task)

        # Step 2: Execute
        execution_results = execute_plan(plan)

        # Step 3: Verify
        verification = verify_results(request.task, execution_results)

        return {
            "task": request.task,
            "plan": plan,
            "execution": execution_results,
            "verification": verification,
        }

    except Exception as e:
        return {"error": str(e), "task": request.task}


@app.get("/health")
def health():
    """Health check"""
    return {"status": "healthy"}


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "AI Ops Assistant - Multi-Agent System",
        "endpoints": {
            "POST /task": "Execute a task (e.g., 'Weather in Delhi and top MERN repos')",
            "GET /health": "Health check",
            "GET /docs": "Interactive API docs",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
