from src.schemas.facilities import FacilityAdd


async def test_crud_facilities(db):
    # CREATE
    new_facility = await db.facilities.add(FacilityAdd(title="Test Facility"))
    await db.commit()
    assert new_facility
    assert new_facility.title == "Test Facility"

    # READ
    facility = await db.facilities.get_one_or_none(id=new_facility.id)
    print(facility, new_facility)

    assert facility
    assert facility.title == new_facility.title
