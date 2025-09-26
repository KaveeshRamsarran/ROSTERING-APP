from App.database import db
from datetime import datetime

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staffID = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    adminID = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    clockIn = db.Column(db.DateTime)
    clockOut = db.Column(db.DateTime)

    def __init__(self, staffID, adminID, start, end):
        self.staffID = staffID
        self.adminID = adminID
        self.start = start
        self.end = end

    def reschedule(self, start, end):
        self.start = start
        self.end = end
        self.clockIn = None
        self.clockOut = None

    def getHoursWorked(self):
        if not self.clockIn or not self.clockOut:
            return 0
        else:
            return (self.clockOut - self.clockIn).total_seconds() / 3600
    
    def get_json(self):
        return{
            'id': self.id,
            'staffID' : self.staffID,
            'adminID' : self.adminID,
            'start' : self.start.strftime("%d/%m/%Y %H:%M"),
            'end' : self.end.strftime("%d/%m/%Y %H:%M"),
            'clockIn' : self.clockIn.strftime("%d/%m/%Y %H:%M") if self.clockIn else None,
            'clockOut' : self.clockOut.strftime("%d/%m/%Y %H:%M") if self.clockOut else None,
        }
