# Rostering App

* (Admin) Schedule a staff member shifts for the week
* (Staff) View combined roster of all staff
* (Staff) Time in/Time out at the stat/end of shift
* (Admin) View shift report for the week

# CLI Commands

Initializes the database and populates it.
```
flask init
```

## Staff Commands

Create a new staff member.
```
flask staff create <name> <password>
Example: flask staff create tom tompass
```

View the full roster for this week.
```
flask staff view_roster
```

Clock staff in or out of a shift.
```
flask staff clock <in|out> <shiftId>
Example: flask staff clock in 4
```

## Admin Commands

Create a new admin.
```
flask admin create <name> <password>
Example: flask admin create john johnpass
```

Schedule a shift.
```
flask admin schedule <staffId> <adminId> <startTime> <endTime>
Example: flask admin schedule 1 1 "26/09/2025 09:00" "26/09/2025 17:00"
```

List all reports.
```
flask admin list_reports
```

Create a new report.
```
flask admin create_report
```

View a report by ID.
```
flask admin view_report <reportId>
Example: flask admin view_report 2
```
