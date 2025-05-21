from flask_login import UserMixin
from flask import current_app
from ldap3 import Server, Connection, ALL

class User(UserMixin):
    def __init__(self, dn, username):
        self.id = username
        self.dn = dn
        self.username = username

    @staticmethod
    def get(user_id):
        ldap_host = current_app.config['LDAP_HOST']
        base_dn = current_app.config['LDAP_BASE_DN']
        user_dn = current_app.config['LDAP_USER_DN']
        bind_dn = current_app.config['LDAP_BIND_DN']
        bind_password = current_app.config['LDAP_BIND_PASSWORD']
        use_ssl = current_app.config['LDAP_USE_SSL']

        server = Server(ldap_host, use_ssl=use_ssl, get_info=ALL)
        conn = Connection(server, user=bind_dn, password=bind_password, auto_bind=True)

        # Build search base and user_rdn robustly
        if user_dn:
            search_base = f"{user_dn},{base_dn}"
            user_rdn = f"uid={user_id},{user_dn},{base_dn}"
        else:
            search_base = base_dn
            user_rdn = f"uid={user_id},{base_dn}"

        search_filter = f"(uid={user_id})"
        conn.search(search_base, search_filter, attributes=['uid'])
        if conn.entries:
            entry = conn.entries[0]
            dn = entry.entry_dn
            username = entry.uid.value
            return User(dn, username)
        return None

    @staticmethod
    def list_users_in_ou(ou=None):
        from flask import current_app
        ldap_host = current_app.config['LDAP_HOST']
        base_dn = current_app.config['LDAP_BASE_DN']
        user_dn = current_app.config['LDAP_USER_DN']
        bind_dn = current_app.config['LDAP_BIND_DN']
        bind_password = current_app.config['LDAP_BIND_PASSWORD']
        use_ssl = current_app.config['LDAP_USE_SSL']

        server = Server(ldap_host, use_ssl=use_ssl, get_info=ALL)
        conn = Connection(server, user=bind_dn, password=bind_password, auto_bind=True)

        # Use the user's OU or the default user_dn
        if ou:
            search_base = f"{ou},{base_dn}"
        elif user_dn:
            search_base = f"{user_dn},{base_dn}"
        else:
            search_base = base_dn

        search_filter = "(objectClass=person)"
        conn.search(search_base, search_filter, attributes=['uid', 'cn'])
        users = []
        for entry in conn.entries:
            users.append({
                'uid': entry.uid.value if 'uid' in entry else '',
                'cn': entry.cn.value if 'cn' in entry else ''
            })
        return users