from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import models
from config import settings
from controllers.authcontrollers import auth
from utils.database import engine

app = FastAPI()

origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_tables():
    models.Base.metadata.create_all(bind=engine)


@app.on_event("startup")
async def startup():

    create_tables()
    print("Application running...")


@app.on_event("shutdown")
async def shutdown():

    print("Shutdown completed")



@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(auth.router, tags=['Auth'])
