# Flask LDAP Authentication Application

This project is a Flask web application that authenticates users against a local OpenLDAP server. It allows users to log in, browse users in read-only mode, and change their own passwords securely.

## Project Structure

```
flask-ldap-app
├── app
│   ├── __init__.py
│   ├── auth.py
│   ├── ldap_utils.py
│   ├── routes.py
│   ├── templates
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── users.html
│   │   └── change_password.html
│   └── static
│       └── style.css
├── config.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/flask-ldap-app.git
   cd flask-ldap-app
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Configure the application:**
   Edit the `config.py` file to set your OpenLDAP server details and secure connection settings.

5. **Run the application:**
   ```
   flask run
   ```

## Usage

- Navigate to `https://test.aispit.net` in your web browser.
- Use the login form to authenticate with your LDAP credentials.
- Once logged in, your username will be displayed in the upper right corner.
- You can browse the list of users in the LDAP directory.
- To change your password, navigate to the change password page.

## Dependencies

- Flask
- Flask-LDAP3-Login
- Any other necessary libraries listed in `requirements.txt`.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.