# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Patient(db.Model):
    __tablename__ = 'patient'
    patient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date)
    gender = db.Column(db.Enum('M', 'F', name='gender_enum'))
    phone = db.Column(db.String(15))
    address = db.Column(db.Text)
    email = db.Column(db.String(100))

    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    lab_results = db.relationship('LabResult', backref='patient', lazy=True)
    bills = db.relationship('Bill', backref='patient', lazy=True)

class Doctor(db.Model):
    __tablename__ = 'doctor'
    doctor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    email = db.Column(db.String(100))
    department = db.Column(db.String(50))

    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

class Appointment(db.Model):
    __tablename__ = 'appointment'
    appointment_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.doctor_id'), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('Scheduled', 'Completed', 'Cancelled', name='status_enum'), default='Scheduled')
    reason = db.Column(db.Text)

class LabResult(db.Model):
    __tablename__ = 'lab_result'
    result_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable=False)
    test_name = db.Column(db.String(100), nullable=False)
    test_date = db.Column(db.Date, default=datetime.utcnow)
    result_value = db.Column(db.Text)
    status = db.Column(db.Enum('Normal', 'Abnormal', name='result_status_enum'))
    notes = db.Column(db.Text)

class Bill(db.Model):
    __tablename__ = 'bill'
    bill_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.appointment_id'))
    date_issued = db.Column(db.Date, default=datetime.utcnow)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum('Paid', 'Unpaid', name='bill_status_enum'), default='Unpaid')

    items = db.relationship('BillItem', backref='bill', lazy=True)

class BillItem(db.Model):
    __tablename__ = 'bill_item'
    item_id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.bill_id'), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Numeric(8, 2), nullable=False)