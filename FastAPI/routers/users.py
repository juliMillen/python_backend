from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

#Inicia el server: uvicorn users:app --reload

#Entidad user
class User(BaseModel):
    id:int
    name:str
    surname:str
    url:str
    age:int

users_list = [User(id=1,name="Julian",surname="Millen",url="https://millen.dev",age=24),
        User(id=2,name="Ricardo",surname="Kaka",url="https://brasileño.dev",age=45),
        User(id=3,name="Fabian",surname="Cubero",url="https://lateral.dev",age=40)]

@router.get("/usersjson")
async def usersjson():
    return [{"name": "Julian","surname":"Millen","url":"https://millen.dev"},
            {"name": "Ricardo","surname":"Kaka","url":"https://brasileño.dev"},
            {"name": "Fabian","surname":"Cubero","url":"https://lateral.dev"}]


@router.get("/usersclass")
async def usersclass():
    return User(name= "Julian",surname="Millen",url="https://millen.dev",age=24)

@router.get("/userslist")
async def usersclass():
    return users_list

## Path
@router.get("/user/{id}")
async def user(id:int):
    searchUser(id)


## Query
@router.get("/userquery")
async def user(id:int):
    searchUser(id)


@router.post("/user/")
async def user(user:User):
    if type(searchUser(user.id)) == User:
        return "{El usuario ya existe}"
    else:
        users_list.append(user)

@router.put("/user/")
async def user(user:User):
    found = False
    for index, usu in enumerate(users_list):
        if usu.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"Error": "No se ha encontrado el usuario"}
    else:
        return user

@router.delete("/user/{id}")
async def deleteUsuer(id:int):
    for index, user in enumerate(users_list):
        if user.id == id:
            del users_list[index]
            return {"message":"Usuario eliminado correctamente"}
    return {"message": "Usuario no encontrado"}
            


## funcion para no repetir codigo
def searchUser(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el usuario"}

