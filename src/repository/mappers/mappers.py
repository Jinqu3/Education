from src.repository.mappers.base import DataMapper

from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel

from src.models.rooms import RoomsORM
from src.schemas.rooms import Room

from src.models.users import UsersORM
from src.schemas.users import User

from src.models.bookings import BookingsORM
from src.schemas.bookings import Booking

from src.models.facilities import FacilitiesORM
from src.schemas.facilities import Facility

from src.models.facilities import RoomsFacilitiesORM
from src.schemas.facilities import RoomFacility


class HotelDataMapper(DataMapper):
    db_model = HotelsORM
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsORM
    schema = Room


class UserDataMapper(DataMapper):
    db_model = UsersORM
    schema = User


class BookingDataMapper(DataMapper):
    db_model = BookingsORM
    schema = Booking


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesORM
    schema = Facility


class RoomFacilityDataMapper(DataMapper):
    db_model = RoomsFacilitiesORM
    schema = RoomFacility
