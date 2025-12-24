from flask import Flask, request, jsonify
import asyncio
from temporalio.client import Client
from temporalio.exceptions import WorkflowAlreadyStartedError
from multiple_trigger_dynamic_workflow import MultiTriggerDynamicWorkflow

app = Flask(__name__)

temporal_client = None

async def get_temporal_client():
    global temporal_client
    if not temporal_client:
        temporal_client = await Client.connect("localhost:7233")
    return temporal_client


@app.route("/trigger", methods=["POST"])
def trigger():
    data = request.json
    workflow_id = data.get("workflow_id")
    trigger_payload = data.get("trigger_payload")
    
    asyncio.run(handle_multiple_trigger_api_trigger(workflow_id, trigger_payload))
    
    return jsonify({"message": "API Request Trigger Sent Successfully"})


async def handle_multiple_trigger_api_trigger(workflow_id, trigger_payload):
    client = await get_temporal_client()
    
    try:
        await client.start_workflow(
            MultiTriggerDynamicWorkflow.run,
            id=workflow_id,
            task_queue="dynamic-task-queue"
        )
    except WorkflowAlreadyStartedError:
        print("Workflow already started")
    
    handle = client.get_workflow_handle(workflow_id)
    await handle.signal(MultiTriggerDynamicWorkflow.api_trigger, trigger_payload)

if __name__ == "__main__":
    app.run(port=5000, debug=True)