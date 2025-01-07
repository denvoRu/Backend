import pandas as pd

from typing import List
from io import BytesIO


async def get_excel_file_with_members(members: List[str]):
    """
    Gets needed data with members and creates a xlsx file with pandas
    :param members: needed members
    """
    df = pd.DataFrame({
        "Участники": members
    })

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Посещаемость")

    output.seek(0)

    chunk_size = 1024 
    while chunk := output.read(chunk_size):
        yield chunk