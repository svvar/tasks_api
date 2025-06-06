from fastapi import APIRouter, Depends, HTTPException, status, Response

from api.schemas.requests import CreateUserRequest, LoginUserRequest
from api.core.security import get_password_argon_hash, argon_verify_password, create_access_token, \
    ACCESS_TOKEN_EXPIRE_MINUTES
from api.schemas.responses import TokenResponse, UserInfoResponse
from database import get_db
from database.operations.user_operations import insert_user, get_user_by_email

router = APIRouter(prefix="/auth")

@router.post("/sign-up", status_code=status.HTTP_201_CREATED, response_model=UserInfoResponse, description="Sign up a new user")
async def create_user(
        user_data: CreateUserRequest,
        db=Depends(get_db)
):
    password_hash = await get_password_argon_hash(user_data.password.get_secret_value())
    try:
        user = await insert_user(db, str(user_data.email), password_hash, user_data.first_name, user_data.last_name)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenResponse, description="Login user")
async def login_user(
        response: Response,
        user_data: LoginUserRequest,
        db=Depends(get_db)
):
    db_user = await get_user_by_email(db, str(user_data.email))
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not await argon_verify_password(user_data.password.get_secret_value(), db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    jwt_token = create_access_token({"id": db_user.id})
    response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return TokenResponse(access_token=jwt_token)

@router.post("/logout", status_code=status.HTTP_200_OK, description="Logout user")
async def logout_user(
        response: Response
):
    response.delete_cookie("access_token")
    return {"detail": "Successfully logged out"}


