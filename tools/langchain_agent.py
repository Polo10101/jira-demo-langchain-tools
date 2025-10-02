from langchain_openai import AzureChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import Tool
from langchain_core.messages import SystemMessage
from config import (endpoint, deployment, subscription_key, api_version, jira_server, auth, headers)
import uuid 
from tools.jira import Jira
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType


jira = Jira(jira_server, auth, headers)

llm = AzureChatOpenAI(
        azure_deployment = deployment,
        api_version = api_version,
        azure_endpoint = endpoint,
        api_key = subscription_key,
        temperature = 0
    )

view_jira_tool = Tool.from_function(
        name="view_ticket",
        description=(
            "Use this tool to retrieve full details of a jira ticket."
            "It returns the ticket summary, description, and comments if there ar any."
            "Use it when the user ask to see the content, context or any field related to a ticket like description, comments or summary."
        ),
        func=jira.view_tickets,
        return_direct=True
    )

create_jira_ticket_tool = Tool.from_function(
        name="create_ticket",
        description="Create a new jira ticket. Needs project where the ticket is going to be created, summary, descprition, and issue_type (task, storie).",
        func=jira.create_tickets,
        return_direct=True
    )

comment_jira_ticket_tool = Tool.from_function(
        name="comment_jira_ticket",
        description="Add a comment to a specific jira ticket. Use this function when users wants to comment a ticket.",
        func=jira.comment_issue,
        return_direct=True
    )

tools = [create_jira_ticket_tool, view_jira_tool, comment_jira_ticket_tool]
    
memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

message = SystemMessage(content="""
You are an expert Jira ticket management assistant.
Your goal is to help the user view, create, or comment on tickets.

Use the available tools to achieve this. Never fabricate answers if you can use a tool. 

- If user ask for comment the ticket take the last ticketID that was viewed.
- If the user wants to view ticket information, use the `view_ticket` tool.
- If they want to create a new ticket, use `create_ticket`.
- If they want to comment on a ticket, use `comment_jira_ticket`.

If you need more details from the user to use the tool (such as a ticket ID or description), ask for them directly and clearly.
If the intentions are unclear, or details are needed to complete an instruction, ask for details."""
)

agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
        handle_parsing_errors = True,
        agent_kwargs={"system_message": message}
    )

"""""response = agent.run("Can you please show me the description from this ticket FAIRENGG-3055")
print(response)"""""

def chat_with_agent():
    print("Hi, I'm here for helping you with Jira, what can I do for you?")
    while True: 
        user_input = input("Tu: ")
        if user_input.lower() in ("exit","quit"):
            break
        try:
            response = agent.invoke(user_input)
            print(response)
        except Exception as e:
            print(f"{e}")
    return