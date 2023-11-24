from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required_dashboard(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:
            flash('Доступ запрещен', 'error')
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return decorated_view


def admin_required_edit_event(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:
            flash('Доступ запрещен', 'error')
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return decorated_view


def admin_required_delete_event(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:
            flash('Доступ запрещен', 'error')
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return decorated_view


def admin_required_delete_user(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:
            flash('Доступ запрещен', 'error')
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return decorated_view
