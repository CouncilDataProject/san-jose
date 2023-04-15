from cdp_backend.database import models as db_models
import fireo
from google.auth.credentials import AnonymousCredentials
from google.cloud.firestore import Client

# Connect to the database
fireo.connection(client=Client(
    project="cdp-san-jose-5d9db455",
    credentials=AnonymousCredentials()
))

# Read from the database
sessions = db_models.Session.collection.fetch(1000)

i=0
for session in sessions:
    if session.session_datetime.year == 2020 and session.session_datetime.month==1 and session.session_datetime.day==7:
        print("Session_time=" + str(session.session_datetime) + " ID=" + str(session.id) + " key=" +str(session.key) +" _update_time=" + str(session._update_time))
    i=i+1

print("----")

dictionary = dict()
sessions_for_delete = []
sessions = db_models.Session.collection.fetch(1000)
for session in sessions:
    if session.session_datetime not in dictionary:
        dictionary[session.session_datetime] = []
    dictionary[session.session_datetime].append(session)
i = 0

# Finding the sessions to delete
for key in sorted(dictionary.keys()):
    if len(dictionary[key]) > 1:
        print(key)
        for session in dictionary[key]:
            if session.session_datetime.year == 2020 and session._update_time.year == 2022:
                sessions_for_delete.append(session)
                print("Session_time=" + str(session.session_datetime) + " ID=" + str(session.id) + " key=" + str(session.key) + " _update_time=" + str(session._update_time) + " delete this from 2020")
            else:
                print("Session_time=" + str(session.session_datetime) + " ID=" + str(session.id) + " key=" + str(session.key) + " _update_time=" + str(session._update_time))
        print("")
        i = i + 1
print(i)

# This will delete the actual sessions
for session in sessions_for_delete:
    db_models.Session.collection.delete(session.key)
