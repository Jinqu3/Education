import pytest
from src.api.dependencies import get_db,async_session_maker
from src.utils.db_manager import DBManager

@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1,"2024-08-01","2024-08-01",200),
    (1,"2024-08-01","2024-08-01",200),
    (1,"2024-08-01","2024-08-01",200),
    (1,"2024-08-01","2024-08-01",200),
    (1,"2024-08-01","2024-08-01",200),
    (1,"2024-08-01","2024-08-01",500),
])
async def test_add_booking(
        room_id, date_from, date_to, status_code,
        db,auth_ac
):
    response = await auth_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async with (DBManager(session_factory=async_session_maker) as _db):
        await _db.bookings.delete()
        await _db.commit()

@pytest.mark.parametrize("room_id, date_from, date_to, status_code, booked_rooms", [
    (1, "2024-08-01", "2024-08-01", 200,1),
    (1, "2024-08-01", "2024-08-01", 200,2),
    (1, "2024-08-01", "2024-08-01", 200,3),
    (1, "2024-08-01", "2024-08-01", 200,4),
    (1, "2024-08-01", "2024-08-01", 200,5)
])
async def test_add_and_get_booking(
        room_id, date_from, date_to, status_code, booked_rooms,
        delete_all_bookings, auth_ac
):

    response = await auth_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)

    response = await auth_ac.get("/bookings/me")
    assert response.status_code == status_code == 200
    assert isinstance(response.json(),list)
    assert len(response.json()) == booked_rooms