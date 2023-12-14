import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import exists 
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from typing import List, Annotated


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class AssetBase(BaseModel):
    asset_name : str
    operating_system : str
    operating_system_version : str

class UserBase(BaseModel):
    username : str
    first_name : str
    last_name : str
    title : str
    department : str
    office : str
    email_address : str

class AssignedAssetsBase(BaseModel):
    user_id : int
    asset_id : int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
def read_root():
    return {"Hello": "World!!"}

@app.get("/all_users")
async def get_all_users(db : db_dependency):
    all_users = db.query(models.Users).all()

    return all_users

@app.get("/all_assets")
async def get_asset_by_name(db : db_dependency):
    all_assets = db.query(models.Assets).all()

    print(all_assets)
    return all_assets

@app.get("/asset/{asset_name}")
async def get_asset_by_name(asset_name: str, db : db_dependency):
    result = db.query(models.Assets).filter(models.Assets.asset_name == asset_name).first()

    print(result)
    return result

@app.post("/asset")
async def create_asset(Assets: AssetBase, db: db_dependency) -> AssetBase:

    new_asset = models.Assets(asset_name=Assets.asset_name , operating_system=Assets.operating_system, operating_system_version=Assets.operating_system_version)
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)

    return new_asset

@app.post("/users")
async def create_user(Users : UserBase, db : db_dependency) -> UserBase:

    new_user = models.Users(username=Users.username, first_name=Users.first_name, last_name=Users.last_name, title=Users.title, department=Users.department, office=Users.office, email_address=Users.email_address)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/assign_assets")
async def assign_asset(request : AssignedAssetsBase, db : db_dependency) -> AssignedAssetsBase:

            
    stmt = exists().where(models.AssignedAssets.asset_id == request.asset_id)
    stmt1 = exists().where(models.Users.id == request.user_id)
    stmt2 = exists().where(models.Assets.id == request.asset_id)

    isAssetAssigned = db.query(stmt).scalar()
    doesUserExist = db.query(stmt1).scalar()
    doesAssetExist = db.query(stmt2).scalar()
    if not doesAssetExist:

        raise HTTPException(status_code=404, detail="Asset not found")

    if not doesUserExist:
        raise HTTPException(status_code=404, detail="User not found")

    if not isAssetAssigned:

        new_assigned_asset = models.AssignedAssets(user_id = request.user_id, asset_id = request.asset_id)
        db.add(new_assigned_asset)
        db.commit()
        db.refresh(new_assigned_asset)

        result = db.query(models.Assets).filter(models.Assets.id == request.asset_id).first()
        
    else:
        raise HTTPException(status_code=400, detail="Assignment already exists")

    return result