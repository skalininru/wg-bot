from datetime import datetime
from ipaddress import IPv4Address

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    role: str
    is_active: bool

    class Config:
        orm_mode = True


class WGUserBase(BaseModel):
    pass

    class Config:
        orm_mode = True


class WGUserCreate(WGUserBase):
    name: str
    ip_address: IPv4Address
    public_key: str
    private_key: str


class WGUser(WGUserCreate):
    id: int
    creation_date: datetime
