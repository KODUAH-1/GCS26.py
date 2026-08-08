import os
import json
import secrets
import threading
from pathlib import Path
ASSETS_DIR = Path(__file__).parent / "assets"
import re

def clean_text(text: str) -> str:
    # Remove <WebsiteContent_...> wrappers
    return re.sub(r"<WebsiteContent_[^>]+>", "", text).replace("</WebsiteContent_wN6mq6q5su8EQb6sSego8>", "")

# Example: print active vs background tabs
for tab in edge_all_open_tabs:
    title = clean_text(tab["pageTitle"])
    url = clean_text(tab["pageUrl"])
    status = "ACTIVE" if tab["isCurrent"] else "BACKGROUND"
    print(f"[{status}] {title} → {url}")

from datetime import datetime, date
from typing import Dict, Any
import io
import sqlite3
import os
from io import BytesIO

DB_FILE = "school.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            grade TEXT
        )
    """)
    conn.commit()
    conn.close()

def backup_db():
    with open(DB_FILE, "rb") as f:
        return f.read()

def restore_db(uploaded_file):
    with open(DB_FILE, "wb") as f:
        f.write(uploaded_file.getbuffer())

def settings_page():
    import streamlit as st
    st.title("⚙️ Backup & Restore")

    # Backup section
    st.subheader("📥 Download Backup")
    if os.path.exists(DB_FILE):
        db_bytes = backup_db()
        st.download_button(
            label="Download school.db",
            data=db_bytes,
            file_name="school_backup.db",
            mime="application/octet-stream"
        )
    else:
        st.warning("No database file found yet.")

    # Restore section
    st.subheader("📤 Restore Backup")
    uploaded_file = st.file_uploader("Upload a backup (.db)", type=["db"])
    if uploaded_file is not None:
        restore_db(uploaded_file)
        st.success("Database restored successfully! Restart the app to apply changes.")

# Initialize DB on startup
init_db()

import streamlit as st
import pandas as pd
import phonenumbers
import bcrypt
import streamlit as st
import pandas as pd

# Apply background styling
import streamlit as st
import pandas as pd

# Apply background styling
def set_background():
    page_bg = """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #87CEFA 70%, #FFD700 30%);
        color: #000000;
    }
    [data-testid="stSidebar"] {
        background-color: #ADD8E6; /* Light Blue */
        color: #FFD700;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #FFD700;
        font-family: 'Trebuchet MS', sans-serif;
    }
    p, label, span, div {
        color: #000000 !important;
        font-family: 'Arial', sans-serif;
    }
    .stDataFrame {
        border: 2px solid #FFD700;
        border-radius: 8px;
    }
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

set_background()



# Optional AI integration (install openai and set OPENAI_API_KEY to enable)
try:
    import openai
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False

# ---------------------------
# App constants and brand palette
# ---------------------------
APP_TITLE = "Global Community School - ERP Portal"
BRAND_PRIMARY = "#0B4DA3"   # Deep Blue
BRAND_ACCENT = "#FFD24A"    # Gold / Yellow
BRAND_SECONDARY = "#064E3B" # Emerald
BRAND_ALERT = "#D92F2F"     # Accent Red
BRAND_BG = "#FBF8F0"        # Soft cream background

DATA_DIR = Path("gcs_data")
UPLOAD_DIR = DATA_DIR / "uploads"
DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)

# ---------------------------
# Persistence helpers
# ---------------------------
def load_json(name: str, default):
    path = DATA_DIR / f"{name}.json"
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default

