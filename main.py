from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, FloatField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.config["SQLALCHEMY_TRACK_MOODIFICATIONS"] = False
db = SQLAlchemy(app)


class AddForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    map_url = StringField("Map Link", validators=[DataRequired(), URL()])
    location = StringField("Location", validators=[DataRequired()])
    seats = SelectField("Number Of Seats", choices=["10+", "20+", "30+", "40+", "50+"], validators=[DataRequired()])
    has_toilet = BooleanField("Does It Have Toilet")
    has_wifi = BooleanField("Does it have Wi-fi")
    has_sockets = BooleanField("Does it have sockets")
    can_take_calls = BooleanField("Can you receive calls in there")
    coffee_price = FloatField("Price Of Coffee")
    submit = SubmitField("Submit")


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cafes")
def cafes():
    cafe_list = []
    header = ["Cafe Name", "Map Link", "Location", "Has Sockets", "Has Toilet", "Has Wifi", "Can Take Calls", "Seats", "Coffee Price"]
    all_cafes = db.session.query(Cafe).all()
    for i in all_cafes:
        i_list = [i.name, i.map_url, i.location, str(i.has_sockets), str(i.has_toilet), str(i.has_wifi), str(i.can_take_calls), i.seats, i.coffee_price]
        cafe_list.append(i_list)
    print(cafe_list)
    print(header)
    return render_template("cafes.html", cafe_list=cafe_list, header=header)


@app.route("/add", methods=["GET","POST"])
def add():
    form = AddForm()
    if form.validate_on_submit():
        if request.form.get("has_sockets") == "y" or request.form.get("has_toilet") == "y" or request.form.get("has_wifi") =="y" or request.form.get("can_take_calls"):
            i = True
        else:
            i = False
        new_cafe = Cafe(
            name=request.form.get("name"),
            location=request.form.get("location"),
            map_url=request.form.get("map_url"),
            img_url="",
            has_sockets=i,
            has_toilet=i,
            has_wifi=i,
            can_take_calls=i,
            seats=request.form.get("seats"),
            coffee_price=f"£{request.form.get('coffee_price')}"
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("cafes"))
    return render_template("add.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
