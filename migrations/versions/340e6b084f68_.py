"""empty message

Revision ID: 340e6b084f68
Revises: 60d5c27c4490
Create Date: 2020-03-04 17:29:02.491291

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '340e6b084f68'
down_revision = '60d5c27c4490'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vehicles', sa.Column('body_type', sa.String(length=80), nullable=True))
    op.create_index(op.f('ix_vehicles_body_type'), 'vehicles', ['body_type'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_vehicles_body_type'), table_name='vehicles')
    op.drop_column('vehicles', 'body_type')
    # ### end Alembic commands ###