def save_json(name: str, data):
    path = DATA_DIR / f"{name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_uploaded_file(uploaded_file):
    dest = UPLOAD_DIR / f"{secrets.token_hex(6)}_{uploaded_file.name}"
    with open(dest, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(dest)

# ---------------------------
# Utilities
# ---------------------------
def validate_phone(p):
    try:
        n = phonenumbers.parse(p, "GH")
        return phonenumbers.is_valid_number(n)
    except Exception:
        return False

# Background task queue (simple)
task_queue = []
def enqueue_task(fn, *args, **kwargs):
    task_queue.append((fn, args, kwargs))
    def runner():
        while task_queue:
            fn2, a2, k2 = task_queue.pop(0)
            try:
                fn2(*a2, **k2)
            except Exception as e:
                print("Background task error:", e)
    threading.Thread(target=runner, daemon=True).start()

# ---------------------------
# Streamlit page config & base CSS (brand-forward)
# ---------------------------
st.set_page_config(page_title=APP_TITLE, page_icon="🎓", layout="wide", initial_sidebar_state="collapsed")
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        padding: 0px !important;
        margin: 0px !important;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 100% !important;
    }
    div.stButton > button {
        background-color: #0B4DA3 !important;
        color: #FFD24A !important;
        border: 2px solid #FFD24A !important;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Load persisted stores into session_state
# ---------------------------
st.session_state.setdefault('authenticated', False)
st.session_state.setdefault('current_user', None)
st.session_state.setdefault('user_role', None)

persist_users = load_json("users", [])
persist_students = load_json("students", [])
persist_teachers = load_json("teachers", [])
persist_receipts = load_json("receipts", [])
persist_sms_logs = load_json("sms_logs", [])
persist_academic = load_json("academic_records", {})
persist_assignments = load_json("assignments", [])
persist_quizzes = load_json("quizzes", [])
persist_exams = load_json("exams", [])
persist_projects = load_json("projects", [])
persist_resources = load_json("resources", [])
persist_announcements = load_json("announcements", [])
persist_attendance = load_json("attendance", {})
persist_lessons = load_json("lessons", {})
persist_parent_links = load_json("parent_links", {})
persist_teacher_assignments = load_json("teacher_assignments", {})
persist_branding = load_json("branding", {"emblem": None, "background": None, "primary": BRAND_PRIMARY, "accent": BRAND_ACCENT})
persist_activity_log = load_json("activity_log", [])
persist_notifications = load_json("notifications", {})

st.session_state.students = pd.DataFrame(persist_students) if persist_students else pd.DataFrame(columns=[
    "ID","Name","Class","Gender","Guardian Phone","Fees Due","Fees Paid","Canteen Deposit","Canteen Utilized","Photo"
])
st.session_state.teachers = pd.DataFrame(persist_teachers) if persist_teachers else pd.DataFrame(columns=[
    "ID","Name","Assigned Class","Subject","Basic Salary"
])
st.session_state.receipts = persist_receipts
st.session_state.sms_logs = persist_sms_logs
st.session_state.academic_records = persist_academic
st.session_state.users = persist_users
st.session_state.assignments = persist_assignments
st.session_state.quizzes = persist_quizzes
st.session_state.exams = persist_exams
st.session_state.projects = persist_projects
st.session_state.resources = persist_resources
st.session_state.announcements = persist_announcements
st.session_state.attendance = persist_attendance if isinstance(persist_attendance, dict) else {}
st.session_state.lessons = persist_lessons if isinstance(persist_lessons, dict) else {}
st.session_state.parent_links = persist_parent_links if isinstance(persist_parent_links, dict) else {}
st.session_state.teacher_assignments = persist_teacher_assignments if isinstance(persist_teacher_assignments, dict) else {}
st.session_state.branding = persist_branding if isinstance(persist_branding, dict) else {"emblem": None, "background": None, "primary": BRAND_PRIMARY, "accent": BRAND_ACCENT}
st.session_state.activity_log = persist_activity_log if isinstance(persist_activity_log, list) else []
st.session_state.notifications = persist_notifications if isinstance(persist_notifications, dict) else {}

# Ensure today's attendance exists
_today = datetime.now().strftime("%Y-%m-%d")
st.session_state.attendance.setdefault(_today, {})

# Persist all
def persist_all():
    save_json("users", st.session_state.get("users", []))
    save_json("students", st.session_state.students.to_dict(orient="records"))
    save_json("teachers", st.session_state.teachers.to_dict(orient="records"))
    save_json("receipts", st.session_state.get("receipts", []))
    save_json("sms_logs", st.session_state.get("sms_logs", []))
    save_json("academic_records", st.session_state.get("academic_records", {}))
    save_json("assignments", st.session_state.get("assignments", []))
    save_json("quizzes", st.session_state.get("quizzes", []))
    save_json("exams", st.session_state.get("exams", []))
    save_json("projects", st.session_state.get("projects", []))
    save_json("resources", st.session_state.get("resources", []))
    save_json("announcements", st.session_state.get("announcements", []))
    save_json("attendance", st.session_state.get("attendance", {}))
    save_json("lessons", st.session_state.get("lessons", {}))
    save_json("parent_links", st.session_state.get("parent_links", {}))
    save_json("teacher_assignments", st.session_state.get("teacher_assignments", {}))
    save_json("branding", st.session_state.get("branding", {}))
    save_json("activity_log", st.session_state.get("activity_log", []))
    save_json("notifications", st.session_state.get("notifications", {}))

# ---------------------------
# Security helpers
# ---------------------------
def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        return False

# Ensure default admin exists
if not any(u.get("role") == "admin" for u in st.session_state.users):
    st.session_state.users.append({"username":"admin","password_hash":hash_password("gcs2026"),"role":"admin","assigned_classes":[],"display_name":"Administrator"})
    persist_all()

def require_role(allowed_roles):
    if st.session_state.get("user_role") not in allowed_roles:
        st.warning("Insufficient permissions for this module.")
        st.stop()

def require_teacher_for_class(username, class_name):
    assigned = st.session_state.get("teacher_assignments", {}).get(username, [])
    return class_name in assigned

def require_roles_or_teacher(allowed_roles, class_context=None):
    role = st.session_state.get("user_role")
    user = st.session_state.get("current_user")
    if role in allowed_roles:
        return True
    if role == "teacher" and class_context:
        if require_teacher_for_class(user, class_context):
            return True
    st.warning("Insufficient permissions for this action.")
    st.stop()

# ---------------------------
# System constants
# ---------------------------
SYSTEM_CLASSES = [
    "Nursery 1", "Nursery 2", "KG 1", "KG 2",
    "Primary 1", "Primary 2", "Primary 3", "Primary 4", "Primary 5", "Primary 6",
    "JHS 1", "JHS 2", "JHS 3"
]
BACKGROUND_MAP = {
    "Dashboard": ASSETS_DIR / "emblem.jpeg",
    "Admission": ASSETS_DIR / "culture.jpeg",
    "Attendance": ASSETS_DIR / "sports.jpeg",
    "Academic": ASSETS_DIR / "science.jpeg",
    "LMS": ASSETS_DIR / "arts.jpeg",
    "AI Assistant": ASSETS_DIR / "ai_lab.jpeg",
}

# ---------------------------
# Dynamic background (use uploaded branding background if present)
# ---------------------------
bg_path = st.session_state.get("branding", {}).get("background")
if bg_path and Path(bg_path).exists():
    st.markdown(f"""
        <style>
            .stApp {{
                background-image: url("file://{bg_path}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            .stApp::before {{
                content: "";
                position: fixed;
                inset: 0;
                background: rgba(251,248,240,0.65);
                pointer-events: none;
            }}
        </style>
    """, unsafe_allow_html=True)

# ---------------------------
# ---------------------------
# UI Helpers & Visual Layouts
# ---------------------------
def apply_module_background(module_name: str):
    bg_path = BACKGROUND_MAP.get(module_name)
    if bg_path and bg_path.exists():
        st.markdown(f"""
            <style>
                .stApp {{
                    background-image: url("file://{bg_path}");
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
                .stApp::before {{
                    content: "";
                    position: fixed;
                    inset: 0;
                    background: rgba(251,248,240,0.65);
                    pointer-events: none;
                }}
            </style>
        """, unsafe_allow_html=True)


# ---------------------------
# Authentication UI (login required before navigation)
# ---------------------------
if not st.session_state.authenticated:
    st.markdown("<div class='auth-container'>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    col1, col2 = st.columns([2,1])
    with col1:
        if st.button("Login"):
            user = next((u for u in st.session_state.users if u["username"] == username), None)
            if user and verify_password(password, user["password_hash"]):
                st.session_state.authenticated = True
                st.session_state.current_user = username
                st.session_state.user_role = user.get("role", "admin")
                # record login in activity log
                entry = {"timestamp": datetime.now().isoformat(), "user": username, "role": user.get("role"), "action": "login", "meta": {}}
                st.session_state.activity_log.insert(0, entry)
                # notify admin(s)
                admins = [u["username"] for u in st.session_state.users if u.get("role")=="admin"]
                for a in admins:
                    st.session_state.notifications.setdefault(a, []).append({"ts": datetime.now().isoformat(), "message": f"{username} logged in", "read": False})
                persist_all()
                st.success("Access granted.")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials.")
    with col2:
        if st.button("Register"):
            if username and password:
                if any(u["username"] == username for u in st.session_state.users):
                    st.error("Username exists.")
                else:
                    role = st.selectbox("Role", ["admin","teacher","parent","student"], key="reg_role")
                    st.session_state.users.append({"username": username, "password_hash": hash_password(password), "role": role, "assigned_classes": [], "display_name": username})
                    persist_all()
                    st.success(f"User {username} created.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Sidebar navigation (only visible after login)
st.sidebar.markdown(f"<div class='sidebar-brand'><strong style='color:{BRAND_PRIMARY}'>GLOBAL COMMUNITY</strong><br><small style='color:#6B7280'>School ERP</small></div>", unsafe_allow_html=True)

# show admin notification count
notif_count = len([n for n in st.session_state.notifications.get(st.session_state.current_user, []) if not n.get("read")]) if st.session_state.current_user else 0
menu_label = "Navigate"
if notif_count > 0 and st.session_state.user_role == "admin":
    menu_label = f"Navigate  🔔{notif_count}"
# --- Branding Header ---
st.markdown(
    f"""
    <div style="text-align:center; padding:20px;">
        <h1 style="color:{BRAND_PRIMARY}; font-family:'Trebuchet MS', sans-serif;">
            GLOBAL COMMUNITY SCHOOL PORTAL
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Always show persisted logo if available
if st.session_state.branding.get("emblem"):
    st.image(st.session_state.branding["emblem"], width=150, caption="School Logo")


menu = st.sidebar.radio(menu_label, [
    "Dashboard",
    "Admission",
    "Attendance",
    "Fees",
    "Canteen",
    "Payroll",
    "Academic",
    "LMS",
    "Teacher Portal",
    "Student Portal",
    "AI Assistant",
    "Users",
    "Parents",
    "Settings",
    "Analytics",
    "Backup"

])

if st.sidebar.button("Logout"):
    # record logout
    entry = {"timestamp": datetime.now().isoformat(), "user": st.session_state.current_user, "role": st.session_state.user_role, "action": "logout", "meta": {}}
    st.session_state.activity_log.insert(0, entry)
    persist_all()
    st.session_state.authenticated = False
    st.session_state.current_user = None
    st.session_state.user_role = None
    st.experimental_rerun()

# ---------------------------
# Helper functions for modules
# ---------------------------

def attendance_summary():
    st.session_state.setdefault("attendance", {})
    summaries = {}
    for date_key, rec in st.session_state.get("attendance", {}).items():
        if not isinstance(rec, dict):
            continue
        for sid, status in rec.items():
            summaries.setdefault(sid, {"Present":0,"Absent":0,"Late":0})
            if status in summaries[sid]:
                summaries[sid][status] += 1
            else:
                summaries[sid]["Late"] += 1
    return summaries

def send_sms_stub(phone, message):
    log = {"Phone": phone, "Message": message, "Date": datetime.now().strftime("%Y-%m-%d %H:%M")}
    st.session_state.sms_logs.append(log)
    persist_all()

def log_action(user, role, action, meta=None):
    entry = {"timestamp": datetime.now().isoformat(), "user": user, "role": role, "action": action, "meta": meta or {}}
    st.session_state.activity_log.insert(0, entry)
    # notify admins for important actions (login already handled)
    if action in ("create_user","delete_user","delete_student","delete_teacher","delete_assignment","delete_quiz","delete_project"):
        admins = [u["username"] for u in st.session_state.users if u.get("role")=="admin"]
        for a in admins:
            st.session_state.notifications.setdefault(a, []).append({"ts": datetime.now().isoformat(), "message": f"{user} performed {action}", "read": False})
    persist_all()

# ---------------------------
# Modules
# ---------------------------

# Dashboard
if menu == "Dashboard":
    st.title("Operations Dashboard")
    # show admin notifications if admin
    if st.session_state.user_role == "admin":
        notifs = st.session_state.notifications.get(st.session_state.current_user, [])
        unread = [n for n in notifs if not n.get("read")]
        if unread:
            st.warning(f"You have {len(unread)} new notification(s). Open Analytics -> Activity Log to view.")
        # quick action to mark all read
        if st.button("Mark notifications read"):
            for n in notifs:
                n["read"] = True
            st.session_state.notifications[st.session_state.current_user] = notifs
            persist_all()
            st.success("Notifications marked read.")

    st.markdown('<div class="hero-card">', unsafe_allow_html=True)
    st.markdown(f"**Welcome, {st.session_state.get('current_user')}** — snapshot for **{datetime.now().strftime('%d %b %Y')}**")
    st.markdown("</div>", unsafe_allow_html=True)

    total_students = len(st.session_state.students)
    total_teachers = len(st.session_state.teachers)
    total_paid = pd.to_numeric(st.session_state.students["Fees Paid"]).sum() if total_students>0 else 0.0
    outstanding = pd.to_numeric(st.session_state.students["Fees Due"]).sum() - total_paid if total_students>0 else 0.0

    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(f"<div class='metric-card'><div class='metric-label'>Learners</div><div class='metric-value'>{total_students}</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-card'><div class='metric-label'>Revenue</div><div class='metric-value'>GHS {total_paid:,.2f}</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='metric-card'><div class='metric-label'>Outstanding</div><div class='metric-value'>GHS {outstanding:,.2f}</div></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='metric-card'><div class='metric-label'>Faculty</div><div class='metric-value'>{total_teachers}</div></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Recent Announcements")
    for ann in st.session_state.get("announcements", [])[-5:]:
        st.markdown(f"**{ann.get('Title','')}** — {ann.get('Body','')}")

# Admission (with delete option)
elif menu == "Admission":
    require_role(["admin",])
    st.title("Learner Admission & Profiles")
    tab1, tab2 = st.tabs(["New Admission","Rosters & Profiles"])
    with tab1:
        st.subheader("New Learner Enrollment")
        with st.form("admit", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                stu_id = st.text_input("Learner ID", value=f"GCS-{datetime.now().strftime('%y')}-{len(st.session_state.students)+1:03d}")
                name = st.text_input("Full Name")
                cls = st.selectbox("Class", SYSTEM_CLASSES)
                gender = st.radio("Gender", ["Male","Female"], horizontal=True)
            with col2:
                phone = st.text_input("Guardian Phone", placeholder="+233XXXXXXXXX")
                fee = st.number_input("Term Fee (GHS)", min_value=0.0, value=3000.0, step=50.0)
                photo = st.file_uploader("Upload Photo (optional)", type=["png","jpg","jpeg"])
                parent_username = st.text_input("Parent account username (create or existing)")
            if st.form_submit_button("Enroll Learner"):
                if not name.strip():
                    st.error("Name required.")
                else:
                    photo_path = save_uploaded_file(photo) if photo else ""
                    new = {"ID":stu_id,"Name":name,"Class":cls,"Gender":gender,"Guardian Phone":phone,"Fees Due":fee,"Fees Paid":0.0,"Canteen Deposit":0.0,"Canteen Utilized":0.0,"Photo":photo_path}
                    st.session_state.students = pd.concat([st.session_state.students, pd.DataFrame([new])], ignore_index=True)
                    # link parent -> student
                    if parent_username:
                        st.session_state.setdefault("parent_links", {})
                        st.session_state["parent_links"].setdefault(parent_username, []).append(stu_id)
                        if not any(u["username"] == parent_username for u in st.session_state.users):
                            st.session_state.users.append({"username": parent_username, "password_hash": hash_password("changeme"), "role": "parent", "assigned_classes": [], "display_name": parent_username})
                    log_action(st.session_state.current_user, st.session_state.user_role, "create_student", {"student_id": stu_id})
                    persist_all()
                    st.success(f"{name} enrolled.")
    with tab2:
        st.subheader("Class Rosters & Delete")
        if len(st.session_state.students) == 0:
            st.info("No learners enrolled.")
        else:
            # show table
            st.dataframe(st.session_state.students, use_container_width=True)
            st.markdown("### Delete a student")
            sid = st.selectbox("Select Learner ID to delete", st.session_state.students["ID"])
            if sid:
                if st.button("Delete selected student"):
                    # confirm
                    confirm = st.checkbox("Confirm deletion of student " + sid, key="confirm_del_student")
                    if confirm:
                        st.session_state.students = st.session_state.students[st.session_state.students["ID"] != sid]
                        # remove from parent links
                        for p, wards in st.session_state.parent_links.items():
                            if sid in wards:
                                wards.remove(sid)
                        log_action(st.session_state.current_user, st.session_state.user_role, "delete_student", {"student_id": sid})
                        persist_all()
                        st.success(f"Student {sid} deleted.")
                        st.experimental_rerun()

# Attendance
elif menu == "Attendance":
    require_role(["admin","teacher"])
    st.title("Daily Attendance")
    today = datetime.now().strftime("%Y-%m-%d")
    st.session_state.setdefault("attendance", {})
    st.session_state["attendance"].setdefault(today, {})

    # Filter students if teacher
    if st.session_state.get("user_role") == "teacher":
        teacher_user = st.session_state.get("current_user")
        allowed_classes = st.session_state.get("teacher_assignments", {}).get(teacher_user, [])
        if not allowed_classes:
            st.info("You are not assigned to any classes yet.")
            students_to_show = st.session_state.students.iloc[0:0]
        else:
            students_to_show = st.session_state.students[st.session_state.students["Class"].isin(allowed_classes)]
    else:
        students_to_show = st.session_state.students

    if len(students_to_show) == 0:
        st.info("No students to show.")
    else:
        for _, row in students_to_show.iterrows():
            key = f"att_{today}_{row['ID']}"
            status = st.radio(f"{row['Name']} ({row['Class']})", ["Present","Absent","Late"], key=key)
            st.session_state["attendance"][today][row['ID']] = status

        st.subheader("Today's Records")
        st.write(st.session_state["attendance"][today])
        st.subheader("Analytics (summary)")
        st.write(attendance_summary())
        if st.button("Save Attendance"):
            log_action(st.session_state.current_user, st.session_state.user_role, "mark_attendance", {"date": today})
            persist_all()
            st.success("Saved.")

# Fees
elif menu == "Fees":
    require_role(["admin",])
    st.title("Fees & Receipts")
    if len(st.session_state.students) > 0:
        sid = st.selectbox("Learner", st.session_state.students["ID"])
        amt = st.number_input("Amount (GHS)", min_value=0.0, step=10.0)
        if st.button("Record Payment"):
            st.session_state.students.loc[st.session_state.students["ID"]==sid, "Fees Paid"] += amt
            st.session_state.receipts.append({"ID":sid,"Amount":amt,"Date":datetime.now().strftime("%Y-%m-%d %H:%M")})
            log_action(st.session_state.current_user, st.session_state.user_role, "record_payment", {"student_id": sid, "amount": amt})
            persist_all()
            st.success("Payment recorded.")
    st.subheader("Receipts")
    st.dataframe(pd.DataFrame(st.session_state.receipts))

# Canteen
elif menu == "Canteen":
    require_role(["admin",])
    st.title("Canteen Accounts")
    if len(st.session_state.students) > 0:
        sid = st.selectbox("Learner", st.session_state.students["ID"])
        deposit = st.number_input("Deposit (GHS)", min_value=0.0, step=5.0)
        spend = st.number_input("Utilize (GHS)", min_value=0.0, step=5.0)
        if st.button("Update"):
            st.session_state.students.loc[st.session_state.students["ID"]==sid, "Canteen Deposit"] += deposit
            st.session_state.students.loc[st.session_state.students["ID"]==sid, "Canteen Utilized"] += spend
            log_action(st.session_state.current_user, st.session_state.user_role, "update_canteen", {"student_id": sid, "deposit": deposit, "spend": spend})
            persist_all()
            st.success("Updated.")
    st.dataframe(st.session_state.students[["ID","Name","Canteen Deposit","Canteen Utilized"]])

# Payroll / Teachers (create teacher accounts and delete)
elif menu == "Payroll":
    require_role(["admin"])
    st.title("Faculty & Payroll")
    with st.form("add_teacher"):
        tid = st.text_input("Teacher Username / ID")
        tname = st.text_input("Full Name")
        assigned_classes = st.multiselect("Assign Classes (multiple)", SYSTEM_CLASSES)
        subject = st.text_input("Subject")
        salary = st.number_input("Basic Salary (GHS)", min_value=0.0, step=100.0)
        if st.form_submit_button("Add Teacher"):
            new_teacher = {"ID": tid, "Name": tname, "Assigned Class": ", ".join(assigned_classes), "Subject": subject, "Basic Salary": salary}
            st.session_state.teachers = pd.concat([st.session_state.teachers, pd.DataFrame([new_teacher])], ignore_index=True)
            if not any(u["username"] == tid for u in st.session_state.users):
                st.session_state.users.append({"username": tid, "password_hash": hash_password("changeme"), "role": "teacher", "assigned_classes": assigned_classes, "display_name": tname})
            else:
                for u in st.session_state.users:
                    if u["username"] == tid:
                        u["assigned_classes"] = assigned_classes
                        u["display_name"] = tname
            st.session_state.teacher_assignments[tid] = assigned_classes
            log_action(st.session_state.current_user, st.session_state.user_role, "create_teacher", {"teacher_id": tid})
            persist_all()
            st.success(f"Teacher {tname} added and assigned to {', '.join(assigned_classes)}.")
    st.subheader("Teachers")
    st.dataframe(st.session_state.teachers)
    st.markdown("### Delete a teacher")
    if len(st.session_state.teachers) > 0:
        del_tid = st.selectbox("Select Teacher ID to delete", st.session_state.teachers["ID"])
        if del_tid and st.button("Delete selected teacher"):
            confirm = st.checkbox("Confirm deletion of teacher " + del_tid, key="confirm_del_teacher")
            if confirm:
                st.session_state.teachers = st.session_state.teachers[st.session_state.teachers["ID"] != del_tid]
                # remove user account if exists
                st.session_state.users = [u for u in st.session_state.users if u["username"] != del_tid]
                st.session_state.teacher_assignments.pop(del_tid, None)
                log_action(st.session_state.current_user, st.session_state.user_role, "delete_teacher", {"teacher_id": del_tid})
                persist_all()
                st.success(f"Teacher {del_tid} deleted.")
                st.experimental_rerun()

# Academic (grades)
elif menu == "Academic":
    require_role(["admin","teacher"])
    st.title("Academic Records")
    if len(st.session_state.students) == 0:
        st.info("No students.")
    else:
        sid = st.selectbox("Learner", st.session_state.students["ID"])
        subj = st.text_input("Subject")
        class_score = st.number_input("Class Score", min_value=0.0, max_value=100.0)
        exam_score = st.number_input("Exam Score", min_value=0.0, max_value=100.0)
        if st.button("Record"):
            st.session_state.academic_records.setdefault(sid, {})
            st.session_state.academic_records[sid][subj] = {"class":class_score,"exam":exam_score}
            log_action(st.session_state.current_user, st.session_state.user_role, "record_grade", {"student_id": sid, "subject": subj})
            persist_all()
            st.success("Recorded.")
        st.write(st.session_state.academic_records.get(sid, {}))

# LMS (lessons, assignments, quizzes, projects) - with delete options
elif menu == "LMS":
    require_role(["admin","teacher","student","parent"])
    st.title("Learning Management System")

    # If teacher, show allowed classes
    if st.session_state.get("user_role") == "teacher":
        teacher_user = st.session_state.get("current_user")
        allowed_classes = st.session_state.get("teacher_assignments", {}).get(teacher_user, [])
        st.info(f"You are limited to classes: {', '.join(allowed_classes) if allowed_classes else 'None assigned'}")

    # Lessons / Class Text
    st.subheader("Lessons / Class Text")
    cls = st.selectbox("Class (for lesson)", SYSTEM_CLASSES, key="lesson_class")
    lesson_title = st.text_input("Lesson Title")
    lesson_body = st.text_area("Lesson Content (class text / notes)")
    if st.button("Publish Lesson"):
        if st.session_state.get("user_role") == "teacher" and cls not in st.session_state.get("teacher_assignments", {}).get(st.session_state.get("current_user"), []):
            st.error("You are not assigned to this class.")
        else:
            st.session_state.lessons.setdefault(cls, []).append({"Title":lesson_title,"Body":lesson_body,"Date":datetime.now().strftime("%Y-%m-%d")})
            log_action(st.session_state.current_user, st.session_state.user_role, "publish_lesson", {"class": cls, "title": lesson_title})
            persist_all()
            st.success("Lesson published.")
    st.write(st.session_state.lessons.get(cls, []))

    st.markdown("---")
    # Assignments
    st.subheader("Assignments")
    with st.form("add_assignment"):
        a_title = st.text_input("Assignment Title")
        a_desc = st.text_area("Description")
        a_class = st.selectbox("Class", SYSTEM_CLASSES, key="assign_class")
        if st.form_submit_button("Add Assignment"):
            if st.session_state.get("user_role") == "teacher" and a_class not in st.session_state.get("teacher_assignments", {}).get(st.session_state.get("current_user"), []):
                st.error("You are not assigned to this class.")
            else:
                st.session_state.setdefault("assignments", []).append({"Title":a_title,"Description":a_desc,"Class":a_class,"Date":datetime.now().strftime("%Y-%m-%d")})
                log_action(st.session_state.current_user, st.session_state.user_role, "create_assignment", {"class": a_class, "title": a_title})
                persist_all()
                st.success("Assignment added.")
    st.dataframe(pd.DataFrame(st.session_state.get("assignments", [])))
    # delete assignment
    st.markdown("### Delete an assignment")
    if st.session_state.get("assignments"):
        assign_titles = [f"{i} | {a['Title']} ({a.get('Class')})" for i,a in enumerate(st.session_state.get("assignments"))]
        sel = st.selectbox("Select assignment to delete", assign_titles)
        if sel and st.button("Delete assignment"):
            idx = int(sel.split("|")[0].strip())
            a = st.session_state["assignments"].pop(idx)
            log_action(st.session_state.current_user, st.session_state.user_role, "delete_assignment", {"title": a.get("Title"), "class": a.get("Class")})
            persist_all()
            st.success("Assignment deleted.")
            st.experimental_rerun()

    st.markdown("---")
    # Quizzes
    st.subheader("Quizzes")
    with st.form("add_quiz"):
        q_title = st.text_input("Quiz Title")
        q_class = st.selectbox("Class", SYSTEM_CLASSES, key="quiz_class")
        q_question = st.text_area("Question")
        q_opt1 = st.text_input("Option 1")
        q_opt2 = st.text_input("Option 2")
        q_opt3 = st.text_input("Option 3")
        q_opt4 = st.text_input("Option 4")
        q_correct = st.selectbox("Correct Option", [q_opt1,q_opt2,q_opt3,q_opt4])
        if st.form_submit_button("Add Quiz"):
            if st.session_state.get("user_role") == "teacher" and q_class not in st.session_state.get("teacher_assignments", {}).get(st.session_state.get("current_user"), []):
                st.error("You are not assigned to this class.")
            else:
                st.session_state.setdefault("quizzes", []).append({"Title":q_title,"Class":q_class,"Question":q_question,"Options":[q_opt1,q_opt2,q_opt3,q_opt4],"Correct":q_correct})
                log_action(st.session_state.current_user, st.session_state.user_role, "create_quiz", {"title": q_title, "class": q_class})
                persist_all()
                st.success("Quiz added.")
    st.dataframe(pd.DataFrame(st.session_state.get("quizzes", [])))
    # delete quiz
    st.markdown("### Delete a quiz")
    if st.session_state.get("quizzes"):
        quiz_titles = [f"{i} | {q['Title']} ({q.get('Class')})" for i,q in enumerate(st.session_state.get("quizzes"))]
        selq = st.selectbox("Select quiz to delete", quiz_titles, key="del_quiz_select")
        if selq and st.button("Delete quiz"):
            idx = int(selq.split("|")[0].strip())
            q = st.session_state["quizzes"].pop(idx)
            log_action(st.session_state.current_user, st.session_state.user_role, "delete_quiz", {"title": q.get("Title"), "class": q.get("Class")})
            persist_all()
            st.success("Quiz deleted.")
            st.experimental_rerun()

    st.markdown("---")
    # Projects
    st.subheader("Projects")
    with st.form("add_project"):
        p_title = st.text_input("Project Title")
        p_desc = st.text_area("Project Description")
        p_class = st.selectbox("Class", SYSTEM_CLASSES, key="proj_class")
        if st.form_submit_button("Add Project"):
            if st.session_state.get("user_role") == "teacher" and p_class not in st.session_state.get("teacher_assignments", {}).get(st.session_state.get("current_user"), []):
                st.error("You are not assigned to this class.")
            else:
                st.session_state.setdefault("projects", []).append({"Title":p_title,"Description":p_desc,"Class":p_class,"Date":datetime.now().strftime("%Y-%m-%d")})
                log_action(st.session_state.current_user, st.session_state.user_role, "create_project", {"title": p_title, "class": p_class})
                persist_all()
                st.success("Project added.")
    st.dataframe(pd.DataFrame(st.session_state.get("projects", [])))
    # delete project
    st.markdown("### Delete a project")
    if st.session_state.get("projects"):
        proj_titles = [f"{i} | {p['Title']} ({p.get('Class')})" for i,p in enumerate(st.session_state.get("projects"))]
        selp = st.selectbox("Select project to delete", proj_titles, key="del_proj_select")
        if selp and st.button("Delete project"):
            idx = int(selp.split("|")[0].strip())
            p = st.session_state["projects"].pop(idx)
            log_action(st.session_state.current_user, st.session_state.user_role, "delete_project", {"title": p.get("Title"), "class": p.get("Class")})
            persist_all()
            st.success("Project deleted.")
            st.experimental_rerun()

# Teacher Portal (dedicated view) - LMS, Attendance, Grades, AI Assistant
elif menu == "Teacher Portal":
    require_role(["teacher","admin"])
    st.title("Teacher Portal")
    teacher = st.session_state.get("current_user")
    assigned = st.session_state.get("teacher_assignments", {}).get(teacher, [])
    st.subheader(f"Welcome {teacher} — Assigned classes: {', '.join(assigned) if assigned else 'None'}")

    # Quick nav
    t_action = st.selectbox("Teacher actions", ["LMS","Attendance","Grades","AI Assistant","Class Rosters","Export Roster CSV"])
    if t_action == "Dashboard":
        st.markdown("**Teacher Dashboard**")
        total_assigned_students = st.session_state.students[st.session_state.students["Class"].isin(assigned)].shape[0] if assigned else 0
        total_assignments = len([a for a in st.session_state.get("assignments", []) if a.get("Class") in assigned])
        total_quizzes = len([q for q in st.session_state.get("quizzes", []) if q.get("Class") in assigned])
        col1,col2,col3 = st.columns(3)
        col1.metric("Assigned Students", total_assigned_students)
        col2.metric("Assignments", total_assignments)
        col3.metric("Quizzes", total_quizzes)

    elif t_action == "LMS":
        st.markdown("### LMS — manage lessons and assignments for your classes")
        cls_choice = st.selectbox("Select class", assigned if assigned else SYSTEM_CLASSES, key="teacher_lms_class")
        st.markdown("**Lessons for class**")
        st.write(st.session_state.lessons.get(cls_choice, []))
        st.markdown("**Assignments for class**")
        st.write([a for a in st.session_state.get("assignments", []) if a.get("Class")==cls_choice])
        st.markdown("**Create quick assignment**")
        with st.form("teacher_quick_assignment"):
            atitle = st.text_input("Title")
            adesc = st.text_area("Description")
            if st.form_submit_button("Publish Assignment"):
                if teacher and assigned and cls_choice not in assigned:
                    st.error("You are not assigned to this class.")
                else:
                    st.session_state.setdefault("assignments", []).append({"Title":atitle,"Description":adesc,"Class":cls_choice,"Date":datetime.now().strftime("%Y-%m-%d")})
                    log_action(teacher, "teacher", "create_assignment", {"class": cls_choice, "title": atitle})
                    persist_all()
                    st.success("Assignment published.")

    elif t_action == "Attendance":
        st.markdown("### Mark attendance for your classes")
        today = datetime.now().strftime("%Y-%m-%d")
        st.session_state.setdefault("attendance", {})
        st.session_state["attendance"].setdefault(today, {})
        for cls in assigned:
            st.markdown(f"#### {cls}")
            roster = st.session_state.students[st.session_state.students["Class"]==cls]
            if roster.empty:
                st.info("No students in this class.")
            else:
                for _, r in roster.iterrows():
                    key = f"att_{today}_{r['ID']}"
                    status = st.radio(f"{r['Name']} ({r['ID']})", ["Present","Absent","Late"], key=key)
                    st.session_state["attendance"][today][r['ID']] = status
        if st.button("Save Attendance (Teacher)"):
            log_action(teacher, "teacher", "mark_attendance", {"date": today})
            persist_all()
            st.success("Attendance saved.")

    elif t_action == "Grades":
        st.markdown("### Grade students")
        cls = st.selectbox("Select class to grade", assigned, key="teacher_grade_class")
        roster = st.session_state.students[st.session_state.students["Class"]==cls]
        if roster.empty:
            st.info("No students.")
        else:
            sid = st.selectbox("Select student", roster["ID"])
            subj = st.text_input("Subject")
            class_score = st.number_input("Class Score", min_value=0.0, max_value=100.0)
            exam_score = st.number_input("Exam Score", min_value=0.0, max_value=100.0)
            if st.button("Save Grade"):
                st.session_state.academic_records.setdefault(sid, {})
                st.session_state.academic_records[sid][subj] = {"class":class_score,"exam":exam_score}
                log_action(teacher, "teacher", "record_grade", {"student_id": sid, "subject": subj})
                persist_all()
                st.success("Grade saved.")
        st.markdown("**Quick view: class grades**")
        class_grades = { st.session_state.academic_records.get(sid, {}) for sid in roster["ID"].tolist()}
        st.write(class_grades)

    elif t_action == "AI Assistant":
        st.markdown("### AI Assistant (teacher tools)")
        prompt = st.text_area("Ask the assistant (e.g., 'Create 5 formative questions for Grade 4 Science on plants')", height=160)
        if st.button("Get AI Response"):
            if not prompt.strip():
                st.error("Enter a prompt.")
            else:
                if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
                    try:
                        openai.api_key = os.getenv("OPENAI_API_KEY")
                        resp = openai.ChatCompletion.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}], max_tokens=600)
                        answer = resp.choices[0].message.content.strip()
                    except Exception as e:
                        answer = f"[AI error] {e}"
                else:
                    answer = f"[Assistant offline] {prompt}"
                st.markdown("**Response**")
                st.write(answer)

    elif t_action == "Class Rosters":
        st.markdown("### Class Rosters")
        for cls in assigned:
            st.markdown(f"**{cls}**")
            roster = st.session_state.students[st.session_state.students["Class"]==cls]
            if roster.empty:
                st.info("No students.")
            else:
                st.dataframe(roster[["ID","Name","Gender","Guardian Phone","Fees Due","Fees Paid"]])

    elif t_action == "Export Roster CSV":
        cls = st.selectbox("Select class to export", assigned, key="teacher_export_class")
        roster = st.session_state.students[st.session_state.students["Class"]==cls]
        if not roster.empty:
            buf = io.StringIO()
            roster.to_csv(buf, index=False)
            buf.seek(0)
            st.download_button("Download CSV", data=buf, file_name=f"{cls}_roster_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")

# Student Portal (dedicated view)
elif menu == "Student Portal":
    require_role(["student","parent","admin","teacher"])
    st.title("Student Portal")
    user = st.session_state.get("current_user")
    student_record = None
    if st.session_state.get("user_role") == "student":
        student_record = st.session_state.students[st.session_state.students["ID"] == user]
        if student_record.empty:
            student_record = st.session_state.students[st.session_state.students["Name"].str.contains(user, na=False)]
    elif st.session_state.get("user_role") == "parent":
        wards = st.session_state.get("parent_links", {}).get(user, [])
        if wards:
            sid = st.selectbox("Select your ward", wards)
            student_record = st.session_state.students[st.session_state.students["ID"] == sid]
    else:
        sid = st.selectbox("Select student", st.session_state.students["ID"] if len(st.session_state.students)>0 else [])
        if sid:
            student_record = st.session_state.students[st.session_state.students["ID"] == sid]

    if student_record is None or student_record.empty:
        st.info("No student profile found for your account. Contact admin to link your profile.")
    else:
        r = student_record.iloc[0]
        st.markdown(f"## {r['Name']} ({r['ID']})")
        if r.get("Photo") and Path(r["Photo"]).exists():
            st.image(r["Photo"], width=160)
        st.write({"Class": r["Class"], "Gender": r["Gender"], "Guardian Phone": r["Guardian Phone"]})
        st.subheader("Attendance (recent)")
        attendance = st.session_state.get("attendance", {})
        recent = {d:attendance[d].get(r["ID"]) for d in sorted(attendance.keys(), reverse=True)[:30] if r["ID"] in attendance[d]}
        st.write(recent)
        st.subheader("Grades")
        grades = st.session_state.get("academic_records", {}).get(r["ID"], {})
        st.write(grades)
        st.subheader("LMS Tasks")
        cls = r["Class"]
        assignments = [a for a in st.session_state.get("assignments", []) if a.get("Class")==cls]
        quizzes = [q for q in st.session_state.get("quizzes", []) if q.get("Class")==cls]
        projects = [p for p in st.session_state.get("projects", []) if p.get("Class")==cls]
        st.write({"Assignments": assignments, "Quizzes": quizzes, "Projects": projects})
        st.subheader("Announcements")
        for ann in st.session_state.get("announcements", [])[-5:]:
            st.markdown(f"**{ann.get('Title','')}** — {ann.get('Body','')}")

# AI Assistant (global)
elif menu == "AI Assistant":
    require_role(["admin","teacher","parent","student"])
    st.title("AI Assistant")
    st.markdown("Optional: set OPENAI_API_KEY in environment to enable external model.")
    prompt = st.text_area("Ask the assistant (lesson ideas, SMS drafts, summaries)", height=150)
    if st.button("Get Response"):
        if not prompt.strip():
            st.error("Enter a prompt.")
        else:
            if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
                try:
                    openai.api_key = os.getenv("OPENAI_API_KEY")
                    resp = openai.ChatCompletion.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}], max_tokens=600)
                    answer = resp.choices[0].message.content.strip()
                except Exception as e:
                    answer = f"[AI error] {e}"
            else:
                answer = f"[Assistant offline] {prompt}"
            st.markdown("**Response**")
            st.write(answer)

# Users (admin) with delete
elif menu == "Users":
    require_role(["admin"])
    st.title("User Management")
    st.dataframe(pd.DataFrame([{"username":u["username"],"role":u["role"], "display_name": u.get("display_name","")} for u in st.session_state.users]))
    with st.form("add_user"):
        uname = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["admin","teacher","student","parent"])
        assigned = st.multiselect("Assign Classes (for teacher)", SYSTEM_CLASSES)
        if st.form_submit_button("Add User"):
            if any(u["username"]==uname for u in st.session_state.users):
                st.error("Username exists.")
            else:
                st.session_state.users.append({"username":uname,"password_hash":hash_password(pw),"role":role,"assigned_classes":assigned,"display_name":uname})
                if role == "teacher":
                    st.session_state.teacher_assignments[uname] = assigned
                log_action(st.session_state.current_user, st.session_state.user_role, "create_user", {"username": uname, "role": role})
                persist_all()
                st.success("User added.")
    st.markdown("### Delete a user")
    usernames = [u["username"] for u in st.session_state.users]
    del_user = st.selectbox("Select user to delete", usernames)
    if del_user and st.button("Delete user"):
        if del_user == st.session_state.current_user:
            st.error("You cannot delete your own account while signed in.")
        else:
            confirm = st.checkbox("Confirm deletion of user " + del_user, key="confirm_del_user")
            if confirm:
                st.session_state.users = [u for u in st.session_state.users if u["username"] != del_user]
                st.session_state.parent_links.pop(del_user, None)
                st.session_state.teacher_assignments.pop(del_user, None)
                log_action(st.session_state.current_user, st.session_state.user_role, "delete_user", {"username": del_user})
                persist_all()
                st.success(f"User {del_user} deleted.")
                st.experimental_rerun()

# Parents portal (restricted)
elif menu == "Parents":
    require_role(["admin","teacher","parent"])
    st.title("Parents Portal")
    user = st.session_state.get("current_user")
    wards = st.session_state.get("parent_links", {}).get(user, [])
    if not wards:
        st.info("No linked wards found for your account. Contact admin to link your child.")
    else:
        for sid in wards:
            student = st.session_state.students[st.session_state.students["ID"] == sid]
            if student.empty:
                continue
            r = student.iloc[0]
            st.markdown(f"### {r['Name']} ({r['ID']}) — {r['Class']}")
            if r.get("Photo"):
                if Path(r["Photo"]).exists():
                    st.image(r["Photo"], width=140)
            st.subheader("Attendance (recent)")
            attendance = st.session_state.get("attendance", {})
            recent = {d:attendance[d].get(sid) for d in sorted(attendance.keys(), reverse=True)[:30] if sid in attendance[d]}
            st.write(recent)
            st.subheader("Grades")
            grades = st.session_state.get("academic_records", {}).get(sid, {})
            st.write(grades)
            st.subheader("Works To Do (LMS)")
            cls = r["Class"]
            assignments = [a for a in st.session_state.get("assignments", []) if a.get("Class")==cls]
            quizzes = [q for q in st.session_state.get("quizzes", []) if q.get("Class")==cls]
            projects = [p for p in st.session_state.get("projects", []) if p.get("Class")==cls]
            st.write({"Assignments": assignments, "Quizzes": quizzes, "Projects": projects})
    st.subheader("Announcements")
    for ann in st.session_state.get("announcements", [])[-5:]:
        st.markdown(f"**{ann.get('Title','')}** — {ann.get('Body','')}")

# Settings & Branding (upload emblem and set background)
elif menu == "Settings":
    require_role(["admin"])
    st.title("Settings & Branding")
    with st.expander("Upload Emblem (permanent)"):
        uploaded = st.file_uploader("Upload emblem (PNG/JPG) - high resolution recommended", type=["png","jpg","jpeg"])
        if uploaded:
            saved = save_uploaded_file(uploaded)
            st.session_state.branding["emblem"] = saved
            if st.checkbox("Use this emblem as background image (large, high-res recommended)"):
                st.session_state.branding["background"] = saved
            log_action(st.session_state.current_user, st.session_state.user_role, "update_branding", {"emblem": saved})
            persist_all()
            st.success("Emblem saved.")
            st.image(saved, width=120)
    with st.expander("Announcements"):
        atitle = st.text_input("Title")
        abody = st.text_area("Body")
        if st.button("Publish Announcement"):
            st.session_state.setdefault("announcements", []).append({"Title":atitle,"Body":abody,"Date":datetime.now().strftime("%Y-%m-%d")})
            log_action(st.session_state.current_user, st.session_state.user_role, "publish_announcement", {"title": atitle})
            persist_all()
            st.success("Published.")

# Analytics (admin only)
elif menu == "Analytics":
    require_role(["admin"])
    st.title("Admin Analytics & Activity Log")
    st.subheader("Activity Log (most recent first)")
    # show activity log table
    if st.session_state.activity_log:
        df_log = pd.DataFrame(st.session_state.activity_log)
        st.dataframe(df_log, use_container_width=True)
        # simple charts
        st.markdown("### Actions by user (top 10)")
        actions_by_user = df_log.groupby("user").size().sort_values(ascending=False).head(10)
        st.bar_chart(actions_by_user)
        st.markdown("### Actions by type")
        actions_by_type = df_log.groupby("action").size().sort_values(ascending=False)
        st.bar_chart(actions_by_type)
        st.markdown("### Daily logins (last 30 days)")
        # compute daily login counts
        df_log['date'] = pd.to_datetime(df_log['timestamp']).dt.date
        daily_logins = df_log[df_log['action']=='login'].groupby('date').size().reindex(pd.date_range(date.today()-pd.Timedelta(days=29), date.today()).date, fill_value=0)
        st.line_chart(daily_logins)
    else:
        st.info("No activity recorded yet.")
    st.markdown("---")
    st.subheader("Notifications")
    notifs = st.session_state.notifications.get(st.session_state.current_user, [])
    if notifs:
        for n in notifs[::-1]:
            status = "✅" if n.get("read") else "🔔"
            st.write(f"{status} {n.get('ts')} — {n.get('message')}")
        if st.button("Mark all notifications read"):
            for n in notifs:
                n["read"] = True
            st.session_state.notifications[st.session_state.current_user] = notifs
            persist_all()
            st.success("Marked read.")
    else:
        st.info("No notifications.")

# Backup & Export
elif menu == "Backup":
    settings_page()   # runs the backup & restore UI
def restore_db(uploaded_file):
    with open(DB_FILE, "wb") as f:
        f.write(uploaded_file.getbuffer())
    # After writing, reload session_state from DB
    reload_data()

def reload_data():
    # Example: reload students and teachers from SQLite
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

