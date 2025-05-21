from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app
from app.models import User
from ldap3 import Server, Connection, ALL

@app.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)

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