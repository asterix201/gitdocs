from flask import Blueprint, session, current_app, flash, redirect, url_for, g
from functools import wraps

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates',
                    static_folder='static')

from . import routes


AUTH_TOKEN = ''
AUTH_STATE_KEY = ''


def is_logged_in():
    if current_app.config.get('LOGIN_DISABLED'):
        return True
    return True if 'AUTH_TOKEN' in session else False


def login_required(func):
    @wraps(func)
    def wrapper_login_required(*args, **kwargs):
        if current_app.config.get('LOGIN_DISABLED'):
            return func(*args, **kwargs)
        elif not is_logged_in():
        # elif not g.is_authenticated:
            flash('You are not currently logged in.')
            return redirect(url_for('auth_bp.login'))
        return func(*args, **kwargs)
    return wrapper_login_required
