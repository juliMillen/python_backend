from fastapi import FastAPI
from routers import products,users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Routers
app.include_router(products.router)
app.include_router(users.router)
app.mount("/static",StaticFiles(directory="static"), name="static") #exponer un recurso estatico

@app.get("/")
async def root():
    return "¡Aprendiendo FastApi!"

@app.get("/url")
async def url():
    return { "url_curso": "https://mouredev.com/python" }