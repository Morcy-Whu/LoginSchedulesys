import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

from extensions import login_required
from config import DAYS
from services.user_service import create_user, authenticate_user, delete_user
from services.slot_service import (
    ensure_default_slots,
    add_slot,
    delete_slot,
    update_slot
)
from services.schedule_service import (
    ensure_schedule,
    toggle_booking,
    get_schedule_view_data
)


# ================== Flask 初始化 ==================
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

# ================== 页面路由 ==================
@app.route("/")
def login_page():
    return render_template("index.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", username=session["username"])


@app.route("/schedule")
@login_required
def schedule_page():
    user_id = session["user_id"]

    ensure_default_slots(user_id)
    ensure_schedule(user_id)

    slots, schedule_data = get_schedule_view_data(user_id)

    return render_template(
        "schedule.html",
        days=DAYS,
        slots=slots,
        schedule=schedule_data
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))


# ================== API：注册 ==================
@app.route("/api/register", methods=["POST"])
def register_api():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return jsonify(error="Missing username or password"), 400

    try:
        create_user(username, password)
        return jsonify(success=True)
    except Exception:
        return jsonify(error="Username already exists"), 409


# ================== API：登录 ==================
@app.route("/api/login", methods=["POST"])
def login_api():
    username = request.form.get("username")
    password = request.form.get("password")

    user = authenticate_user(username, password)
    if not user:
        return jsonify(error="Invalid credentials"), 401

    session["user_id"] = user["id"]
    session["username"] = user["username"]
    return jsonify(success=True)


# ================== API：删除账号 ==================
@app.route("/api/delete_account", methods=["POST"])
@login_required
def delete_account_api():
    delete_user(session["user_id"])
    session.clear()
    return jsonify(success=True)


# ================== API：时间段 ==================
@app.route("/api/slots", methods=["POST"])
@login_required
def add_slot_api():
    start = request.form.get("start")
    end = request.form.get("end")

    if not start or not end:
        return jsonify(error="Invalid time"), 400

    add_slot(session["user_id"], start, end)
    return jsonify(success=True)


@app.route("/api/slots/<int:slot_id>", methods=["POST"])
@login_required
def delete_slot_api(slot_id):
    delete_slot(session["user_id"], slot_id)
    return jsonify(success=True)


@app.route("/api/slots/<int:slot_id>/update", methods=["POST"])
@login_required
def update_slot_api(slot_id):
    start = request.form.get("start")
    end = request.form.get("end")

    if not start or not end:
        return jsonify(error="Invalid time"), 400

    update_slot(session["user_id"], slot_id, start, end)
    return jsonify(success=True)


# ================== API：切换预约状态 ==================
@app.route("/toggle", methods=["POST"])
@login_required
def toggle_api():
    toggle_booking(
        session["user_id"],
        request.form.get("day"),
        request.form.get("slot_id")
    )
    return redirect(url_for("schedule_page"))


# ================== 启动 ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
