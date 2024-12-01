from fastapi import APIRouter, Depends, Response

router = APIRouter()


@router.post("/login", description="Authorizes the user")
async def login():
    return "Authorization completed"
