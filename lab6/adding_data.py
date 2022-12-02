from models import db, app, User, Ticket, Category, Purchase
from flask_sqlalchemy.session import Session
from werkzeug.security import generate_password_hash

import pymysql
pymysql.install_as_MySQLdb()

session = Session(db)

with app.app_context():
    admin = User(username='admin1', first_name='Rosana', last_name='Klym', email='annros2003@gmail.com',
                 password=generate_password_hash('12345'), phone='0984337438', user_status='admin')

    user1 = User(username='user1', first_name='John', last_name='Smith', email='jo@gmail.com',
                 password=generate_password_hash('1234567'), phone='0986756432', user_status='user')
    user2 = User(username='user2', first_name='Monica', last_name='Bale', email='moni@gmail.com',
                 password=generate_password_hash('12**1'), phone='0965656832', user_status='user')
    user3 = User(username='user3', first_name='Tom', last_name='Hanks', email='tommy@mail.com',
                 password=generate_password_hash('helloworld'), phone='0936756832', user_status='user')

    db.session.add(admin)
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()

    category1 = Category(name='theater')
    category2 = Category(name='festival')
    category3 = Category(name='sport')
    category4 = Category(name='concert')

    db.session.add(category1)
    db.session.add(category2)
    db.session.add(category3)
    db.session.add(category4)
    db.session.commit()

    ticket1 = Ticket(name='Coachella', price=2000, category_id=category2.category_id, quantity=5000, date='2023-04-19',
                     place='California', status='available')
    ticket2 = Ticket(name='Zahid Fest', price=1000, category_id=category2.category_id, quantity=4000, date='2023-08-23',
                     place='Lvivska oblast', status='available')
    ticket3 = Ticket(name='Don Kihot', price=600, category_id=category1.category_id, quantity=500, date='2023-11-29',
                     place='Opera theater', status='available')

    db.session.add(ticket1)
    db.session.add(ticket2)
    db.session.add(ticket3)
    db.session.commit()

    purchase1 = Purchase(user_id=user3.user_id, ticket_id=ticket3.ticket_id, quantity=2, total_price=1200, status='bought')
    purchase2 = Purchase(user_id=user2.user_id, ticket_id=ticket1.ticket_id, quantity=1, total_price=2000, status='booked')
    purchase3 = Purchase(user_id=user3.user_id, ticket_id=ticket2.ticket_id, quantity=2, total_price=2000, status='bought')
    purchase4 = Purchase(user_id=user1.user_id, ticket_id=ticket3.ticket_id, quantity=1, total_price=600, status='bought')
    purchase5 = Purchase(user_id=user2.user_id, ticket_id=ticket1.ticket_id, quantity=3, total_price=6000, status='booked')

    db.session.add(purchase1)
    db.session.add(purchase2)
    db.session.add(purchase3)
    db.session.add(purchase4)
    db.session.add(purchase5)
    db.session.commit()
