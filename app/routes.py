from flask import render_template, redirect, url_for, request, flash, session
from app.auth import login, logout, change_password
from app.ldap_utils import get_all_users
from flask_login import login_required, current_user

@app.route('/')
@login_required
def index():
    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_user(username, password):
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check your credentials.', 'danger')
    return render_template('login.html')

@app.route('/users')
@login_required
def users():
    user_list = get_all_users()
    return render_template('users.html', users=user_list)

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        if change_user_password(current_user.username, new_password):
            flash('Password changed successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Failed to change password.', 'danger')
    return render_template('change_password.html')