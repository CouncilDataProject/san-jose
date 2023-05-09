from cdp_backend.database import models as db_models
import fireo
from google.auth.credentials import AnonymousCredentials
from google.cloud.firestore import Client
import requests
import sys

# Connect to the database
fireo.connection(client=Client(
    project="cdp-san-jose-5d9db455",
    credentials=AnonymousCredentials()
))

sessions_for_delete = []
sessions = db_models.Session.collection.fetch(1000)
for session in sessions:
    response = ""
    try:
        requests.head(session.video_uri)
        print(session.video_uri)
    except requests.exceptions.ConnectionError:
        sessions_for_delete.append(session)
        print(f"delete {session.video_uri}")
print(len(sessions_for_delete))

# This will delete the actual sessions
if sys.argv[-1] == "real":
    for session in sessions_for_delete:
        db_models.Session.collection.delete(session.key)
elif sys.argv[-1] == "dry_run":
    print(f"This is a dry run, but if it were real, {len(sessions_for_delete)} duplicates would be deleted.")
else:
    print("Please pass a valid parameter: \"real\" or \"dry_run.\"")
