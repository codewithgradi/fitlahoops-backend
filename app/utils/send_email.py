import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv


class Email:
    def __init__(self):
        self.sender = self.get_organisation_email()
        self.receiver = None  
        self.message = None  # will hold the MIMEMultipart()

    def set_receiver(self,receiver_email):
        self.receiver = receiver_email

    def get_app_password(self):
        load_dotenv()
        return os.getenv("APP_PASSWORD")
    
    def  get_organisation_email(self):
        load_dotenv()
        return os.getenv("OUR_EMAIL")

    def send_email(self):
        if self.message is None:
            print("Error: Message is not structured or body not attached")
            return
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.sender, self.get_app_password())
                server.sendmail(self.sender, self.receiver, self.message.as_string())
            print("Email Was sent")

        except Exception as e:
            print(f"Error: {e}")

    # Creates The email
    def structure(self):
        self.message = MIMEMultipart()
        self.message["From"] = self.sender
        if self.receiver is not None:
            self.message["To"] = self.receiver
            self.message["Subject"] = "Fitlahoops Welcome Email"
            return self.message


    # Email body content
    def email_body(self, body):
        self.structure()
        self.message.attach(MIMEText(body, "plain"))



