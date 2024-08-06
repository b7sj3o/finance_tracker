from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)


class Finance(Base):
    __tablename__ = "finances"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    balance = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    user = relationship("User", back_populates="finances")


User.finances = relationship("Finance", order_by=Finance.id, back_populates="user")

engine = create_engine("sqlite:///finance.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
