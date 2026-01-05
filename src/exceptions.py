
class BaseException(Exception):
    detail = "Непредвиденная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

class ObjectNotFoundException(BaseException):

    detail = "Объект не найден"

class AllRoomsAreBookedException(BaseException):

    detail = "Не осталось свободных номеров"

class InvalidDateOrderException(BaseException):

    detail = "Дата заезда позже даты выезда"

class DatesCannotBeEqualException(BaseException):

    detail = "Дата выезда равна дате заезда"

class CanNotAddObjectException(BaseException):

    detail = "Невозможно создать объект"

class CanNotDeleteObjectException(BaseException):

    detail = "Невозможно удалить объект"

class CanNotСhangeObjectException(BaseException):

    detail = "Невозможно изменить объект"

class ObjectAlreadyExistsException(BaseException):

    detail = "Объект уже создан"