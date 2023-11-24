from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    TextAreaField,
    FileField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from wtforms.fields import DateField
from flask_wtf.file import FileRequired, FileAllowed
from datetime import datetime
from app.models import Event
from app import app


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')


class ContactForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Сообщение', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Отправить')


class EditProfileForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Сохранить изменения')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Текущий пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите новый пароль', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Изменить пароль')


class EventFilterForm(FlaskForm):
    title = StringField('Название мероприятия')
    date_time = DateField('Дата и время мероприятия', format='%Y-%m-%d', validators=[Optional()])
    location = StringField('Место проведения')
    submit = SubmitField('Фильтровать')


class CreateEventForm(FlaskForm):
    title = StringField('Название мероприятия', validators=[DataRequired()])
    description = TextAreaField('Описание мероприятия')
    date_time = DateField('Дата и время проведения', format='%Y-%m-%d', validators=[DataRequired()])
    location = StringField('Место проведения')
    photo = FileField('Загрузить фотографию', validators=[FileRequired(), FileAllowed(app.config['UPLOADS_ALLOW_EXTENSIONS'], 'Только изображения!')])
    submit = SubmitField('Создать мероприятие')

    def validate_date_time(self, field):
        if field.data <= datetime.now().date():
            raise ValidationError('Мероприятие должно быть запланировано на будущее.')

    def validate_description(self, field):
        max_length = 500
        if len(field.data) > max_length:
            raise ValidationError(f'Описание не должно превышать {max_length} символов.')

    def validate_title(self, field):
        if Event.query.filter_by(title=field.data).first():
            raise ValidationError('Мероприятие с таким названием уже существует. Выберите другое название.')


class EditEventForm(FlaskForm):
    title = StringField('Название мероприятия', validators=[Optional()])
    description = TextAreaField('Описание мероприятия', validators=[Optional()])
    date_time = DateField('Дата и время проведения', format='%Y-%m-%d', validators=[Optional()])
    location = StringField('Место проведения', validators=[Optional()])
    photo = FileField('Загрузить фотографию', validators=[Optional(), FileAllowed(app.config['UPLOADS_ALLOW_EXTENSIONS'], 'Только изображения!')])
    submit = SubmitField('Обновить мероприятие')
