from fastapi import APIRouter, Depends
from schemas import Todo, TodoBody, SuccessMsg
from fastapi import Request, Response, HTTPException
from fastapi.encoders import jsonable_encoder
from database import db_create_todo, db_get_single_todo, db_get_todos, db_update_todo, db_delete_todo
from starlette.status import HTTP_201_CREATED
from typing import List
from fastapi_csrf_protect import CsrfProtect
from auth_utils import AuthJwtCsrf

router = APIRouter()
auth = AuthJwtCsrf()

@router.post('/api/todo', response_model=Todo)
async def create_todo(request: Request, response: Response, data: TodoBody, csrf_protect: CsrfProtect = Depends()):
    new_token = auth.verify_csrf_update_jwt(request, csrf_protect, request.headers)
    todo = jsonable_encoder(data)
    res = await db_create_todo(todo)
    response.status_code = HTTP_201_CREATED
    response.set_cookie(
        key='access_token', value=f'Bearer {new_token}', samesite='none', secure=True, httponly=True
    )
    if res:
        return res
    return HTTPException(
        status_code=400,
        detail="Create task failed",
    )
    

@router.get('/api/todo', response_model=List[Todo])
async def get_todos(request: Request):
    auth.verify_jwt(request)
    res = await db_get_todos()
    return res


@router.get('/api/todo/{id}', response_model=Todo)
async def get_single_todo(id: str, request: Request, response: Response):
    new_token, _ = auth.verify_update_jwt(request)
    res = await db_get_single_todo(id)
    response.set_cookie(
        key='acces_token', value=f'Bearer {new_token}', samesite='none', secure=True, httponly=True
    )
    if res:
        return res
    raise HTTPException(
        status_code=404, detail="Task of ID: {id} does not exist")
    

@router.put('/api/todo/{id}', response_model=Todo)
async def update_todo(id: str, data: TodoBody, request: Request, response: Response, csrf_protect: CsrfProtect = Depends()):
    new_token = auth.verify_csrf_update_jwt(request, csrf_protect, request.headers)
    todo = jsonable_encoder(data)
    res = await db_update_todo(id, todo)
    response.set_cookie(
        key='access_token', value=f'Bearer {new_token}', samesite='none', secure=True, httponly=True
    )
    if res :
        return res
    raise HTTPException(
        status_code=404, detail="Update task failed")
    

@router.delete('/api/todo/{id}', response_model=SuccessMsg)
async def delete_todo(id: str, request: Request, response: Response, csrf_protect: CsrfProtect = Depends()):
    new_token = auth.verify_csrf_update_jwt(request, csrf_protect, request.headers)
    res = await db_delete_todo(id)
    response.set_cookie(
        key='access_token', value=f'Bearer {new_token}', samesite='none', secure=True, httponly=True
    )
    if res:
        return {"message": "Delete task successfully"}
    raise HTTPException(
        status_code=404, detail="Delete task failed")
    