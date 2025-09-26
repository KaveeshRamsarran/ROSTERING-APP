from App.database import db
from App.controllers.staff import createStaff
from App.controllers.admin import createAdmin

def initialize():
    """
    Creates tables and seeds a default admin + staff if they don't exist.
    """
    db.create_all()

    # seed admin
    createAdmin('Mangalie', 'mangaliepass')

    # seed staff
    createStaff('Kevin', 'kevinpass')
