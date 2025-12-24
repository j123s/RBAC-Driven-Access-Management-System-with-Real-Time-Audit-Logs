import pandas as pd
import os
import bcrypt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "users.csv")

def init_users():
    if not os.path.exists(USERS_FILE):
        pd.DataFrame(columns=["username", "password_hash", "role"]).to_csv(USERS_FILE, index=False)

init_users()

def load_users():
    return pd.read_csv(USERS_FILE, dtype=str)

# Create default admin securely
def create_default_admin():
    users = load_users()
    if "admin" not in users["username"].values:
        hashed = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
        users.loc[len(users)] = ["admin", hashed, "Admin"]
        users.to_csv(USERS_FILE, index=False)

create_default_admin()

def signup_user(username, password, role):
    users = load_users()

    if role == "Admin":
        return False, "Admin signup disabled"

    if username in users["username"].values:
        return False, "User already exists"

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users.loc[len(users)] = [username, hashed, role]
    users.to_csv(USERS_FILE, index=False)

    return True, "Signup successful"

def authenticate_user(username, password, role):
    users = load_users()
    user = users[(users["username"] == username) & (users["role"] == role)]

    if user.empty:
        return False

    stored_hash = user.iloc[0]["password_hash"].encode()
    return bcrypt.checkpw(password.encode(), stored_hash)
