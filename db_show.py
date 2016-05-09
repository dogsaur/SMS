#!flask/bin/python
from app import db, models

users = models.User.query.all()
print(users)

images = models.Image.query.all()
print(images)

products = models.Product.query.all()
print(products)

trades = models.TradeRecord.query.all()
print(trades)

suppliers = models.Supply.query.all()
print(suppliers)
