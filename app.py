from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

# SIGNUP
@app.post("/signup")
def signup_post():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    hashed = generate_password_hash(password)

    try:
        user = User(username=username, email=email, password=hashed)
        db.session.add(user)
        db.session.commit()
        return render_template("signup_success.html", username=username)
    except:
        return render_template("signup_error.html")

# LOGIN
@app.post("/login")
def login_post():
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        return render_template("login_error.html", message="User not found")

    if not check_password_hash(user.password, password):
        return render_template("login_error.html", message="Incorrect password")

    return render_template("login_success.html", username=user.username)




@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/hotel")
def hotel():
    return render_template("hotel.html")


@app.route("/tickets")
def tickets():
    return render_template("tickets.html")


@app.route("/purchase", methods=["POST"])
def purchase():
    ticket_type = request.form.get("ticket_type")

    prices = {
        "adult": 18,
        "child": 10,
        "family": 45
    }
    price = prices.get(ticket_type, 0)

    return render_template(
        "confirmation.html",
        ticket_type=ticket_type.capitalize(),
        price=price
    )

@app.route("/hotelpurchase", methods=["POST"])
def hotelpurchase():
    ticket_type = request.form.get("hotel_type")

    prices = {
        "single": 50,
        "twin": 80,
        "family": 120
    }
    price = prices.get(ticket_type, 0)

    return render_template(
        "hotelconfirmation.html",
        ticket_type=ticket_type.capitalize(),
        price=price
    )

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
