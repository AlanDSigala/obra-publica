from database import db

class Estimacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_estimacion = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    importe_contrato = db.Column(db.Float, nullable=False)
    importe_estimado_acum_anterior = db.Column(db.Float, nullable=False)
    importe_estimado_actual = db.Column(db.Float, nullable=False)
    importe_estimado_acum_actual = db.Column(db.Float, nullable=False)
    saldo_por_estimar = db.Column(db.Float, nullable=False)
    numero_contrato = db.Column(db.String(50), nullable=False)
    razon_social = db.Column(db.String(100), nullable=False)
    periodo = db.Column(db.String(50), nullable=False)
    frente_id = db.Column(db.Integer, db.ForeignKey('frente.id'), nullable=False)
    frente = db.relationship('Frente', backref=db.backref('estimaciones', lazy=True))