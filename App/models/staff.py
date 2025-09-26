from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from datetime import datetime

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    Shifts = db.relationship('Shift', backref="staff")
    
    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username' : self.username,
            'Shifts' : [shift.get_json() for shift in self.Shifts]
        }

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password, password)
