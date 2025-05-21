from flask import Flask
from flask_ldap3_login import AuthenticationResponse, LDAP3LoginManager
from ldap3 import Server, Connection
import os

app = Flask(__name__)

# Load configuration from environment variables or a config file
app.config['LDAP_HOST'] = os.getenv('LDAP_HOST', 'localhost')
app.config['LDAP_BASE_DN'] = os.getenv('LDAP_BASE_DN', 'dc=example,dc=com')
app.config['LDAP_USER_DN'] = os.getenv('LDAP_USER_DN', 'ou=users,dc=example,dc=com')
app.config['LDAP_BIND_DN'] = os.getenv('LDAP_BIND_DN', 'cn=admin,dc=example,dc=com')
app.config['LDAP_BIND_PASSWORD'] = os.getenv('LDAP_BIND_PASSWORD', 'your_password')
app.config['LDAP_USE_SSL'] = True

# Initialize LDAP manager
ldap_manager = LDAP3LoginManager(app)

#from app import routes, auth, ldap_utils

# Ensure the app is ready to run
if __name__ == '__main__':
    app.run(ssl_context='adhoc')