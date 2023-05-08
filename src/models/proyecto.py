
from database import db 


class Proyecto(db.Model):
    id = db.Column(db.Integer, primary_key= True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.String(200))
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_final = db.Column(db.DateTime, nullable=False)

