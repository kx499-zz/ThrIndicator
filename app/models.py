from app import db
import datetime
import re
from config import TTL_VALUES, DATA_TYPES, DIRECTIONS, VALIDATE, SOURCES


class Indicator(db.Model):
    __tablename__ = "indicator"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(64), index=True, nullable=False)
    data_type = db.Column(db.String(64), nullable=False)
    direction = db.Column(db.String(64), nullable=False)
    ttl = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    last = db.Column(db.DateTime, nullable=False, onupdate=datetime.datetime.utcnow)
    details = db.Column(db.Text())
    source = db.Column(db.String(64), nullable=False)
    __table_args__ = (db.UniqueConstraint("value", "data_type", "source"), )

    def __init__(self, value, ttl, data_type, source, direction='both', details='{}'):
        if not (ttl in TTL_VALUES and data_type in DATA_TYPES and direction in DIRECTIONS and source in SOURCES):
            raise Exception("Incorrect ttl, data_type, or direction")
        rex = VALIDATE.get(data_type)
        if rex and not re.search(rex, value):
            raise Exception("Value doesn't match data_type")
        self.value = value
        self.source = source
        self.direction = direction
        self.ttl = ttl
        self.data_type = data_type
        self.details = details
        self.created = datetime.datetime.utcnow()
        self.last = datetime.datetime.utcnow()


    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<Indicator %r: %r>' % (self.source, self.value)


