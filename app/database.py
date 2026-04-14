import json

shipments = {}

with open("shipments.json", "r") as f:
    data = json.load(f)

    if isinstance(data, list):
        for value in data:
            shipments[value["id"]] = value
    else:
        for key, value in data.items():
            shipments[int(key)] = {"id": int(key), **value}


def save():
    with open("shipments.json", "w") as f:
        json.dump(list(shipments.values()), f, indent=4)