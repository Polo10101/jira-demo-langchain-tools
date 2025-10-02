import os
from dotenv import load_dotenv

load_dotenv()

# Jira keys
jira_server = os.getenv("server")
jira_user = os.getenv("user")
jira_api_token = os.getenv("token")

# AzureOpenAI keys
endpoint = os.getenv("endpoint")
deployment = os.getenv("deployment")
subscription_key = os.getenv("subscription_key")
api_version = os.getenv("api_version")


headers = {
    "Accept": "application/json"
}

auth = (jira_user, jira_api_token)