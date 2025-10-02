#from fastapi import FastAPI
#from jira import JIRA

from tools.jira import Jira
from config import (jira_server, auth, headers)
from tools.langchain_agent import chat_with_agent

# This function was added at the begining for playing around with the Jira fucntions without any llm and agent-framework.  
"""def choice():

    incase = input("What do you want to do?: \n1.-View tickets\n2.-Create tickets\n3.-Add comment to a ticket\n")
    jira = Jira(jira_server, auth, headers)

    match incase:
        case "1":
            key = input("What's the ticket number you want to view?")
            jira.view_tickets(key)
            response = jira.view_tickets(key)
            print("\nResponse: ", (response))
        case "2":
            project = "ITS"
            issue_summary = input("What is the summary of the ticket?\n") 
            issue_description = input("What's description of the issue?\n")
            issue_type = "Task"
            jira.create_tickets(project, issue_summary, issue_description, issue_type)
        case "3":
            key = input("What is the ticket number in which you want to add a comment?\n")
            comment = input("What's the comment you want to add to the ticket?\n")
            jira.comment_issue(key, comment)
        case "4":
            chat_with_agent()
        case _:
            print("Try it again:\n", choice())
    return

choice()"""
chat_with_agent()


