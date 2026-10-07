import json
from pathlib import Path

import pytest


@pytest.fixture
def studio_data():
    data_path = Path(__file__).resolve().parent.parent / "data" / "studio.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_no_classes_in_maintenance_rooms(studio_data):
    """Ensure no classes are scheduled in rooms under maintenance."""
    room_status = {r["id"]: r["status"] for r in studio_data["rooms"]}

    for session in studio_data["schedule"]:
        assigned_room = session["room_id"]
        status = room_status.get(assigned_room)
        assert status != "maintenance", (
            f"Business rule violation: Class '{session['title']}' is scheduled "
            f"in room '{assigned_room}' which is currently under maintenance!"
        )


def test_class_capacity_not_exceeded(studio_data):
    """Ensure session attendees do not exceed room capacity limits."""
    room_capacity = {r["id"]: r["capacity"] for r in studio_data["rooms"]}

    for session in studio_data["schedule"]:
        capacity = room_capacity.get(session["room_id"], 0)
        assert session["registered"] <= capacity, (
            f"Overcapacity: Class '{session['title']}' has {session['registered']} "
            f"attendees for a room capacity of {capacity}."
        )
