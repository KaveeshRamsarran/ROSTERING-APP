from App.models import Staff, Shift
from App.database import db
from datetime import datetime

def createStaff(name, password):
    newStaff = Staff(name=name, password=password)
    db.session.add(newStaff)
    db.session.commit()
    return newStaff

def clockInOut(shiftID, type, time=None):
    shift = Shift.query.get(shiftID)
    if not shift:
        return "Invalid Shift ID"
    
    if not time:
        time = datetime.now()

    if type == "in":
        if shift.clockIn:
            return "Already clocked in"
        shift.clockIn = time
    elif type == "out":
        if shift.clockOut:
            return "Already clocked out"
        shift.clockOut = time
    else:
        return "Invalid type. The proper type format is (in/out)"

    db.session.add(shift)
    db.session.commit()
    return f'Clocked {type} at {time.strftime("%d/%m/%Y %H:%M")} for shiftID: {shiftID}'

def listStaff():
    Staff = Staff.query.all()
    str = ""
    for staff in Staff:
        str += f'ID: {staff.id}, Name: {staff.name}\n'
    return str

def getStaff(id):
    return db.session.get(Staff, id)

def deleteStaff(id):
    staff = Staff.query.get(id)
    if not staff: return None
    db.session.delete(staff)
    db.session.commit()
