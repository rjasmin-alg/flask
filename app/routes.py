from flask import render_template, request, redirect, url_for, session, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app
from app.models import User
from ldap3 import Server, Connection, ALL
import requests

@app.route('/')
@login_required
def home():
    location = session.get('location')
    weather = None
    if location:
        try:
            # Get plain text weather from wttr.in
            resp = requests.get(f'https://wttr.in/{location}?format=3', timeout=3)
            if resp.status_code == 200:
                weather = resp.text
            else:
                weather = "Could not fetch weather."
        except Exception:
            weather = "Could not fetch weather."
    return render_template('home.html', user=current_user, weather=weather)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        ldap_host = app.config['LDAP_HOST']
        base_dn = app.config['LDAP_BASE_DN']
        user_dn = app.config['LDAP_USER_DN']
        use_ssl = app.config['LDAP_USE_SSL']

        # Build user_rdn robustly
        if user_dn:
            user_rdn = f"uid={username},{user_dn},{base_dn}"
        else:
            user_rdn = f"uid={username},{base_dn}"

        server = Server(ldap_host, use_ssl=use_ssl, get_info=ALL)
        try:
            conn = Connection(server, user=user_rdn, password=password, auto_bind=True)
            print(f"LDAP bind successful for {username}")
            user = User(user_rdn, username)
            login_user(user)
            return redirect(url_for('home'))
        except Exception as e:
            print(f"LDAP bind failed for {username}: {e}")
            flash('Invalid credentials or LDAP error.', 'danger')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/users')
@login_required
def list_users():
    # Extract the OU from the logged-in user's DN
    user_ou = None
    parts = current_user.dn.split(',')
    for part in parts:
        if part.strip().startswith('ou='):
            user_ou = part.strip()
            break
    users = User.list_users_in_ou(user_ou)
    return render_template('users.html', users=users)

@app.route('/change_location', methods=['GET', 'POST'])
@login_required
def change_location():
    if request.method == 'POST':
        location = request.form['location']
        session['location'] = location
        flash('Location updated!', 'success')
        return redirect(url_for('home'))
    return render_template('change_location.html')