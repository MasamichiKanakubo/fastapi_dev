from fastapi import APIRouter
from fastapi import Request, Response
from fastapi.encoders import jsonable_encoder
from schemas import UserBody, SuccessMsg , UserInfo
from database import(
    db_signup,
    db_login
)
from auth_utils import AuthJwtCsrf

router = APIRouter()
auth = AuthJwtCsrf()


@router.post('/api/register', response_model=UserInfo)
async def signup(user: UserBody):
    user = jsonable_encoder(user)
    new_user = await db_signup(user)
    return new_user


@router.post('/api/login', response_model=SuccessMsg)
async def login(user: UserBody, response: Response):
    user = jsonable_encoder(user)
    token = await db_login(user)
    response.set_cookie(
        key='access_token', value=f"Bearer {token}", samesite='none', secure=True, httponly=True
    )
    return {'message': 'Successfully logged in'}