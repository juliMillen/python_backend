from pymongo import MongoClient

## Modulo conexion MongoDB: pip install pymongo
## Ejecucion: en la cmd: mongod.exe
## al no poner un path toma como defecto el servidor local

#Base de datos Local
#db_client = MongoClient().local

##Base de datos remota
db_client = MongoClient("mongodb+srv://julimillen:g4eH4bTzxS64AkQd@bdcursopython.aoejg.mongodb.net/?retryWrites=true&w=majority&appName=bdCursoPython").bdCursoPython
