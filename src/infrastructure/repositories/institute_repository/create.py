from src.infrastructure.database import db, commit_rollback, Institute

async def create_institute(
    institute_name: str,
    institute_short_name: str,
    institute_address: str
):
    institute = Institute(
        name=institute_name,
        short_name=institute_short_name,
        rating=0,
        address=institute_address,
    )

    db.add(institute)
    await commit_rollback()