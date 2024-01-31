from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.routers.users import user_router as user_router
from backend.database import EntityNotFoundException, DuplicateEntityException

app = FastAPI(
    title="Pony Express API",
    description="Chat application",
    version="0.1.0"
)

app.include_router(user_router)

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
 