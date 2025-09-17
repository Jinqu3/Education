"""create users table

Revision ID: 73c1d82b2d46
Revises: ee57158ea2a6
Create Date: 2025-09-18 00:25:05.601799

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "73c1d82b2d46"
down_revision: Union[str, Sequence[str], None] = "ee57158ea2a6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email",name= "unique_email_cnstr"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
