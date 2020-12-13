from dataclasses import dataclass
from typing import List

from users.models import Role, User


@dataclass
class RoleData:
    name: str

    @staticmethod
    def from_model(role: Role):
        return RoleData(name=role.name)


@dataclass
class UserData:
    email: str
    user_type: str
    roles: List[RoleData]

    @staticmethod
    def from_model(user: User):
        return UserData(
            email=user.email,
            user_type=user.user_type,
            roles=[RoleData.from_model(role) for role in user.user_roles]
        )
