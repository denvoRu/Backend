def user_to_save_dict(user):
    return {
        "id": user.id,
        "first_name": user.first_name,
        "second_name": user.second_name,
        "third_name": user.third_name,
        "email": user.email
    }
