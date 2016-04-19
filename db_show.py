#!flask/bin/python
from app import db, models

users = models.User.query.all()
print(users)
images = models.Image.query.all()
print(images)
