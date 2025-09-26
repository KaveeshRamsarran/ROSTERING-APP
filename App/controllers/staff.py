from App.models import Shift, Staff
from datetime import datetime, timedelta

# View roster for the week (for all staff or a specific username)
def view_roster(username=None):
    today = datetime.now().date()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    if username:
        staff = Staff.query.filter_by(username=username).first()
        if not staff:
            return f"Staff '{username}' not found."
        shifts = Shift.query.filter(Shift.staffID == staff.id, Shift.start >= start, Shift.start <= end).all()
        if not shifts:
            return f"No shifts found for {username} this week."
        return '\n'.join([f"{s.start.strftime('%d/%m/%Y %H:%M')} - {s.end.strftime('%d/%m/%Y %H:%M')}" for s in shifts])
    else:
        out = []
        for staff in Staff.query.all():
            shifts = Shift.query.filter(Shift.staffID == staff.id, Shift.start >= start, Shift.start <= end).all()
            if shifts:
                out.append(f"{staff.username}:")
                out.extend([f"  {s.start.strftime('%d/%m/%Y %H:%M')} - {s.end.strftime('%d/%m/%Y %H:%M')}" for s in shifts])
        return '\n'.join(out) if out else "No shifts scheduled for any staff this week."

# Clock in or out of a shift
def clock_shift(direction, shift_id):
    shift = Shift.query.get(shift_id)
    if not shift:
        return f"Shift {shift_id} not found."
    now = datetime.now()
    if direction == 'in':
        if shift.clockIn:
            return f"Already clocked in for shift {shift_id}."
        shift.clockIn = now
        db.session.commit()
        return f"Clocked in for shift {shift_id} at {now.strftime('%d/%m/%Y %H:%M')}"
    elif direction == 'out':
        if not shift.clockIn:
            return f"Cannot clock out before clocking in for shift {shift_id}."
        if shift.clockOut:
            return f"Already clocked out for shift {shift_id}."
        shift.clockOut = now
        db.session.commit()
        return f"Clocked out for shift {shift_id} at {now.strftime('%d/%m/%Y %H:%M')}"
    else:
        return "Invalid direction. Use 'in' or 'out'."
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
