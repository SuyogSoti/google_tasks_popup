from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from parser import Task, parse_date

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/tasks']


def get_task_service():
    """Shows basic usage of the Tasks API.
    Prints the title and ID of the first 10 task lists.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('/Users/suyogsoti/code/add_task/token.json'):
        creds = Credentials.from_authorized_user_file(
            '/Users/suyogsoti/code/add_task/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/suyogsoti/code/add_task/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('/Users/suyogsoti/code/add_task/token.json', 'w') as token:
            token.write(creds.to_json())

    return build('tasks', 'v1', credentials=creds).tasks()


tasks = get_task_service()
TODO_LIST = "MTQ4MDYwMzA5MTAyMTUxMTIxMTU6MDow"


def create_task(task: Task):
    body = {
        "title": task.title,
    }
    if task.description:
        body["notes"] = task.description
    if task.duedate:
        body["due"] = parse_date(task.duedate).isoformat() + 'Z'
    return tasks.insert(tasklist=TODO_LIST, body=body).execute()


if __name__ == '__main__':
    create_task(
        Task(title="launcher creates task",
             description="launcher description",
             duedate="tuesday"))
