import random
from datetime import datetime
import os
import uuid
from dotenv import load_dotenv
import bcrypt
from app.utils.send_email import Email
import re
import cloudinary
import cloudinary.uploader
import cloudinary.uploader
from fastapi import UploadFile,HTTPException

load_dotenv()

class Utils:
    #Sends email
    def _send_email(self,recipient:str,body:str):
        email_client = Email()
        email_client.set_receiver(recipient)
        email_client.email_body(body)
        email_client.send_email()

    #Sends email to user thanking the for volunteers after they have filled the form
    def send_appreciation_email(self,user_email:str,name:str):
        body =f'''
Hi there,

Thank you for signing up with {name} ! We're excited to have you on board 
and can’t wait to work with you on fitlahoops.

If you have any questions, feel free to reach out anytime.

Best regards,
The Fitla Hoops Team

            '''
        self._send_email(user_email,body)

    #Sends upcoming game updates to users who clicked the get updates and volunteers
    def send_updates_email(self,email:str):
        body =f"""
Hi there,

Get ready! We have exciting games coming up soon that you won’t want to miss.

Checkout Our Website for fixtures.

Stay tuned for schedules and updates.

Best regards,
The Fitla Hoops Team
                """
        self._send_email(email,body)

    
    @staticmethod
    def validate_incoming_email(email:str)->bool:
        EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(EMAIL_REGEX, email):
            return True
        else:
            return False


    #generates a 20 alphanumeric id
    @staticmethod
    def generate_id()->str:
        chars = '1234567890QWERTYUIOPLKJHGFDSAZXCVBNMmnbvcxzasdfghjklpoiuytrewq'
        return ''.join(random.choices(chars,k=20))
    
    #returns date format
    @staticmethod
    def format_date():
        today = datetime.now()
        return  f"{today.year}-{today.month:02d}-{today.day:02d}"
    
    #
    @staticmethod
    def load_dotenv_variables():
        #Variables on dotenv
        admin_username = os.getenv("ADMIN_USERNAME")
        admin_password = os.getenv("ADMIN_PASSWORD_HASH")
        secrete_key = os.getenv("SECRET_KEY")
        return admin_username,admin_password,secrete_key


    @staticmethod
    def hashing(password:str):
        #hashing the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        return hashed_password.decode()

    @staticmethod
    def verify_password(plain_password:str,hashed_password:str)->bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'),hashed_password.encode('utf-8'))
    

class Cloud:
    def __init__(self):
        self.config()

    def upload_to_cloudinary(self,file:UploadFile, folder:str)->str:
    #Uploads File and returns image url + public id
        self.validate_image_file(file)
        unique_name = self.create_image_name(folder)

        try:
            result = cloudinary.uploader.upload(
            file.file,
            folder=folder,
            public_id=unique_name,
            resource_type="image",
            )
        except Exception as e:
            raise HTTPException(status_code=500,detail=f"Upload Failed: {str(e)}")
        return {
            "secure_url":result.get("secure_url"),
            "public_id":result.get("public_id")
                }
    
    
    def create_image_name(self,folder:str)->str:
        unique_id = uuid.uuid4().hex[:10]  # 10-character unique ID
        return f"{folder}/{unique_id}"

    def validate_image_file(self,file:UploadFile):
        accepted_formats = ["image/jpeg","image/png"]
        if file.content_type not in accepted_formats or not (file.filename.lower().endswith('.jpg') or file.filename.lower().endswith('.png')):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type.Only JPEG and PNG files are allowed"
                )

    def get_cloudinary_data(self):
        cloud_name= os.getenv("CLOUDINARY_CLOUD_NAME")
        cloud_api_key= os.getenv("CLOUDINARY_API_KEY")
        cloud_api_secret= os.getenv("CLOUDINARY_API_SECRET")
        return cloud_name,cloud_api_key,cloud_api_secret
    
    def config(self):
        cloud_name, api_key, api_secret = self.get_cloudinary_data()
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True
        )


    def delete_image_from_cloudinary(self,public_id: str):
        try:
            result = cloudinary.uploader.destroy(public_id, resource_type="image")
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete image: {str(e)}")


