from typing import List

from medical_history.dataclasses import MedicalAppointmentSummaryData
from medical_history.interactors import MedicalAppointmentSummaryInteractor


def list_medical_appointment_summaries() -> List[MedicalAppointmentSummaryData]:
    return [MedicalAppointmentSummaryData.from_model(medical_appointment_summary) for medical_appointment_summary in
            MedicalAppointmentSummaryInteractor.list()]
