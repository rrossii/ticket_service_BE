from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
from flask_marshmallow import Marshmallow
# import requests
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:*sashros*@localhost:3306/ticket_shop"
Base = declarative_base()

db = SQLAlchemy(app)

ma = Marshmallow(app)


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

    def __init__(self, username, first_name, last_name, email, password, phone, user_status):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone = phone
        self.user_status = user_status


class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'username', 'first_name', 'last_name', 'email', 'password', 'phone', 'user_status')


user_schema = UserSchema()  # strict=True
users_schema = UserSchema(many=True)  # strict=True


@app.route('/user', methods=['POST'])
def create_user():
    username = request.json['username']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']
    phone = request.json['phone']
    user_status = request.json['user_status']

    new_user = User(username, first_name, last_name, email, password, phone, user_status)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()

    result = []

    for user in users:
        result.append({'user_id':user.user_id, 'username':user.username, 'first_name':user.first_name, 'last_name':user.last_name, 'email':user.email,
                       'password':user.password, 'phone':user.phone, "user_status":user.user_status})
    return jsonify(result)


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


#
# with app.app_context():
#     db.create_all()


@app.route("/", methods=['GET'])
def home():
    return "Hello Home!"


@app.route("/api/v1/hello-world-8")  # was /localhost:5000
def hello():
    return "<h2 style='color:green'>Hello World! 8</h2>"


if __name__ == "__main__":  # was with app.app.context()
    app.run(debug=True)
