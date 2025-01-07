from src.infrastructure.database import has_instance, Feedback


async def has_feedback_by_created_at(dto: dict):
    """
    Checks that some feedback exists
    :param dto: data of feedback to find
    """
    return await has_instance(
        Feedback, 
        (Feedback.comment == dto["comment"],
        Feedback.created_at == dto["created_at"],
        Feedback.chosen_markers == dto["chosen_markers"],
        Feedback.mark == dto["mark"])
    )
