"""added pays date

Revision ID: efdf0a80493e
Revises: 959b09f500da
Create Date: 2024-06-19 15:38:24.804407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'efdf0a80493e'
down_revision: Union[str, None] = '959b09f500da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pay', sa.Column('datetime_cr', sa.DateTime(), nullable=False))
    op.add_column('pay', sa.Column('datetime_fn', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pay', 'datetime_fn')
    op.drop_column('pay', 'datetime_cr')
    # ### end Alembic commands ###