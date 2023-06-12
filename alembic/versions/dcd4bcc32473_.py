"""empty message

Revision ID: a2405180edba
Revises: 83df682d7b1f
Create Date: 2022-11-06 18:42:30.701267

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

# revision identifiers, used by Alembic.
revision = 'a2405180edba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user',
        Column('user_id', Integer, primary_key=True, nullable=False),
        Column('username', String(45), unique=True, nullable=False),
        Column('first_name', String(45), nullable=False),
        Column('last_name', String(45), nullable=False),
        Column('email', String(45), unique=True, nullable=False),
        Column('password', String(255), nullable=False),
        Column('phone', String(20), nullable=False),
        Column('user_status', Enum("admin", "user")),
        PrimaryKeyConstraint('user_id'),
    )

    op.create_table(
        'category',
        Column('category_id', Integer, primary_key=True, nullable=False),
        Column('name', String(45), unique=True, nullable=False),
        PrimaryKeyConstraint('category_id'),
    )

    op.create_table(
        'ticket',
        Column('ticket_id', Integer, primary_key=True, nullable=False),
        Column('name', String(45), nullable=False),
        Column('price', Integer, nullable=False),
        Column('category_id', Integer, ForeignKey("category.category_id"), nullable=False),
        Column('quantity', Integer, nullable=False),
        Column('date', DateTime, nullable=False),
        Column('place', String(45), nullable=False),
        Column('status', Enum("available", "sold out")),
        Column('info', String(1500), nullable=False),
        Column('image', String(250), nullable=False),
        PrimaryKeyConstraint('ticket_id'),
        ForeignKeyConstraint(('category_id',), ('category.category_id',), ondelete='CASCADE')
    )

    op.create_table(
        'purchase',
        Column('purchase_id', Integer, primary_key=True, nullable=False),
        Column('ticket_id', Integer, ForeignKey("ticket.ticket_id"), nullable=False),
        Column('user_id', Integer, ForeignKey("user.user_id"), nullable=False),
        Column('quantity', Integer, nullable=False),
        Column('total_price', Integer, nullable=False),
        Column('status', Enum('bought', 'booked', 'canceled')),
        PrimaryKeyConstraint('purchase_id'),
        ForeignKeyConstraint(('ticket_id',), ['ticket.ticket_id'], ondelete='CASCADE'),
        ForeignKeyConstraint(('user_id',), ['user.user_id'], ondelete='CASCADE')
    )

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###