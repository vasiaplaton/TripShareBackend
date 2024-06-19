"""fixed places

Revision ID: 34585d4a4cae
Revises: 68726f35873d
Create Date: 2024-06-19 14:22:54.381645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34585d4a4cae'
down_revision: Union[str, None] = '68726f35873d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('places', 'latitude_dd')
    op.add_column('places', sa.Column('latitude_dd', sa.Float(), nullable=False))

    op.drop_column('places', 'longitude_dd')
    op.add_column('places', sa.Column('longitude_dd', sa.Float(), nullable=False))


def downgrade() -> None:
    op.drop_column('places', 'latitude_dd')
    op.add_column('places', sa.Column('latitude_dd', sa.VARCHAR(), nullable=False))

    op.drop_column('places', 'longitude_dd')
    op.add_column('places', sa.Column('longitude_dd', sa.VARCHAR(), nullable=False))
