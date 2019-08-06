"""mare

Revision ID: b2f38d020927
Revises: 9f5b370042cd
Create Date: 2019-08-06 18:25:06.069316

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2f38d020927'
down_revision = '9f5b370042cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_models_name', table_name='models')
    op.drop_column('models', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('models', sa.Column('name', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.create_index('ix_models_name', 'models', ['name'], unique=False)
    # ### end Alembic commands ###
