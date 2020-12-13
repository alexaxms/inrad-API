from dataclasses import dataclass
from typing import List, Optional

from medical_history.models import Patient, MedicalAppointmentImage, MedicalAppointmentSummary
from users.dataclasses import UserData


@dataclass
class PatientData:
    name: str
    last_name: str
    phone_number: str

    @staticmethod
    def from_model(patient: Patient):
        return PatientData(
            name=patient.name,
            last_name=patient.last_name,
            phone_number=patient.phone_number
        )


@dataclass
class MedicalAppointmentImageData:
    img_link: str

    @staticmethod
    def from_model(medical_appointment_image: MedicalAppointmentImage):
        return MedicalAppointmentImageData(
            img_link=medical_appointment_image.img_link
        )


@dataclass
class MedicalAppointmentSummaryData:
    summary: str
    user: UserData
    patient: PatientData
    images: Optional[List[MedicalAppointmentImageData]]

    @staticmethod
    def from_model(medical_appointment_summary: MedicalAppointmentSummary):
        return MedicalAppointmentSummaryData(
            summary=medical_appointment_summary.summary,
            user=UserData.from_model(medical_appointment_summary.user),
            patient=PatientData.from_model(medical_appointment_summary.patient),
            images=[MedicalAppointmentImageData.from_model(image) for image in medical_appointment_summary.images]
        )
