# URL - https://app.prefect.cloud/account/8ff8f613-92c4-44ce-b811-f9956023e78d/workspace/04d8fca9-df2e-40c8-ae4f-a3733114c475/dashboard

# URL - https://app.prefect.cloud/api/docs

import requests
import os
import csv

# Replace these variables with your actual Prefect Cloud credentials
PREFECT_API_KEY = "pnu_4yYYsbgXIQtlkNhRhB9zFJcKu5dw2E4jUSoo"  # Your Prefect Cloud API key
ACCOUNT_ID = "604b53a1-1edb-4258-8a91-ac39c528143c"  # Your Prefect Cloud Account ID
WORKSPACE_ID = "66585d7a-ff8d-4d96-96cd-4aabacc5b01f"  # Your Prefect Cloud Workspace ID
FLOW_ID = "1bcc3271-5c19-4b9f-a57d-7a0d238e78f5"  # Your Flow ID
DEPLOYMENT_ID = "80f824fd-8d76-4884-b8ca-5239a924d841"  # Your Deployment ID
FLOW_RUN_ID = "a6bd8007-31de-4617-928d-85016cf5e7cc"

# Correct API URL to get flow details
PREFECT_API_URL = f"https://api.prefect.cloud/api/accounts/{ACCOUNT_ID}/workspaces/{WORKSPACE_ID}/flow_runs/{FLOW_RUN_ID}/logs/download"

# Set up headers with Authorization
headers = {"Authorization": f"Bearer {PREFECT_API_KEY}"}

# Make the request using GET
response = requests.get(PREFECT_API_URL, headers=headers)

# Check the response status
if response.status_code == 200:
    directory_path = "../output/logs/"
    csv_filename = "output_logs.csv"
    text_filename = "output_logs.txt"
    csv_file_path = os.path.join(directory_path, csv_filename)
    text_file_path = os.path.join(directory_path, text_filename)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    with open(text_file_path, "w") as textfile:
        textfile.write(response.text)
    print("\n================================================================");
    print(f"Logs are downloaded and saved to {text_file_path}")
    print("=================================================================\n");

    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for row in csv.reader(response.text.splitlines()):
            csv_writer.writerow(row)

    print("\n=======================================================================");
    print(f"Logs in CSV data format are downloaded and saved to {csv_file_path}")
    print("==========================================================================\n");
else:
    print(f"Error: Received status code {response.status_code}")
    print(f"Response content: {response.text}")

