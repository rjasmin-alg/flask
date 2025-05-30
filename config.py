import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    LDAP_HOST = 'ldap://localhost:389'  # Replace with your LDAP server address
    LDAP_BASE_DN = 'dc=nodomain'
    LDAP_USER_DN = 'ou=users,' + LDAP_BASE_DN
    LDAP_BIND_DN = 'cn=admin,' + LDAP_BASE_DN
    LDAP_BIND_PASSWORD = os.environ.get('LDAP_BIND_PASSWORD') or 'your_bind_password_here'
    LDAP_PORT = 389  # Use 389 for non-SSL connections
    LDAP_USE_SSL = False  # Set to True for secure connections
    LDAP_USER_OBJECT_CLASS = 'inetOrgPerson'
    LDAP_USER_LOGIN_ATTRIBUTE = 'uid'  # Change as per your LDAP schema
    LDAP_USER_DISPLAY_NAME_ATTRIBUTE = 'cn'  # Change as per your LDAP schema