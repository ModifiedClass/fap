from flask_mongoengine import MongoEngine
import datetime


db = MongoEngine()

class Base(db.Document):
    meta = {
        'abstract': True,
    }
    create_time = db.DateTimeField(default=datetime.datetime.utcnow)
    status = db.IntField(default=1)
    remark = db.StringField()
