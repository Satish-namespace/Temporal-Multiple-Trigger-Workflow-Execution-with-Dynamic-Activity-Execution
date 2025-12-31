import asyncio
from datetime import datetime
from temporalio.client import Client
from temporalio.exceptions import WorkflowAlreadyStartedError
from multiple_trigger_dynamic_workflow import MultiTriggerDynamicWorkflow

async def main():
    client = await Client.connect("localhost:7233")
    workflow_id = "user_workflow_1"
    task_queue = "dynamic-task-queue"

    # while True:
    now = datetime.now()
    print(f"[{now}] Sending scheduled trigger...")

    try:
        await client.start_workflow(
            MultiTriggerDynamicWorkflow,
            id=workflow_id,
            task_queue=task_queue,
        )
        print("Workflow started successfully.")
    except WorkflowAlreadyStartedError:
        print("Workflow already running, sending signal instead.")
    trigger_payload = {
        "trigger": "scheduled_trigger",
        "cron": "*/1 * * * *",
        "activities": ["activity_e", "activity_c", "activity_d"]
    }

    workflow_handle = client.get_workflow_handle(workflow_id)
    await workflow_handle.signal(MultiTriggerDynamicWorkflow.scheduled_trigger, trigger_payload)

    # await asyncio.sleep(15) 

if __name__ == "__main__":
    asyncio.run(main())
