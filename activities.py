from temporalio import activity
from datetime import datetime

@activity.defn
async def activity_a(payload: str):
    result = f"Activity A executed with payload: {payload} at {datetime.now()}"
    print(result)
    return result

@activity.defn
async def activity_b(payload: str):
    result = f"Activity B executed with payload: {payload} at {datetime.now()}"
    print(result)
    return result

@activity.defn
async def activity_c(payload: str):
    result = f"Activity C executed with payload: {payload} at {datetime.now()}"
    print(result)
    return result

@activity.defn
async def activity_d(payload: str):
    result = f"Activity D executed with payload: {payload} at {datetime.now()}"
    print(result)
    return result

@activity.defn
async def activity_e(payload: str):
    result = f"Activity E executed with payload: {payload} at {datetime.now()}"
    print(result)
    return result

@activity.defn
async def report_result(result: str):
    print(f"Reporting result: {result}")
    # Could be a webhook, DB insert, or other external system
    return result