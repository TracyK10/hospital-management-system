#!/usr/bin/env python3

from models.__init__ import CONN, CURSOR
from models.patient import Patient

def seed_database():
    # Drop and create the patients table
    Patient.drop_table()
    Patient.create_table()

    # Create seed data for patients
    Patient.create("John Doe", 30, 1)
    Patient.create("Jane Smith", 25, 2)
    Patient.create("Alice Johnson", 40, 3)
    Patient.create("Bob Brown", 50, 4)
    Patient.create("Eve Davis", 35, 5)
    Patient.create("Frank Wilson", 45, 6)
    Patient.create("Grace Lee", 28, 7)
    Patient.create("Hank Martinez", 60, 8)
    Patient.create("Ivy Robinson", 32, 9)
    Patient.create("Jack Clark", 38, 10)

seed_database()
print("Seeded database")