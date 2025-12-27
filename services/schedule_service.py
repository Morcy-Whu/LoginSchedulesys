from db import execute, fetch_all
from config import DAYS


def ensure_schedule(user_id):
    slots = fetch_all(
        "SELECT id FROM time_slots WHERE user_id = ?",
        (user_id,)
    )

    for slot in slots:
        for day in DAYS:
            execute("""
                INSERT OR IGNORE INTO schedule (user_id, day, slot_id)
                VALUES (?, ?, ?)
            """, (user_id, day, slot["id"]))


def toggle_booking(user_id, day, slot_id):
    execute("""
        UPDATE schedule
        SET is_booked = 1 - is_booked
        WHERE user_id = ? AND day = ? AND slot_id = ?
    """, (user_id, day, slot_id))


def get_schedule_view_data(user_id):
    """
    专门为 schedule.html 准备的数据结构
    """

    slots = fetch_all("""
        SELECT *
        FROM time_slots
        WHERE user_id = ?
        ORDER BY start_time
    """, (user_id,))

    rows = fetch_all("""
        SELECT s.day, s.is_booked, t.label, t.id AS slot_id
        FROM schedule s
        JOIN time_slots t ON s.slot_id = t.id
        WHERE s.user_id = ?
    """, (user_id,))

    schedule_data = {day: {} for day in DAYS}

    for row in rows:
        schedule_data[row["day"]][row["label"]] = {
            "booked": bool(row["is_booked"]),
            "slot_id": row["slot_id"]
        }

    return slots, schedule_data
