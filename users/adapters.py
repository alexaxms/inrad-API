from users.dataclasses import RoleData, UserData
from users.models import Role, User


def role_model_to_data(role: Role) -> RoleData:
    return RoleData(name=role.name)


def user_model_to_data(user: User) -> UserData:
    return UserData(
        email=user.email,
        user_type=user.user_type,
        roles=[role_model_to_data(role) for role in user.user_roles.all()]
    )
