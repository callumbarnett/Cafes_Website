from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, RadioField
from wtforms.fields.html5 import URLField
import os

app = Flask(__name__)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=True)
    has_wifi = db.Column(db.Boolean, nullable=True)
    has_sockets = db.Column(db.Boolean, nullable=True)
    can_take_calls = db.Column(db.Boolean, nullable=True)
    coffee_price = db.Column(db.String(250), nullable=True)


# ADD Cafe Form
class AddCafe(FlaskForm):
    name = StringField(u"Name of Cafe", validators=[DataRequired()])
    map_url = URLField(u"Copy and paste a link to the cafe on Maps", validators=[DataRequired()])
    img_url = URLField(u"A image link of the cafe", validators=[DataRequired()])
    location = StringField(u"Location of new cafe", validators=[DataRequired()])
    seats = StringField(u"Min number - Max number of seats", validators=[DataRequired()])
    has_toilet = RadioField("Are there toilets available?", choices=[(1, 'Yes'), (0, 'No')],
                            validators=[DataRequired()])
    has_wifi = RadioField("Is there WiFi available?", choices=[(1, 'Yes'), (0, 'No')], validators=[DataRequired()])
    has_sockets = RadioField("Are there sockets for charging?", choices=[(1, 'Yes'), (0, 'No')], validators=[DataRequired()])
    can_take_calls = RadioField("Is there mobile signal?", choices=[(1, 'Yes'), (0, 'No')], validators=[DataRequired()])
    coffee_price = StringField("How much is an Americano?", validators=[DataRequired()])
    submit = SubmitField(u"Add Cafe")


@app.route("/")
def home():
    all_cafes = db.session.query(Cafe).all()
    return render_template('index.html', cafes=all_cafes)


@app.route("/add", methods=['GET', 'POST'])
def add():
    add_cafe = AddCafe()
    if request.method == 'POST':
        if request.form['has_toilet'] == 1:
            toilet_bool = True
        else:
            toilet_bool = False
        if request.form['has_wifi'] == 1:
            wifi_bool = True
        else:
            wifi_bool = False
        if request.form['has_sockets'] == 1:
            sockets_bool = True
        else:
            sockets_bool = False
        if request.form['can_take_calls'] == 1:
            calls_bool = True
        else:
            calls_bool = False
        # Create Cafe
        new_cafe = Cafe(
            name=request.form['name'],
            map_url=request.form['map_url'],
            img_url=request.form['img_url'],
            location=request.form['location'],
            seats=request.form['seats'],
            has_toilet=toilet_bool,
            has_wifi=wifi_bool,
            has_sockets=sockets_bool,
            can_take_calls=calls_bool,
            coffee_price=request.form['coffee_price'])
        db.session.add(new_cafe)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('add.html', form=add_cafe)


@app.route('/delete')
def delete():
    cafe_id = request.args.get('id')
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
