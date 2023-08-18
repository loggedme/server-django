import uuid

from user.models import User


def get_user(id_or_handle: str) -> User:
    try:
        uuid_obj = uuid.UUID(id_or_handle)
        return User.objects.get(id=uuid_obj)
    except ValueError:
        return User.objects.get(handle=id_or_handle)
    raise User.DoesNotExist
