from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from werkzeug.security import generate_password_hash, check_password_hash




app = Flask(__name__)



class Base(DeclarativeBase):
    pass



app.config["SECRET_KEY"] = "mySecretKey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'       # your Gmail address
app.config['MAIL_PASSWORD'] = 'your_app_password'          # your Gmail app password
app.config['MAIL_USE_TLS'] = True




mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

def generate_token(email):
    return s.dumps(email, salt='email-confirm')

def verify_token(token, expiration=3600):
    try:
        return s.loads(token, salt='email-confirm', max_age=expiration)
    except:
        return None




db = SQLAlchemy(model_class=Base)
db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(Data, user_id)


class Data(UserMixin,db.Model):
    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    name:Mapped[str] = mapped_column(String(250),nullable=False)
    email:Mapped[str] = mapped_column(String(250),nullable=False,unique=True)
    password:Mapped[str] = mapped_column(String(250),nullable=False)

with app.app_context():
    db.create_all()


@app.route("/home")
@login_required
def home():
    return render_template('home.html',data=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('signup'))

@app.route("/",methods=["GET","POST"])
def signup():
    if request.method == "POST":
        user = db.session.execute(db.select(Data).where(Data.email == request.form['email'])).scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('signup'))

        hash_and_salted_password = generate_password_hash(
            request.form['password'],
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = Data(
            email=request.form['email'],
            name=request.form['name'],
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template('signup.html')


@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        password = request.form["password"]
        result = db.session.execute(db.select(Data).where(Data.email == request.form["email"]))
        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template("login.html")

@app.route("/forget-password",methods=["GET","POST"])
def forget_password():
    if request.method == 'POST':
        email = request.form['email']
        print(email)
        user = db.session.execute(db.select(Data).where(Data.email == email)).scalar()
        print(user)
        if user:
            print(email)
            token = generate_token(email)
            reset_url = url_for('reset_password', token=token, _external=True)
            msg = Message('Password Reset Link',
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[email])
            msg.body = f'Click the link to reset your password: {reset_url}'
            mail.send(msg)
            return render_template('message.html', message="Check your email for the password reset link.")
        else:
            print(email)
            flash("Email not found.")
            return redirect(url_for('forget_password'))
    return render_template('forgot.html')

@app.route('/reset-password/<token>', methods=['GET','POST'])
def reset_password(token):
    email = verify_token(token)
    user = db.session.execute(db.select(Data).where(Data.email == email)).scalar()
    # print(user)
    if not email:
        return render_template('message.html', message="Invalid or expired token.")
    if request.method == 'POST':
        password = request.form['password']
        confirm = request.form['confirm']
        print(password,confirm)
        if password.__eq__(confirm):
            print(password, confirm)
            hash_and_salted_password = generate_password_hash(
                password,
                method='pbkdf2:sha256',
                salt_length=8
            )
            user.password = hash_and_salted_password
            db.session.commit()
            return render_template('message.html', message="Password updated successfully.",sub_message="You can now log in using your new password.")
        else:
            return render_template('message.html', message="Password do not match",sub_message="Try Again")
    return render_template('reset-password.html', token=token)



if __name__ == "__main__":
    app.run(debug=True)
