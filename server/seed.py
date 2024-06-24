#!/usr/bin/env python3
# server/seed.py

import datetime
import logging
from app import app
from models import db, Employee, Meeting, Project, EmployeeMeeting, EmployeeProject

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

with app.app_context():
    try:
        # Delete all rows in tables
        logger.info("Deleting all rows in tables...")
        Employee.query.delete()
        Meeting.query.delete()
        Project.query.delete()
        EmployeeMeeting.query.delete()
        EmployeeProject.query.delete()

        # Add employees
        logger.info("Adding employees...")
        e1 = Employee(name="Uri Lee", hire_date=datetime.datetime(2022, 5, 17))
        e2 = Employee(name="Tristan Tal", hire_date=datetime.datetime(2020, 1, 30))
        e3 = Employee(name="Sasha Hao", hire_date=datetime.datetime(2021, 12, 1))
        e4 = Employee(name="Taylor Jai", hire_date=datetime.datetime(2015, 1, 2))
        db.session.add_all([e1, e2, e3, e4])
        db.session.commit()

        # Add meetings
        logger.info("Adding meetings...")
        m1 = Meeting(topic="Software Engineering Weekly Update",
                     scheduled_time=datetime.datetime(2023, 10, 31, 9, 30),
                     location="Building A, Room 142")
        m2 = Meeting(topic="Github Issues Brainstorming",
                     scheduled_time=datetime.datetime(2023, 12, 1, 15, 15),
                     location="Building D, Room 430")
        db.session.add_all([m1, m2])
        db.session.commit()

        # Add projects
        logger.info("Adding projects...")
        p1 = Project(title="XYZ Project Flask server", budget=50000)
        p2 = Project(title="XYZ Project React UI", budget=100000)
        db.session.add_all([p1, p2])
        db.session.commit()

        # Many-to-many relationship between employee and meeting
        logger.info("Creating many-to-many relationships between employees and meetings...")
        em1 = EmployeeMeeting(employee_id=e1.id, meeting_id=m1.id)
        em2 = EmployeeMeeting(employee_id=e2.id, meeting_id=m1.id)
        em3 = EmployeeMeeting(employee_id=e3.id, meeting_id=m2.id)
        em4 = EmployeeMeeting(employee_id=e4.id, meeting_id=m2.id)
        db.session.add_all([em1, em2, em3, em4])
        db.session.commit()

        # Many-to-many relationship between employee and project through assignment
        logger.info("Creating many-to-many relationships between employees and projects...")
        ep1 = EmployeeProject(employee_id=e1.id, project_id=p1.id)
        ep2 = EmployeeProject(employee_id=e2.id, project_id=p1.id)
        ep3 = EmployeeProject(employee_id=e3.id, project_id=p2.id)
        ep4 = EmployeeProject(employee_id=e4.id, project_id=p2.id)
        db.session.add_all([ep1, ep2, ep3, ep4])
        db.session.commit()

        logger.info("Seeding completed successfully!")

    except Exception as e:
        logger.error("An error occurred while seeding the database: %s", e)
        db.session.rollback()
    finally:
        db.session.close()
