from app.models.model import my_session,GalleryItem, Volunteer,Event,Admin as AdminModel
from typing import List,Optional
from sqlalchemy.exc import OperationalError
from app.utils.utils import Utils
from datetime import datetime
from fastapi import HTTPException
from app.schemas.schemas import EventUpdate,GalleryUpdate
class Admin:
    #Gallery Table

    #Adds to gallery table
    def add_to_gallery(self,cat:str,img:str,public_id:str,title:str)->Optional[GalleryItem]:
        try:
            new_content = GalleryItem(category=cat,img=img,public_id=public_id,title=title)
            if new_content:
                my_session.add(new_content)
                my_session.commit()
                return new_content
            return None
        except OperationalError:
            raise HTTPException(status_code=500,detail="DB is available")
    #Returns galery
    def get_gallery(self,skip:int,limit:int)->List[GalleryItem]:
        return my_session.query(GalleryItem).offset(skip).limit(limit).all() or None
    
    #Delete gallery item
    def destroy_gallery(self,id:str)->Optional[GalleryItem]:
        item= my_session.query(GalleryItem).filter(GalleryItem.id ==id).first()
        if item:
            my_session.delete(item)
            my_session.commit()
            return item
        return None
    
    #Updates Existing GAllery Item
    def update_gallery(self,update_gallery_item:GalleryUpdate,id:str)->GalleryItem:
        item = my_session.query(GalleryItem).filter(GalleryItem.id==id).first()
        if not item:
            return None
        if update_gallery_item.category:
            item.category=update_gallery_item.category
        if update_gallery_item.img:
            item.img=update_gallery_item.img
        if update_gallery_item.title:
            item.title=update_gallery_item.title
        my_session.commit()
        my_session.refresh(item)
        return item



    #Volunteer Table Queries

    #Retrieves all Volunteers
    def get_volunteers(self,skip:int,limit:int)->List[Volunteer]:
        return my_session.query(Volunteer).offset(skip).limit(limit).all() or None
    
    def add_volunteer(self,fullname:str,email:str,role:str,reason:Optional[str]=None)->Optional[Volunteer]:
        existing_user= my_session.query(Volunteer).filter(Volunteer.email==email).first()
        if existing_user:
            raise HTTPException(status_code=400,detail=f"{email} already exist")
        valid_email = Utils.validate_incoming_email(email)
        if not valid_email:
            raise HTTPException(status_code=400,detail="Invalid Email Address")

        try:
            volunteer = Volunteer(full_name=fullname,email=email,role=role,reason=reason)
            my_session.add(volunteer)
            my_session.commit()
            my_session.refresh(volunteer)
            return volunteer
        except:
            my_session.rollback()
            raise HTTPException(status_code=500,detail="Database error while adding Volunteers")
    
    #Delete Volunteer  
    def destroy_volunteer(self,id:str)->Optional[Volunteer]:
        volunteer= my_session.query(Volunteer).filter(Volunteer.id ==id).first()
        if volunteer:
            my_session.delete(volunteer)
            my_session.commit()
            return volunteer
        return None


    # Event table Queries

    #called on the frontend when page loads
    def get_all_events(self,skip:int,limit:int)->List[Event]:
        return my_session.query(Event).offset(skip).limit(limit).all() or None


    #removes event from event table
    def remove_event(self,id:str)->Optional[Event]:
        event = my_session.query(Event).filter(Event.id==id).first()
        if event:
            my_session.delete(event)
            my_session.commit()
            return event
        return None

    #updates existing event
    def update_event(self,id:str,update_data:EventUpdate)->Optional[Event]:
        event = my_session.query(Event).filter(Event.id==id).first()
        if not event:
            return None
        if update_data.date_:
            event.date=update_data.date_
        if update_data.name:
            event.name=update_data.name
        if update_data.location:
            event.location=update_data.location
        
        my_session.commit()
        my_session.refresh(event)
        return event
        
    #adds new event to event table
    def add_event(self,date:datetime,name:str,location:str)->Optional[Event]:
        try:
            new_event= Event(date=date,name=name,location=location)
            if new_event:
                my_session.add(new_event)
                my_session.commit()
                my_session.refresh(new_event)
                return new_event
        except Exception as e:
            print(e)

    #Admin Table
    #CREATE ADMIN
    def admin_create(self,username:str,password:str)->AdminModel:
        user = AdminModel(password=password,username=username)
        if user:
            my_session.add(user)
            my_session.commit()
            my_session.refresh(user)
            return user
        else:
            return None
    #Login
    def admin_login(self,password:str,username:str)->Optional[AdminModel]:
        admin = my_session.query(AdminModel).filter(AdminModel.username==username).first()
        if admin:
            hashed_password = admin.password
            if Utils.verify_password(password, hashed_password):
                return admin
        return None
    
    #Change password
    def update_admin_password(self,new_password:str,id:str)->Optional[AdminModel]:
        admin = my_session.query(AdminModel).filter(AdminModel.id==id).first()
        if admin:
            hashed_password = Utils.hashing(new_password)
            admin.password= hashed_password
            my_session.commit()
            return admin
        return None
    
    #Remove Credentials of one admin
    def remove_admin(self,id:str)->Optional[AdminModel]:
        event = my_session.query(AdminModel).filter(AdminModel.id==id).first()
        if event:
            my_session.delete(event)
            my_session.commit()
            return event
        return None
    
    #Returns admin details
    def get_admin_deatails(self)->List[AdminModel]:
        return my_session.query(AdminModel).all() or None

    

    
def get_admin():
    return Admin()