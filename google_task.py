from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import functools
from parser import Task, parse_date

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/tasks']
TODO_LIST = os.environ.get("todo_list", "MTQ4MDYwMzA5MTAyMTUxMTIxMTU6MDow")
cached_token_file = os.environ.get(
    "token", '/Users/suyogsoti/code/add_task/token.json')
client_secrets_file = os.environ.get(
    "client_secrect", '/Users/suyogsoti/code/add_task/credentials.json')


def get_task_service():
    """Shows basic usage of the Tasks API.
    Prints the title and ID of the first 10 task lists.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(cached_token_file):
        creds = Credentials.from_authorized_user_file(cached_token_file,
                                                      SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(cached_token_file, 'w') as token:
            token.write(creds.to_json())

    return build('tasks', 'v1', credentials=creds).tasks()


tasks = get_task_service()


def create_task(task: Task):
    body = {
        "title": task.title,
    }
    if task.description:
        body["notes"] = task.description
    if task.duedate:
        body["due"] = parse_date(task.duedate).isoformat() + 'Z'
    return tasks.insert(tasklist=TODO_LIST, body=body).execute()


@functools.lru_cache()
def get_tasks() -> list[Task]:
    results = tasks.list(tasklist=TODO_LIST, maxResults=10).execute()
    items = results.get('items', [])
    task_list: list[Task] = []
    for t in items:
        if t['status'] != 'needsAction':
            continue
        task_list.append(
            Task(title=t.get('title', None),
                 description=t.get("notes", None),
                 duedate=t.get("due", None)))
    return task_list


if __name__ == '__main__':
    create_task(
        Task(title="launcher creates task",
             description="launcher description",
             duedate="tuesday"))
    get_tasks()
