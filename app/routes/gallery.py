from fastapi import HTTPException,Depends,File,UploadFile,APIRouter,status,Body,Query,Form
from fastapi.responses import JSONResponse
from app.schemas.schemas import GalleryUpdate,Gallery #pydantic schema
from app.models.db import get_admin,Admin #has functions that interact with db
from app.auth.jwt_bearer import JWTBearer
from typing import List
from app.utils.utils import Cloud
#Working

router = APIRouter(
    tags=['Gallery'],
    prefix='/gallery'
)
cloud =   Cloud()


#Gallery Routes
@router.get('/',response_model=list[Gallery])
def get_all_gallery_items(admin:Admin=Depends(get_admin),
                            skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of items to return")):
    items =  admin.get_gallery(skip=skip,limit=limit)
    if items:
        return items
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No items in the Gallery")
        


@router.post('/',response_model=Gallery,dependencies=[Depends(JWTBearer())])
def add_event_to_gallary(
    cat:str=Form(...),
    img:UploadFile=File(...),
    title:str=Form(...),
    admin:Admin=Depends(get_admin)):
    try:
        upload_result = cloud.upload_to_cloudinary(file=img,folder='gallery',)
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Image Upload Failed: {str(e)}")
    
    new_content = admin.add_to_gallery(cat,upload_result["secure_url"],upload_result['public_id'],title)


    if new_content:
        return new_content
    else :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Gallery Content Created')
    
@router.delete('/{id}',response_model=Gallery,dependencies=[Depends(JWTBearer())])
def destroy(id:str,admin:Admin=Depends(get_admin)):
    item = admin.destroy_gallery(id)
    if item:
        return item
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Gallery not found or Deletion Failed")

#updated eent with id
@router.put('/{id}',response_model=Gallery,dependencies=[Depends(JWTBearer())])
def update(id:str, updated_date:GalleryUpdate=Body(...),admin:Admin=Depends(get_admin)):
    result = admin.update_gallery(updated_date,id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Could not updtate")
    else:
        return result
