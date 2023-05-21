from database import db 

class Frente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    no_contrato = db.Column(db.String(50), nullable=False)
    fecha_final = db.Column(db.Date, nullable=False)
    proyecto_id = db.Column(db.Integer, db.ForeignKey('proyecto.id'), nullable=False)
    proyecto = db.relationship('Proyecto', backref=db.backref('frentes', lazy=True))
    catalogos_relacionados = db.relationship('Catalogo', backref='frente', lazy=True)