# URL - https://app.prefect.cloud/account/8ff8f613-92c4-44ce-b811-f9956023e78d/workspace/04d8fca9-df2e-40c8-ae4f-a3733114c475/dashboard

# URL - https://app.prefect.cloud/api/docs

import requests
import os
import json

# Replace these variables with your actual Prefect Cloud credentials
PREFECT_API_KEY = "pnu_4yYYsbgXIQtlkNhRhB9zFJcKu5dw2E4jUSoo"  # Your Prefect Cloud API key
ACCOUNT_ID = "604b53a1-1edb-4258-8a91-ac39c528143c"  # Your Prefect Cloud Account ID
WORKSPACE_ID = "66585d7a-ff8d-4d96-96cd-4aabacc5b01f"  # Your Prefect Cloud Workspace ID
FLOW_ID = "1bcc3271-5c19-4b9f-a57d-7a0d238e78f5"  # Your Flow ID

# Correct API URL to get flow details
PREFECT_API_URL = f"https://api.prefect.cloud/api/accounts/{ACCOUNT_ID}/workspaces/{WORKSPACE_ID}/flows/{FLOW_ID}"

# Set up headers with Authorization
headers = {"Authorization": f"Bearer {PREFECT_API_KEY}"}

# Make the request using GET
response = requests.get(PREFECT_API_URL, headers=headers)

# Check the response status
if response.status_code == 200:
    flow_info = response.json()
    print(flow_info)
    directory_path = "../output/json/"
    filename = "flow.json"
    file_path = os.path.join(directory_path, filename)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    with open(file_path, "w") as f:
        json.dump(flow_info, f, indent=4)  # Indent for better readability
    print("\n================================================================");
    print("JSON object written to:", file_path)
    print("=================================================================\n");
else:
    print(f"Error: Received status code {response.status_code}")
    print(f"Response content: {response.text}")

