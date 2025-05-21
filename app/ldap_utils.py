from ldap3 import Server, Connection, ALL, NTLM, MODIFY_REPLACE

LDAP_SERVER = 'ldap://localhost:389'  # Replace with your LDAP server address
BASE_DN = 'dc=nodomain'  # Adjust according to your LDAP structure

def authenticate(username, password):
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user=f'uid={username},{BASE_DN}', password=password)
    if conn.bind():
        conn.unbind()
        return True
    return False

def search_users(filter='(objectClass=person)'):
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user='cn=admin,' + BASE_DN, password='admin_password')  # Use appropriate admin credentials
    if conn.bind():
        conn.search(BASE_DN, filter, attributes=['uid', 'cn', 'mail'])
        users = conn.entries
        conn.unbind()
        return users
    return []

def change_user_password(username, old_password, new_password):
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user=f'uid={username},{BASE_DN}', password=old_password)
    if conn.bind():
        conn.modify(f'uid={username},{BASE_DN}', {'userPassword': [(MODIFY_REPLACE, [new_password])]})
        conn.unbind()
        return True
    return False

def get_user_location(username):
    server = Server('test.aispit.net', get_info=ALL)
    conn = Connection(server, user=username, password='user_password', authentication=NTLM)  # You may need to adjust this
    if conn.bind():
        conn.search('dc=example,dc=com', f'(sAMAccountName={username})', attributes=['l'])
        if conn.entries:
            return conn.entries[0]['l'].value
    return None

def set_user_location(username, location):
    server = Server('test.aispit.net', get_info=ALL)
    conn = Connection(server, user=username, password='user_password', authentication=NTLM)  # You may need to adjust this
    if conn.bind():
        dn = f'CN={username},ou=users,dc=example,dc=com'  # Adjust DN as needed
        conn.modify(dn, {'l': [(MODIFY_REPLACE, [location])]})
        return conn.result['result'] == 0
    return False

def get_all_users():
    """
    Returns a list of all users in the LDAP directory.
    Each user is represented as a dictionary with 'uid', 'cn', and 'mail' attributes.
    """
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user='cn=admin,' + BASE_DN, password='admin_password')  # Use appropriate admin credentials
    users = []
    if conn.bind():
        conn.search(BASE_DN, '(objectClass=person)', attributes=['uid', 'cn', 'mail'])
        for entry in conn.entries:
            user = {
                'uid': str(entry.uid) if 'uid' in entry else None,
                'cn': str(entry.cn) if 'cn' in entry else None,
                'mail': str(entry.mail) if 'mail' in entry else None
            }
            users.append(user)
        conn.unbind()
    return users