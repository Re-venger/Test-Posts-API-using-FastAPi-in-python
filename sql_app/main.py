from fastapi import FastAPI
from . import models
from .database import engine, get_db
from .utils import *
from .routers import posts, users, auth

# create an access for the model we created
models.Base.metadata.create_all(bind=engine)

#* Fast API instance
app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

    

















