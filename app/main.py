from fastapi import FastAPI
from app.routes import users_router, profiles_router

app = FastAPI(docs_url="/")

app.include_router(users_router, prefix='/users')
app.include_router(profiles_router, prefix='/profiles')
