from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

db = SQLAlchemy()


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100))
    status = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime())
    filename = db.Column(db.String(500))
    format = db.Column(db.String(50))

class TasksSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tasks
        include_relationships = True
        include_pk = True
        load_instance = True