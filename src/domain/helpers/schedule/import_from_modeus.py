from src.domain.extensions import selenium
from src.infrastructure.repositories import (
    schedule_repository, 
    teacher_repository,
    subject_repository
)

from uuid import UUID
from aiomodeus import AioModeus
from datetime import datetime


async def import_from_modeus_by_id(
    teacher_id: UUID, 
    *,
    subject_id: UUID = None,
    with_counter: bool = False,
    week_count: int = 2
):
    teacher = await teacher_repository.get_by_id(teacher_id)
    if subject_id:
        subject = await subject_repository.get_by_id(subject_id)
        subject_name = subject.name
    else:
        subject_name = None

    FIO = " ".join([
        teacher["second_name"], 
        teacher["first_name"], 
        teacher["third_name"]
    ])

    token = "eyJ4NXQiOiJORGhpTkROalpHTmpORFl6WXpJMVpUQmhZakUxTUdOaE1EQTJOelk0TTJKa1pEQTVaREptTXciLCJraWQiOiJkMGVjNTE0YTMyYjZmODhjMGFiZDEyYTI4NDA2OTliZGQzZGViYTlkIiwiYWxnIjoiUlMyNTYifQ.eyJhdF9oYXNoIjoiMjVYMkdKSVUxNGRRMlQ2Rzd5aHM4QSIsInN1YiI6ImRhZjJhNGQwLWQ4OTctNDY0OC05NDQxLTdkZjI0YTliMzM5ZCIsImF1ZCI6WyIzQ3VGM0ZzTnlSTGlGVmowSWwyZkl1amZ0dzBhIl0sImF6cCI6IjNDdUYzRnNOeVJMaUZWajBJbDJmSXVqZnR3MGEiLCJFeHRlcm5hbFBlcnNvbklkIjoiYzRjODYxZmYtZDgyOS00M2IyLWJkNmYtOTU1ZDU1MDVkOTdkIiwiaXNzIjoiaHR0cHM6XC9cL3VyZnUtYXV0aC5tb2RldXMub3JnXC9vYXV0aDJcL3Rva2VuIiwicHJlZmVycmVkX3VzZXJuYW1lIjoi0KHQvNC40YDQvdC-0LIg0JXQstCz0LXQvdC40Lkg0KHQtdGA0LPQtdC10LLQuNGHIiwiZXhwIjoxNzM4NTM1ODM2LCJub25jZSI6IlJIQk5iMWcwV1dGcmFuTlFaSGR1YVRWVE5DMTNXakJ6VUhGTVVXY3RjelItU1dGeVZ6WTJTbTFJT1VSUyIsImlhdCI6MTczODQ0OTQzNiwicGVyc29uX2lkIjoiYmIyNDc4ZTgtMDVhYi00OGQyLTkxYjYtZjQwZDU1MzI3YWRkIn0.Eo4gl3hVyn8z0zsZmK9GFoWXLBtdXPS3WImRXKLy6nbb2K9_XsX6MZFz7YD4tlYlwmMlUkqldDYH-_4MgsaDeBA2as--QPliyPXUWW7EyM8QgJSJ7mfUnXlvHOYcBpGPt2FphB2hg1OEwhxpfoDZCvsPaFGy7FNm89Lbwqaj8AfNs_d66bBRlQLw6NN9wUBmoCfOWsR1nG6rxVOoFPN9cxT8FzRyI3QSeX5-OxsHWWTnxFNwslmiSKR-MruYgtJDB_zatqfi169DD0v2aB2Q7YusfwNjh1Oftbod-xNkqGvoRjXOR_JSZQd515uBO38oJHGfmGy4FEH9XNteHwQ9hw" # selenium.auth()
    aim = AioModeus(token)  
    
    if week_count == 1:
        schedules = await aim.get_schedule_for_week_by_teacher_name(
            FIO,
            subject_name=subject_name,
            with_counter=with_counter,
            custom_date=datetime(2025, 2, 25)
        )

        result = await schedule_repository.get_exists_by_subject_id(
            schedules, 
            subject_id
        )
    else:
        schedules = await aim.get_schedule_for_two_week_by_teacher_name(
            FIO,
            subject_name=subject_name,
            with_counter=with_counter,
            custom_date=datetime(2025, 2, 25)
        )

        result = await schedule_repository.get_exists_by_subject_id(
            schedules[0], 
            subject_id
        )

        result.extend(
            await schedule_repository.get_exists_by_subject_id(
                schedules[1], 
                subject_id
            )
        )
    
    return result
    
    
