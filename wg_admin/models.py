import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime

from db import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    role = Column(String)
    is_active = Column(Boolean, default=True)


class WGUser(Base):
    __tablename__ = "wg_user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    ip_address = Column(String)
    public_key = Column(String)
    private_key = Column(String)
    creation_date = Column(DateTime, default=datetime.datetime.now)
