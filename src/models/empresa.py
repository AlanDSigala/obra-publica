from database import db

class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    razon_social = db.Column(db.String(50), nullable=False)
    rfc = db.Column(db.String(15), nullable=False)
    numero_iva = db.Column(db.String(20), nullable=False)
    cmic= db.Column(db.String(20), nullable=False)