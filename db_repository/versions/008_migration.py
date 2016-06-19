from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
product = Table('product', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('product_name', String),
    Column('category', String),
    Column('bar_code', Integer),
    Column('size', String),
    Column('inprice', Numeric),
    Column('price', Numeric),
    Column('inventory', Integer),
    Column('supply_id', Integer),
    Column('picture_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['product'].columns['inventory'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['product'].columns['inventory'].drop()
