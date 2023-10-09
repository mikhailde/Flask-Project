from datetime import datetime
from flask_mail import Mail, Message
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.models import User
from app.forms import LoginForm, RegistrationForm, EditProfileForm, ChangePasswordForm, ContactForm

mail = Mail(app)

current_year = datetime.now().year

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home', current_year=current_year)

@app.route('/about')
def about():
    return render_template('about.html', title='About Us', current_year=current_year)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Отправка почты
        msg = Message('Обратная связь - EventHub', sender=app.config['MAIL_USERNAME'], recipients=[form.email.data])
        msg.body = f'Имя: {form.name.data}\nEmail: {form.email.data}\nСообщение: {form.message.data}'
        mail.send(msg)
        
        flash('Ваше сообщение отправлено успешно!', 'info')
        return redirect(url_for('contact'))
    return render_template('contact.html', title='Contact Us', form=form, current_year=current_year)

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