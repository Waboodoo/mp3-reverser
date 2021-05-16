from uuid import UUID


def is_valid_uuid4(uuid):
    try:
        uuid_obj = UUID(uuid, version=4)
    except ValueError:
        return False
    return str(uuid_obj) == uuid
