from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection

# revision identifiers, used by Alembic.
revision = '83e5de9401ea'
down_revision = 'b71b0d3c3ae7'
branch_labels = None
depends_on = None

def upgrade():
    # Check if the table already exists
    conn = op.get_bind()
    inspector = reflection.Inspector.from_engine(conn)
    tables = inspector.get_table_names()

    def upgrade():
        # Ensure the 'users' table is created correctly
        if not op.get_bind().has_table('users'):
            op.create_table('users',
                            sa.Column('username', sa.String(length=50), nullable=False),
                            sa.Column('email', sa.String(length=120), nullable=False),
                            sa.Column('password_hash', sa.String(length=128), nullable=False),
                            sa.Column('role', sa.Enum('WORKER', 'ADMIN', name='roleenum'), nullable=False),
                            sa.Column('id', sa.Integer(), nullable=False),
                            sa.Column('created_at', sa.DateTime(), nullable=False),
                            sa.Column('updated_at', sa.DateTime(), nullable=False),
                            sa.PrimaryKeyConstraint('id')
                            )
            with op.batch_alter_table('users', schema=None) as batch_op:
                batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=True)
                batch_op.create_index(batch_op.f('ix_users_role'), ['role'], unique=False)


def downgrade():
    # Drop the users table if it exists
    conn = op.get_bind()
    inspector = reflection.Inspector.from_engine(conn)
    tables = inspector.get_table_names()

    if 'users' in tables:
        with op.batch_alter_table('users', schema=None) as batch_op:
            batch_op.drop_index(batch_op.f('ix_users_role'))
            batch_op.drop_index(batch_op.f('ix_users_email'))

        op.drop_table('users')

    # Similarly for other tables...
