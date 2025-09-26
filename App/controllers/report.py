from App.models import Staff, Shift, Report
from App.database import db
from datetime import datetime, timedelta

def createRoster():
    today = datetime.now().date()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    roster = {}
    for staff in Staff.query.all():
        shifts = Shift.query.filter(Shift.staffID == staff.id, Shift.start >= start, Shift.start <= end).all()
        roster[staff.name] = [f'{s.start.strftime("%d/%m/%Y %H:%M")} - {s.end.strftime("%d/%m/%Y %H:%M")}' for s in shifts]
    return roster

def createReportData():
    today = datetime.now().date()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    data = {}
    for staff in Staff.query.all():
        totalWorkedHours = 0
        shiftIDs = []
      
        shifts = Shift.query.filter(Shift.staffID == staff.id, Shift.start >= start, Shift.start <= end).all()
        for shift in shifts:
            shiftIDs.append(shift.id)
            totalWorkedHours += shift.getHoursWorked()
        data[staff.name] = {
            "totalWorkedHours": totalWorkedHours,
            "shiftIDs": shiftIDs
        }
    return data

def createReport():
    roster = createRoster()
    data = createReportData()
    reportData = Report(roster=roster, data=data)
    db.session.add(reportData)
    db.session.commit()
    return reportData

def listReports():
    reports = Report.query.all()
    str = ""
    for report in reports:
        str += f'Report {report.id}. Date: {report.timestamp.strftime("%d/%m/%Y %H:%M")}\n'
    return str

def printReportInfo(report):
    str = f'''
        Report: {report["id"]}
        Date: {report["timestamp"]}
    '''
    for staffName, data in report["data"].items():
        str += f'''
       ______________________________________________________
           Name: {staffName},
           Hours: {data["totalWorkedHours"]:.2f},
           Shifts: {data["shiftIDs"]}
        '''
    return str

def getReport(id):
    return db.session.get(Report, id)

def deleteReport(id):
    report = Report.query.get(id)
    if not report: return None
    db.session.delete(report)
    db.session.commit()
    return True
