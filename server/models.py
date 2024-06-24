from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

# Association tables for many-to-many relationships
EmployeeMeeting = db.Table('employee_meeting',
    db.Column('employee_id', db.Integer, db.ForeignKey('employees.id'), primary_key=True),
    db.Column('meeting_id', db.Integer, db.ForeignKey('meetings.id'), primary_key=True)
)

EmployeeProject = db.Table('employee_project',
    db.Column('employee_id', db.Integer, db.ForeignKey('employees.id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True)
)

class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    meetings = db.relationship('Meeting', secondary=EmployeeMeeting, back_populates='employees')
    projects = db.relationship('Project', secondary=EmployeeProject, back_populates='employees')

    def __repr__(self):
        return f"<Employee {self.id}, {self.name}, {self.hire_date}>"

class Meeting(db.Model):
    __tablename__ = "meetings"

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String, nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String, nullable=False)
    employees = db.relationship('Employee', secondary=EmployeeMeeting, back_populates='meetings')

    def __repr__(self):
        return f"<Meeting {self.id}, {self.topic}, {self.scheduled_time}, {self.location}>"

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    employees = db.relationship('Employee', secondary=EmployeeProject, back_populates='projects')

    def __repr__(self):
        return f"<Project {self.id}, {self.title}, {self.budget}>"
