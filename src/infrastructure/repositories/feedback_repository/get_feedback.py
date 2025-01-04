from src.infrastructure.database.extensions.row_to_dict import row_to_dict
from src.infrastructure.models.page_response import PageResponse
from src.infrastructure.models.feedback_with_fields import (
    FeedbackWithExtraFieldsResponse
)
from src.infrastructure.database import (
    Feedback, ExtraField, ExtraFieldSetting, db
)

from sqlalchemy import select, distinct, text, desc as order_desc, func
from typing import Tuple, List
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
    try:
        feedback_stmt = select(
            Feedback.id, 
            Feedback.student_name,
            Feedback.mark,
            Feedback.chosen_markers,
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
            ExtraField.value.alias("answer"), 
            ExtraFieldSetting.extra_field_name.alias("question")
        ).join(
            ExtraFieldSetting, 
            ExtraFieldSetting.id == ExtraField.extra_field_setting_id
        ).where(
            ExtraField.feedback_id.in_(feedbacks_id),
        )

        extra_fields = await db.execute(extra_fields_stmt)
        extra_fields = list(row_to_dict(i) for i in extra_fields.all())

        feddbacks_with_fields = FeedbackWithExtraFieldsResponse(feedbacks)

        total_page = ceil(total_record / limit)

        return PageResponse(
            page_number=page,
            page_size=limit,
            total_record=total_record,
            total_pages=total_page,
            content=feddbacks_with_fields.to_dict(),
        )
    except Exception as e:
        await db.commit_rollback()
        raise Exception(str(e))


async def get_all_for_excel(lesson_id: UUID) -> Tuple[List[dict], List[dict]]:
    try:
        feedback_stmt = select(
            Feedback.id, 
            Feedback.student_name,
            Feedback.mark,
            Feedback.chosen_markers,
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
            ExtraField.value.alias("answer"), 
            ExtraFieldSetting.extra_field_name.alias("question")
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
    stmt = select(Feedback.mark ,func.count(Feedback.mark)).select_from(Feedback).where(
        Feedback.lesson_id == lesson_id,
        Feedback.is_disabled == False
    ).group_by(Feedback.mark)

    executed = await db.execute(stmt)

    return { str(i): j for i, j in executed.all() }


async def get_members(lesson_id: UUID):
    stmt = distinct(select(Feedback.student_name).where(
        Feedback.lesson_id == lesson_id,
        Feedback.student_name != "",
        Feedback.is_disabled == False
    ))

    names = await db.execute(stmt)
    return list([i[0] for i in names.all()])
