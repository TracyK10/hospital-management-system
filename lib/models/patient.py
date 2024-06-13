# lib/models/patient.py
from models.__init__ import CONN, CURSOR
from medical_record import MedicalRecord
from appointment import Appointment

class Patient:
    
    all = {}
    
    def __init__(self, first_name, last_name, age, id=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.medical_records = []
        self.appointments = []

    def __repr__(self):
        return (
            f"Patient(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, age={self.age}, medical_records={self.medical_records}, appointments={self.appointments})"
        )
    
    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, first_name):
        if isinstance(first_name, str) and len(first_name) > 0:
            self._first_name = first_name
        else:
            raise ValueError("First name must be a non-empty string")

    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, last_name):
        if isinstance(last_name, str) and len(last_name) > 0:
            self._last_name = last_name
        else:
            raise ValueError("Last name must be a non-empty string")
            
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, age):
        if isinstance(age, int) and age > 0:
            self._age = age
        else:
            raise ValueError("Age must be a positive integer")
    
    @classmethod
    def create_table(cls):
        """Create a new table to persist the attributes of Patient instances"""
        sql = """
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
        """Drop the table that persists the attributes of Patient instances"""
        sql = "DROP TABLE IF EXISTS patients"
        CURSOR.execute(sql)
        CONN.commit()
    
    def save(self):
        """Persist the attributes of a Patient instance to the database"""
        sql = """
            INSERT INTO patients (first_name, last_name, age)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.first_name, self.last_name, self.age))
        CONN.commit()
        self.id = CURSOR.lastrowid
    
    def update(self):
        """Update the table row corresponding to the current Patient instance"""
        sql = """
            UPDATE patients
            SET first_name = ?, last_name = ?, age = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.first_name, self.last_name, self.age, self.id))
        CONN.commit()
    
    def delete(self):
        """Delete the table row corresponding to the current Patient instance"""
        sql = "DELETE FROM patients WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
    
    @classmethod
    def create(cls, first_name, last_name, age):
        """Create a new Patient instance and persist it to the database"""
        patient = cls(first_name, last_name, age)
        patient.save()
        return patient
    
    @classmethod
    def instance_from_db(cls, row):
        """Return a Patient object having the attribute values from the table row."""
        
        # Check the dictionary for existing instances using the row's primary key
        patient = cls.all.get(row[0])
        if patient:
            # Ensure attributes match row values in case local instance was modified
            patient.first_name = row[1]
            patient.last_name = row[2]
            patient.age = row[3]
        else:
            # Create a new instance using row values
            patient = cls(row[1], row[2], row[3], id=row[0])
            cls.all[row[0]] = patient
        
        # Retrieve and assign related medical records
        patient.medical_records = MedicalRecord.find_by_patient_id(patient.id)
        # Retrieve and assign related appointments
        patient.appointments = Appointment.find_by_patient_id(patient.id)
        
        return patient
    
    @classmethod
    def get_all(cls):
        """Return a list of all Patient instances persisted to the database"""
        sql = "SELECT * FROM patients"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        """Return the Patient instance with the given primary key"""
        sql = "SELECT * FROM patients WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name(cls, first_name, last_name):
        """Return a list of Patient instances with the given name"""
        sql = "SELECT * FROM patients WHERE first_name = ? AND last_name = ?"
        row = CURSOR.execute(sql, (first_name, last_name)).fetchone()
        return cls.instance_from_db(row) if row else None
