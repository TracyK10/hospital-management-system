from models.patient import Patient
from models.medical_record import MedicalRecord
from models.appointment import Appointment

def exit_program():
    print("Goodbye!")
    exit()

def list_patients():
    patients = Patient.get_all()
    for patient in patients:
        print(patient)

def find_patient_by_name():
    first_name = input("Enter the patient's first name: ")
    last_name = input("Enter the patient's last name: ")
    patient = Patient.find_by_name(first_name, last_name)
    print(patient) if patient else print(f'Patient {first_name} {last_name} not found')

def find_patient_by_id():
    id_ = input("Enter the patient's id: ")
    patient = Patient.find_by_id(id_)
    print(patient) if patient else print(f'Patient {id_} not found')

def create_patient():
    first_name = input("Enter the patient's first name: ")
    last_name = input("Enter the patient's last name: ")
    age = int(input("Enter the patient's age: "))
    gender = input("Enter the patient's gender (Male/Female/Other): ")
    try:
        patient = Patient.create(first_name, last_name, age, gender)
        print(f'Success: {patient}')
    except Exception as exc:
        print("Error creating patient: ", exc)

def update_patient():
    id_ = input("Enter the patient's id: ")
    if patient := Patient.find_by_id(id_):
        try:
            first_name = input("Enter the patient's new first name: ")
            patient.first_name = first_name
            last_name = input("Enter the patient's new last name: ")
            patient.last_name = last_name
            age = int(input("Enter the patient's new age: "))
            patient.age = age
            gender = input("Enter the patient's new gender (Male/Female/Other): ")
            patient.gender = gender

            patient.update()
            print(f'Success: {patient}')
        except Exception as exc:
            print("Error updating patient: ", exc)
    else:
        print(f'Patient {id_} not found')

def delete_patient():
    id_ = input("Enter the patient's id: ")
    if patient := Patient.find_by_id(id_):
        patient.delete()
        print(f'Patient {id_} deleted')
    else:
        print(f'Patient {id_} not found')

def list_patient_medical_records():
    patient_id = input("Enter the patient's id: ")
    if patient := Patient.find_by_id(patient_id):
        medical_records = MedicalRecord.find_by_patient_id(patient.id)
        for record in medical_records:
            print(record)
    else:
        print(f'Patient {patient_id} not found')

def list_patient_appointments():
    patient_id = input("Enter the patient's id: ")
    if patient := Patient.find_by_id(patient_id):
        appointments = Appointment.find_by_patient_id(patient.id)
        for appointment in appointments:
            print(appointment)
    else:
        print(f'Patient {patient_id} not found')
