import jwt

from lab6.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import cross_origin

from lab6.utils import *


def user_validation(phone, email, user_status, first_name, last_name):
    UserSchema.Meta.validate_phone(phone)
    UserSchema.Meta.validate_email(email)
    UserSchema.Meta.validate_user_status(user_status)
    UserSchema.Meta.validate_name(None, first_name, last_name)


def ticket_validation(price, category_id, quantity, status):
    TicketSchema.Meta.validate_price(price)
    TicketSchema.Meta.validate_category_id(category_id)
    TicketSchema.Meta.validate_quantity(quantity)
    TicketSchema.Meta.validate_status(status, quantity)


def purchase_validation(user_id, ticket_id, quantity, total_price, status):
    PurchaseSchema.Meta.validate_user_id(user_id)
    PurchaseSchema.Meta.validate_ticket_id(ticket_id)
    PurchaseSchema.Meta.validate_quantity(quantity)
    PurchaseSchema.Meta.validate_total_price(total_price)
    PurchaseSchema.Meta.validate_status(status)


def token_required(func):
    def decorated(*args, **kwargs):
        token = request.headers["Authorization"]

        if "Bearer b" in token:
            token = token.replace("Bearer b", '')
            token = token.replace("'", '')
        else:
            token = token.replace("Bearer ", '')

        if not token:
            return jsonify({"message": "Token is missing"}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = db.session.query(User).filter_by(email=data["email"]).one()

            if current_user.user_status != "admin":
                return jsonify({"message": "No access"}), 404
        except:
            return jsonify({"message": "Token is invalid"}), 401
        return func(*args, **kwargs)

    decorated.__name__ = func.__name__
    return decorated


def token_required_for_user_and_purchase_operations(func):
    def decorated(*args, **kwargs):
        token = request.headers["Authorization"]

        if "Bearer b" in token:
            token = token.replace("Bearer b", '')
            token = token.replace("'", '')
        else:
            token = token.replace("Bearer ", '')

        if not token:
            return jsonify({"message": "Token is missing"}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = db.session.query(User).filter_by(email=data["email"]).one()

            if current_user.user_id != int(kwargs["user_id"]):
                return jsonify({"message": "No access"}), 404
        except:
            return jsonify({"message": "Token is invalid"}), 401

        return func(*args, **kwargs)

    decorated.__name__ = func.__name__
    return decorated


@app.route('/user/login', methods=['POST'])
@cross_origin()
def login():
    # ======
    db.session.commit()
    # ======

    email = request.json.get("email", '')
    password = request.json.get("password", '')

    user = User.query.filter_by(email=email).first()

    if user:
        correct_password = check_password_hash(user.password, password)
        if correct_password:
            token = jwt.encode({"email": email, "user": user.username}, app.config['SECRET_KEY'])

            session["username"] = user.username

            return jsonify({"first_name": user.first_name, "last_name": user.last_name, "token": token.decode('UTF-8'),
                            "password": user.password, "phone": user.phone,
                            "username": user.username, "email": user.email, "user_status": user.user_status,
                            "user_id": user.user_id})
    return jsonify({"error": "Wrong credentials!"}), 401


@app.route('/user/logout', methods=['DELETE'])
def logout():
    username = request.json["username"]
    d = session
    if "username" in session and username in session[
        "username"]:  # якщо існує колонка юзернейм і в ній є наш користувач
        session.pop("username", None)
        return jsonify({"message": "You successfully logged out"}), 200
    else:
        return jsonify({"message": "You haven't been logged in"}), 404


@app.route('/user/register', methods=['POST'])
def create_user():
    username = request.json['username']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']
    phone = request.json['phone']
    user_status = request.json['user_status']

    user_status = user_status.lower()

    password_hashed = generate_password_hash(password)

    new_user = User(username, first_name, last_name, email, password_hashed, phone, user_status)

    user_by_email = User.query.filter_by(email=email).first()
    user_by_username = User.query.filter_by(username=username).first()
    if user_by_email is not None:
        return jsonify({"error": "User with this email already exists, try again"}), 404
    if user_by_username is not None:
        return jsonify({"error": "User with this username already exists, try again"}), 404
    if len(password) < 8:
        raise ValidationError("Password must be greater than or equal to 8")

    user_validation(phone, email, user_status, first_name, last_name)

    db.session.add(new_user)
    db.session.commit()

    res = user_schema.jsonify(new_user)
    res.headers.add('Access-Control-Allow-Origin', '*')
    res.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    res.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    res.headers.add('Access-Control-Allow-Credentials', True)
    return res


@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()

    result = []

    for user in users:
        result.append({'user_id': user.user_id, 'username': user.username, 'first_name': user.first_name,
                       'last_name': user.last_name, 'email': user.email,
                       'password': user.password, 'phone': user.phone, "user_status": user.user_status})
    return jsonify(result)


@app.route('/user/<user_id>', methods=['PUT'])
@token_required_for_user_and_purchase_operations
def update_user_info(user_id):
    user = User.query.get(user_id)

    if user is None:
        return "User not found", 404

    username = request.json['username']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    # password = request.json['password'] // відновити потім коли буде змога змінити пароль
    phone = request.json['phone']

    user.username = username
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    # user.password = generate_password_hash(password)
    user.phone = phone

    UserSchema.Meta.validate_phone(phone)
    UserSchema.Meta.validate_email(email)
    UserSchema.Meta.validate_name(None, first_name, last_name)

    db.session.commit()

    return user_schema.jsonify(user)


@app.route('/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)

    if user is None:
        return "User not found", 404

    return user_schema.jsonify(user)


@app.route('/user/<user_id>', methods=['DELETE'])
@token_required_for_user_and_purchase_operations
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return "User not found", 404

    db.session.delete(user)
    db.session.commit()

    return "Deleted successfully", 204


@app.route('/tickets', methods=['GET'])
def get_all_tickets():
    tickets = Ticket.query.all()

    result = []

    for ticket in tickets:
        result.append({'ticket_id': ticket.ticket_id, 'name': ticket.name, 'price': ticket.price,
                       'category_id': ticket.category_id, 'quantity': ticket.quantity,
                       'date': ticket.date, 'place': ticket.place, "status": ticket.status, "image": ticket.image, "info": ticket.info})

    return jsonify(result)


@app.route('/tickets', methods=['POST'])
@token_required
def create_ticket():
    name = request.json['name']
    price = request.json['price']
    category = request.json['category']
    quantity = request.json['quantity']
    date = request.json['date']
    place = request.json['place']
    info = request.json['info']
    image = "/images/" + request.json['imageName']

    category_id = category_name_to_id(category)

    new_ticket = Ticket(name, price, category_id, quantity, date, place, "available", info, image)

    ticket_validation(price, category_id, quantity, "available")

    db.session.add(new_ticket)
    db.session.commit()

    return ticket_schema.jsonify(new_ticket), 200


@app.route('/tickets/<ticket_id>', methods=['PUT'])
@token_required
def update_ticket_info(ticket_id):
    ticket = Ticket.query.get(ticket_id)

    if ticket is None:
        return jsonify({"message": "Ticket not found"}), 404

    name = request.json['updatedName']
    price = request.json['updatedPrice']
    category = request.json['updatedCategory']
    quantity = request.json['updatedQuantity']
    # date = request.json['updatedDate']
    place = request.json['updatedPlace']
    status = request.json['updatedStatus']
    info = request.json['updatedInfo']
    image = "/images/" + request.json['updatedImageName']

    category_id = category_name_to_id(category)

    if status == "sold out" and quantity > 0:
        return jsonify({"message": "There are more than 0 tickets, so status can't be sold out!"}), 404

    ticket.name = name
    ticket.price = price
    ticket.category_id = category_id
    ticket.quantity = quantity
    # ticket.date = date
    ticket.place = place
    ticket.status = status
    ticket.info = info
    ticket.image = image

    ticket_validation(price, category_id, quantity, status)

    db.session.commit()

    return ticket_schema.jsonify(ticket), 200


@app.route('/tickets/<ticket_id>', methods=['DELETE'])
@token_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)

    if ticket is None:
        return jsonify({"message": "Ticket not found"}), 404

    db.session.delete(ticket)
    db.session.commit()

    return "Deleted successfully", 204


@app.route('/tickets/<ticket_id>', methods=['GET'])
def get_ticket_by_id(ticket_id):
    ticket = Ticket.query.get(ticket_id)

    if ticket is None:
        return jsonify({"message": "Ticket not found"}), 404

    return ticket_schema.jsonify(ticket)


@app.route('/tickets/findByStatus', methods=['GET'])
def get_tickets_by_status():
    status = request.json['status']
    tickets = Ticket.query.filter_by(status=status)

    if not isinstance(status, str):
        return jsonify({"message": "Invalid status value"}), 400

    result = []

    for ticket in tickets:
        result.append({'ticket_id': ticket.ticket_id, 'name': ticket.name, 'price': ticket.price,
                       'category_id': ticket.category_id, 'quantity': ticket.quantity,
                       'date': ticket.date, 'place': ticket.place, "status": ticket.status, "image": ticket.image, "info": ticket.info})

    if len(result) == 0:
        return jsonify({"message": "Tickets not found"}), 404

    return jsonify(result), 200


@app.route('/tickets/findByCategory/<category_name>', methods=['GET'])
def get_tickets_by_category(category_name):
    # category_name = request.json['category']
    category_name = category_name.lower()

    if not isinstance(category_name, str):
        return jsonify({"message": "Invalid category value"}), 400

    category = db.session.query(Category).filter_by(name=category_name).one()
    categ_id = category.category_id

    if category is None:
        return jsonify({"message": "Category not found"}), 404

    tickets = Ticket.query.filter_by(category_id=categ_id)

    result = []

    for ticket in tickets:
        result.append({'ticket_id': ticket.ticket_id, 'name': ticket.name, 'price': ticket.price,
                       'category_id': ticket.category_id, 'quantity': ticket.quantity,
                       'date': ticket.date, 'place': ticket.place, "status": ticket.status, "image": ticket.image, "info": ticket.info})

    if len(result) == 0:
        return jsonify({"message": "Tickets not found"}), 404

    return jsonify(result), 200


@app.route('/tickets/findByDate', methods=['GET'])
def get_tickets_by_date():
    date = request.json['date']
    tickets = Ticket.query.filter_by(date=date)

    result = []

    for ticket in tickets:
        result.append({'ticket_id': ticket.ticket_id, 'name': ticket.name, 'price': ticket.price,
                       'category_id': ticket.category_id, 'quantity': ticket.quantity,
                       'date': ticket.date, 'place': ticket.place, "status": ticket.status, "image": ticket.image, "info": ticket.info})

    if len(result) == 0:
        return jsonify({"message": "Tickets not found"}), 404

    return jsonify(result), 200


@app.route('/tickets/buy/<ticket_id>', methods=['POST'])
def buy_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)

    if ticket is None:
        return jsonify({"message": "Ticket not found"}), 404

    ticket_price = db.session.query(Ticket).filter_by(ticket_id=ticket_id).one().price

    quantity = request.json['quantity']
    user_id = request.json['user_id']

    user = User.query.get(user_id)

    if user is None:
        return jsonify({"message": "User not found"}), 404
    if ticket.quantity == 0:
        ticket.status = 'sold out'
        return jsonify({"message": "These tickets are sold out"}), 404
    if ticket.quantity < quantity:
        return jsonify({"message": f"There are only {ticket.quantity} tickets"}), 404
    if ticket.quantity == 1:
        ticket.status = 'sold out'

    ticket.quantity -= int(quantity)

    purchase_user_id = user_id
    purchase_ticket_id = int(ticket_id)
    purchase_quantity = quantity
    purchase_total_price = ticket_price * quantity
    purchase_status = 'bought'

    purchase = Purchase(purchase_user_id, purchase_ticket_id, purchase_quantity, purchase_total_price, purchase_status)

    purchase_validation(purchase_user_id, purchase_ticket_id, purchase_quantity, purchase_total_price, purchase_status)

    db.session.add(purchase)
    db.session.commit()

    return purchase_schema.jsonify(purchase), 200


@app.route('/tickets/book/<ticket_id>', methods=['POST'])
def book_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)

    if ticket is None:
        return jsonify({"message": "Ticket not found"}), 404

    ticket_price = db.session.query(Ticket).filter_by(ticket_id=ticket_id).one().price

    quantity = request.json['quantity']
    user_id = request.json['user_id']

    user = User.query.get(user_id)

    if user is None:
        return jsonify({"message": "User not found"}), 404
    if isinstance(ticket_id, type(int)):
        return jsonify({"message": "Invalid ticket_id value"}), 400
    if isinstance(quantity, type(int)):
        return jsonify({"message": "Quantity value must be integer"}), 400
    if quantity < 0:
        return jsonify({"message": "Quantity value must be positive"}), 400
    if ticket.quantity == 0:
        ticket.status = 'sold out'
        return jsonify({"message": "These tickets are sold out"}), 404
    if ticket.quantity < quantity:
        return jsonify({"message": f"There are only {ticket.quantity} tickets"}), 404
    if ticket.quantity == 1:
        ticket.status = 'sold out'

    ticket.quantity -= int(quantity)

    purchase_user_id = user_id
    purchase_ticket_id = int(ticket_id)
    purchase_quantity = quantity
    purchase_total_price = ticket_price * quantity
    purchase_status = 'booked'

    purchase = Purchase(purchase_user_id, purchase_ticket_id, purchase_quantity, purchase_total_price, purchase_status)

    purchase_validation(purchase_user_id, purchase_ticket_id, purchase_quantity, purchase_total_price, purchase_status)

    db.session.add(purchase)
    db.session.commit()

    return purchase_schema.jsonify(purchase), 200


