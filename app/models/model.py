from sqlalchemy import String,ForeignKey,Column,create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase,relationship
from app.utils.utils import Utils
from sqlalchemy import Date


#insite Utils in a static method used to generate a 20 alphanumeric id

engine = create_engine('sqlite:///main.db',echo=False)

class Base(DeclarativeBase):
    pass

#Table Fields
class GalleryItem(Base):
    __tablename__='gallery'
    id = Column(String,primary_key=True,default=Utils.generate_id)
    category=Column(String,nullable=False)
    img=Column(String,nullable=True)
    title = Column(String,nullable=False)
    public_id = Column(String, nullable=False) 

class Event(Base):
    __tablename__='events'
    id=Column(String,primary_key=True,default=Utils.generate_id)
    date = Column(Date,nullable=False)
    name = Column(String,nullable=False)
    location = Column(String,nullable=False)

class Volunteer(Base):
    __tablename__='volunteer'
    id=Column(String,primary_key=True,default=Utils.generate_id)
    full_name= Column(String,nullable=False)
    email= Column(String,nullable=False)
    role=Column(String,nullable=False)
    reason = Column(String,nullable=True)

class Admin(Base):
    __tablename__='admin'
    id = Column(String,nullable=False,primary_key=True,default=Utils.generate_id)
    username = Column(String,nullable=False)
    password = Column(String, nullable=False)

#crates table
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

my_session = Session()

