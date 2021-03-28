from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()



@app.post("/admins/", response_model=schemas.Admin)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    admin = crud.get_admins(db)
    if len(admin) > 0:
        raise HTTPException(status_code=400, detail="Only one admin can exist")
    return crud.create_admin(db=db, admin=admin)


@app.get("/admins/", response_model=List[schemas.Admin])
def read_users(db: Session = Depends(get_db)):
    admins = crud.get_admins(db)
    return admins
