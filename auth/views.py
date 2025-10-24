from flask import render_template, redirect, url_for, flash, request
from . import auth
from .forms import LoginForm, RegistrationForm
from models import User, db
from flask_login import login_user, logout_user, login_required, current_user

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('juegos'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data
        )
        user.password = form.password.data 
        
        db.session.add(user)
        db.session.commit()
        
        flash('¡Te has registrado exitosamente! Ahora puedes iniciar sesión.')
        return redirect(url_for('auth.login'))
        
    return render_template('registro.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('juegos'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() 
        
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('juegos')
            return redirect(next_page)
        else:
            flash('Email o contraseña incorrectos.')
            
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.')
    return redirect(url_for('juegos'))