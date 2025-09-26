from App.models import Admin, Staff, Shift
from App.database import db
from datetime import datetime

def createAdmin(name, password):
    newAdmin = Admin(name=name, password=password)
    db.session.add(newAdmin)
    db.session.commit()
    return newAdmin

def schedule(staffID, adminID, startStr, endStr):
    staffUser = Staff.query.get(staffID)
    if not staffUser:
        print("Invalid Staff ID")
        return None
    
    try:
        start = datetime.strptime(startStr, "%d/%m/%Y %H:%M")
        end = datetime.strptime(endStr, "%d/%m/%Y %H:%M")
    except ValueError:
        print("Invalid format. The proper format is (DD/MM/YYYY HH:MM)")
        return None
    
    scheduledShift = Shift(staffID=staffID, adminID=adminID, start=start, end=end)
    db.session.add(scheduledShift)
    db.session.commit()
    return scheduledShift

def listAdmins():
    admins = Admin.query.all()
    str = ""
    for admin in admins:
        str += f'User: {admin.id} - ID: {admin.name}\n'
    return str

def getAdmin(id):
    return db.session.get(Admin, id)

def deleteAdmin(id):
    admin = Admin.query.get(id)
    if not admin: return None
    db.session.delete(admin)
    db.session.commit()
