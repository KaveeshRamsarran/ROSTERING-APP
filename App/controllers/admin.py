from App.models import Shift
from App.database import db
from datetime import datetime

# Schedule a shift
def schedule_shift(staff_id, admin_id, start_time, end_time):
    try:
        start = datetime.strptime(start_time, "%d/%m/%Y %H:%M")
        end = datetime.strptime(end_time, "%d/%m/%Y %H:%M")
    except Exception:
        return "Invalid date format. Use DD/MM/YYYY HH:MM."
    shift = Shift(staffID=staff_id, adminID=admin_id, start=start, end=end)
    db.session.add(shift)
    db.session.commit()
    return f"Scheduled shift for staff {staff_id} from {start_time} to {end_time}."
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
