from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class User(Base):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The user's username, must be unique.
        email (str): The user's email address, must be unique.
        password_hash (str): A hashed version of the user's password.

    Relationships:
        finances (list of Finance): List of financial records associated with the user.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    finances = relationship("Finance", order_by="Finance.id", back_populates="user")


class Finance(Base):
    """
    Represents a financial record associated with a user.

    Attributes:
        id (int): The unique identifier for the financial record.
        user_id (int): The ID of the user this record belongs to.
        balance (float): The balance amount.
        currency (str): The currency of the balance.

    Relationships:
        user (User): The user associated with this financial record.
    """

    __tablename__ = "finances"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    balance = Column(Float, nullable=False)
    currency = Column(String, nullable=False)

    user = relationship("User", back_populates="finances")


engine = create_engine("sqlite:///finance.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
