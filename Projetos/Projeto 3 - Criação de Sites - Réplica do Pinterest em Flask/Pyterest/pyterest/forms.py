# Criar os formulários do site
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from pyterest import bccrypt
from pyterest.models import User


class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    confirmation_button = SubmitField("Fazer Login")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("Usuário inexistente, crie uma conta.")

    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not bccrypt.check_password_hash(user.password, password.data):
            raise ValidationError(
                "Senha inválida! Por favor, verifique a senha e tente novamente."
            )


class RegistrationForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Nome do usuário", validators=[DataRequired()])
    password = PasswordField(
        "Senha", validators=[DataRequired(), Length(min=6, max=20)]
    )
    confirmation_pass = PasswordField(
        "Confirmar a Senha",
        validators=[
            DataRequired(),
            EqualTo("password", message="As senhas precisam ser iguais."),
        ],
    )
    confirmation_button = SubmitField("Criar Conta")

    def validate_email(self, email):
        usuario = User.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail já cadastrado! Faça login para continuar.")

    def validate_password(self, password):
        user_password = User.query.filter_by(password=password.data).first()
        if user_password == "" or len(password.data) < 6:
            raise ValidationError(
                "Senha inválida! Por favor, verifique a senha e tente novamente."
            )


class PictureForm(FlaskForm):
    picture = FileField("Foto", validators=[DataRequired()])
    confirmation_button = SubmitField("Enviar")
