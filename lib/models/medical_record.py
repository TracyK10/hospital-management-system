# lib/models/medical_record.py
from models.__init__ import CONN, CURSOR
from models.patient import Patient
from models.doctor import Doctor

class MedicalRecord:
    
    all = {}
    
    def __init__(self, patient_id, doctor_id, record_date, diagnosis, treatment, id=None):
        self.id = id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.record_date = record_date
        self.diagnosis = diagnosis
        self.treatment = treatment

    def __repr__(self):
        return (
            f"MedicalRecord(id={self.id}, patient_id={self.patient_id}, doctor_id={self.doctor_id}, record_date={self.record_date}, diagnosis={self.diagnosis}, treatment={self.treatment})"
        )
    
    @property
    def diagnosis(self):
        return self._diagnosis
    
    @diagnosis.setter
    def diagnosis(self, diagnosis):
        if isinstance(diagnosis, str) and len(diagnosis) > 0:
            self._diagnosis = diagnosis
        else:
            raise ValueError("Diagnosis must be a non-empty string")

    @property
    def treatment(self):
        return self._treatment
    
    @treatment.setter
    def treatment(self, treatment):
        if isinstance(treatment, str) and len(treatment) > 0:
            self._treatment = treatment
        else:
            raise ValueError("Treatment must be a non-empty string")
    
    @property
    def record_date(self):
        return self._record_date
    
    @record_date.setter
    def record_date(self, record_date):
        self._record_date = record_date  # You might want to add more validation here
    
    @property
    def patient_id(self):
        return self._patient_id
    
    @patient_id.setter
    def patient_id(self, patient_id):
        if isinstance(patient_id, int) and patient_id > 0:
            self._patient_id = patient_id
        else:
            raise ValueError("Patient ID must be a positive integer")
    
    @property
    def doctor_id(self):
        return self._doctor_id
    
    @doctor_id.setter
    def doctor_id(self, doctor_id):
        if isinstance(doctor_id, int) and doctor_id > 0:
            self._doctor_id = doctor_id
        else:
            raise ValueError("Doctor ID must be a positive integer")
    
    @classmethod
    def create_table(cls):
        """Create a new table to persist the attributes of MedicalRecord instances"""
        sql = """
            CREATE TABLE IF NOT EXISTS medical_records (
                id INTEGER PRIMARY KEY,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                record_date TEXT NOT NULL,
                diagnosis TEXT NOT NULL,
                treatment TEXT NOT NULL,
                FOREIGN KEY(patient_id) REFERENCES patients(id),
                FOREIGN KEY(doctor_id) REFERENCES doctors(id)
            )
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
        """Drop the table that persists the attributes of MedicalRecord instances"""
        sql = "DROP TABLE IF EXISTS medical_records"
        CURSOR.execute(sql)
        CONN.commit()
    
    def save(self):
        """Persist the attributes of a MedicalRecord instance to the database"""
        sql = """
            INSERT INTO medical_records (patient_id, doctor_id, record_date, diagnosis, treatment)
            VALUES (?, ?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.patient_id, self.doctor_id, self.record_date, self.diagnosis, self.treatment))
        CONN.commit()
        self.id = CURSOR.lastrowid
    
    def update(self):
        """Update the table row corresponding to the current MedicalRecord instance"""
        sql = """
            UPDATE medical_records
            SET patient_id = ?, doctor_id = ?, record_date = ?, diagnosis = ?, treatment = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.patient_id, self.doctor_id, self.record_date, self.diagnosis, self.treatment, self.id))
        CONN.commit()
    
    def delete(self):
        """Delete the table row corresponding to the current MedicalRecord instance"""
        sql = "DELETE FROM medical_records WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
    
    @classmethod
    def create(cls, patient_id, doctor_id, record_date, diagnosis, treatment):
        """Create a new MedicalRecord instance and persist it to the database"""
        medical_record = cls(patient_id, doctor_id, record_date, diagnosis, treatment)
        medical_record.save()
        return medical_record
    
    @classmethod
    def instance_from_db(cls, row):
        """Return a MedicalRecord object having the attribute values from the table row."""
        
        # Check the dictionary for existing instances using the row's primary key
        medical_record = cls.all.get(row[0])
        if medical_record:
            # Ensure attributes match row values in case local instance was modified
            medical_record.patient_id = row[1]
            medical_record.doctor_id = row[2]
            medical_record.record_date = row[3]
            medical_record.diagnosis = row[4]
            medical_record.treatment = row[5]
        else:
            # Create a new instance using row values
            medical_record = cls(row[1], row[2], row[3], row[4], row[5], id=row[0])
            cls.all[row[0]] = medical_record
        
        return medical_record
    
    @classmethod
    def get_all(cls):
        """Return a list of all MedicalRecord instances persisted to the database"""
        sql = "SELECT * FROM medical_records"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        """Return the MedicalRecord instance with the given primary key"""
        sql = "SELECT * FROM medical_records WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_patient_id(cls, patient_id):
        """Return a list of MedicalRecord instances for the given patient_id"""
        sql = "SELECT * FROM medical_records WHERE patient_id = ?"
        CURSOR.execute(sql, (patient_id,))
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_doctor_id(cls, doctor_id):
        """Return a list of MedicalRecord instances for the given doctor_id"""
        sql = "SELECT * FROM medical_records WHERE doctor_id = ?"
        CURSOR.execute(sql, (doctor_id,))
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

