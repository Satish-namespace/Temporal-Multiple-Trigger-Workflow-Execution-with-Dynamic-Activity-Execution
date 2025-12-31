from temporalio import workflow
from datetime import timedelta, datetime
from typing import Dict, Any
from trigger_execution_workflow import TriggerExecutionWorkflow
from temporalio.workflow import ParentClosePolicy

@workflow.defn
class MultiTriggerDynamicWorkflow:
    def __init__(self):
        self._queue: list[Dict[str, Any]] = []

    @workflow.signal
    def api_trigger(self, trigger_payload: Dict[str, Any]):
        self._queue.append(trigger_payload)
        
    @workflow.signal
    def scheduled_trigger(self, trigger_payload: Dict[str, Any]):
        self._queue.append(trigger_payload)

    @workflow.run
    async def run(self):
        idle_timeout = timedelta(seconds=60)

        while True:
            if not self._queue:
                await workflow.sleep(idle_timeout.total_seconds())
                if not self._queue:
                    workflow.logger.info("Idle timeout reached, closing workflow.")
                    break

            while self._queue:
                payload = self._queue.pop(0)
                check = payload.get('cron')
                workflow.logger.info(f"DEBUG: CRON VALUE: {check}")
                if check:
                    await workflow.start_child_workflow(
                        TriggerExecutionWorkflow.run,
                        payload,
                        id=f"{workflow.info().workflow_id}:{workflow.now()}",
                        task_queue="dynamic-task-queue",
                        cron_schedule=check,
                        parent_close_policy=ParentClosePolicy.ABANDON
                    )
                else:
                    await workflow.execute_child_workflow(
                        TriggerExecutionWorkflow.run,
                        payload,
                        id=f"{workflow.info().workflow_id}:{workflow.now()}",
                        task_queue="dynamic-task-queue",
                        run_timeout=timedelta(minutes=5),
                    )
