from flask import (render_template, redirect, url_for,
                   request, current_app)
from flask_login import current_user, login_user, logout_user

from app import login_manager
from . import auth_bp
from .forms import SignupForm, LoginForm
from .models import User


@auth_bp.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        user = User.get_by_email(email)
        if user is not None:
            error = f'Email {email} in use'
        else:
            user = User(name=name, email=email)
            user.set_password(password)
            user.save()
            # Log user
            login_user(user, remember=True)
            return redirect(url_for('public.index'))
    return render_template("auth/signup_form.html", form=form, error=error)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)

        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('public.index'))
        else:
            error = f'Invalid credentials'
            return render_template("auth/login_form.html", form=form, error=error)

    return render_template('auth/login_form.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))



@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))