"""create fuzzystrmatch extension

Revision ID: 5ba64bcb5473
Revises: 34585d4a4cae
Create Date: 2024-06-19 14:34:38.030314

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ba64bcb5473'
down_revision: Union[str, None] = '34585d4a4cae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('CREATE EXTENSION IF NOT EXISTS fuzzystrmatch')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('DROP EXTENSION IF EXISTS fuzzystrmatch')
    # ### end Alembic commands ###
