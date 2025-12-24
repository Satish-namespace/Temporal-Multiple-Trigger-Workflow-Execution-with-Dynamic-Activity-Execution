from temporalio.worker import Worker
from workflow import SingleTriggerDynamicWorkflow
from temporalio.client import Client
from activities import activity_a, activity_b, activity_c, activity_d, activity_e, report_result
from multiple_trigger_dynamic_workflow import MultiTriggerDynamicWorkflow
from trigger_execution_workflow import TriggerExecutionWorkflow
async def main():
    client = await Client.connect("localhost:7233")
    # worker = Worker(
    #     client,
    #     task_queue="single-trigger-task-queue",
    #     workflows=[SingleTriggerDynamicWorkflow],
    #     activities=[activity_a, activity_b, activity_c, activity_d, activity_e, report_result]
    # )
    
    dynamic_worker = Worker(
        client,
        task_queue="dynamic-task-queue",
        workflows=[MultiTriggerDynamicWorkflow, TriggerExecutionWorkflow],
        activities=[activity_a, activity_b, activity_c, activity_d, activity_e]  
    )
    await dynamic_worker.run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())