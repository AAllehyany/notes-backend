from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from . import crud, models, schemas
from .db import SessionLocal, engine
from .helpers import hash_password

SECRET_KEY="DEMOSECRETLMAO"
ALGORITHM="HS256"

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



# Dependency

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()

@app.post("/token")
def authenticate_admin(db: Session, data: OAuth2PasswordRequestForm = Depends()):

    admin = crud.get_admin_by_email(data.username)

    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    hashed_password = hash_password(data.password)

    if not hash_password == admin.hashed_password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    
    

@app.post("/admins", response_model=schemas.Admin)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    admin = crud.get_admins(db)
    if len(admin) > 0:
        raise HTTPException(status_code=400, detail="Only one admin can exist")
    return crud.create_admin(db=db, admin=admin)


@app.get("/admins/", response_model=List[schemas.Admin])
def read_users(db: Session = Depends(get_db)):
    admins = crud.get_admins(db)
    return admins


@app.get("/clients")
async def get_clients(token: str = Depends(oauth2_scheme)):
    return {"token": token}