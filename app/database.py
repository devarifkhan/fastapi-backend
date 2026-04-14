import json

shipments = {}

with open("shipments.json", "r") as f:
    data = json.load(f)

    for value in data:
        shipments[value["id"]] = value


def save():
    with open("shipments.json", "w") as f:
        json.dump(list(shipments.values()), f, indent=4)