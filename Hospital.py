from abc import ABC, abstractmethod
from datetime import datetime

class InvalidPatientIdException(Exception): pass
class NoDoctorAvailableException(Exception): pass

class Person(ABC):
    def __init__(self, id, name, age):
        self.id, self.name, self.age = id, name, age
    @abstractmethod
    def role(self): pass
    def __str__(self): return f"{self.role()}[{self.id}, {self.name}, {self.age}]"

class Patient(Person):
    def __init__(self, id, name, age, ailment):
        super().__init__(id, name, age)
        self.ailment, self.admitted = ailment, False
    def role(self): return "Patient"

class Doctor(Person):
    def __init__(self, id, name, age, specialization):
        super().__init__(id, name, age)
        self.specialization, self.available = specialization, True
    def role(self): return "Doctor"


class Appointment:
    counter = 1
    def __init__(self, patient, doctor, when):
        self.id = f"A{Appointment.counter}"; Appointment.counter += 1
        self.patient, self.doctor, self.when = patient, doctor, when
    def __str__(self): return f"Appt[{self.id}] {self.patient.name} with Dr.{self.doctor.name} at {self.when}"


class HospitalOperations(ABC):
    @abstractmethod
    def admit(self, patient): pass
    @abstractmethod
    def schedule(self, patient_id, specialization, when): pass
    @abstractmethod
    def bill(self, patient_id): pass


class Hospital(HospitalOperations):
    def __init__(self):
        self.patients, self.doctors, self.appointments, self.bills = {}, {}, {}, {}
    def register(self, person):
        if isinstance(person, Patient):
            self.patients[person.id] = person
            self.bills[person.id] = []
        else:
            self.doctors[person.id] = person
    def admit(self, patient):
        if patient.id not in self.patients: raise InvalidPatientIdException
        patient.admitted = True
        self.bills[patient.id].append(("Admission", 5000))
        print(f"Admitted {patient.name}")
    def schedule(self, pid, spec, when):
        if pid not in self.patients: raise InvalidPatientIdException
        for d in self.doctors.values():
            if d.specialization == spec and d.available:
                appt = Appointment(self.patients[pid], d, when)
                self.appointments[appt.id] = appt
                d.available = False
                self.bills[pid].append(("Appointment", 1000))
                print(appt)
                return appt
        raise NoDoctorAvailableException
    def bill(self, pid):
        if pid not in self.bills: raise InvalidPatientIdException
        total = sum(cost for _, cost in self.bills[pid])
        print(f"Bill for {pid}: {self.bills[pid]}, Total={total}")
        return total


if __name__ == "__main__":
    h = Hospital()
    d = Doctor("D1","Smith",45,"Cardiology"); h.register(d)
    p = Patient("P1","Alice",30,"Chest Pain"); h.register(p)
    try:
        h.admit(p)
        h.schedule("P1","Cardiology",datetime(2025,9,28,10))
        h.bill("P1")
    except Exception as e: print("Error:", e)
