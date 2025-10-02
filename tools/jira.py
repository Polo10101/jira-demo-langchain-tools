import requests
from tools.json_parse import extrat_text_fields

class Jira:
    def __init__(self, server, auth, headers):
        self.server = server
        self.auth = auth
        self.headers = headers

    def create_tickets(self, project, issue_summary, issue_description, issue_type):
        
        url = f"{self.server}/rest/api/3/issue"

        payload = {
            "fields": {
                "project": {"key": f"{project}"},
                "summary": issue_summary,
                "description": {
                    "content": [
                        {
                        "content": [
                            {
                            "text": issue_description,
                            "type": "text"
                            }
                        ],
                        "type": "paragraph"
                        }
                    ],
                    "type": "doc",
                    "version": 1
                    },
                    "issuetype": {"name": issue_type} # Issue_type can be changed for other values, or allow to the user to change it to any he desired.   
                }
            }   

        response = requests.post(url, json=payload, auth=self.auth, headers=self.headers)
        
        if response.status_code == 201:
            response_data = response.json()
            return {
                "status": "success",
                "action":"create_tickets",
                "issuekey": response_data.get("key"),
                "issue_url": response_data.get("self")
                }
        else: 
            return {
                "status": "error",
                "action":"create_ticket",
                "response": response.text,
                "error_code": response.status_code,
                "message": "There was a problem with the creation of ticket."
            }
        
    # This function only will be used inside "view_tickets" for getting comments from each ticket that user wants to see.
    def _view_comments(self, issuekey):
        comments = f"{self.server}/rest/api/3/issue/{issuekey}/comment"
        comments_response = requests.get(comments, auth=self.auth, headers=self.headers) 

        if comments_response.status_code == 200:
            comments = comments_response.json().get("comments", [])
            parsed_comments = []

            for c in comments:
                author = c.get("author", {}).get("displayName", "Not recognized")
                comment = c.get("body", {})
                comments = extrat_text_fields(comment)
                parsed_comments.append(f"Author:{author} - Comment:{comments}")
        else: 
            print("No hay comentarios en el ticket")
        
        return "\n".join(parsed_comments)


    def view_tickets(self, issuekey):
        url = f"{self.server}/rest/api/3/issue/{issuekey}"
        response = requests.get(url, headers=self.headers, auth=self.auth)
        
        if response.status_code == 200:
            issue = response.json()
            fields = issue["fields"]
            summary = fields.get("summary")
            description = fields.get("description", {})
            descriptionn = extrat_text_fields(description)
            comments = self._view_comments(issuekey)
            
            print(f"Ticket: {issuekey}\n")
            print(f"Summary: {summary}\n")
            print(f"Description: {descriptionn}\n")
            comments_sum = len(comments)
            if comments_sum > 1:
                print(f"Comentarios:\n{comments}")
                
            
            return {
                    "status": "success",
                    "action": "view_ticket",
                    "issue_key": issuekey,
                    "data": {
                        "summary": summary,
                        "description": descriptionn,
                        "comments": comments
                        }
                }
        else:
            return {
                "status": "error",
                "action": "view_ticket",
                "issue_key": issuekey,
                "response": response.text,
                "error_code": response.status_code,
                "message": "Ticket not found or access denied" 
            }    
    
    def comment_issue(self ,key, comment):
        url = f"{self.server}/rest/api/3/issue/{key}/comment"

        payload = {
                    "body": {
                "content": [
                {
                    "content": [
                    {
                        "text": comment,
                        "type": "text"
                    }
                    ],
                    "type": "paragraph"
                }
                ],
                "type": "doc",
                "version": 1
            }
        }

        response = requests.post(url, json = payload, auth=self.auth, headers=self.headers)
        print(response.text)

        if response == 201: 
            print("The comment was added coreectly.")
            return {
                "status": "success",
                "action":"add_comment",
                "issuekey":key,
                "comment":comment
                }
        else: 
            return {
                "status": "error",
                "action":"add_comment",
                "issuekey":key,
                "response": response.text,
                "error_code": response.status_code,
                "message": "There was a problem with comment the ticket."
            }