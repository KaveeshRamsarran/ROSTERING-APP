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
        # simple string output
        staff_list = get_all_staff()
        out = [f"id={s.id}, username={s.username}" for s in staff_list]
        click.echo("\n".join(out) if out else "No staff found.")

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
        out = [f"id={a.id}, username={a.username}" for a in admins]
        click.echo("\n".join(out) if out else "No admins found.")

app.cli.add_command(admin_cli)

# -------------------------
# Optional: simple health command
# -------------------------
@app.cli.command("ping", help="Quick app health check")
def ping():
    click.echo("pong")
