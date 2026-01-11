from fastapi import APIRouter, Body,HTTPException
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.exceptions import ObjectAlreadyExistsException, FacilityNotFoundException,FacilityNotFoundHTTPException,FacilityAlreadyExistsHTTPException
from src.services.facilities import FacilitiesService


router = APIRouter(prefix="/facilities", tags=["Особенности"])


@router.get("")
@cache(expire=20)
async def get_facilities(
    db: DBDep,
):
    facilities = await FacilitiesService(db).get_facilities()
    return facilities



@router.get("/{facility_id}")
async def get_facility(
    db: DBDep,
    facility_id: int,
):
    try:
        facility = await FacilitiesService(db).get_facility(facility_id=facility_id)
    except FacilityNotFoundException:
        raise FacilityNotFoundHTTPException
    return facility


@router.delete("/{facility_id}")
async def delete_facilities(
    facility_id: int,
    db: DBDep,
):
    await FacilitiesService(db).delete_facility(facility_id=facility_id)
    return {"status": "OK"}


@router.post("")
async def create_facility(
    db: DBDep,
    facility_data: FacilityAdd = Body(),
):
    try:
        facility = await FacilitiesService(db).add_facility(
            facility_data=facility_data
        )
    except ObjectAlreadyExistsException:
        raise FacilityAlreadyExistsHTTPException
    return {"status": "OK", "data": facility}
