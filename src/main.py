from models import Proyecto
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy





app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/obra.db'
db = SQLAlchemy(app)
db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro')
def registro():
    return render_template('formulario_proyecto.html ')

@app.route('/consultar', methods=['POST'])
def consultar():
    return render_template('consultar.html')

@app.route('/registro/values', methods=['POST'])
def registroValues():
    proyecto = Proyecto(nombre=request.form['nombre'], 
    descripcion=request.form['descripcion'],
    fecha_inicio=request.form['fecha_inicio'],
    fecha_final=request.form['fecha_final'])
    #db.session.add(proyecto)
    #db.session.commit()
    return render_template('registro_proyecto.html')

    
@app.route('/registro/frentes', methods=['POST'])
def registroFrentes():
    return render_template('frentes_obra.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
