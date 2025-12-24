from temporalio import workflow
from datetime import timedelta
from typing import Dict, Any, List
from activities import (
    activity_a,
    activity_b,
    activity_c,
    activity_d,
    activity_e,
)

@workflow.defn
class TriggerExecutionWorkflow:

    @workflow.run
    async def run(self, payload: Dict[str, Any]):
        trigger = payload["trigger"]
        activities: List[str] = payload["activities"]

        workflow.logger.info(
            f"Trigger '{trigger}' executing activities {activities}"
        )

        for activity_name in activities:
            await self._run_activity(activity_name)


    async def _run_activity(self, activity_name: str):
        activity_registry = {
            "activity_a": activity_a,
            "activity_b": activity_b,
            "activity_c": activity_c,
            "activity_d": activity_d,
            "activity_e": activity_e,
        }

        if activity_name not in activity_registry:
            raise ValueError(f"Unknown activity: {activity_name}")

        await workflow.execute_activity(
            activity_registry[activity_name],
            f"Payload for {activity_name}",
            task_queue="dynamic-task-queue",
            start_to_close_timeout=timedelta(seconds=30),
        )
