from fastapi import HTTPException,Depends,APIRouter,status,BackgroundTasks,Query
from app.schemas.schemas import VolunteerCreate,Volunteer #pydantic schema
from app.models.db import get_admin,Admin #has functions that interact with db
from app.auth.jwt_bearer import JWTBearer
from app.utils.utils import Utils
#working
router = APIRouter(
    tags=['Volunteers'],
    prefix='/volunteers'
)

#Volunteers Routes
@router.get('/',response_model=list[Volunteer],dependencies=[Depends(JWTBearer())])
def get_all_volunteers(admin:Admin=Depends(get_admin),
                       skip:int=Query(0,ge=0,description="Number of items to skip"),
                       limit:int=Query(10,ge=1,le=100,description="Maximum number of items ro return")):
    result = admin.get_volunteers(skip=skip,limit=limit)
    if result: return admin.get_volunteers(skip=skip,limit=limit)
    else:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No Volunteers")

@router.post('/',response_model=Volunteer)
def add_volunteer(content:VolunteerCreate,background_tasks:BackgroundTasks,admin:Admin=Depends(get_admin)):
   user = admin.add_volunteer(fullname=content.fullname,
                              email=content.email,
                              role=content.role,
                              reason=content.reason)
   utils = Utils()
   background_tasks.add_task(utils.send_appreciation_email,
                             user_email=user.email,
                             name=user.full_name)
   if user:
      return user
   else:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Could not create Volunteer")

#Delete Volunteer Credentials
@router.delete('/{id}',response_model=Volunteer,dependencies=[Depends(JWTBearer())])
def destroy(id:str,admin:Admin=Depends(get_admin)):
    volunteer = admin.destroy_volunteer(id)
    if volunteer:
        return volunteer
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Credentials not found or Deletion Failed")
