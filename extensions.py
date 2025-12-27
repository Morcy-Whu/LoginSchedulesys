from functools import wraps
from flask import session, redirect, url_for
from db import get_db


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("pages.login_page"))
        return func(*args, **kwargs)
    return wrapper

def toggle_booking(user_id, day, slot_id):
    cur = get_db().cursor()

    cur.execute("""
        SELECT booked FROM schedule
        WHERE user_id=? AND day=? AND slot_id=?
    """, (user_id, day, slot_id))

    row = cur.fetchone()
    new_state = 0 if row["booked"] else 1

    cur.execute("""
        UPDATE schedule
        SET booked=?
        WHERE user_id=? AND day=? AND slot_id=?
    """, (new_state, user_id, day, slot_id))

    get_db().commit()
    return bool(new_state)
