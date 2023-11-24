from flask import flash, redirect, url_for, request
from flask_login import login_required
from app import app, db
from app.models import User, Event
from app.forms import EditEventForm
from app.utils import render_template_with_cookies, process_event_photo, current_year

from app.decorators import (
    admin_required_dashboard, admin_required_edit_event,
    admin_required_delete_event, admin_required_delete_user
)

@app.route('/admin_dashboard')
@login_required
@admin_required_dashboard
def admin_dashboard():
    total_users = User.query.count()
    events = Event.query.all()
    users = User.query.all()
    return render_template_with_cookies(
        'admin/admin_dashboard.html',
        title='Admin Dashboard',
        current_year=current_year,
        total_users=total_users,
        events=events,
        users=users
    )

@app.route('/edit_event/<event_id>', methods=['GET', 'POST'])
@login_required
@admin_required_edit_event
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = EditEventForm(obj=event)

    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.date_time = form.date_time.data
        event.location = form.location.data
        filename = process_event_photo(form)
        if filename:
            event.photo_filename = filename
        db.session.commit()
        flash('Мероприятие успешно обновлено!', 'success')
        return redirect(url_for('admin_dashboard'))

    print(form.errors)
    return render_template_with_cookies(
        'admin/edit_event.html',
        title='Редактировать мероприятие',
        form=form,
        event=event,
        current_year=current_year
    )

@app.route('/delete_event', methods=['POST'])
@login_required
@admin_required_delete_event
def delete_event():
    event_id = request.form.get('event_id')
    event = Event.query.get(event_id)

    if event:
        db.session.delete(event)
        db.session.commit()
        flash(f'Мероприятие "{event.title}" успешно удалено.', 'success')
    else:
        flash('Мероприятие не найдено.', 'danger')

    return redirect(url_for('admin_dashboard'))

@app.route('/delete_user', methods=['POST'])
@login_required
@admin_required_delete_user
def delete_user():
    user_id = request.form.get('user_id')
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f'Пользователь "{user.username}" успешно удален.', 'success')
    else:
        flash('Пользователь не найден.', 'danger')

    return redirect(url_for('admin_dashboard'))
