from typing import List


def get_unique_lessons(lessons: List) -> List: 
    unique_lessons = []
    for lesson in lessons:
        lesson_name = lesson["lesson_name"]
        lesson_date = lesson["date"]
        lesson_start_time = lesson["start_time"]
        lesson_date_end_time = lesson["end_time"]

        if any(
            filter(
                (lambda x: 
                    x["lesson_name"] == lesson_name and 
                    x["date"] == lesson_date and 
                    x["start_time"] == lesson_start_time and 
                    x["end_time"] == lesson_date_end_time
                ), 
                unique_lessons
            )
        ):
            continue

        unique_lessons.append(lesson)

    return unique_lessons