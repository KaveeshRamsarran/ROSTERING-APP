from App.models import Staff
from App.database import db

def createStaff(username, password):
    # prevent duplicate usernames
    if Staff.query.filter_by(username=username).first():
        return None
    newStaff = Staff(username=username, password=password)
    db.session.add(newStaff)
    db.session.commit()
    return newStaff

def get_all_staff():
    return Staff.query.all()

def get_all_staff_json():
    return [s.get_json() for s in Staff.query.all()]
