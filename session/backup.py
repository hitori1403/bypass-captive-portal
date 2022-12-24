import json


def store_data(client, session):
    data = {
        "name": session.name,
        "bssid": client.bssid,
        "station": client.station,
        "username": session.username,
        "etr": session.etr,
    }

    sessions = []

    try:
        with open("sessions.json", "r") as f:
            sessions = json.load(f)
    except:
        pass

    sessions.append(data)

    with open("sessions.json", "w") as f:
        json.dump(sessions, f)
