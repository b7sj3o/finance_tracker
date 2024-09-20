import csv
import bcrypt
from db import User, db_session


def get_user(username: str):
    """
    Retrieves a user from the database by their username.

    Args:
        username (str): The username of the user to retrieve.

    Returns:
        User: The user object if found, or None if no user with the given username exists.
    """
    return db_session.query(User).filter_by(username=username).first()


def register_user(username: str, email: str, password: str):
    """
    Registers a new user in the database with the given username, email, and password.

    The password is hashed before storing it in the database.

    Args:
        username (str): The username for the new user.
        email (str): The email address for the new user.
        password (str): The password for the new user.

    Returns:
        None
    """
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    new_user = User(username=username, email=email, password_hash=password_hash)
    db_session.add(new_user)
    db_session.commit()


def check_password(user: User, password: str):
    """
    Checks if the provided password matches the hashed password of the user.

    Args:
        user (User): The user object whose password is being checked.
        password (str): The password to check.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8"))


def login_user(username: str, password: str):
    """
    Attempts to log in a user with the given username and password.

    Args:
        username (str): The username of the user trying to log in.
        password (str): The password of the user trying to log in.

    Returns:
        bool: True if the username and password match a user in the database, False otherwise.
    """
    user = get_user(username)
    if user and check_password(user, password):
        return True
    return False


def get_all_users():
    """
    Retrieves all users from the database.

    Returns:
        list: A list of User objects representing all users in the database.
    """
    return db_session.query(User).all()


def generate_csv_report():
    """
    Generates a CSV report of all users in the database and saves it to a file.

    The CSV file includes the user's ID, username, email, and a placeholder for balance.

    Returns:
        str: The path to the generated CSV report file.
    """
    with open("report.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Username", "Email", "Balance"])
        for user in get_all_users():
            writer.writerow([user.id, user.username, user.email, "Balance Placeholder"])
    return "report.csv"
