"""
decorators.py

Decorators for URL handlers

"""

import logging
from functools import wraps
from google.appengine.api import users
from flask import redirect, request, abort
from application import app


def login_required_user(func):
    """Allows only selected users"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not users.get_current_user():
            return redirect(users.create_login_url(request.url))
        if users.get_current_user().email() not in app.config["ADMIN_EMAILS"]:
            logging.warning("Email " + users.get_current_user().email() + " not allowed in Admin")
            abort(404)
        return func(*args, **kwargs)
    return decorated_view


def login_required(func):
    """Requires standard login credentials"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not users.get_current_user():
            return redirect(users.create_login_url(request.url))
        return func(*args, **kwargs)
    return decorated_view


def admin_required(func):
    """Requires App Engine admin credentials"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if users.get_current_user():
            if not users.is_current_user_admin():
                abort(401)  # Unauthorized
            return func(*args, **kwargs)
        return redirect(users.create_login_url(request.url))
    return decorated_view
