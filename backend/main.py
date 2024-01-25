from fastapi import FastAPI

from backend.routers.users import user_router as user_router

app = FastAPI()

app.include_router(user_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
 