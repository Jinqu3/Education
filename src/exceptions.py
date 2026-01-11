from datetime import date
from fastapi import HTTPException

# === Базовые исключения ===
class BaseAppException(Exception):
    detail = "Непредвиденная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BaseAppHTTPException(HTTPException):
    def __init__(self, status_code: int = 500, detail: str = None):
        super().__init__(status_code=status_code, detail=detail)


# === Объект не найден===
class ObjectNotFoundException(BaseAppException):
    detail = "Объект не найден"


class FacilityNotFoundException(ObjectNotFoundException):
    detail = "Удобство не найдено"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"

class UserNotFoundException(BaseAppException):

    detail = "Пользователь не найден"


# === HTTP-исключения: 404 ===
class FacilityNotFoundHTTPException(BaseAppHTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Удобство не найдено"
        )


class HotelNotFoundHTTPException(BaseAppHTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Отель не найден"
        )


class RoomNotFoundHTTPException(BaseAppHTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Номер не найден"
        )

class UserNotFoundHTTPException(BaseAppHTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail=f"Пользователь не найден"
        )


# === Бизнес-логика: обычные исключения ===

class IncorrectPasswordException(BaseAppException):

    detail = "Неверный пароль"

class AllRoomsAreBookedException(BaseAppException):
    detail = "Не осталось свободных номеров"


class InvalidDateOrderException(BaseAppException):
    detail = "Дата заезда позже даты выезда"


class DatesCannotBeEqualException(BaseAppException):
    detail = "Дата выезда равна дате заезда"


class ObjectAlreadyExistsException(BaseAppException):
    detail = "Объект уже создан"

class UserAlreadyExistsException(ObjectAlreadyExistsException):

    detail = "Пользователь уже существует"


# === HTTP-исключения: ===

class IncorrectPasswordHTTPException(BaseAppHTTPException):

    def __init__(self):
        super().__init__(
            status_code=409,
            detail="Неверный пароль"
        )

class FacilityAlreadyExistsHTTPException(BaseAppHTTPException):
    def __init__(self):
        super().__init__(
            status_code=409,
            detail="Удобство уже создано"
        )


class UserAlreadyExistsHTTPException(BaseAppHTTPException):
    def __init__(self, email: str):
        super().__init__(
            status_code=409,
            detail=f"Пользователь c email {email} уже существует"
        )


class AllRoomsAreBookedHTTPException(BaseAppHTTPException):
    def __init__(self):
        super().__init__(
            status_code=409,
            detail="Все номера данного типа забронировали"
        )


# === Валидация дат ===
def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(
            status_code=409,
            detail="Дата заезда не может быть позже или равна дате выезда"
        )