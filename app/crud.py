from sqlalchemy.orm import Session


from . import models, schemas
from .helpers import hash_password
def get_admin(db: Session, admin_id: int):
    return db.query(models.Admin).filter(models.Admin.id == admin_id).first()

def get_admin_by_email(db: Session, email: str):
    return db.query(models.Admin).filter(models.Admin.email == email).first()

def get_admins(db: Session):
    return db.query(models.Admin).all()

def create_admin(db: Session, admin: schemas.AdminCreate):
    db_admin = models.Admin(email=admin.email, hashed_password=hash_password(admin.password))
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin