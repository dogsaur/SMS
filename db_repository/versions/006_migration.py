from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
trade_record = Table('trade_record', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('product_id', Integer),
    Column('customer_id', Integer),
    Column('userid', Integer),
    Column('quantity', Integer),
    Column('total_price', Numeric),
    Column('time', DateTime),
)

product = Table('product', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('product_name', String),
    Column('category', String),
    Column('bar_code', Integer),
    Column('size', String),
    Column('inprice', Numeric),
    Column('price', Numeric),
    Column('supply', Integer),
    Column('picture_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['trade_record'].columns['quantity'].create()
    post_meta.tables['trade_record'].columns['total_price'].create()
    post_meta.tables['product'].columns['category'].create()
    post_meta.tables['product'].columns['inprice'].create()
    post_meta.tables['product'].columns['size'].create()
    post_meta.tables['product'].columns['supply'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['trade_record'].columns['quantity'].drop()
    post_meta.tables['trade_record'].columns['total_price'].drop()
    post_meta.tables['product'].columns['category'].drop()
    post_meta.tables['product'].columns['inprice'].drop()
    post_meta.tables['product'].columns['size'].drop()
    post_meta.tables['product'].columns['supply'].drop()
