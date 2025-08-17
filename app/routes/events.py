from fastapi import HTTPException,Depends,APIRouter,status,Body,Query
from app.schemas.schemas import EventCreate,Event as EventSchema,EventUpdate #pydantic schema
from app.models.db import get_admin,Admin #has functions that interact with db
from app.auth.jwt_bearer import JWTBearer
#working
router = APIRouter(
    tags=['Events'],
    prefix='/events'
)

#Returns all Events
@router.get('/',response_model=list[EventSchema])
def get_all_events(admin:Admin=Depends(get_admin),
                     skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of items to return")):
    events = admin.get_all_events(skip=skip,limit=limit)
    if not events:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No events are available")
    else:
        return events
    
#Creates An upcoming event
@router.post('/',response_model=EventSchema,dependencies=[Depends(JWTBearer())])
def create_event(event:EventCreate, admin:Admin=Depends(get_admin)):
    new_event = admin.add_event(event.date,event.name,event.location)
    if new_event is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Failed To Create Post")
    return new_event

#deletes and event
@router.delete('/{id}',response_model=EventSchema,dependencies=[Depends(JWTBearer())])
def destroy(id:str,admin:Admin=Depends(get_admin)):
    event = admin.remove_event(id)
    if event:
        return event
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Event not found or Deletion Failed")

#updated eent with id
@router.put('/{id}',response_model=EventSchema,dependencies=[Depends(JWTBearer())])
def update(id:str, updated_date:EventUpdate=Body(...),admin:Admin=Depends(get_admin)):
    result = admin.update_event(id,updated_date)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Could not updtate")
    else:
        return result
