# Hospital Management System

## Overview

The Hospital Management System is a Python command-line application designed to help manage patient records, doctor information, appointments, and medical records. It uses SQLite as its database to store and retrieve data efficiently.

## Directory Structure

hospital_management/
│
├── __init__.py
├── main.py
├── database.py
├── patient.py
├── doctor.py
├── appointment.py
└── medical_record.py

## Features

- **Manage Patients**: Add, view, update, and delete patient records.
- **Manage Doctors**: Add, view, update, and delete doctor records.
- **Manage Appointments**: Schedule, view, update, and cancel appointments.
- **Manage Medical Records**: Add, view, update, and delete medical records.

## Database Schema

### Patients Table (`patients`)
- `id`: INTEGER, PRIMARY KEY, AUTOINCREMENT
- `name`: TEXT, NOT NULL
- `age`: INTEGER
- `gender`: TEXT
- `medical_history`: TEXT

### Doctors Table (`doctors`)
- `id`: INTEGER, PRIMARY KEY, AUTOINCREMENT
- `name`: TEXT, NOT NULL
- `specialization`: TEXT
- `availability`: TEXT

### Appointments Table (`appointments`)
- `id`: INTEGER, PRIMARY KEY, AUTOINCREMENT
- `patient_id`: INTEGER, FOREIGN KEY REFERENCES `patients`(`id`)
- `doctor_id`: INTEGER, FOREIGN KEY REFERENCES `doctors`(`id`)
- `appointment_date`: TEXT

### Medical Records Table (`medical_records`)
- `id`: INTEGER, PRIMARY KEY, AUTOINCREMENT
- `patient_id`: INTEGER, FOREIGN KEY REFERENCES `patients`(`id`)
- `doctor_id`: INTEGER, FOREIGN KEY REFERENCES `doctors`(`id`)
- `record_date`: TEXT
- `diagnosis`: TEXT
- `treatment`: TEXT

## Installation

1. **Clone the repository**:
    `

2. **Create a virtual environment** (optional but recommended):
   

3. **Install dependencies**:
   

4. **Initialize the database**:
    The database will be automatically initialized when you run the main application.

## Usage

Run the application:

python3 cli.py
