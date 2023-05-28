from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
from flask_marshmallow import Marshmallow
from marshmallow import validates, ValidationError
# import requests
import pymysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

pymysql.install_as_MySQLdb()


app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:*Sash_Ros*19@localhost:3306/ticket_shop"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:*Sash_Ros*19@localhost:3306/test_ticket_shop"
app.config['SECRET_KEY'] = "super-secret"
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
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    user_status = db.Column(db.Enum('admin', 'user'), nullable=False)

    def __init__(self, username, first_name, last_name, email, password, phone, user_status):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone = phone
        self.user_status = user_status

    # def __repr__(self):
    #     return f"<User {self.id} name = {self.first_name} last name = {self.last_name}>"


class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'username', 'first_name', 'last_name', 'email', 'password', 'phone', 'user_status')

        @validates("phone")
        def validate_phone(self):
            if len(self) != 10:
                raise ValidationError("Phone size must be 10")
            if not self.isnumeric():
                raise ValidationError("Phone number cannot contain letters")

        @validates("email")
        def validate_email(self):
            if '@' not in self and '.' not in self:
                raise ValidationError("Email must contain @ and dot")
            if '@' not in self:
                raise ValidationError("Email must contain @")
            if '.' not in self:
                raise ValidationError("Email must contain dot")

        @validates("user_status")
        def validate_user_status(self):
            if self not in ('user', 'admin'):
                raise ValidationError("Status must be 'user' either 'admin'")

        @validates("name")
        def validate_name(self, first_name, last_name):
            if not last_name.isalpha() and not first_name.isalpha():
                raise ValidationError("First and last name cannot contain numbers")
            if not first_name.isalpha():
                raise ValidationError("First name cannot contain numbers")
            if not last_name.isalpha():
                raise ValidationError("Last name cannot contain numbers")


user_schema = UserSchema()  # strict=True
users_schema = UserSchema(many=True)  # strict=True


class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))

    def __repr__(self):
        return f"<Category {self.name}>"

    # todo: think about __init__ later
    def __init__(self, name):
        self.name = name


class CategorySchema(ma.Schema):
    class Meta:
        fields = ('category_id', 'name')


category_schema = CategorySchema()


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
    info = db.Column(db.String(1500), nullable=False)
    image = db.Column(db.String(250), nullable=False)

    # commented this when the problem was with deleting ticket from database
    # def __repr__(self):
    #     return f"<{self.name} costs {self.price}, takes place in {self.place}. It is {self.status} on site>"

    def __init__(self, name, price, category_id, quantity, date, place, status, info, image):
        self.name = name
        self.price = price
        self.category_id = category_id
        self.quantity = quantity
        self.date = date
        self.place = place
        self.status = status
        self.info = info
        self.image = image


class TicketSchema(ma.Schema):
    class Meta:
        fields = ('name', 'price', 'category_id', 'quantity', 'date', 'place', 'status', 'info', 'image')

        @validates("price")
        def validate_price(self):
            if not isinstance(self, int):
                raise ValidationError("Price must be integer")

        @validates("category_id")
        def validate_category_id(self):
            if not isinstance(self, int):
                raise ValidationError("Category ID must be integer")

        @validates("quantity")
        def validate_quantity(self):
            if not isinstance(self, int):
                raise ValidationError("Quantity must be integer")

        @validates("status")
        def validate_status(self, *args):
            if self not in ('available', 'sold out'):
                raise ValidationError("Ticket status must be 'available' either 'sold out'")
            if self == 'sold out' and args[0] > 0:
                raise ValidationError(
                    f"Please change input data, ticket cannot have status 'sold out' with quantity {args[0]}")
            if self == 'available' and args[0] <= 0:
                raise ValidationError(
                    f"Please change input data, ticket cannot have status 'available' with quantity {args[0]}")


ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)


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

    def __init__(self, user_id, ticket_id, quantity, total_price, status):
        self.user_id = user_id
        self.ticket_id = ticket_id
        self.quantity = quantity
        self.total_price = total_price
        self.status = status


class PurchaseSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'ticket_id', 'quantity', 'total_price', 'status')

        @validates("ticket_id")
        def validate_ticket_id(self):
            if not isinstance(self, int):
                raise ValidationError("Ticket ID must be integer")

        @validates("user_id")
        def validate_user_id(self):
            if not isinstance(self, int):
                raise ValidationError("User ID must be integer")

        @validates("quantity")
        def validate_quantity(self):
            if not isinstance(self, int):
                raise ValidationError("Quantity must be integer")

        @validates("total_price")
        def validate_total_price(self):
            if not isinstance(self, int):
                raise ValidationError("Total price must be integer")

        @validates("status")
        def validate_status(self):
            if self not in ('bought', 'booked'):
                raise ValidationError("Purchase status must be 'booked' either 'bought'")


purchase_schema = PurchaseSchema()


# with app.app_context():
#     db.create_all()


if __name__ == "__main__":  # was with app.app.context()
    app.run(debug=True)
