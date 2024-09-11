"""Removed farm model and the relationships

Revision ID: d35433ca167c
Revises: 68c7b5d2f1a7
Create Date: 2024-09-11 04:39:29.278252

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd35433ca167c'
down_revision = '68c7b5d2f1a7'
branch_labels = None
depends_on = None


def upgrade():
    # Drop foreign keys and indexes from tables referencing 'farms'

    with op.batch_alter_table('flocks', schema=None) as batch_op:
        batch_op.drop_index('ix_flocks_farm_id')
        batch_op.drop_constraint('flocks_farm_id_fkey', type_='foreignkey')
        batch_op.drop_column('farm_id')

    with op.batch_alter_table('health_records', schema=None) as batch_op:
        batch_op.drop_index('ix_health_records_farm_id')
        batch_op.drop_constraint('health_records_farm_id_fkey', type_='foreignkey')
        batch_op.drop_column('farm_id')

    with op.batch_alter_table('inventory', schema=None) as batch_op:
        batch_op.drop_index('ix_inventory_farm_id')
        batch_op.drop_constraint('unique_inventory_entry', type_='unique')
        batch_op.create_unique_constraint('unique_inventory_entry', ['item_name', 'purchase_date'])
        batch_op.drop_constraint('inventory_farm_id_fkey', type_='foreignkey')
        batch_op.drop_column('farm_id')

    with op.batch_alter_table('production', schema=None) as batch_op:
        batch_op.drop_index('ix_production_farm_id')
        batch_op.drop_constraint('production_farm_id_fkey', type_='foreignkey')
        batch_op.drop_column('farm_id')

    # Drop the 'farms' table last
    with op.batch_alter_table('farms', schema=None) as batch_op:
        batch_op.drop_index('ix_farms_location')
        batch_op.drop_index('ix_farms_owner_id')

    op.drop_table('farms')


def downgrade():
    # Recreate the 'farms' table
    op.create_table('farms',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
                    sa.Column('location', sa.VARCHAR(length=200), nullable=False),
                    sa.Column('owner_id', sa.INTEGER(), nullable=False),
                    sa.Column('created_at', postgresql.TIMESTAMP(), nullable=False),
                    sa.Column('updated_at', postgresql.TIMESTAMP(), nullable=False),
                    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], name='farms_owner_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='farms_pkey')
                    )

    with op.batch_alter_table('farms', schema=None) as batch_op:
        batch_op.create_index('ix_farms_location', ['location'], unique=False)
        batch_op.create_index('ix_farms_owner_id', ['owner_id'], unique=False)

    # Re-add 'farm_id' column, constraints, and indexes to dependent tables

    with op.batch_alter_table('flocks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('farm_id', sa.INTEGER(), nullable=False))
        batch_op.create_foreign_key('flocks_farm_id_fkey', 'farms', ['farm_id'], ['id'])
        batch_op.create_index('ix_flocks_farm_id', ['farm_id'], unique=False)

    with op.batch_alter_table('health_records', schema=None) as batch_op:
        batch_op.add_column(sa.Column('farm_id', sa.INTEGER(), nullable=False))
        batch_op.create_foreign_key('health_records_farm_id_fkey', 'farms', ['farm_id'], ['id'])
        batch_op.create_index('ix_health_records_farm_id', ['farm_id'], unique=False)

    with op.batch_alter_table('inventory', schema=None) as batch_op:
        batch_op.add_column(sa.Column('farm_id', sa.INTEGER(), nullable=False))
        batch_op.create_foreign_key('inventory_farm_id_fkey', 'farms', ['farm_id'], ['id'])
        batch_op.drop_constraint('unique_inventory_entry', type_='unique')
        batch_op.create_unique_constraint('unique_inventory_entry', ['farm_id', 'item_name', 'purchase_date'])
        batch_op.create_index('ix_inventory_farm_id', ['farm_id'], unique=False)

    with op.batch_alter_table('production', schema=None) as batch_op:
        batch_op.add_column(sa.Column('farm_id', sa.INTEGER(), nullable=False))
        batch_op.create_foreign_key('production_farm_id_fkey', 'farms', ['farm_id'], ['id'])
        batch_op.create_index('ix_production_farm_id', ['farm_id'], unique=False)

