from bson import ObjectId
from .Common import CommonModel
from pydantic import EmailStr


class EmployeeModel(CommonModel):
    id: int
    username: str
    email: EmailStr
   