from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
supply = Table('supply', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', INTEGER),
    Column('city', VARCHAR),
    Column('buyer', VARCHAR),
    Column('order_contact', VARCHAR),
    Column('contact_information', VARCHAR),
)

supply = Table('supply', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', Integer),
    Column('city', String),
    Column('buyer', String),
    Column('order_contact', String),
    Column('tel', String),
    Column('address', String),
    Column('email', String),
    Column('manager', String),
    Column('payment_method', String),
    Column('bank_account', String),
    Column('evidence', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['supply'].columns['contact_information'].drop()
    post_meta.tables['supply'].columns['address'].create()
    post_meta.tables['supply'].columns['bank_account'].create()
    post_meta.tables['supply'].columns['email'].create()
    post_meta.tables['supply'].columns['evidence'].create()
    post_meta.tables['supply'].columns['manager'].create()
    post_meta.tables['supply'].columns['payment_method'].create()
    post_meta.tables['supply'].columns['tel'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['supply'].columns['contact_information'].create()
    post_meta.tables['supply'].columns['address'].drop()
    post_meta.tables['supply'].columns['bank_account'].drop()
    post_meta.tables['supply'].columns['email'].drop()
    post_meta.tables['supply'].columns['evidence'].drop()
    post_meta.tables['supply'].columns['manager'].drop()
    post_meta.tables['supply'].columns['payment_method'].drop()
    post_meta.tables['supply'].columns['tel'].drop()
