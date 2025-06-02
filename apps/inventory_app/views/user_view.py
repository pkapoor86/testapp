from flask import session

def display_login_result(user):
    if user:
        return f"Welcome, {user['username']}!"
    return "Login failed."
