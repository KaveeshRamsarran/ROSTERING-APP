import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Staff, Admin, Shift, Report
from App.main import create_app
from App.controllers import (
    create_user, get_all_users_json, get_all_users, initialize,
    createAdmin, schedule, listAdmins, getAdmin, deleteAdmin,
    createStaff, clockInOut, listStaff, getStaff, deleteStaff,
    getShiftInfo, deleteShift, printShiftInfo,
    createRoster, createReportData, createReport, listReports, printReportInfo, getReport, deleteReport
)

app = create_app()
migrate = get_migrate(app)


'''
Database Init Command
'''
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')


'''
User Commands
'''
user_cli = AppGroup('user', help='User object commands')

@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli)


'''
Staff Commands
'''
staff_cli = AppGroup('staff', help='Staff object commands')

@staff_cli.command("list", help="Lists all staff users in the database")
def list_staff_command():
    print(listStaff())

@staff_cli.command("view_roster", help="View the combined staff roster for this week")
def view_roster_command():
    roster = createRoster()
    output = 'All shifts this week/Total roster this week:\n'
    for staff in roster:
        str += f'\n{staff}:\n'
        for shift in roster[staff]:
            str += f'{shift}\n'
    print(str)

@staff_cli.command("create", help="Creates a staff user")
@click.argument('name', default="tom")
@click.argument('password', default="tompass")
def create_staff_command(name, password):
    staff = createStaff(name, password)
    if not staff:
        print("Error creating staff user")
    else:
        print(f'Staff user {staff.name} successfully created!')

@staff_cli.command("clock", help="Clock in/out of a shift")
@click.argument("type", type=click.Choice(["in", "out"], case_sensitive=False))
@click.argument("shiftId", type=int)
def clock_staff_command(type, shiftId):
    string = clockInOut(shiftId, type)
    print(string)

app.cli.add_command(staff_cli)


'''
Admin Commands
'''
admin_cli = AppGroup('admin', help='Admin object commands')

@admin_cli.command("list", help="Lists all admin users in the database")
def list_admin_command():
    print(listAdmins())

@admin_cli.command("create", help="Creates an admin user")
@click.argument('name', default="john")
@click.argument('password', default="johnpass")
def create_admin_command(name, password):
    admin = createAdmin(name, password)
    if not admin:
        print("Error creating admin user")
    else:
        print(f'Admin user {admin.name} successfully created!')

@admin_cli.command("schedule", help='Schedules a shift for a staff user')
@click.argument("staffId", type=int)
@click.argument("adminId", type=int)
@click.argument("startTime")
@click.argument("endTime")
def schedule_shift_command(staffId, adminId, startTime, endTime):
    shift = schedule(staffId, adminId, startTime, endTime)
    if not shift:
        print("Error scheduling shift")
    else:
        print(f'Shift scheduled! {shift.get_json()}')

@admin_cli.command("list_reports", help="Lists all reports in the database")
def list_reports_command():
    print(listReports())

@admin_cli.command("create_report", help="Creates a new report")
def create_report_command():
    report = createReport()
    if not report:
        print("Error generating report")
    else:
        print(f'Report generated!\n\n {printReportInfo(report.get_json())}')

@admin_cli.command("view_report", help="View a report by ID")
@click.argument("reportId", type=int)
def view_report_command(reportId):
    report = getReport(reportId)
    if not report:
        print("Could not find report")
    else:
        print(printReportInfo(report.get_json()))

app.cli.add_command(admin_cli)

'''
Test Commands
'''
test = AppGroup('test', help='Testing commands')

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)
