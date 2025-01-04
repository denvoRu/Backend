import pandas as pd

from typing import List
from io import BytesIO


async def get_excel_file_with_feedbacks(
    feedback_data: List[dict], 
    extra_fields_data: List[dict]
):
    feedback_df = pd.DataFrame(feedback_data)
    extra_fields_df = pd.DataFrame(extra_fields_data)

    extra_fields_pivot = (
        extra_fields_df
        .pivot(
            values="answer",  # Столбец с ответами
            index="feedback_id",  # Столбец для связи
            columns="question"  # Столбец с вопросами
        )
        .rename({"feedback_id": "id"})  # Переименовываем для связи
    )

    result_df = feedback_df.join(extra_fields_pivot, on="id", how="left")
    output = BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        result_df.to_excel(writer, sheet_name="Отзывы")

    output.seek(0)

    chunk_size = 1024 
    while chunk := output.read(chunk_size):
        yield chunk
