# from sqlalchemy import  create_engine, MetaData,Table,Column,Integer,String,ForeignKey,Float
# from sqlalchemy.orm import Session

# #Used to create engine and engine used to connect to database
# #echo used to see what happens when we running command
# engine = create_engine('sqlite:///main.db',echo=True) 

# meta = MetaData()

# #definition of a table
# people = Table(
#     "people",
#     meta,
#     Column('id',Integer, primary_key=True),
#     Column('name',String,nullable=False),
#     Column('age',Integer)
# )
# things = Table(
#     "things",
#     meta,
#     Column('id',Integer,primary_key=True),
#     Column('description',String,nullable=False),
#     Column('value',Float),
#     Column('owner',Integer,ForeignKey('people.id'))
# )

# #creates tables on db
# meta.create_all(engine)

# #work with tables
# connection = engine.connect()
# # inser_statement = people.insert().values(name="Jane",age=31)
# # result = connection.execute(inser_statement)
# # connection.commit()

# # select = people.select().where(people.c.age>30)
# # result = connection.execute(select)

# # for row in result.fetchall():
# #     print(row)

# # people_update = people.update().where(people.c.id==2).values(name="David",age=45)
# # result = connection.execute(people_update)
# # connection.commit()

# # delete_stat= people.delete().where(people.c.name=="Gradi")
# # result = connection.execute(delete_stat)
# # connection.commit()

# people_inst= people.insert().values([
#     {"name":"Clara",'age':40},
#     {"name":"Joyce",'age':10},
#     {"name":"ClaAra",'age':30},
#     {"name":"Aztec",'age':20},
#     {"name":"Plame",'age':12},
# ])
# insert_things  = things.insert().values([
#     {'owner':2,"description":"Ams","value":800.70},
#     {'owner':2,"description":"what","value":10.70},
#     {'owner':3,"description":"ani","value":5.70},
#     {'owner':4,"description":"bad","value":80.70},
#     {'owner':5,"description":"Cool","value":90.70}
# ])
# # connection.execute(people_inst)
# # connection.commit()
# # connection.execute(insert_things)
# # connection.commit()
# # connection.commit()

# join_statement = people.join(things, people.c.id == things.c.owner)

# select_statement = people.select().with_only_columns(people.c.name , things.c.description).select_from(join_statement)
# result = connection.execute(select_statement)

# for row in result.fetchall():
#     print(row)

from sqlalchemy import create_engine, Integer,String,Float,Column,ForeignKey
from sqlalchemy.orm import DeclarativeBase,sessionmaker,relationship


engine = create_engine('sqlite:///main.db',echo=True)

Base = DeclarativeBase()

class Person(Base):
    __tablename__='people'
    id = Column(Integer, primary_key=True)
    name = Column(String,nullable=False)
    age = Column(Integer)

    things = relationship('Thing',back_populates='person')

class Thing(Base):
    __tablename__="things"
    id=Column(Integer,primary_key=True)
    description=Column(String,nullable=False)
    value =Column(Float)
    owner = Column(Integer,ForeignKey('people.id'))

    person = relationship('Person',back_populates='things')

#creates table
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

new_person = Person(name="Charlie",age=31)
session.add(new_person)
session.flush()#gives us access to id temprorily
new_thing = Thing(description="camera",value=500,owner=new_person.id)
session.add(new_thing)
session.commit()

print(new_person.things)
print(new_thing.person.name)

session.query()

