# Flow Manager Design

## Explanation of the flow design:
How do the tasks depend on one another?
  - ##### Tasks depend on one another based on the result they provide and the conditions that are bound to them in the `outcome, target_task_success, target_task_failure` fields.
How is the success or failure of a task evaluated?
 - ##### Each task returns a result with a status field, when a task is complete, the procedure of looking up the  condition associated with the task.
 What happens if a task fails or succeeds?
 - ##### When a task succeeds, the flow manager checks the condition, if the conditions `outcome` field matches the outcome of the task, it proceeds to task in the `target_task_success` field. If the tasks fails and outcome does not match the conditions `outcome` field that this task is assigned to in `source_task`. the flow ends its process
 
 ##
 
 ### Running this project
install packages using ` pip install "fastapi[standard]" fastapi pydantic typing`

run `fastapi dev .\FlowManager.py` and open http://127.0.0.1:8000/docs

send a post request using curl

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/exec_flow' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "flow": {
    "id": "test123",
    "name": "test",
    "start_task": "task1",
    "tasks": [
      {
        "name": "task1",
        "description": "string"
      },
      {
        "name": "task2",
        "description": "Process data"
      },
      {
        "name": "task3",
        "description": "Store data"
      }
    ],
    "conditions": [
      {
        "name": "condition_task1_result",
        "description": "Evaluate the result of task1. If successful, proceed to task2; otherwise, end the flow.",
        "source_task": "task1",
        "outcome": "success",
        "target_task_success": "task2",
        "target_task_failure": "end"
      },
      {
        "name": "condition_task2_result",
        "description": "Evaluate the result of task2. If successful, proceed to task3; otherwise, end the flow.",
        "source_task": "task2",
        "outcome": "success",
        "target_task_success": "task3",
        "target_task_failure": "end"
      }
    ]
  }
}
```
