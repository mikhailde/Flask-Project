from flask import render_template, flash, redirect, url_for, request
from flask_mail import Mail, Message
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from app import app, db
from app.models import Event
from app.forms import ContactForm, CreateEventForm, EventFilterForm
from app.utils import render_template_with_cookies, get_cookie, process_event_photo, current_year

mail = Mail(app)

@app.route('/')
@app.route('/index')
def index():
    show_cookie_banner = get_cookie("cookies_accepted") != "true"
    events = Event.query.all()
    return render_template_with_cookies('main/index.html', title='Home', current_year=current_year, events=events, show_cookie_banner=show_cookie_banner)

@app.route('/about')
def about():
    return render_template_with_cookies('main/about.html', title='About Us', current_year=current_year)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message('Обратная связь - EventHub', sender=app.config['MAIL_USERNAME'], recipients=[form.email.data])
        msg.body = f'Имя: {form.name.data}\nEmail: {form.email.data}\nСообщение: {form.message.data}'
        mail.send(msg)
        flash('Ваше сообщение отправлено успешно!', 'info')
        return redirect(url_for('contact'))
    return render_template_with_cookies('main/contact.html', title='Contact Us', form=form, current_year=current_year)

@app.route('/user')
@login_required
def user():
    return render_template_with_cookies('main/user.html', title='Личный кабинет', user=current_user, current_year=current_year)

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
    return render_template_with_cookies('main/event_catalog.html', title='Event Catalog', form=form, events=events, current_year=current_year)

@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = CreateEventForm()
    if form.validate_on_submit():
        filename = process_event_photo(form)
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
    return render_template_with_cookies('main/create_event.html', title='Создать мероприятие', form=form)
