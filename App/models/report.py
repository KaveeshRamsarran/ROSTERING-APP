from App.database import db
from datetime import datetime

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    roster = db.Column(db.JSON, nullable=False)
    data = db.Column(db.JSON, nullable=False)

    def __init__(self, roster, data):
        self.timestamp = datetime.now()
        self.roster = roster
        self.data = data

    def get_json(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.strftime("%d/%m/%Y %H:%M"),
            'roster': self.roster,
            'data': self.data
        }
