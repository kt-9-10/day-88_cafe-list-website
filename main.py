from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    has_sockets: Mapped[int] = mapped_column(Integer, nullable=False)
    has_toilet: Mapped[int] = mapped_column(Integer, nullable=False)
    has_wifi: Mapped[int] = mapped_column(Integer, nullable=False)
    can_take_calls: Mapped[int] = mapped_column(Integer, nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=False)


class AddForm(FlaskForm):
    name = StringField(label="The Cafe's name", name="name", validators=[DataRequired()])
    map_url = StringField(label='A URL for the google map', name="map_url", validators=[DataRequired()])
    img_url = StringField(label='A URL for the background image', name="img_url", validators=[DataRequired()])
    location = StringField(label='The location', name="location", validators=[DataRequired()])
    has_sockets = RadioField(label="Has the cafe sockets?", name="has_sockets", choices=[('1', 'Yes'), ('0', 'No')])
    has_toilet = RadioField(label="Has the cafe toilet?", name="has_toilet", choices=[('1', 'Yes'), ('0', 'No')])
    has_wifi = RadioField(label="Has the cafe wifi?", name="has_wifi", choices=[('1', 'Yes'), ('0', 'No')])
    can_take_calls = RadioField(label="Can the cafe take calls?", name="can_take_calls", choices=[('1', 'Yes'), ('0', 'No')])
    seats = StringField(label='Number of seats at the cafe', name="seats", validators=[DataRequired()])
    coffee_price = StringField(label="The Cafe's coffee price", name="coffee_price", validators=[DataRequired()])
    submit = SubmitField(label='SUBMIT POST')


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(Cafe)).scalars()
    cafes = result.all()
    for cafe in cafes:
        if cafe.has_wifi:
            cafe.has_wifi = "○"
        else:
            cafe.has_wifi = "×"
        if cafe.has_sockets:
            cafe.has_sockets = "○"
        else:
            cafe.has_sockets = "×"
        if cafe.has_toilet:
            cafe.has_toilet = "○"
        else:
            cafe.has_toilet = "×"
        if cafe.can_take_calls:
            cafe.can_take_calls = "○"
        else:
            cafe.can_take_calls = "×"
    return render_template("index.html", cafes=cafes)


@app.route('/delete/<cafe_id>')
def delete_cafe(cafe_id):
    cafe = db.get_or_404(Cafe, cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect('/')


@app.route('/new-cafe', methods=["GET", "POST"])
def add_new_cafe():
    if request.method == 'POST':
        add_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location"),
            has_sockets=request.form.get("has_sockets"),
            has_toilet=request.form.get("has_toilet"),
            has_wifi=request.form.get("has_wifi"),
            can_take_calls=request.form.get("can_take_calls"),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price")
        )
        with app.app_context():
            db.session.add(add_cafe)
            db.session.commit()
        return redirect('/')

    form = AddForm()
    return render_template("make-cafe.html", form=form)


if __name__ == "__main__":
    app.run(debug=True, port=5003)
