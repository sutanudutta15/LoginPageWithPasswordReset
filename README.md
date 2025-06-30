# 🔐 Flask Auth App — Signup, Login, Password Reset

A beginner-friendly Flask web application that allows users to:

- ✅ Register (Sign Up)
- ✅ Log In
- ✅ Reset their password securely via email


---

## ✨ Features

- 📝 User Registration (Signup)
- 🔐 User Login with validation
- 📧 Forgot Password via Email
- 🔑 Secure, time-limited reset tokens using `itsdangerous`
- 📬 Email integration using Gmail SMTP and Flask-Mail
- 💡 Simple, modular structure and templates for easy editing

---

## 🧰 Tech Stack

- Python
- Flask
- Flask-Mail
- itsdangerous
- HTML (Jinja templates)

---

## 📁 Folder Structure

project/
│
├── app.py # Main Flask application file
├── requirements.txt # Python dependencies
└── templates/ # HTML templates (Jinja2)
├── signup.html
├── login.html
├── forgot_password.html
├── reset_password.html
└── message.html


---

## 🚀 Getting Started

### 🔁 1. Clone the Repository

```bash
git clone https://github.com/your-username/flask-auth-app.git
cd flask-auth-app

🐍 2. Create Virtual Environment (optional)

python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows

📦 3. Install Dependencies

pip install -r requirements.txt
Or manually:

pip install flask flask-mail itsdangerous


📧 Email Configuration
This app uses Gmail SMTP to send password reset links.


🔐 Step 1: Generate Gmail App Password
Go to https://myaccount.google.com/apppasswords

Enable 2-Step Verification if not already enabled.

Generate an App Password for "Mail".

Use that password in your Flask app configuration.

✍️ Step 2: Set Email Config in app.py
Edit the following lines in app.py:

app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'
▶️ Run the App

python app.py

Visit http://localhost:5000 in your browser.