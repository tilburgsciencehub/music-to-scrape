# exceptions.py
class CarInfoException(Exception):
    ...


class CarInfoNotFoundError(CarInfoException):
    def __init__(self):
        self.status_code = 404
        self.detail = "User Info Not Found"