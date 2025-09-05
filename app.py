from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Patient, Doctor, Appointment, LabResult, Bill, BillItem
from config import DATABASE_URL
from datetime import datetime
import os
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', DATABASE_URL)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'iuahdueglwf7etf8326rwd' # Change this to a secure key in production

# Initialize DB
db.init_app(app)

# Create tables (only once)
with app.app_context():
    db.create_all()

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

# ========== PATIENTS ==========
@app.route('/patients')
def list_patients():
    patients = Patient.query.all()
    return render_template('patient/list.html', patients=patients)

@app.route('/patients/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        patient = Patient(
            name=request.form['name'],
            dob=request.form['dob'],
            gender=request.form['gender'],
            phone=request.form['phone'],
            address=request.form['address'],
            email=request.form['email']
        )
        db.session.add(patient)
        db.session.commit()
        flash('Patient added successfully!')
        return redirect(url_for('list_patients'))
    return render_template('patient/form.html')

# ========== APPOINTMENTS ==========
@app.route('/appointments')
def list_appointments():
    appointments = Appointment.query.all()
    return render_template('appointment/list.html', appointments=appointments)

@app.route('/appointments/add', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'POST':
        apt = Appointment(
            patient_id=request.form['patient_id'],
            doctor_id=request.form['doctor_id'],
            date_time=request.form['date_time'],
            reason=request.form['reason']
        )
        db.session.add(apt)
        db.session.commit()
        flash('Appointment scheduled!')
        return redirect(url_for('list_appointments'))

    patients = Patient.query.all()
    doctors = Doctor.query.all()
    return render_template('appointment/form.html', patients=patients, doctors=doctors)

@app.route('/appointments/<int:apt_id>')
def view_appointment(apt_id):
    apt = Appointment.query.get_or_404(apt_id)
    return render_template('appointment/view.html', apt=apt)

# ========== BILLING ==========
@app.route('/bills')
def list_bills():
    bills = Bill.query.all()
    return render_template('billing/list.html', bills=bills)

@app.route('/bills/add', methods=['GET', 'POST'])
def add_bill():
    if request.method == 'POST':
        # Create new bill
        bill = Bill(
            patient_id=request.form['patient_id'],
            appointment_id=request.form.get('appointment_id') or None,
            total_amount=float(request.form['total_amount']),
            status=request.form['status']
        )
        db.session.add(bill)
        db.session.commit()

        # Add bill items (optional)
        descriptions = request.form.getlist('item_description')
        amounts = request.form.getlist('item_amount')

        for desc, amt in zip(descriptions, amounts):
            if desc and amt:
                item = BillItem(
                    bill_id=bill.bill_id,
                    description=desc,
                    amount=float(amt)
                )
                db.session.add(item)
        db.session.commit()

        flash('Bill created successfully!')
        return redirect(url_for('list_bills'))

    patients = Patient.query.all()
    appointments = Appointment.query.all()
    return render_template('billing/form.html', patients=patients, appointments=appointments)

@app.route('/bills/<int:bill_id>')
def view_bill(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    return render_template('billing/view.html', bill=bill)


if __name__ == '__main__':
    app.run(debug=True)