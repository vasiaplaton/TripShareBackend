"""nullablr images

Revision ID: 1f6308df7d9b
Revises: abaeec5cfcd8
Create Date: 2024-05-29 11:42:26.381546

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f6308df7d9b'
down_revision: Union[str, None] = 'abaeec5cfcd8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('reviews', 'image_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('reviews', 'image_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
