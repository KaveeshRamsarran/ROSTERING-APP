from .user import create_user
from .admin import createAdmin, schedule
from .staff import createStaff, clockInOut
from App.database import db
from datetime import datetime

def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    createStaff('Kevin', 'kevinpass')
    createStaff('Jojo', 'jojopass')
    createAdmin('Mangalie', 'mangaliepass')
    createAdmin('Badrie', 'badriepass')
    
    # Kevin’s shifts, handled by admin Mangalie.
    shift1 = schedule(1, 1, "22/09/2025 08:00", "22/09/2025 09:30")
    shift2 = schedule(1, 1, "23/09/2025 10:00", "23/09/2025 12:00")
    shift3 = schedule(1, 1, "25/09/2025 14:00", "25/09/2025 15:00")
    shift4 = schedule(1, 1, "27/09/2025 18:00", "27/09/2025 19:00")
    
    # Jojo’s shifts, handled by admin Badrie.
    shift5 = schedule(2, 2, "22/09/2025 11:00", "22/09/2025 12:00")
    shift6 = schedule(2, 2, "23/09/2025 16:00", "23/09/2025 17:00")
    shift7 = schedule(2, 2, "24/09/2025 17:00", "24/09/2025 18:30")
    shift8 = schedule(2, 2, "26/09/2025 20:00", "26/09/2025 21:00")
    
    # Kevin clock-ins/outs.
    clockInOut(1, "in", datetime.strptime("22/09/2025 08:05", "%d/%m/%Y %H:%M"))
    clockInOut(1, "out", datetime.strptime("22/09/2025 09:25", "%d/%m/%Y %H:%M"))
    
    clockInOut(2, "in", datetime.strptime("23/09/2025 10:10", "%d/%m/%Y %H:%M"))
    clockInOut(2, "out", datetime.strptime("23/09/2025 11:55", "%d/%m/%Y %H:%M"))
    
    clockInOut(3, "in", datetime.strptime("25/09/2025 14:02", "%d/%m/%Y %H:%M"))
    clockInOut(3, "out", datetime.strptime("25/09/2025 14:58", "%d/%m/%Y %H:%M"))
    
    clockInOut(4, "in", datetime.strptime("27/09/2025 18:03", "%d/%m/%Y %H:%M"))
    clockInOut(4, "out", datetime.strptime("27/09/2025 18:55", "%d/%m/%Y %H:%M"))    
    
    # Jojo clock-ins/outs.
    clockInOut(5, "in", datetime.strptime("22/09/2025 11:05", "%d/%m/%Y %H:%M"))
    clockInOut(5, "out", datetime.strptime("22/09/2025 11:59", "%d/%m/%Y %H:%M"))
    
    clockInOut(6, "in", datetime.strptime("23/09/2025 16:10", "%d/%m/%Y %H:%M"))
    clockInOut(6, "out", datetime.strptime("23/09/2025 16:55", "%d/%m/%Y %H:%M"))
    
    clockInOut(7, "in", datetime.strptime("24/09/2025 17:01", "%d/%m/%Y %H:%M"))
    clockInOut(7, "out", datetime.strptime("24/09/2025 18:20", "%d/%m/%Y %H:%M"))
    
    clockInOut(8, "in", datetime.strptime("26/09/2025 20:15", "%d/%m/%Y %H:%M"))
    clockInOut(8, "out", datetime.strptime("26/09/2025 20:58", "%d/%m/%Y %H:%M"))
