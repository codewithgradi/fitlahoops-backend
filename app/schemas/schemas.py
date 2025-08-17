from pydantic import BaseModel,ConfigDict,Field
from datetime import date
from  typing import Optional

#Admin Schema

# Pydantic schema for response
class AdminResponse(BaseModel):
    id: str
    password: str
    username: str
    model_config = ConfigDict(from_attributes=True)  # For ORM support

class Admin(BaseModel):
    username : str
    password : str

class LoginRequest(BaseModel):
    username : str
    password : str

class LoginResponse(BaseModel):
    username: str
    access_token: str
    token_type: str = "bearer"




#Event Schema
class Event(BaseModel):
    id:str
    name: str
    location:str
    date: date
    
    model_config = ConfigDict(from_attributes=True)


#Event Create  : Data client needs to provide to create a new event
class EventCreate(BaseModel):
    name:str
    location : str
    date:date

#Event Update
class EventUpdate(BaseModel):
    name:Optional[str]=None
    location : Optional[str]=None
    date_:Optional[date]=None
    
#Gallery Schema
class Gallery(BaseModel):
    id:str
    title:str
    img:str
    category:str

class GalleryUpdate(BaseModel):
    title:Optional[str]=None
    img:Optional[str]=None
    category:Optional[str]=None
    
#Volunteers Schema
class Volunteer(BaseModel):
    id: str
    fullname: str =Field(...,alias="full_name")
    email:str
    role:str
    reason : Optional[str]=None
    model_config = ConfigDict(from_attributes=True)
#Volunteers Schema
class VolunteerCreate(BaseModel):
    fullname: str
    email:str
    role:str
    reason : Optional[str]=None