from flask import Blueprint, request, redirect, url_for, flash, session, render_template
from flask_login import login_required, current_user
from ldap3 import Server, Connection, ALL, NTLM
from app.ldap_utils import change_user_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        server = Server('test.aispit.net', get_info=ALL)
        conn = Connection(server, user=username, password=password, authentication=NTLM)

        if conn.bind():
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('routes.index'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        # Use current_user.username instead of session['username']
        if change_user_password(current_user.username, new_password):
            flash('Password changed successfully!', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Failed to change password. Please try again.', 'danger')

    return render_template('change_password.html')