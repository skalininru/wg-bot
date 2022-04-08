from sqlalchemy.orm import Session

from models import WGUser
from schemas import WGUser as wguser_scheme


def get_wguser_by_name(db: Session, username: str):
    wg_user = db.query(WGUser).filter_by(name=username).first()
    return wg_user


def get_wguser_list(db: Session):
    wg_user_list = db.query(WGUser).all()
    return wg_user_list


def create_wguser(db: Session, wguser: wguser_scheme):
    wg_user = WGUser(
        name=wguser.name,
        ip_address=str(wguser.ip_address),
        public_key=wguser.public_key,
        private_key=wguser.private_key,
    )
    db.add(wg_user)
    db.commit()
    db.refresh(wg_user)
    return wg_user
