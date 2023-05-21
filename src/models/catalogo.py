from database import db

class Catalogo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(50), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    unidad = db.Column(db.String(50), nullable=False)
    costo_unitario = db.Column(db.Float, nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    frente_id = db.Column(db.Integer, db.ForeignKey('frente.id'), nullable=False)
