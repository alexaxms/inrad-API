from model_bakery import baker

from users.adapters import role_model_to_data, user_model_to_data


def test_role_model_to_data():
    role_model = baker.prepare("users.Role")
    role_data = role_model_to_data(role_model)
    assert role_model.name == role_data.name


def test_user_model_to_data():
    user_model = baker.prepare("users.User")
    user_data = user_model_to_data(user_model)
    assert user_model.email == user_data.email
    assert user_model.user_type == user_data.user_type
    assert len(user_model.user_roles.all()) == len(user_data.roles)