@app.route('/tickets/book/<purchase_id>/<user_id>', methods=['DELETE'])
def cancel_booking(purchase_id, user_id):
    booking = Purchase.query.get(purchase_id)

    if booking is None:
        return jsonify({"message": "Booking not found"}), 404

    if booking.user_id != int(user_id):
        return jsonify({"message": "You haven't booked this event"}), 404

    booking_status = db.session.query(Purchase).filter_by(purchase_id=purchase_id).one().status
    if booking_status == 'bought':
        return jsonify({"message": "This ticket is already bought, cannot cancel this purchase"}), 404

    ticket_id = db.session.query(Purchase).filter_by(purchase_id=purchase_id).one().ticket_id
    ticket = db.session.query(Ticket).filter_by(ticket_id=ticket_id).one()
    booking_quantity = db.session.query(Purchase).filter_by(purchase_id=purchase_id).one().quantity
    ticket.quantity += booking_quantity

    db.session.delete(booking)
    db.session.commit()

    return jsonify({"message": "Canceled successfully"}), 204


@app.route('/tickets/buy', methods=['GET'])
@token_required # only admins can see all purchases
def get_all_purchases():
    purchases = Purchase.query.all()

    result = []

    if purchases is None:
        return jsonify({"message": "Empty"}), 200

    for purchase in purchases:
        result.append({'purchase_id': purchase.purchase_id, 'ticket_id': purchase.ticket_id,
                       'quantity': purchase.quantity, "user_id": purchase.user_id,
                       'total_price': purchase.total_price, 'status': purchase.status})

    return jsonify(result)


@app.route('/tickets/user-purchase/<user_id>', methods=['GET'])
@token_required_for_user_and_purchase_operations
def get_purchases_by_user_id(user_id):
    purchases = Purchase.query.filter_by(user_id=user_id)

    result = []

    if purchases is None:
        return jsonify({"message": "Empty"}), 200

    for purchase in purchases:
        result.append({'purchase_id': purchase.purchase_id, 'ticket_id': purchase.ticket_id,
                       'quantity': purchase.quantity, "user_id": purchase.user_id,
                       'total_price': purchase.total_price, 'status': purchase.status})

    return jsonify(result)


#
if __name__ == "__main__":  # was with app.app.context()
    app.run(debug=True)
