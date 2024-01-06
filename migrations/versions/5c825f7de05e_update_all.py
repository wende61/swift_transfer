"""update all

Revision ID: 5c825f7de05e
Revises: 432d5361e9e5
Create Date: 2024-01-05 16:30:53.911693

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5c825f7de05e'
down_revision = '432d5361e9e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=500), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('customers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=False),
    sa.Column('customer_email', sa.String(length=255), nullable=False),
    sa.Column('address', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('swift_connect_request', schema=None) as batch_op:
        batch_op.drop_column('customer_name')
        batch_op.drop_column('customer_email')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('swift_connect_request', schema=None) as batch_op:
        batch_op.add_column(sa.Column('customer_email', mysql.VARCHAR(length=255), nullable=False))
        batch_op.add_column(sa.Column('customer_name', mysql.VARCHAR(length=255), nullable=False))

    op.drop_table('customers')
    op.drop_table('user')
    # ### end Alembic commands ###