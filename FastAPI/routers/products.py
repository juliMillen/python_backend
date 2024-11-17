from fastapi import APIRouter

router = APIRouter(prefix="/products", responses={404: {"message":"No encontrado"}}) #ruta por defecto products y seteamos un response para cuando haya algun error

products_list = ["Producto 1","Producto 2",
                 "Producto 3","Producto 4"]

@router.get("/")
async def products():
    return ["Producto 1","Producto 2","Producto 3","Producto 4"]

@router.get("/{id}")
async def products(id:int):
    return products_list[id]