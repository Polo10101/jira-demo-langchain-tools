
"""This file was made for testing the JIRA package"""

from jira import JIRA
import os
from dotenv import load_dotenv

load_dotenv()

jira_server = os.getenv("server")
jira_user = os.getenv("user")
jira_api_token = os.getenv("token")

try:
    jira_client = JIRA(
        server=jira_server,
        basic_auth=(jira_user, jira_api_token)
)
    user_info = jira_client.current_user()
    print(f"Usuario valido {user_info}")
except Exception as e:
    print("Error, no hay conexion")