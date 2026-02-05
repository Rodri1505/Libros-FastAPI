from models.libro import Libro

libros: list[Libro] = [
    Libro(id=1,titulo="El ojo del mundo",autor="Robert Jordan", fecha_publicacion="1980-07-15",digital=True),
    Libro(id=2,titulo="Buenos Presagios",autor="Terry Pratchet", fecha_publicacion="2000-12-10",digital=True),
    Libro(id=3,titulo="El tercer gemelo",autor="Ken Follet", fecha_publicacion="1995-05-03",digital=False)

    
]