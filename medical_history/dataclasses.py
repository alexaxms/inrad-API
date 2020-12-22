from dataclasses import dataclass
from typing import List, Optional

from users.dataclasses import UserData


@dataclass
class PatientData:
    name: str
    last_name: str
    phone_number: str


@dataclass
class MedicalAppointmentImageData:
    img_link: str


@dataclass
class MedicalAppointmentSummaryData:
    summary: str
    user: UserData
    patient: PatientData
    images: Optional[List[MedicalAppointmentImageData]]
