from fastapi import APIRouter
from schemas import Todo, TodoBody
from fastapi import Request, Response, HTTPException
from fastapi.encoders import jsonable_encoder
from database import db_create_todo
from starlette.status import HTTP_201_CREATED

router = APIRouter()

@router.post('/api/todo', response_model=Todo)
async def create_todo(request: Request, response: Response, data: TodoBody):
    todo = jsonable_encoder(data)
    res = await db_create_todo(todo)
    response.status_code = HTTP_201_CREATED
    if res:
        return res
    return HTTPException(
        status_code=400,
        detail="Create task failed",
    )
    