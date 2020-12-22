from medical_history.dataclasses import PatientData, MedicalAppointmentImageData, MedicalAppointmentSummaryData
from medical_history.models import MedicalAppointmentImage, Patient, MedicalAppointmentSummary
from users.adapters import user_model_to_data


def patient_model_to_data(patient: Patient) -> PatientData:
    return PatientData(
        name=patient.name,
        last_name=patient.last_name,
        phone_number=patient.phone_number
    )


def img_model_to_data(medical_appointment_image: MedicalAppointmentImage) -> MedicalAppointmentImageData:
    return MedicalAppointmentImageData(
        img_link=medical_appointment_image.img_link
    )


def medical_appointment_summary_model_to_data(
        medical_appointment_summary: MedicalAppointmentSummary) -> MedicalAppointmentSummaryData:
    return MedicalAppointmentSummaryData(
        summary=medical_appointment_summary.summary,
        user=user_model_to_data(medical_appointment_summary.user),
        patient=patient_model_to_data(medical_appointment_summary.patient),
        images=[img_model_to_data(image) for image in medical_appointment_summary.images.all()]
    )
