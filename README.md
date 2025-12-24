# Temporal-Multiple-Trigger-Workflow-Execution-with-Dynamic-Activity-Execution

## Triggers
- Api POST Request Trigger
- Scheduled Trigger

## Parent Workflow
- Maintains are queue to collect the triggers
- If No Triggers are generated within 1 minute then workflow is marked completed
- If any Triggers are generated then, the trigger payload is appended to the queue
- On each iteration if trigger payload exist then Child Workflow is delegated the task to execute the trigger payload

## Child Workflow
- Trigger Payload is received by the child workflow
- Activities list and Trigger type is recognized
- The list of activities are executed in the order they are defined in the Child Workflow

## Run the Workflow
#### Create Virtual Environment
```bash
python -m venv env
```
#### Activate Virtual Environment
```bash
source env/bin/activate
```
#### Install Dependencies
```bash
pip install -r requirements.txt
```
#### Start Temporal Server
```bash
temporal server start-dev
```
#### Start Worker
```bash
python worker.py
```
#### Start Flask API App
```bash
python multiple_trigger_app.py
```

## Flask API - API Request Trigger
- Used multiple_trigger_app.py Flask API app to simulate the POST request
```bash
curl -X POST https://localhost:{Flask_App_Port}/trigger      -H "Content-Type: application/json"      -d '{
           "workflow_id": "user_workflow_1",
           "trigger_payload": {
               "trigger": "api_trigger",
               "activities": ["activity_b", "activity_c", "activity_d"]
           }
         }'
```

## Scheduled Trigger
- Python File to simulate the trigger generation every 15 seconds
```bash
python schedule_trigger.py
```