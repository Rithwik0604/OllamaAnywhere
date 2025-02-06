from contextlib import asynccontextmanager

import sys

from dotenv import load_dotenv
from fastapi import FastAPI

import database

load_dotenv()


async def perform_checks():
    database.create_tables()


@asynccontextmanager
async def lifespan(app: FastAPI):
    perform_checks()
    yield
    print("server go boom")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello world"}


@app.get("/get-users")
async def get_users():
    """returns all users. Returns empty list if none

    Returns:
        list[User]: returns a list of dictionaries containing users
    """
    users = database.get_users()
    return [user for user in users]


if __name__ == "__main__":
    # to reset the database for a fresh start
    if len(sys.argv) > 1 and sys.argv[1] == "reset":
        database.setup()
        database.reset_db()
        print("Database reset. Exiting...")
        exit(0)
