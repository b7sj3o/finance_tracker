from config import dp
from db import db_session, Finance, User
from .routes import router

def setup_handlers():
    dp.include_router(router)
