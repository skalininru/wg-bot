from sqlalchemy.orm import Session

from models import User


def get_user_by_name(db: Session, username: str):
    wga_user = db.query(User).filter_by(name=username).first()
    return wga_user


def get_role_by_name(db: Session, username: str):
    wga_user = db.query(User).filter_by(name=username).first()
    if wga_user:
        return wga_user.role
    else:
        return None


def create_admin_user(db: Session, username: str):
    wga_user = User(
        name=username,
        role="admin"
    )
    db.add(wga_user)
    db.commit()
    db.refresh(wga_user)
    return wga_user
