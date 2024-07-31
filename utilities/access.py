from functools import wraps
from flask import session, request, current_app, redirect, url_for


def login_req(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" in session:
            return func(*args, **kwargs)
        return redirect(url_for("bp_auto.auto"))
    return wrapper


def group_req(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" in session:
            user_group = session.get("user_group")
            if user_group:
                access = current_app.config["access_config"]
                user_target = request.blueprint
                if user_group in access and user_target in access[user_group]:
                    return func(*args, **kwargs)
                return "Доступа нет"
        return redirect(url_for("bp_auto.auto"))
    return wrapper
