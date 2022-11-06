from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base

import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:*sashros*@localhost:3306/ticket_shop"
# Base = declarative_base()
# conn = pymysql.connect(db='ticket_shop', user='root', passwd='*sashros*', host='localhost')

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True, nullable=False)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(45), nullable=False)
    phone = db.Column(db.String(45), nullable=False)
    user_status = db.Column(db.Enum('admin', 'user'), nullable=False)

    def __repr__(self):
        return f"<User {self.id} name = {self.first_name} last name = {self.last_name}>"


class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))

    def __repr__(self):
        return f"<Category {self.name}>"


class Ticket(db.Model):
    __tablename__ = 'ticket'
    ticket_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    place = db.Column(db.String(45), nullable=False)
    status = db.Column(db.Enum('available', 'sold out'), nullable=False)

    def __repr__(self):
        return f"<{self.name} costs {self.price}, takes place in {self.place}. It is {self.status} on site>"


class Purchase(db.Model):
    __tablename__ = 'purchase'
    purchase_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.ticket_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('bought', 'booked', 'canceled'), nullable=False)

    def __repr__(self):
        return f"<User {self.user_id} {self.status} {self.quantity} ticket/s {self.ticket_id}. Final cost: {self.total_price}>"


with app.app_context():
    db.create_all()


@app.route("/", methods=['GET'])
def home():
    return "Hello Home!"


@app.route("/api/v1/hello-world-8") # was /localhost:5000
def hello():
    return "<h2 style='color:green'>Hello World! 8</h2>"


if __name__ == "__main__": # was with app.app.context()
    app.run(debug=True)
