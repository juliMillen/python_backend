## Autenticacion basica
from fastapi import FastAPI, Depends,HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

#Entidad user
class User(BaseModel):
    username:str
    full_name:str
    email:str
    disabled:bool

#Usuario de base de datos
class UserDB(User):
    password:str



users_db = {
    "juliMillen":{
        "username":"juliMillen",
        "full_name":"Julian Millen",
        "email":"julimillen@gmail.com",
        "disabled":False,
        "password":"1234"
    },
     "ariOrtega":{
        "username":"ariOrtega",
        "full_name":"Ariel Ortega",
        "email":"ariOrtega@gmail.com",
        "disabled":True,
        "password":"1234plate"
    },
     "mBernardo":{
        "username":"mBernardo",
        "full_name":"Mauricio Bernardo",
        "email":"bernardoMa@gmail.com",
        "disabled":False,
        "password":"1234ma"
    },
     "Robert26":{
        "username":"Robert26",
        "full_name":"Roberto Sanchez",
        "email":"rsanchez@gmail.com",
        "disabled":True,
        "password":"123456"
    }
}

def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])
    
async def current_user(token:str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, 
                            detail="Credenciales de autenticacion invalidas", 
                            headers={"WWW-Authenticate":"Bearer"})
    
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Usuario inactivo")
    
    return user

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
   user_db = users_db.get(form.username)
   if not user_db:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
   
   user = search_user_db(form.username)
   if not form.password == user.password:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña es incorrecta")
   
   return {"acces_token": user.username, "token_type":"bearer"}


@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
       