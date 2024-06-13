from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from .base_model import Base
from database.db import engine

Session = sessionmaker(bind=engine)

class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True)
    appointment_date = Column(DateTime, nullable=False)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False)
    notes = Column(String)

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")

    @classmethod
    def create(cls, appointment_date, patient_id, doctor_id, notes=None):
        session = Session()
        appointment = cls(appointment_date=appointment_date, patient_id=patient_id, doctor_id=doctor_id, notes=notes)
        session.add(appointment)
        session.commit()
        session.close()
        return appointment

    @classmethod
    def delete(cls, appointment_id):
        session = Session()
        appointment = session.query(cls).get(appointment_id)
        if appointment:
            session.delete(appointment)
            session.commit()
        session.close()
        return appointment

    @classmethod
    def get_all(cls):
        session = Session()
        appointments = session.query(cls).all()
        session.close()
        return appointments

    @classmethod
    def find_by_id(cls, appointment_id):
        session = Session()
        appointment = session.query(cls).get(appointment_id)
        session.close()
        return appointment

    def __repr__(self):
        return f"Appointment(id={self.id}, appointment_date={self.appointment_date}, patient_id={self.patient_id}, doctor_id={self.doctor_id}, notes={self.notes})"