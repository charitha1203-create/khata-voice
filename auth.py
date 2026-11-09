import json
import os
from datetime import date

USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")

DEFAULT_USERS = {
    "chari": {
        "shop_name": "Chari Kirana Store (శ్రీ లక్ష్మి కిరాణా)",
        "owner_name": "Chari",
        "pin": "1234",
        "language": "te",
        "created_at": str(date.today())
    }
}


def load_users():
    if not os.path.exists(USERS_FILE):
        save_users(DEFAULT_USERS)
        return dict(DEFAULT_USERS)
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return dict(DEFAULT_USERS)


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def register_user(username, shop_name, owner_name, pin, language="te"):
    users = load_users()
    key = username.strip().lower()
    if not key:
        return False, "Username cannot be empty."
    if key in users:
        return False, f"Account '{username}' already exists. Please login."
    if len(str(pin).strip()) < 4:
        return False, "PIN must be at least 4 digits."
        
    users[key] = {
        "shop_name": shop_name.strip() or f"{username}'s Shop",
        "owner_name": owner_name.strip() or username,
        "pin": str(pin).strip(),
        "language": language if language in ("te", "hi", "en") else "te",
        "created_at": str(date.today())
    }
    save_users(users)
    return True, f"Account created successfully for '{users[key]['shop_name']}'!"


def authenticate_user(username, pin):
    users = load_users()
    key = username.strip().lower()
    if key not in users:
        return False, None, "Account not found. Please sign up first."
    user = users[key]
    if user["pin"] != str(pin).strip():
        return False, None, "Incorrect PIN. Please try again."
    user_copy = dict(user)
    user_copy["username"] = key
    return True, user_copy, "Login successful!"


def update_language(username, language):
    users = load_users()
    key = username.strip().lower()
    if key in users and language in ("te", "hi", "en"):
        users[key]["language"] = language
        save_users(users)
        return True
    return False


if __name__ == "__main__":
    print("Testing auth...")
    ok, u, msg = authenticate_user("chari", "1234")
    print("Default login:", ok, u["shop_name"], u["language"])
    reg_ok, reg_msg = register_user("ravi_kirana", "Ravi General Stores", "Ravi", "5678", "hi")
    print("Register:", reg_ok, reg_msg)
    auth_ok, auth_u, auth_msg = authenticate_user("ravi_kirana", "5678")
    print("New login:", auth_ok, auth_u["language"])
