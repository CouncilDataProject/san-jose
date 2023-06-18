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

# Read from the database

dictionary = dict()
for session in sessions:
    if session.session_datetime not in dictionary:
        dictionary[session.session_datetime] = []
    dictionary[session.session_datetime].append(session)

# Finding the sessions to delete
for key in sorted(dictionary.keys()):
    if len(dictionary[key]) > 1:
        print(key)
        for session in dictionary[key]:
            # The San Jose City Council videos only play if they have "archive-video"
            # as their URI sub-domain.
            if str(session.video_uri).startswith("https://archive-video"):
                print(f"Session_time={str(session.session_datetime)} ID={str(session.id)} key={str(session.key)} update_time={str(session._update_time)} video_url={str(session.video_uri)}")
            else:
                sessions_for_delete.append(session)
                print(f"Session_time={str(session.session_datetime)} ID={str(session.id)} key={str(session.key)} update_time={str(session._update_time)} video_url={str(session.video_uri)} delete this")
        print("")

# Confirm that the sessions in sessions_for_delete do not have an accessible video.
i = 0
for session in sessions_for_delete:
    try:
        requests.head(session.video_uri)

        # If a video exists, do not remove it.
        # Instead, throw an exception and stop the program,
        # as there was something wrong with the list of sessions to delete.
        raise Exception(f"This video should be deleted: {str(session.video_uri)}")
    except requests.exceptions.ConnectionError:
        i += 1
        print(f"({i}) {session.video_uri} will be deleted")
print(len(sessions_for_delete))

# This will delete the actual sessions
if sys.argv[-1] == "real":
    for session in sessions_for_delete:
        db_models.Session.collection.delete(session.key)
elif sys.argv[-1] == "dry_run":
    print(f"This is a dry run, but if it were real, {len(sessions_for_delete)} duplicates would be deleted.")
else:
    print("Please pass a valid parameter: \"real\" or \"dry_run.\"")
