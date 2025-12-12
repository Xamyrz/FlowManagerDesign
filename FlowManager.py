from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from enum import Enum
import random
import asyncio

app = FastAPI(title="Flow Manager API")


class Task(BaseModel):
    name: str
    description: str

class Condition(BaseModel):
    name: str
    description: str
    source_task: str
    outcome: str
    target_task_success: str
    target_task_failure: str

class Flow(BaseModel):
    id: str
    name: str
    start_task: str
    tasks: List[Task]
    conditions: List[Condition]

class FlowRequest(BaseModel):
    flow: Flow


class Outcomes(Enum):
    SUCCESS = "success"
    FAILURE = "failure"

class Task:
    async def task1():
        print("Executing Task 1: Fetch data")
        success = random_success()
        print(f"Task 1 completed with status: {success}")
        return {"status": success, "data": {"value": random.randint(1, 100)}}

    async def task2(data):
        print("Executing Task 2: Process data")
        if "value" in data:
            processed = data["value"] * 2
            return {"status": random_success(), "data": {"processed": processed}}
        return {"status": Outcomes.FAILURE.value}

    async def task3(data):
        print("Executing Task 3: Store data")
        if "processed" in data:
            print(f"Data stored: {data['processed']}")
            return {"status": random_success()}
        return {"status": Outcomes.FAILURE.value}

TASK_FUNCTIONS = {
    "task1": Task.task1,
    "task2": Task.task2,
    "task3": Task.task3,
}

def random_success():
    return Outcomes.SUCCESS.value if random.choice([True, False]) else Outcomes.FAILURE.value

async def exec_flow(flow: Flow):
    current_task = flow.start_task
    task_results = {}

    while current_task != "end":
        print(f"Running {current_task}...")
        task_func = TASK_FUNCTIONS.get(current_task)

        if not task_func:
            raise HTTPException(status_code=400, detail=f"Task {current_task} not implemented")

        if task_results:
            result = await task_func(task_results.get("data", {}))
        else:
            result = await task_func()

        task_results = result

        condition = next((c for c in flow.conditions if c.source_task == current_task), None)

        if not condition:
            break

        if result["status"] == condition.outcome:
            current_task = condition.target_task_success
        else:
            current_task = condition.target_task_failure

    return {"flow_id": flow.id, "status": task_results["status"], "results": task_results}

@app.post("/exec_flow")
async def run_flow(flow_request: FlowRequest):
    flow = flow_request.flow
    result = await exec_flow(flow)
    return result