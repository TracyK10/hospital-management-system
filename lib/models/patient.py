# lib/models/patient.py
from models.__init__ import CONN, CURSOR
from medical_record import Record

class Patient:
    
    all = {}
    
    def __init__(self, name, age, medical_records_id, id=None):
        self.id = id
        self.name = name
        self.age = age
        self.medical_records_id = medical_records_id
    
    def __repr__(self):
        return (
            f"Patient(id={self.id}, name={self.name}, age={self.age}, medical_records={self.medical_records})"
        )
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name) > 0:
            self._name = name
        else:
            raise ValueError("Name must be a non-empty string")
            
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, age):
        if isinstance(age, int) and age > 0:
            self._age = age
        else:
            raise ValueError("Age must be a positive integer")
    
    @property
    def medical_records(self):
        return self._medical_records
    
    @medical_records.setter
    def medical_records(self, medical_records):
        if type(medical_records) is int and Record.find_by_id(medical_records):
            self._medical_records = medical_records
        else:
            raise ValueError("Medical records must reference a record in the database")
    
    @classmethod
    def create_table(cls):
        """Create a new table to persist the attributes of Patient instances"""
        sql = """
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                medical_records INTEGER,
                FOREIGN KEY (medical_records) REFERENCES medical_records(id)
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
            INSERT INTO patients (name, age, medical_records)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.name, self.age, self.medical_records))
        CONN.commit()
        self.id = CURSOR.lastrowid
    
    def update(self):
        """Update the table row corresponding to the current Patient instance"""
        sql = """
            UPDATE patients
            SET name = ?, age = ?, medical_records = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.age, self.medical_records, self.id))
        CONN.commit()
    
    def delete(self):
        """Delete the table row corresponding to the current Patient instance"""
        sql = "DELETE FROM patients WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
    
    @classmethod
    def create(cls, name, age, medical_records_id):
        """Create a new Patient instance and persist it to the database"""
        patient = cls(name, age, medical_records_id)
        patient.save()
        return patient
    
    @classmethod
    def instance_from_db(cls, row):
        """Return an Patient object having the attribute values from the table row."""
        
        # check the dictionary for existing instances using the row's primary key
        patient = cls.all.get(row[0])
        if patient:
            # ensure attributes match row values in case local instance was modified
            patient.name = row[1]
            patient.age = row[2]
            patient.medical_records_id = row[3]
        else:
            # create a new instance using row values
            patient = cls(row[1], row[2], row[3], id=row[0])
            cls.all[row[0]] = patient
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
    def find_by_name(cls, name):
        """Return a list of Patient instances with the given name"""
        sql = "SELECT * FROM patients WHERE name = ?"
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None