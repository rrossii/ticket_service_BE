from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:*sashros*@localhost:5000/ticket_shop'  # change if doesnt work

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
    name = db.String(45)

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

@app.route("/", methods=['GET'])
def home():
    return "Hello Home!"

@app.route("/localhost:5000/api/v1/hello-world-8")
def hello():
    return "<h2 style='color:green'>Hello World! 8</h2>"

if __name__ == "__main__":
    app.run(debug=True)
