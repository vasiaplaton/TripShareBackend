"""initial migration

Revision ID: 4dbcaebf413a
Revises: 
Create Date: 2024-06-18 22:58:29.497586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4dbcaebf413a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('password_hash', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('surname', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('birthday', sa.String(), nullable=False),
    sa.Column('musicPreferences', sa.String(), nullable=True),
    sa.Column('info', sa.String(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('talkativeness', sa.Integer(), nullable=True),
    sa.Column('attitude_towards_smoking', sa.Integer(), nullable=True),
    sa.Column('attitude_towards_animals_during_the_trip', sa.Integer(), nullable=True),
    sa.Column('avatar_url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('cars',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('brand', sa.String(), nullable=False),
    sa.Column('model', sa.String(), nullable=False),
    sa.Column('color', sa.String(), nullable=False),
    sa.Column('year_of_manufacture', sa.Integer(), nullable=False),
    sa.Column('iamges_url', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('chats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id_1', sa.Integer(), nullable=False),
    sa.Column('user_id_2', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id_1'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id_2'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('writer_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['writer_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('chat_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['chats.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trips',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('max_passengers', sa.Integer(), nullable=False),
    sa.Column('cost_sum', sa.Integer(), nullable=False),
    sa.Column('max_two_passengers_in_the_back_seat', sa.Boolean(), nullable=False),
    sa.Column('smoking_allowed', sa.Boolean(), nullable=False),
    sa.Column('pets_allowed', sa.Boolean(), nullable=False),
    sa.Column('free_trunk', sa.Boolean(), nullable=False),
    sa.Column('status', sa.Enum('NEW', 'BRONED', 'FULLY_BRONNED', 'IN_PROGRESS', 'FINISHED', name='tripstatus'), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=False),
    sa.Column('driver_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['car_id'], ['cars.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['driver_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stops',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('place', sa.String(), nullable=False),
    sa.Column('place_name', sa.String(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=False),
    sa.Column('is_start', sa.Boolean(), nullable=False),
    sa.Column('is_stop', sa.Boolean(), nullable=False),
    sa.Column('num', sa.Integer(), nullable=False),
    sa.Column('trip_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['trip_id'], ['trips.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('request_datetime', sa.DateTime(), nullable=False),
    sa.Column('status', sa.Enum('CREATED', 'ACCEPTED', 'DECLINED', 'PAYED', 'FINISHED', 'ERROR', name='requeststatus'), nullable=False),
    sa.Column('status_change_datetime', sa.DateTime(), nullable=True),
    sa.Column('cost', sa.Integer(), nullable=False),
    sa.Column('number_of_seats', sa.Integer(), nullable=False),
    sa.Column('departure_id', sa.Integer(), nullable=False),
    sa.Column('arrival_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('trip_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['arrival_id'], ['stops.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['departure_id'], ['stops.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['trip_id'], ['trips.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('requests')
    op.drop_table('stops')
    op.drop_table('trips')
    op.drop_table('chat_messages')
    op.drop_table('reviews')
    op.drop_table('chats')
    op.drop_table('cars')
    op.drop_table('users')
    # ### end Alembic commands ###
