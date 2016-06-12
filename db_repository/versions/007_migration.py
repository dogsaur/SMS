from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
product = Table('product', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('product_name', VARCHAR),
    Column('bar_code', INTEGER),
    Column('price', NUMERIC),
    Column('picture_id', INTEGER),
    Column('category', VARCHAR),
    Column('inprice', NUMERIC),
    Column('size', VARCHAR),
    Column('supply', INTEGER),
)

product = Table('product', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('product_name', String),
    Column('category', String),
    Column('bar_code', Integer),
    Column('size', String),
    Column('inprice', Numeric),
    Column('price', Numeric),
    Column('supply_id', Integer),
    Column('picture_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['product'].columns['supply'].drop()
    post_meta.tables['product'].columns['supply_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['product'].columns['supply'].create()
    post_meta.tables['product'].columns['supply_id'].drop()
