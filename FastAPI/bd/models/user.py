from pydantic import BaseModel,Field

class User(BaseModel):
    id:str | None = Field(default=None)  
    username:str
    email:str