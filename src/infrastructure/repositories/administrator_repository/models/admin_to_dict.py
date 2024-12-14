from src.infrastructure.database.models.administrator import Administrator

def admin_to_save_dict(admin: Administrator):
    return {
        "id": admin.id,
        "first_name": admin.first_name,
        "second_name": admin.second_name,
        "third_name": admin.third_name,
        "email": admin.email
    }