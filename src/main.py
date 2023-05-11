from models.proyecto import Proyecto
from models.frente import Frente
from flask import Flask, render_template, request, redirect, session, url_for
from database import db
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///obra.db'
with app.app_context():
    db.init_app(app)
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

# función que muestra el formulario
@app.route('/registro/proyecto', methods=['POST'])
def registroProyecto():
    return render_template('registro_proyecto.html')

# función que procesa los datos del formulario
@app.route('/registro/proyecto1', methods=['POST'])
def procesarRegistroProyecto():
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    fecha_inicio = datetime.strptime(request.form.get('fecha_inicio'), '%Y-%m-%d')
    fecha_final = datetime.strptime(request.form.get('fecha_final'), '%Y-%m-%d')

    # guardar los datos en la base de datos
    proyecto = Proyecto(nombre=nombre, descripcion=descripcion, fecha_inicio=fecha_inicio, fecha_final=fecha_final)
    db.session.add(proyecto)
    db.session.commit()
    # redirigir al usuario a la página que muestra el formulario
    return redirect(url_for('registroFrentes', proyecto_id=proyecto.id))

    
@app.route('/registro/frentes')
def registroFrentes():
    proyectos = db.session.query(Proyecto).all()
    return render_template('frentes_obra.html', proyectos=proyectos)


@app.route('/proyectos')
def listar_proyectos():
    proyectos = Proyecto.query.all()
    return render_template('proyectos.html', proyectos=proyectos)

@app.route('/registro/frentes/1')
def procesarRegistrarFrentre():
    proyecto_id = request.form.get('proyecto_id')
    proyecto = session.query(Proyecto).get(proyecto_id)

    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    fecha_inicio = datetime.strptime(request.form.get('fecha_inicio'), '%Y-%m-%d')
    no_contrato = request.form.get('no_contrato')
    fecha_final = datetime.strptime(request.form.get('fecha_final'), '%Y-%m-%d')
    proyecto_asociado = request.form.get('proyecto')  
    # guardar los datos en la base de datos
    frente = Frente(nombre=nombre, descripcion=descripcion, fecha_inicio=fecha_inicio, no_contrato=no_contrato, fecha_final=fecha_final, proyecto_id= proyecto_asociado)
    db.session.add(frente)
    db.session.commit()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
