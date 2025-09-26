from App.models import Shift
from App.database import db

def getShiftInfo(id):
    shift = Shift.query.get(id)
    return shift.get_json() if shift else None

def deleteShift(id):
    shift = Shift.query.get(id)
    if not shift: return None
    db.session.delete(shift)
    db.session.commit()
    return True

def printShiftInfo(shift):
    str = f"""
        ID: {shift["id"]}
        Start: {shift["start"]}
        End: {shift["end"]}
        Clock In: {shift["clockIn"]}
        Clock Out: {shift["clockOut"]}
    """
    return str
