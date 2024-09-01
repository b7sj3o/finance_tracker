from .config import dp, bot, API_BASE_URL
from .utils import (
    generate_csv_report,
    get_all_users,
    get_user,
    check_password,
    register_user,
)
from .db.models import db_session, User, Finance
from .handlers import setup_handlers

setup_handlers()

if __name__ == "__main__":
    dp.run_polling(bot)
