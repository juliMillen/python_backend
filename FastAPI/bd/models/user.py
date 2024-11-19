from pydantic import BaseModel

class User(BaseModel):
    id:str | None   #significa que el id puede ser opcional
    username:str
    email:str