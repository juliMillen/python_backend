from fastapi import APIRouter, Depends,HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt,JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCES_TOKEN_DURATION = 10        #DURACION DEL TOKEN 10 minutos
SECRET= "557063b76a7310987ce8be3a4e80d18e4cca072d883c29b9c89610500238f0c1"

router = APIRouter()

#Dependencias de OAuth2
oauth2 = OAuth2PasswordBearer(tokenUrl="logins")

#Encriptador de contraseñas
crypt = CryptContext(schemes=["bcrypt"])

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
        "password":"$2a$12$JJWzHFOT.tAGY/H4Eay6ROpQeM4sdfJJiK7Nq.DRzL2gwGHXu5ZRC"
    },
     "ariOrtega":{
        "username":"ariOrtega",
        "full_name":"Ariel Ortega",
        "email":"ariOrtega@gmail.com",
        "disabled":True,
        "password":"$2a$12$KL.QXsciH5QliRkTHKlrXOVqEQrlIvxaXq1hZWH.IaIN.RwocvTGq"
    },
     "mBernardo":{
        "username":"mBernardo",
        "full_name":"Mauricio Bernardo",
        "email":"bernardoMa@gmail.com",
        "disabled":False,
        "password":"$2a$12$n6ZwPT5elJsR4WJF6htK9.QvMtt6tFLyfYotHhd6jk5v2R2J.W.7m"
    },
     "Robert26":{
        "username":"Robert26",
        "full_name":"Roberto Sanchez",
        "email":"rsanchez@gmail.com",
        "disabled":True,
        "password":"$2a$12$EyUy84hIi1gh78LVMUnWNehaKiZxUQ1qFxAJGWDbUe0zq.7NXab/u"
    }
}

#Funcion para buscar usuarios
def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])
    
#Dependencia para autenticar usuarios a partir del token
async def auth_user(token:str = Depends(oauth2)):
   exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, 
                            detail="Credenciales de autenticacion invalidas", 
                            headers={"WWW-Authenticate":"Bearer"})

   try:
    username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
    if username is None:
        raise exception
   except JWTError:
       raise exception
   
   return search_user(username)

async def current_user(user:User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Usuario inactivo")
    return user

@router.post("/logins")
async def login(form: OAuth2PasswordRequestForm = Depends()):
   user_db = users_db.get(form.username)
   if not user_db:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
   
   user = search_user_db(form.username)

   #verificando contraseñas
   if not crypt.verify(form.password,user.password):
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña es incorrecta")

   acces_token = {"sub":user.username, 
                  "exp": (datetime.utcnow() + timedelta(minutes=ACCES_TOKEN_DURATION)).timestamp()}

   return {"access_token": jwt.encode(acces_token, SECRET, algorithm=ALGORITHM), "token_type":"bearer"}


@router.get("/users/mee")
async def me(user: User = Depends(current_user)):
    return user       