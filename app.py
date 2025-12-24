import streamlit as st
import pandas as pd
import os
from datetime import datetime
from auth import signup_user, authenticate_user

# ------------------ PAGE CONFIG ------------------
st.set_page_config("RBAC System", "🔐", layout="centered")

# ------------------ GLOBAL STYLES ------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #667eea, #764ba2);
}

.main {
    background: transparent;
}

.card {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(12px);
    padding: 30px;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    color: white;
}

h1, h2, h3, label {
    color: white !important;
}

.stButton>button {
    width: 100%;
    border-radius: 8px;
    padding: 10px;
    font-weight: bold;
}

.sidebar .sidebar-content {
    background: linear-gradient(180deg, #1f2933, #111827);
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ------------------ FILE PATHS ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.csv")
LOGS_FILE = os.path.join(BASE_DIR, "logs.csv")
USERS_FILE = os.path.join(BASE_DIR, "users.csv")

# ------------------ ROLES ------------------
ROLES = {
    "Admin": ["read", "write", "delete", "manage_users", "view_logs"],
    "Manager": ["read", "write"],
    "User": ["read"],
    "Auditor": ["view_logs"]
}

# ------------------ INIT FILES ------------------
def init_files():
    if not os.path.exists(DATA_FILE):
        pd.DataFrame(columns=["id", "content", "created_by", "time"]).to_csv(DATA_FILE, index=False)

    if not os.path.exists(LOGS_FILE):
        pd.DataFrame(columns=["user", "role", "action", "time"]).to_csv(LOGS_FILE, index=False)

init_files()

# ------------------ LOGGING ------------------
def log_action(user, role, action):
    logs = pd.read_csv(LOGS_FILE)
    logs.loc[len(logs)] = {
        "user": user,
        "role": role,
        "action": action,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    logs.to_csv(LOGS_FILE, index=False)

# ------------------ SESSION STATE ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ------------------ TITLE ------------------
st.title("🔐 Role-Based Access Control System")

# ================== AUTH SECTION ==================
if not st.session_state.logged_in:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Secure RBAC Login")

    role = st.selectbox("Select Role", list(ROLES.keys()))

    if role == "Admin":
        choice = st.radio("Action", ["Login"])
        st.info("Admin signup is disabled")
    else:
        choice = st.radio("Action", ["Login", "Signup"])

    if choice == "Signup":
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Create Account"):
            ok, msg = signup_user(u, p, role)
            st.success(msg) if ok else st.error(msg)

    if choice == "Login":
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate_user(u, p, role):
                st.session_state.logged_in = True
                st.session_state.user = u
                st.session_state.role = role
                log_action(u, role, "Login")
                st.rerun()
            else:
                st.error("Invalid credentials or role")

    st.markdown('</div>', unsafe_allow_html=True)

# ================== DASHBOARD ==================
else:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader(f"👋 Welcome, {st.session_state.user}")
    st.markdown(f"**Role:** `{st.session_state.role}`")
    st.markdown('</div>', unsafe_allow_html=True)

    st.sidebar.success(f"{st.session_state.role} Dashboard")
    actions = ROLES[st.session_state.role] + ["logout"]
    action = st.sidebar.radio("Actions", actions)

    # -------- READ --------
    if action == "read":
        st.subheader("📄 Read Data")
        df = pd.read_csv(DATA_FILE)
        if df.empty:
            st.info("No data available")
        else:
            st.dataframe(df)
        log_action(st.session_state.user, st.session_state.role, "Read")

    # -------- WRITE --------
    elif action == "write":
        st.subheader("✍️ Write Data")
        content = st.text_area("Enter data")
        if st.button("Save"):
            if content.strip():
                df = pd.read_csv(DATA_FILE)
                df.loc[len(df)] = [
                    len(df) + 1,
                    content,
                    st.session_state.user,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ]
                df.to_csv(DATA_FILE, index=False)
                log_action(st.session_state.user, st.session_state.role, "Write")
                st.success("Data saved")
            else:
                st.warning("Data cannot be empty")

    # -------- DELETE --------
    elif action == "delete":
        st.subheader("🗑️ Delete Data")
        df = pd.read_csv(DATA_FILE)
        if df.empty:
            st.info("No data to delete")
        else:
            did = st.selectbox("Select ID", df["id"])
            if st.button("Delete"):
                df = df[df["id"] != did]
                df.to_csv(DATA_FILE, index=False)
                log_action(st.session_state.user, st.session_state.role, f"Delete {did}")
                st.success("Deleted")
                st.rerun()

    # -------- MANAGE USERS --------
    elif action == "manage_users":
        st.subheader("👑 Manage Users")
        st.dataframe(pd.read_csv(USERS_FILE))

    # -------- VIEW LOGS --------
    elif action == "view_logs":
        st.subheader("📜 Audit Logs")
        st.dataframe(pd.read_csv(LOGS_FILE))

    # -------- LOGOUT --------
    elif action == "logout":
        log_action(st.session_state.user, st.session_state.role, "Logout")
        st.session_state.clear()
        st.rerun()
