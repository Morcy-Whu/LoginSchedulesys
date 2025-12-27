from db import execute, fetch_one, fetch_all
from config import DAYS, DEFAULT_SLOTS


def ensure_default_slots(user_id):
    count = fetch_one(
        "SELECT COUNT(*) AS c FROM time_slots WHERE user_id = ?",
        (user_id,)
    )["c"]

    if count > 0:
        return

    for start, end in DEFAULT_SLOTS:
        label = f"{start} - {end}"
        execute("""
            INSERT INTO time_slots (user_id, label, start_time, end_time)
            VALUES (?, ?, ?, ?)
        """, (user_id, label, start, end))


def add_slot(user_id, start, end):
    label = f"{start} - {end}"

    cur = execute("""
        INSERT INTO time_slots (user_id, label, start_time, end_time)
        VALUES (?, ?, ?, ?)
    """, (user_id, label, start, end))

    slot_id = cur.lastrowid

    for day in DAYS:
        execute("""
            INSERT INTO schedule (user_id, day, slot_id)
            VALUES (?, ?, ?)
        """, (user_id, day, slot_id))

    return slot_id


def update_slot(user_id, slot_id, start, end):
    label = f"{start} - {end}"

    execute("""
        UPDATE time_slots
        SET start_time = ?, end_time = ?, label = ?
        WHERE id = ? AND user_id = ?
    """, (start, end, label, slot_id, user_id))


def delete_slot(user_id, slot_id):
    execute("DELETE FROM schedule WHERE slot_id = ?", (slot_id,))
    execute("""
        DELETE FROM time_slots
        WHERE id = ? AND user_id = ?
    """, (slot_id, user_id))
