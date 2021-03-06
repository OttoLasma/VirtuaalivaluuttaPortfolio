from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm
from application.portfolio.models import Portfolio


@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form=LoginForm())

    form = LoginForm(request.form)
    # mahdolliset validoinnit

    user = User.query.filter_by(
        username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form=form, error="No such username or password")

    login_user(user)
    return redirect(url_for("index"))


@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/auth/register", methods=["GET", "POST"])
def auth_register():
    if request.method == "GET":
        return render_template("auth/registerform.html", form=RegisterForm())

    form = RegisterForm(request.form)



    existingUser = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if existingUser:
        form.username.errors.append("The username has already taken")
        return render_template("auth/registerform.html", form=form)

    u = User(form.name.data, form.username.data, form.password.data)
    
    db.session().add(u)
    db.session().commit()

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form=form,
                               error="Käyttäjänimi tai salasana väärin")

    print("Käyttäjä " + user.name + " tunnistettiin")
    p = Portfolio(user.id, 0, 0, 0, 0)
    db.session().add(p)
    db.session().commit()
    login_user(user)
    return redirect(url_for("index"))