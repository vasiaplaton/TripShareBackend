"""removed

Revision ID: abaeec5cfcd8
Revises: 95b90c300951
Create Date: 2024-05-29 11:10:07.466729

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abaeec5cfcd8'
down_revision: Union[str, None] = '95b90c300951'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('trips', 'e_cigarettes_allowed')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trips', sa.Column('e_cigarettes_allowed', sa.BOOLEAN(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###