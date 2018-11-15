from app import db


class License(db.Model):
    machine_id = db.Column(db.String, primary_key=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)