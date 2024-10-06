# Criar as rotas do site
import os.path

from flask import render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename

from pyterest import app, bccrypt, database
from pyterest.forms import FormLogin, RegistrationForm, PictureForm
from pyterest.models import User, Picture


@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        user = User.query.filter_by(email=form_login.email.data).first()
        if user and bccrypt.check_password_hash(
            user.password.encode("utf-8"), form_login.password.data
        ):
            login_user(user, remember=True)
            return redirect(url_for("profile", id_user=user.id))
    return render_template("index.html", form=form_login)


@app.route("/criar-conta", methods=["GET", "POST"])
def criar_conta():
    form_criar_conta = RegistrationForm()
    if form_criar_conta.validate_on_submit():
        password = bccrypt.generate_password_hash(
            form_criar_conta.password.data
        ).decode("utf-8")
        user = User(
            username=form_criar_conta.username.data,
            password=password,
            email=form_criar_conta.email.data,
        )
        database.session.add(user)
        database.session.commit()
        login_user(user, remember=True)
        return redirect(url_for("profile", id_user=user.id))
    return render_template("criar_conta.html", form=form_criar_conta)


@app.route("/profile/<id_user>", methods=["GET", "POST"])
@login_required
def profile(id_user):
    if int(id_user) == current_user.id:
        pricture_form = PictureForm()
        if pricture_form.validate_on_submit():
            file_picture = pricture_form.picture.data
            sec_filename = secure_filename(file_picture.filename)
            path = os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                app.config["UPLOAD_FOLDER"],
                sec_filename,
            )
            file_picture.save(path)

            picture = Picture(image=sec_filename, id_user=current_user.id)
            database.session.add(picture)
            database.session.commit()
        return render_template("profile.html", user=current_user, form=pricture_form)
    else:
        user = User.query.get(int(id_user))
        return render_template("profile.html", user=user, form=None)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))


@app.route("/feed")
@login_required
def feed():
    pictures = Picture.query.order_by(Picture.date.desc()).all()
    return render_template("feed.html", pictures=pictures)
