from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

class Assets(Base):
    __tablename__ = "Assets"

    id = Column(Integer, primary_key=True)
    asset_name = Column(String)
    operating_system = Column(String)
    operating_system_version = Column(String)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "asset_name": "PC0000-NY",
                    "operating_system": "Windows 10 Pro",
                    "operating_system_version": "",
                }
            ]
        }
    }

class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    title = Column(String)
    department = Column(String)
    office = Column(String)
    email_address = Column(String)

    #Users can have many assets assigned to them

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "johns",
                    "first_name": "John",
                    "last_name": "smith",
                    "title": "DevOPS Engineer",
                    "department": "DevOPS",
                    "office": "NYC",
                    "email_address": "johns@mydomain.com",
                }
            ]
        }
    }

class AssignedAssets(Base):
    __tablename__ = "assigned_assets"
    
    user_id = Column(Integer, ForeignKey('Users.id'), primary_key=True)
    asset_id = Column(Integer, ForeignKey('Assets.id'), primary_key=True)

    