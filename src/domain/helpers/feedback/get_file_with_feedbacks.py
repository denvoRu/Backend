import pandas as pd

from typing import List
from io import BytesIO


async def get_excel_file_with_feedbacks(
    feedback_data: List[dict], 
    extra_fields_data: List[dict]
):
    """
    Gets needed data with feedbacks and creates a xlsx file with pandas
    :param feedback_data: data of feedbacks
    :param extra_fields_data: data of extra fields that chosen for feedback form
    """
    result_df = pd.DataFrame(feedback_data)

    if extra_fields_data and len(extra_fields_data) > 0:
        extra_fields_df = pd.DataFrame(extra_fields_data)

        extra_fields_pivot = (
            extra_fields_df
            .pivot(
                values="answer",  # Столбец с ответами
                index="id",  # Столбец для связи
                columns="question"  # Столбец с вопросами
            )
            .rename({"feedback_id": "id"})  # Переименовываем для связи
        )

        result_df = result_df.join(extra_fields_pivot, on="id", how="left")
    
    output = BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        result_df.to_excel(writer, sheet_name="Отзывы", index=False)
        worksheet = writer.sheets["Отзывы"]  # pull worksheet object
        for idx, _ in enumerate(result_df):  # loop through all columns
            worksheet.set_column(idx, idx, 50)  # set column width

    output.seek(0)

    chunk_size = 1024 
    while chunk := output.read(chunk_size):
        yield chunk
