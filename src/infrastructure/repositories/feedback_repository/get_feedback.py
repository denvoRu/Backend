from src.infrastructure.database.extensions.row_to_dict import row_to_dict
from src.infrastructure.models.tag import BadTag, GoodTag
from src.infrastructure.models.page_response import PageResponse
from src.infrastructure.models.feedback_with_fields import (
    FeedbackWithExtraFieldsResponse
)
from src.infrastructure.database import (
    Feedback, Lesson, StudyGroup, Subject, ExtraField, ExtraFieldSetting, db
)

from sqlalchemy import distinct, select, text, desc as order_desc, func
from typing import Tuple, Union, List, Dict, get_args
from math import ceil
from uuid import UUID


async def get_all(  
    lesson_id: UUID,
    page, 
    limit, 
    sort, 
    search, 
    desc
):
    """
    Gets all feedbacks
    :param lesson_id: lesson of feedback
    :param page: current page
    :param limit: number of feedbacks
    :param sort: sort order
    :param search: search string
    :param desc: descending/ascending sort
    """
    feedback_stmt = select(
        Feedback.id, 
        Feedback.mark,
        Feedback.tags,
        Feedback.comment,
        Feedback.created_at
    ).where(
        Feedback.lesson_id == lesson_id,
        Feedback.is_disabled == False
    )

    if sort is not None and sort != "":
        sorted_columns = map(text, sort.split(","))
        if desc == 1:
            sorted_columns = map(order_desc, sorted_columns)

        feedback_stmt = feedback_stmt.order_by(*sorted_columns)

    # count query
    count_query = select(func.count(1)).select_from(feedback_stmt)
    total_record = (await db.execute(count_query)).scalar() or 0

    feedback_stmt = feedback_stmt.offset((page - 1) * limit).limit(limit)


    feedbacks = await db.execute(feedback_stmt)
    feedbacks = list(row_to_dict(i) for i in feedbacks.all())

    feedbacks_id = [feedback["id"] for feedback in feedbacks]

    extra_fields_stmt = select(
        ExtraField.feedback_id,
        ExtraField.value.label("answer"), 
        ExtraFieldSetting.extra_field_name.label("question")
    ).select_from(ExtraField).join(
        ExtraFieldSetting, 
        ExtraFieldSetting.id == ExtraField.extra_field_setting_id
    ).where(
        ExtraField.feedback_id.in_(feedbacks_id),
    )

    extra_fields = await db.execute(extra_fields_stmt)
    extra_fields = list(row_to_dict(i) for i in extra_fields.all())

    feddbacks_with_fields = FeedbackWithExtraFieldsResponse(
        feedbacks, 
        extra_fields
    )

    total_page = ceil(total_record / limit)

    return PageResponse(
        page_number=page,
        page_size=limit,
        total_record=total_record,
        total_pages=total_page,
        content=feddbacks_with_fields.to_dict(),
    )


async def get_all_for_excel(lesson_id: UUID) -> Tuple[List[dict], List[dict]]:
    """
    Gets all feedbacks for xlsx file
    :param lesson_id: lesson of feedback
    """
    try:
        feedback_stmt = select(
            Feedback.id,
            Feedback.mark,
            Feedback.tags,
            Feedback.comment,
            Feedback.created_at
        ).where(
            Feedback.lesson_id == lesson_id,
            Feedback.is_disabled == False
        )


        feedbacks = await db.execute(feedback_stmt)
        feedbacks = list(row_to_dict(i) for i in feedbacks.all())

        feedbacks_id = [feedback["id"] for feedback in feedbacks]

        extra_fields_stmt = select(
            ExtraField.feedback_id,
            ExtraField.value.label("answer"), 
            ExtraFieldSetting.extra_field_name.label("question")
        ).join(
            ExtraFieldSetting, 
            ExtraFieldSetting.id == ExtraField.extra_field_setting_id
        ).where(
            ExtraField.feedback_id.in_(feedbacks_id),
        )

        extra_fields = await db.execute(extra_fields_stmt)
        extra_fields = list(row_to_dict(i) for i in extra_fields.all())

        return (feedbacks, extra_fields)

    except Exception as e:
        await db.commit_rollback()
        raise Exception(str(e))


async def get_statistics(lesson_id: UUID):
    """
    Gets statistics for all feedbacks
    :param lesson_id: lesson of feedbacks
    """
    subject_stmt = select(
        Subject.id, 
        Subject.name, 
        Subject.rating
    ).select_from(Lesson).join(
        StudyGroup,
        StudyGroup.id == Lesson.study_group_id
    ).join(
        Subject, 
        StudyGroup.subject_id == Subject.id 
    ).where(Lesson.id == lesson_id)
    marks = select(Feedback.mark ,func.count(Feedback.mark).label("count")).select_from(Feedback).where(
        Feedback.lesson_id == lesson_id,
        Feedback.is_disabled == False
    ).group_by(Feedback.mark)
    
    subject = (await db.execute(subject_stmt)).one()
    print(subject)
    marks = await db.execute(marks)

    marks_dict = { str(i): j for i, j in marks.all() }
    tags = await get_tags(lesson_id)

    bad_tags_with_count = get_tags_by_literal(tags, BadTag)
    good_tags_with_count = get_tags_by_literal(tags, GoodTag)

    return {
        "subject_id": subject[0],
        "subject_name": subject[1],
        "subject_rating": subject[2],
        "marks": marks_dict,
        "bad_tags": bad_tags_with_count,
        "good_tags": good_tags_with_count
    }


async def get_tags(lesson_id: UUID) -> Dict[str, int]:
    stmt = select(
        text("unnest(string_to_array(tags, ', ')) AS tag_name"),
        text("array_length(string_to_array(tags, ', '), 1) AS tag_count")
    ).select_from(Feedback).where(
        Feedback.lesson_id == lesson_id,
        Feedback.is_disabled == False
    ).order_by(order_desc(text("tag_count")))

    tags = await db.execute(stmt)
    return { str(i): j for i, j in tags.all() }


async def get_members(lesson_id: UUID):
    stmt = select(distinct(Feedback.student_name), Feedback.created_at).where(
        Feedback.lesson_id == lesson_id,
        Feedback.student_name != "",
        Feedback.is_disabled == False
    )

    names = await db.execute(stmt)
    return [{
        "name": i[0],
        "created_at": i[1]
    } for i in names.all()]


def get_tags_by_literal(tags: Dict[str, int], literal: Union[GoodTag, BadTag]):
    return [
        {
            "name": i,
            "count": tags[i]
        } for i in tags if i in get_args(literal)
    ]
            