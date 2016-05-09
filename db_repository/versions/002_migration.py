from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
suppliers = Table('suppliers', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('suppliers_name', Integer),
    Column('city', String),
    Column('buyer', String),
    Column('order_contact', String),
    Column('contact_information', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['suppliers'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['suppliers'].drop()
