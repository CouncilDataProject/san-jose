from cdp_backend.database import models as db_models
import fireo
from google.auth.credentials import AnonymousCredentials
from google.cloud.firestore import Client
import sys

# Connect to the database
fireo.connection(client=Client(
    project="cdp-san-jose-5d9db455",
    credentials=AnonymousCredentials()
))

# Read from the database
sessions = db_models.Session.collection.fetch(1000)

dictionary = dict()
sessions_for_delete = []
sessions = db_models.Session.collection.fetch(1000)
for session in sessions:
    if session.session_datetime not in dictionary:
        dictionary[session.session_datetime] = []
    dictionary[session.session_datetime].append(session)

# Finding the sessions to delete
for key in sorted(dictionary.keys()):
    if len(dictionary[key]) > 1:
        print(key)
        for session in dictionary[key]:
            if session.session_datetime.year == 2020 and session._update_time.year == 2022:
                sessions_for_delete.append(session)
                print(f"Session_time={str(session.session_datetime)} ID={str(session.id)} key={str(session.key)} update_time={str(session._update_time)} delete this from 2020")
            else:
                print(f"Session_time={str(session.session_datetime)} ID={str(session.id)} key={str(session.key)} update_time={str(session._update_time)}")
        print("")

# This will delete the actual sessions
if sys.argv[-1] == "real":
    for session in sessions_for_delete:
        db_models.Session.collection.delete(session.key)
elif sys.argv[-1] == "dry_run":
    print(f"This is a dry run, but if it were real, {len(sessions_for_delete)} duplicates would be deleted.")
else:
    print("Please pass a valid parameter: \"real\" or \"dry_run.\"")
