from pydantic import BaseModel

class CreateUserSchema(BaseModel):
    name: str
    password: str
    email: str

class UserSchema(CreateUserSchema):
    id: int
