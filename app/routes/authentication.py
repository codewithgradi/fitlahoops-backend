from fastapi import HTTPException,Depends,APIRouter,status,Body
from app.schemas.schemas import LoginRequest,AdminResponse,LoginResponse #pydantic schema
from app.models.db import get_admin,Admin #has functions that interact with db
from app.utils.utils import Utils
from app.auth.jwt_bearer import JWTBearer
from app.auth.jwt_handler import create_access_token
from typing import List

#working
router = APIRouter(
    tags=['Authentication'],
    prefix='/auth'
)



@router.post('/login',response_model=LoginResponse)
def login(admin:Admin=Depends(get_admin),credentials:LoginRequest = Body(...)):
    username = credentials.username
    password = credentials.password
    user = admin.admin_login(password,username)

    if user:
        #create access token
        access_tokken = create_access_token({"sub":user.username})
        return {
            "username":user.username,
            "access_token":access_tokken,
            "token_type":"bearer"
        }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Credentials")


@router.post('/create',response_model=AdminResponse)
def create_admin_logins(username:str,password:str,admin:Admin=Depends(get_admin)):
    hashed_password = Utils.hashing(password)
    result = admin.admin_create(username,hashed_password)
    if result:
        return AdminResponse.model_validate(result)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Admin was not created')
    

@router.put('/login',response_model=AdminResponse,dependencies=[Depends(JWTBearer())])
def update_admin(id:str,new_password:str,admin:Admin=Depends(get_admin)):
    hashed_password = Utils.hashing(new_password)
    result = admin.update_admin_password(hashed_password,id)
    if result:
        return result
    else:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED,detail="Invalid ADMIN CREDENTIALS")


@router.get('/',response_model=List[AdminResponse],dependencies=[Depends(JWTBearer())])
def get_admin_data(admin:Admin=Depends(get_admin)):
    details = admin.get_admin_deatails()
    if details : 
        return details
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No data could be found")

#Delete Admin Credentials
@router.delete('/{id}',response_model=AdminResponse,dependencies=[Depends(JWTBearer())])
def destroy(id:str,admin:Admin=Depends(get_admin)):
    event = admin.remove_admin(id)
    if event:
        return event
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Credentials not found or Deletion Failed")

