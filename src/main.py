from models.proyecto import Proyecto
from flask import Flask, render_template, request, redirect, url_for
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

    print(f'nombre: {nombre}')
    print(f'descripcion: {descripcion}')
    print(f'fecha_inicio: {fecha_inicio}')
    print(f'fecha_final: {fecha_final}')
    print(f'hola')


    # guardar los datos en la base de datos
    proyecto = Proyecto(nombre=nombre, descripcion=descripcion, fecha_inicio=fecha_inicio, fecha_final=fecha_final)
    db.session.add(proyecto)
    db.session.commit()
    # redirigir al usuario a la página que muestra el formulario
    return redirect(url_for('registroFrentes', proyecto_id=proyecto.id))

    
@app.route('/registro/frentes/<int:proyecto_id>')
def registroFrentes(proyecto_id):
    proyecto = Proyecto.query.get(proyecto_id)

    if proyecto is None:
        return redirect(url_for('consultar'))

    return render_template('frentes_obra.html', proyecto=proyecto)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
