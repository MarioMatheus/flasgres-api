"""Add endereco relationship

Revision ID: 5e70c3d6b08e
Revises: 0f6a3e76ec28
Create Date: 2021-03-08 00:12:51.491284

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e70c3d6b08e'
down_revision = '0f6a3e76ec28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('endereco',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cep', sa.String(length=9), nullable=False),
    sa.Column('rua', sa.String(length=255), nullable=False),
    sa.Column('numero', sa.Integer(), nullable=False),
    sa.Column('complemento', sa.String(length=255), nullable=True),
    sa.Column('municipio', sa.String(length=255), nullable=True),
    sa.Column('estado', sa.String(length=255), nullable=True),
    sa.Column('pais', sa.String(length=255), nullable=True),
    sa.Column('usuario_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('endereco')
    # ### end Alembic commands ###
