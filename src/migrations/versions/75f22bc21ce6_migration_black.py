"""migration_black

Revision ID: 75f22bc21ce6
Revises: ef8bf7718ca7
Create Date: 2024-11-06 23:44:56.946710

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "75f22bc21ce6"
down_revision: Union[str, None] = "ef8bf7718ca7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###