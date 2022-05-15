"""Added a users table

Revision ID: e3f9f7b828ae
Revises: 67d24fcb7077
Create Date: 2022-05-15 11:08:52.661078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3f9f7b828ae'
down_revision = '67d24fcb7077'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.String(length=255), nullable=False))
    op.add_column('users', sa.Column('password_hash', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('bio', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('profile_image_path', sa.String(length=255), nullable=True))
    op.drop_constraint('users_uname_key', 'users', type_='unique')
    op.create_unique_constraint(None, 'users', ['username'])
    op.drop_column('users', 'uname')
    op.drop_column('users', 'p_word')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('p_word', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('uname', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'users', type_='unique')
    op.create_unique_constraint('users_uname_key', 'users', ['uname'])
    op.drop_column('users', 'profile_image_path')
    op.drop_column('users', 'bio')
    op.drop_column('users', 'password_hash')
    op.drop_column('users', 'username')
    # ### end Alembic commands ###
