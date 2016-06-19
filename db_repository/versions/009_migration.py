from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
stock_record = Table('stock_record', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('product_id', Integer),
    Column('supply_id', Integer),
    Column('quantity', Integer),
    Column('inprice', Numeric),
    Column('time', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['stock_record'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['stock_record'].drop()
