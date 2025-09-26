import click
from flask.cli import AppGroup

from App.main import create_app
from App.database import get_migrate
from App.database import db

# controllers
from App.controllers.initialize import initialize
from App.controllers.staff import createStaff, get_all_staff, get_all_staff_json
from App.controllers.admin import createAdmin, get_all_admins, get_all_admins_json

# models (for .first_or_404() usage if needed later)
from App.models import Staff, Admin

app = create_app()
migrate = get_migrate(app)

# -------------------------
# Database init
# -------------------------
@app.cli.command("init", help="Creates tables and seeds default data")
def init():
    initialize()
    click.echo("Database initialized and seed complete.")

# -------------------------
# Staff CLI
# -------------------------
staff_cli = AppGroup('staff', help='Staff commands')

@staff_cli.command("create", help='Create a staff user')
@click.argument("username")
@click.argument("password")
def staff_create(username, password):
    staff = createStaff(username, password)
    if staff is None:
        return click.echo(f"Staff '{username}' already exists.")
    click.echo(staff.get_json())

@staff_cli.command("list", help='List all staff (string/json)')
@click.argument("format", default="string")
def staff_list(format):
    if format == "json":
        click.echo(get_all_staff_json())
    else:
        staff_list = get_all_staff()
        if not staff_list:
            click.echo("No staff found.")
            return
        header = f"{'ID':<5} {'Username':<20} {'Role':<10}"
        rows = [header, '-'*len(header)]
        for s in staff_list:
            rows.append(f"{s.id:<5} {s.username:<20} {'Staff':<10}")
        click.echo("\n".join(rows))


# -------------------------
# Staff: view_roster
# -------------------------
@staff_cli.command("view_roster", help="View roster for the week")
@click.argument("username", required=False)
def staff_view_roster(username=None):
    # Placeholder: implement actual logic in controller
    from App.controllers.staff import view_roster
    result = view_roster(username) if username else view_roster()
    click.echo(result)

# -------------------------
# Staff: clock in/out
# -------------------------
@staff_cli.command("clock", help="Clock staff in or out of a shift")
@click.argument("direction")
@click.argument("shift_id")
def staff_clock(direction, shift_id):
    # Placeholder: implement actual logic in controller
    from App.controllers.staff import clock_shift
    result = clock_shift(direction, shift_id)
    click.echo(result)

app.cli.add_command(staff_cli)

# -------------------------
# Admin CLI
# -------------------------
admin_cli = AppGroup('admin', help='Admin commands')

@admin_cli.command("create", help='Create an admin user')
@click.argument("username")
@click.argument("password")
def admin_create(username, password):
    admin = createAdmin(username, password)
    if admin is None:
        return click.echo(f"Admin '{username}' already exists.")
    # expect Admin to have get_json(); if not, print minimal fields
    try:
        click.echo(admin.get_json())
    except Exception:
        click.echo(f"id={admin.id}, username={admin.username}")

@admin_cli.command("list", help='List all admins (string/json)')
@click.argument("format", default="string")
def admin_list(format):
    if format == "json":
        click.echo(get_all_admins_json())
    else:
        admins = get_all_admins()
        if not admins:
            click.echo("No admins found.")
            return
        header = f"{'ID':<5} {'Username':<20} {'Role':<10}"
        rows = [header, '-'*len(header)]
        for a in admins:
            rows.append(f"{a.id:<5} {a.username:<20} {'Admin':<10}")
        click.echo("\n".join(rows))

# -------------------------
# User CLI (table output)
# -------------------------
@app.cli.command("user_list", help="List all users (string/json)")
@click.argument("format", default="string")
def user_list(format):
    from App.controllers.user import get_all_users, get_all_users_json
    if format == "json":
        click.echo(get_all_users_json())
    else:
        users = get_all_users()
        if not users:
            click.echo("No users found.")
            return
        header = f"{'ID':<5} {'Username':<20} {'Role':<10}"
        rows = [header, '-'*len(header)]
        for u in users:
            rows.append(f"{u.id:<5} {u.username:<20} {'User':<10}")
        click.echo("\n".join(rows))


# -------------------------
# Admin: schedule shift
# -------------------------
@admin_cli.command("schedule", help="Schedule a shift")
@click.argument("staff_id")
@click.argument("admin_id")
@click.argument("start_time")
@click.argument("end_time")
def admin_schedule(staff_id, admin_id, start_time, end_time):
    from App.controllers.admin import schedule_shift
    result = schedule_shift(staff_id, admin_id, start_time, end_time)
    click.echo(result)

# -------------------------
# Admin: list reports
# -------------------------
@admin_cli.command("list_reports", help="List all reports")
def admin_list_reports():
    from App.controllers.report import list_reports
    from App.models import Report
    reports = Report.query.all()
    if not reports:
        click.echo("No reports found.")
        return
    header = f"{'ID':<5} {'Timestamp':<20}"
    rows = [header, '-'*len(header)]
    for r in reports:
        rows.append(f"{r.id:<5} {r.timestamp.strftime('%d/%m/%Y %H:%M'):<20}")
    click.echo("\n".join(rows))

# -------------------------
# Shift CLI (table output)
# -------------------------
@app.cli.command("shift_list", help="List all shifts (string/json)")
@click.argument("format", default="string")
def shift_list(format):
    from App.models import Shift
    shifts = Shift.query.all()
    if format == "json":
        click.echo([s.get_json() for s in shifts])
    else:
        if not shifts:
            click.echo("No shifts found.")
            return
        header = f"{'ID':<5} {'StaffID':<8} {'AdminID':<8} {'Start':<17} {'End':<17} {'ClockIn':<17} {'ClockOut':<17}"
        rows = [header, '-'*len(header)]
        for s in shifts:
            rows.append(f"{s.id:<5} {s.staffID:<8} {s.adminID:<8} {s.start.strftime('%d/%m/%Y %H:%M'):<17} {s.end.strftime('%d/%m/%Y %H:%M'):<17} "
                        f"{s.clockIn.strftime('%d/%m/%Y %H:%M') if s.clockIn else '-':<17} {s.clockOut.strftime('%d/%m/%Y %H:%M') if s.clockOut else '-':<17}")
        click.echo("\n".join(rows))

# -------------------------
# Admin: create report
# -------------------------
@admin_cli.command("create_report", help="Create a new report")
def admin_create_report():
    from App.controllers.report import create_report
    result = create_report()
    click.echo(result)

# -------------------------
# Admin: view report by ID
# -------------------------
@admin_cli.command("view_report", help="View a report by ID")
@click.argument("report_id")
def admin_view_report(report_id):
    from App.controllers.report import view_report
    result = view_report(report_id)
    click.echo(result)

app.cli.add_command(admin_cli)

# -------------------------
# Optional: simple health command
# -------------------------
@app.cli.command("ping", help="Quick app health check")
def ping():
    click.echo("pong")
