from flask import Flask
from flask_ldap3_login import LDAP3LoginManager
from flask_login import LoginManager
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'supersecret')  # Needed for sessions

# LDAP config
app.config['LDAP_HOST'] = os.getenv('LDAP_HOST', 'localhost')
app.config['LDAP_BASE_DN'] = os.getenv('LDAP_BASE_DN', 'dc=nodomain')
app.config['LDAP_USER_DN'] = os.getenv('LDAP_USER_DN', 'ou=People')  # e.g., 'ou=People' or leave empty
app.config['LDAP_BIND_DN'] = os.getenv('LDAP_BIND_DN', 'cn=admin,dc=nodomain')
app.config['LDAP_BIND_PASSWORD'] = os.getenv('LDAP_BIND_PASSWORD', 'testtest')
app.config['LDAP_USE_SSL'] =  False

# Initialize LDAP manager
ldap_manager = LDAP3LoginManager(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

from app import routes
from app.auth import auth_bp

app.register_blueprint(auth_bp)

# Ensure the app is ready to run
if __name__ == '__main__':
    app.run(ssl_context='adhoc')