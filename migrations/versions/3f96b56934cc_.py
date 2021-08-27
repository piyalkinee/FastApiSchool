"""empty message

Revision ID: 3f96b56934cc
Revises: 6ade01631acc
Create Date: 2021-08-27 13:22:06.275921

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f96b56934cc'
down_revision = '6ade01631acc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('email', sa.String(length=256), nullable=True),
    sa.Column('password', sa.String(length=256), nullable=True),
    sa.Column('group', sa.String(length=256), nullable=True),
    sa.Column('time_of_creation', sa.DateTime(), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=True)
    op.create_table('courses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('time_of_creation', sa.DateTime(), nullable=True),
    sa.Column('user_creator_id', sa.Integer(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_creator_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_courses_id'), 'courses', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_courses_id'), table_name='courses')
    op.drop_table('courses')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###