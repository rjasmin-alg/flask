from flask import Blueprint, request, redirect, url_for, flash, session
from ldap3 import Server, Connection, ALL, NTLM
from app.ldap_utils import search_users, change_user_password

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
def change_password():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        new_password = request.form['new_password']
        if change_password(session['username'], new_password):
            flash('Password changed successfully!', 'success')
            return redirect(url_for('routes.index'))
        else:
            flash('Failed to change password. Please try again.', 'danger')

    return render_template('change_password.html')