from .config import dp, bot
from .db.models import db_session, User, Finance
from .handlers import setup_handlers

setup_handlers()

if __name__ == "__main__":
    dp.run_polling(bot)
