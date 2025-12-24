"""initial_schema

Revision ID: 96c09015d01d
Revises:
Create Date: 2025-12-24 19:16:01.920042

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "96c09015d01d"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create test_calls table
    op.create_table(
        "test_calls",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("agent_id", sa.String(), nullable=False),
        sa.Column("driver_name", sa.String(), nullable=False),
        sa.Column("phone_number", sa.String(), nullable=False),
        sa.Column("load_number", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_test_calls_agent_id"), "test_calls", ["agent_id"], unique=False)

    # Create call_results table
    op.create_table(
        "call_results",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("call_id", sa.String(), nullable=False),
        sa.Column("transcript", sa.String(), nullable=False),
        sa.Column("structured_data", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["call_id"], ["test_calls.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("call_results")
    op.drop_index(op.f("ix_test_calls_agent_id"), table_name="test_calls")
    op.drop_table("test_calls")
