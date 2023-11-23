from datetime import datetime, timedelta
from flask_mail import Mail, Message
from flask import render_template, flash, redirect, url_for, request, make_response
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app import app, db
from app.models import User, Event
from app.forms import LoginForm, RegistrationForm, EditProfileForm, ChangePasswordForm, ContactForm, CreateEventForm, EventFilterForm, EditEventForm

mail = Mail(app)

current_year = datetime.now().year

def admin_required_dashboard(func):
    """
    Декоратор, проверяющий, является ли текущий пользователь администратором.
    Если не админ, перенаправляет на главную страницу.
    """

    def admin_dashboard(*args, **kwargs):
        if not current_user.is_admin:
            flash('Доступ запрещен', 'error')
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return admin_dashboard

def admin_required_edit_event(func):
    """
    Декоратор, проверяющий, является ли текущий пользователь администратором.
    Если не админ, перенаправляет на главную страницу.
    """
    def edit_event(*args, **kwargs):
        if not current_user.is_admin:
            flash('Доступ запрещен', 'error')
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return edit_event

def admin_required_delete_event(func):
    """
    Декоратор, проверяющий, является ли текущий пользователь администратором.
    Если не админ, перенаправляет на главную страницу.
    """
    def delete_event(*args, **kwargs):
        if not current_user.is_admin:
            flash('Доступ запрещен', 'error')
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return delete_event

def admin_required_delete_user(func):
    """
    Декоратор, проверяющий, является ли текущий пользователь администратором.
    Если не админ, перенаправляет на главную страницу.
    """
    def delete_user(*args, **kwargs):
        if not current_user.is_admin:
            flash('Доступ запрещен', 'error')
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return delete_user

def set_cookie(response, name, value, days):
    expires = datetime.utcnow() + timedelta(days=days)
    response.set_cookie(name, value, expires=expires, secure=True, httponly=True, samesite='Strict')

def get_cookie(name):
    return request.cookies.get(name, "")

@app.route('/')
@app.route('/index')
def index():

    show_cookie_banner = get_cookie("cookies_accepted") != "true"

    events = Event.query.all()
    return render_template('index.html', title='Home', current_year=current_year, events=events, show_cookie_banner=show_cookie_banner)

@app.route('/about')
def about():
    return render_template('about.html', title='About Us', current_year=current_year)

@app.route('/contact', methods=['GET', 'POST'])
def contact():

    cookies_accepted = get_cookie("cookies_accepted") == "true"

    form = ContactForm()
    if form.validate_on_submit():
        msg = Message('Обратная связь - EventHub', sender=app.config['MAIL_USERNAME'], recipients=[form.email.data])
        msg.body = f'Имя: {form.name.data}\nEmail: {form.email.data}\nСообщение: {form.message.data}'
        mail.send(msg)
        
        flash('Ваше сообщение отправлено успешно!', 'info')
        return redirect(url_for('contact'))
    return render_template('contact.html', title='Contact Us', form=form, current_year=current_year, cookies_accepted=cookies_accepted)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверное имя пользователя или пароль', 'error')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('Вход выполнен успешно!', 'info')
        return redirect(url_for('index'))
    return render_template('login.html', title='Вход в аккаунт', form=form, current_year=current_year)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, вы зарегистрированы!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, current_year=current_year)

@app.route('/user')
@login_required
def user():
    return render_template('user.html', title='Личный кабинет', user=current_user, current_year=current_year)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Информация о профиле обновлена!', 'info')
        return redirect(url_for('user'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_profile.html', title='Редактировать профиль', form=form, current_year=current_year)

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Пароль изменен!', 'info')
            return redirect(url_for('user'))
        else:
            flash('Неверный текущий пароль', 'error')
    return render_template('change_password.html', title='Изменить пароль', form=form, current_year=current_year)

@app.route('/event_catalog', methods=['GET', 'POST'])
def event_catalog():
    form = EventFilterForm()
    if form.validate_on_submit():
        query = Event.query
        if form.title.data:
            query = query.filter(Event.title.ilike(f'%{form.title.data}%'))

        if form.date_time.data:
            query = query.filter(Event.date_time == str(form.date_time.data) + " 00:00:00.000000")

        if form.location.data:
            query = query.filter(Event.location.ilike(f'%{form.location.data}%'))

        events = query.all()
    else:
        events = Event.query.all()

    return render_template('event_catalog.html', title='Event Catalog', form=form, events=events, current_year=current_year)

@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = CreateEventForm()
    if form.validate_on_submit():
        photo = form.photo.data
        if photo:
            filename = secure_filename(photo.filename)
            photo_path = app.config['UPLOADS_DEFAULT_DEST']
            photo.save(f'{photo_path}/{filename}')
        else:
            filename = None

        new_event = Event(
            title=form.title.data,
            description=form.description.data,
            date_time=form.date_time.data,
            location=form.location.data,
            organizer_id=current_user.id,
            photo_filename=filename
        )
        db.session.add(new_event)
        db.session.commit()
        flash('Мероприятие успешно создано!', 'success')
        return redirect(url_for('index'))
    print(form.errors)
    return render_template('create_event.html', title='Создать мероприятие', form=form)

@app.route('/admin_dashboard')
@login_required
@admin_required_dashboard
def admin_dashboard():
    """
    Роут для дашборда, доступного только для админа.
    """
    # Пример: Получение статистики для дашборда
    total_users = User.query.count()
    admin_count = User.query.filter_by(is_admin=True).count()
    user_count = total_users - admin_count

    events = Event.query.all()
    users = User.query.all() 

    return render_template(
        'admin_dashboard.html',
        title='Admin Dashboard',
        current_year=current_year,
        total_users=total_users,
        admin_count=admin_count,
        user_count=user_count,
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

        # Если пользователь загружает новое изображение, обновите соответствующие поля
        photo = form.photo.data
        if photo:
            filename = secure_filename(photo.filename)
            photo_path = app.config['UPLOADS_DEFAULT_DEST']
            photo.save(f'{photo_path}/{filename}')
            event.photo_filename = filename

        db.session.commit()
        flash('Мероприятие успешно обновлено!', 'success')
        return redirect(url_for('admin_dashboard'))

    print(form.errors)

    return render_template('edit_event.html', title='Редактировать мероприятие', form=form, event=event, current_year=current_year)

@app.route('/delete_event', methods=['POST'])
@login_required
@admin_required_delete_event
def delete_event():
    event_id = request.form.get('event_id')
    event = Event.query.get(event_id)

    if event:
        # Удаляем мероприятие из базы данных
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
        # Удаляем пользователя из базы данных
        db.session.delete(user)
        db.session.commit()
        flash(f'Пользователь "{user.username}" успешно удален.', 'success')
    else:
        flash('Пользователь не найден.', 'danger')

    return redirect(url_for('admin_dashboard'))