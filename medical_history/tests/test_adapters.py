from model_bakery import baker

from medical_history.adapters import patient_model_to_data, img_model_to_data, medical_appointment_summary_model_to_data


def test_patient_model_to_data():
    patient_model = baker.prepare("medical_history.Patient")
    patient_data = patient_model_to_data(patient_model)
    assert patient_model.name == patient_data.name
    assert patient_model.last_name == patient_data.last_name
    assert patient_model.phone_number == patient_data.phone_number


def test_img_model_to_data():
    img_model = baker.prepare("medical_history.MedicalAppointmentImage")
    img_data = img_model_to_data(img_model)
    assert img_model.img_link == img_data.img_link


def test_medical_appointment_summary_model_to_data():
    medical_appointment_summary_model = baker.prepare("medical_history.MedicalAppointmentSummary")
    medical_appointment_summary_data = medical_appointment_summary_model_to_data(medical_appointment_summary_model)
    assert medical_appointment_summary_model.summary == medical_appointment_summary_data.summary
    assert patient_model_to_data(medical_appointment_summary_model.patient) == medical_appointment_summary_data.patient
    assert len(medical_appointment_summary_model.images.all()) == len(medical_appointment_summary_data.images)
