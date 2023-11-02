"""empty message

Revision ID: b8edda29d5d4
Revises: efce0b132925
Create Date: 2023-11-02 19:20:48.823080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8edda29d5d4'
down_revision = 'efce0b132925'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('review',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('review_text', sa.Text(), nullable=True),
    sa.Column('image', sa.LargeBinary(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('quest_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['quest_id'], ['quest.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_review_review_text'), ['review_text'], unique=False)

    with op.batch_alter_table('quest', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quest', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_review_review_text'))

    op.drop_table('review')
    # ### end Alembic commands ###
