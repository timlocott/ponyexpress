from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.routers.users import user_router
from backend.routers.chats import chat_router
from backend.auth import auth_router
from backend.database import EntityNotFoundException, DuplicateEntityException, create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Pony Express API",
    description="Chat application",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(chat_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], # change this as appropriate for your setup
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(EntityNotFoundException)
def handle_entity_not_found(
    _request: Request, 
    exception: EntityNotFoundException) -> JSONResponse:
    return JSONResponse(
            status_code=404,
            content={
                "detail": {
                    "type": "entity_not_found",
                    "entity_name": exception.entity_name,
                    "entity_id": exception.entity_id,
                }
            }
        )

@app.exception_handler(DuplicateEntityException)
def handle_duplicate_entity(
    _request: Request,
    exception: DuplicateEntityException) -> JSONResponse:
    return JSONResponse(
            status_code=422,
            content={
                "detail": {
                    "type": "duplicate_entity",
                    "entity_name": exception.entity_name,
                    "entity_id": exception.entity_id,
                }
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
 