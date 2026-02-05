from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI,Depends, HTTPException
from data.db import libros
from models.libro import Libro
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    mensaje = "Hola mundo"
    return templates.TemplateResponse("index.html", {"request": request, "mensaje": mensaje})

@app.get("/libros",response_class=HTMLResponse)
async def ver_libros(request: Request):
    return templates.TemplateResponse("libros.html",{"request": request, "libros": libros})

@app.get("/libros/{libro_id}",response_class=HTMLResponse)
async def  buscar_libro_id(libro_id:int, request: Request):
    libro_encontrado=buscar_libro(libro_id)
    if not libro_encontrado:
        raise HTTPException(status_code=404, detail= "Libro no encontrado")
    return templates.TemplateResponse("libros_detalle.html",{"request": request, "libro":libro_encontrado})

@app.get("/libros",response_model=list[Libro])
async def listar_libros():
    return libros

def siguiente_id() -> int:
    if len(libros) == 0:
        return 1
    else:
        return max(libro.id for libro in libros if libro.id is not None) + 1
    
@app.post("/libros",status_code=201)
async def insertar_libro(libro:Libro):
    libro.id=siguiente_id
    libros.append(libro)
    return libro

def buscar_libro(libro_id:int):
    for libro in libros:
        if libro.id == libro_id:
            return libro
    return None

@app.put("/libros/{libro_id}", response_model=Libro)
async def actualizar_libro(libro_id:int,libro_actualizado:Libro):
    libro=buscar_libro(libro_id)
    if libro is None:
        raise HTTPException(status_code=404,detail="Libro no encontrado")
    if libro_actualizado.titulo is not None:
        libro.titulo=libro_actualizado.titulo
    if libro_actualizado.autor is not None:
        libro.titulo=libro_actualizado.titulo
    if libro_actualizado.fecha_publicacion is not None:
        libro.fecha_publicacion=libro_actualizado.fecha_publicacion
    if libro_actualizado.digital is not None:
        libro.digital=libro_actualizado.digital
    return libro

@app.delete("/libros/{libro_id}",status_code=204)
async def eliminar_libro(libro_id:int):
    libro =buscar_libro(libro_id)
    if libro is None:
        raise HTTPException(status_code=404,detail="Libro no encontrado")
    libros.remove(libro)
    return{"mensaje":"Libro eliminado correctamente."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)

