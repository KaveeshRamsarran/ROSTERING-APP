from App.models import Admin
from App.database import db

def createAdmin(username, password):
    # prevent duplicate usernames
    if Admin.query.filter_by(username=username).first():
        return None
    newAdmin = Admin(username=username, password=password)
    db.session.add(newAdmin)
    db.session.commit()
    return newAdmin

def get_all_admins():
    return Admin.query.all()

def get_all_admins_json():
    return [a.get_json() for a in Admin.query.all()]
