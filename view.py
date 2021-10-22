from flask import Flask, render_template, request, abort, session
from flask_mail import Message, Mail
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import json

from werkzeug.utils import redirect

app = Flask(__name__)

app.config["SECRET_KEY"] = "bestzfamily"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "davidheroku05@gmail.com"
app.config["MAIL_PASSWORD"] = "surajbilly"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"]= True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root@localhost/flask_blog"
db = SQLAlchemy(app)
admin = Admin(app)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    location = db.Column(db.String(255))
    price = db.Column(db.Numeric(10,2))
    image = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    slug = db.Column(db.String(255))

class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)

admin.add_view(SecureModelView(Posts, db.session))

imgs = []

mail = Mail(app)

with open("products.txt", "r") as f:
    data = json.load(f)

@app.route("/")
def home():
    img_count = 0
    for house in data["Houses"]:
        imgs.append(house["image"])
    page = request.args.get('page', 1, type=int)
    posts = Posts.query.order_by(Posts.date_posted.desc()).paginate(page=page, per_page=6)
    return render_template("index.html", posts=posts, imgs=imgs, img_count=img_count)


@app.route("/contact/<string:slug>", methods=["GET", "POST"])
def house_contact(slug):
    try:
        ndora = "ndora"
        post = Posts.query.filter_by(slug=slug).one()
        if request.method == 'POST':
            name = request.form.get("name")
            tag = request.form.get("house-tag")
            email = request.form.get("email")
            phone = request.form.get("phone")
            message = request.form.get("message")
            msg = Message(subject=f"Mail from {name}", body=f"Name: {name}\nHouse-Tag: {tag}\nE-Mail: {email}\nPhone: {phone}\n\n\n{message}", sender="davidheroku05@gmail.com", recipients=["davidheroku05@gmail.com"])
            mail.send(msg)
            return redirect("/")
    except:
        abort(404)
    return render_template("contact.html", post=post, ndora=ndora)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")
        msg = Message(subject=f"Mail from {name}", body=f"Name: {name}\nE-Mail: {email}\nPhone: {phone}\n\n\n{message}", sender="davidheroku05@gmail.com", recipients=["davidheroku05@gmail.com"])
        mail.send(msg)
        return redirect("/")
    post = Posts.query.all()
    return render_template("contact.html", post=post)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/service")
def services():
    return render_template("services.html")

@app.route("/post/<string:slug>")
def post(slug):
    post = Posts.query.filter_by(slug=slug).one()
    return render_template("post.html", post=post)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")        
        if username == "Ndora" and password == "ndora@2021":
            session['logged_in'] = True
            return redirect("/admin")
        else:
            return render_template("login.html", failed=True)
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)