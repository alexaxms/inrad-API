from medical_history.models import MedicalAppointmentSummary


class MedicalAppointmentSummaryInteractor():
    @staticmethod
    def list():
        return MedicalAppointmentSummary.objects.all()
