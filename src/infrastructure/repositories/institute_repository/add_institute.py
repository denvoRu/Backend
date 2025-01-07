from src.infrastructure.database import Institute, add_instance


async def add(
    institute_name: str,
    institute_short_name: str,
    institute_address: str
):
    """
    Adds an institute to the database.
    :param institute_name: name of the institute
    :param institute_short_name: short name of the institute
    :param institute_address: address of the institute
    """
    institute = Institute(
        name=institute_name,
        short_name=institute_short_name,
        rating=0,
        address=institute_address,
    )

    await add_instance(institute)
