from lab6.models import *


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
        result.append({'user_id': user.user_id, 'username': user.username, 'first_name': user.first_name,
                       'last_name': user.last_name, 'email': user.email,
                       'password': user.password, 'phone': user.phone, "user_status": user.user_status})
    return jsonify(result)


@app.route('/user/<user_id>', methods=['PUT'])
def update_user_info(user_id):
    user = User.query.get(user_id)

    if user is None:
        return "User not found", 404

    username = request.json['username']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']
    phone = request.json['phone']
    user_status = request.json['user_status']

    user.username = username
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.password = password
    user.phone = phone
    user.user_status = user_status

    db.session.commit()

    return user_schema.jsonify(user)


@app.route('/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)

    if user is None:
        return "User not found", 404

    return user_schema.jsonify(user)


@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return "User not found", 404
    db.session.delete(user)
    db.session.commit()
    return "Deleted successfully", 204


@app.route('/user/login', methods=['POST'])
def login():
    # TODO: in 8 lab
    pass


@app.route('/user/logout', methods=['DELETE'])
def logout():
    pass


@app.route('/tickets', methods=['GET'])
def get_all_tickets():
    tickets = Ticket.query.all()

    result = []

    for ticket in tickets:
        result.append({'ticket_id': ticket.ticket_id, 'name': ticket.name, 'price': ticket.price,
                       'category_id': ticket.category_id, 'quantity': ticket.quantity,
                       'date': ticket.date, 'place': ticket.place, "status": ticket.status})
    return jsonify(result)


@app.route('/ticket', methods=['POST'])
def create_ticket():
    name = request.json['name']
    price = request.json['price']
    category_id = request.json['category_id']
    quantity = request.json['quantity']
    date = request.json['date']
    place = request.json['place']
    status = request.json['status']

    new_ticket = Ticket(name, price, category_id, quantity, date, place, status)

    db.session.add(new_ticket)
    db.session.commit()

    return ticket_schema.jsonify(new_ticket), 200


@app.route('/ticket/<ticket_id>', methods=['PUT'])
def update_ticket_info(ticket_id):
    ticket = Ticket.query.get(ticket_id)

    if ticket is None:
        return jsonify({"message": "Ticket not found"}), 404

    name = request.json['name']
    price = request.json['price']
    category_id = request.json['category_id']
    quantity = request.json['quantity']
    date = request.json['date']
    place = request.json['place']
    status = request.json['status']

    ticket.name = name
    ticket.price = price
    ticket.category_id = category_id
    ticket.quantity = quantity
    ticket.date = date
    ticket.place = place
    ticket.status = status

    db.session.commit()

    return ticket_schema.jsonify(ticket), 200


@app.route('/ticket/<ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)

    if ticket is None:
        return jsonify({"message": "Ticket not found"}), 404

    db.session.delete(ticket)
    db.session.commit()

    return "Deleted successfully", 204


if __name__ == "__main__":  # was with app.app.context()
    app.run(debug=True)
