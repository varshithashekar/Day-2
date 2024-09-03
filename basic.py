from pydantic import BaseModel, Field
import json
from enum import Enum
from dataclasses import dataclass

class User(BaseModel):
    id: str = Field(..., title="User ID")
    name: str = Field(..., title="Name", max_length=50)
    age: int = Field(..., title="Age", ge=0, le=150)
    email: str = Field(..., title="Email")

class UserID(str, Enum):
    VAR_04 = "var_04"

class details:
    email:str

class CustomError(Exception):
    pass

class NegativeIDError(CustomError):
    def __init__(self, id, message="Invalid user ID"):
        self.id = id
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.id} -> {self.message}'

def validate_user_id(u_id:str):
    if u_id != UserID.VAR_04.value:
        raise NegativeIDError(u_id)
    print("Valid user ID:", u_id)


try:
    u_id = input("Enter user ID: ")
    validate_user_id(u_id)
    

    user = User(
        id=u_id,
        name=input("Enter name: "),
        age=int(input("Enter age: ")),
        email=input("Enter email: ")
    )
    


    user_json = user.json()
    print("Serialized JSON:", user_json)


    user_from_json = User.parse_raw(user_json)
    print("Deserialized User:", user_from_json)


except NegativeIDError as e:
    print("Caught an exception:", e)
except ValueError as e:
    print("Invalid input:", e)

