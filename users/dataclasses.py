from dataclasses import dataclass
from typing import List


@dataclass
class RoleData:
    name: str



@dataclass
class UserData:
    email: str
    user_type: str
    roles: List[RoleData]
