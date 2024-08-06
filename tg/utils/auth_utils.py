import bcrypt
from db.models import User, db_session

def get_user(username: str):
    return db_session.query(User).filter_by(username=username).first()

def register_user(username: str, email: str, password: str):
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(username=username, email=email, password_hash=password_hash)
    db_session.add(new_user)
    db_session.commit()

def check_password(user: User, password: str):
    return bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8'))
