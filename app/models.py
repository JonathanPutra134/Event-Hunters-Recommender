from app.db import db
from sqlalchemy import ARRAY
import uuid

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eventcreator_id = db.Column(db.Integer)
    category = db.Column(ARRAY(db.String(500)))
    preregister_date = db.Column(db.Date)
    endregister_date = db.Column(db.Date)
    startevent_date = db.Column(db.Date)
    endevent_date = db.Column(db.Date)
    created_at = db.Column(db.TIMESTAMP(timezone=True))
    updated_at = db.Column(db.TIMESTAMP(timezone=True))
    latitude = db.Column(db.String(255))
    longitude = db.Column(db.String(255))
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    is_online = db.Column(db.Boolean)
    tags = db.Column(ARRAY(db.String(20000)))
    featured_images = db.Column(ARRAY(db.String(20000)))
    guest_star = db.Column(ARRAY(db.String(20000)))
    location = db.Column(db.String(20000))

class EventsViews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    event_id = db.Column(db.Integer)
    view_date = db.Column(db.TIMESTAMP(timezone=True))

class EventsBookmarks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    event_id = db.Column(db.Integer)
    bookmark_date = db.Column(db.TIMESTAMP(timezone=True))

class Tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    event_id = db.Column(db.Integer)
    registered_date = db.Column(db.TIMESTAMP(timezone=True))


class Ratings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    event_id = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    rating_date = db.Column(db.TIMESTAMP(timezone=True))

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    longitude = db.Column(db.String(255))
    latitude = db.Column(db.String(255))

class Sessions(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4))
    user_id = db.Column(db.Integer)
    created_at = db.Column(db.TIMESTAMP(timezone=True))
    expiration = db.Column(db.TIMESTAMP(timezone=True))
