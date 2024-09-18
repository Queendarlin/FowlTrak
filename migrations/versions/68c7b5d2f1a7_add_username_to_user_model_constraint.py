"""Add username to user model constraint

Revision ID: 68c7b5d2f1a7
Revises: 83e5de9401ea
Create Date: 2024-09-07 20:35:57.282667
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = '68c7b5d2f1a7'
down_revision = '83e5de9401ea'
branch_labels = None
depends_on = None


def upgrade():
    # Get the connection to the database
    conn = op.get_bind()

    # Check if the 'username' column exists in the 'users' table
    check_column_query = text(
        "SELECT column_name FROM information_schema.columns WHERE table_name = :table_name AND column_name = :column_name"
    )
    result = conn.execute(check_column_query, {'table_name': 'users', 'column_name': 'username'})

    # If the 'username' column does not exist, add it
    if result.fetchone() is None:
        with op.batch_alter_table('users', schema=None) as batch_op:
            batch_op.add_column(sa.Column('username', sa.String(length=255), nullable=False))
            batch_op.create_unique_constraint('uq_users_username', ['username'])
    else:
        with op.batch_alter_table('users', schema=None) as batch_op:
            batch_op.create_unique_constraint('uq_users_username', ['username'])


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('uq_users_username', type_='unique')
        batch_op.drop_column('username')
