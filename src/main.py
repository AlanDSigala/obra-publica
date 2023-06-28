from models.empresa import Empresa
from models.proyecto import Proyecto
from models.frente import Frente
from models.catalogo import Catalogo
from models.estimacion import Estimacion
from flask import Flask, render_template, request, redirect, session, url_for
from database import db
from datetime import datetime, date

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
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
    empresas = db.session.query(Empresa).all()
    return render_template('frentes_obra.html', proyectos=proyectos, empresas=empresas)


@app.route('/proyectos')
def listar_proyectos():
    proyectos = Proyecto.query.all()
    return render_template('proyectos.html', proyectos=proyectos)


@app.route('/registro/frentes/<int:id>', methods=['POST'])
def procesarRegistrarFrentre(id):
    proyecto_id = request.form.get('proyecto_id')
    proyecto = Proyecto.query.filter_by(id=proyecto_id).first()

    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    fecha_inicio = datetime.strptime(request.form.get('fecha_inicio'), '%Y-%m-%d')
    no_contrato = request.form.get('no_contrato')
    fecha_final = datetime.strptime(request.form.get('fecha_final'), '%Y-%m-%d')
    empresa_id = request.form.get('empresa_asociada')
 
    # guardar los datos en la base de datos
    frente = Frente(nombre=nombre, descripcion=descripcion, fecha_inicio=fecha_inicio, no_contrato=no_contrato, fecha_final=fecha_final, proyecto_id= proyecto_id, empresa_id= empresa_id)
    db.session.add(frente)
    db.session.commit()
    return redirect(url_for('gestionar_catalogo', frente_id=frente.id))

@app.route('/proyecto/detalles/<int:id>')
def detalles_proyecto(id):
    proyecto = Proyecto.query.get(id)
    frentes = Frente.query.filter_by(proyecto_id=proyecto.id).all()
    return render_template('detalle_proyecto.html', proyecto=proyecto, frentes=frentes)

@app.route('/proyecto/editar/<int:id>', methods= ['POST', 'GET'] )
def editar_proyecto(id):
    proyecto = Proyecto.query.get(id)
    if request.method == 'POST':
        proyecto.nombre = request.form['nombre']
        proyecto.descripcion= request.form['descripcion']
        proyecto.fecha_inicio = datetime.strptime(request.form.get('fecha_inicio'), '%Y-%m-%d')
        proyecto.fecha_final = datetime.strptime(request.form.get('fecha_final'), '%Y-%m-%d')
        db.session.commit()
        return redirect(url_for('listar_proyectos'))
    
    return render_template('edit_proyectos.html',proyecto=proyecto)

@app.route('/proyecto/detalles/<int:id>/frente/<int:proyecto_id>/editar', methods=['POST','GET'])
def editar_frente(proyecto_id,id):
    frente = Frente.query.get(proyecto_id)
    proyecto = Proyecto.query.get(id)
    if request.method == 'POST':
        frente.nombre=request.form['nombre']
        frente.descripcion= request.form['descripcion']
        frente.fecha_inicio = datetime.strptime(request.form.get('fecha_inicio'), '%Y-%m-%d')
        frente.no_contrato =request.form['no_contrato']
        frente.fecha_final = datetime.strptime(request.form.get('fecha_final'), '%Y-%m-%d')
        db.session.commit()
        return redirect(url_for('detalles_proyecto',id=id))
    
    return render_template('edit_frentes.html',proyecto=proyecto,frente=frente)
        


@app.route('/proyecto/detalles/<int:proyecto_id>/frente/<int:frente_id>')
def detalle_frente(proyecto_id, frente_id):
    
    proyecto = db.session.query(Proyecto).get(proyecto_id)
    frente = db.session.query(Frente).get(frente_id)
    catalogos = db.session.query(Catalogo).filter_by(frente_id=frente_id).all()
    empresa = db.session.query(Empresa).get(frente.empresa_id)
  
    return render_template('detalle_frente.html', frente=frente, proyecto=proyecto, catalogos=catalogos, empresa=empresa)

@app.route('/registro/catalogo/<int:frente_id>', methods=['GET', 'POST'])
def gestionar_catalogo(frente_id):
    frente = Frente.query.get(frente_id)

    if request.method == 'POST':
        clave = request.form.get('clave')
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        unidad = request.form.get('unidad')
        costo = request.form.get('costo')
        cantidad = request.form.get('cantidad')
        importe = float(costo) * float(cantidad)
    
        # guardar los datos en la base de datos
        catalogo = Catalogo(clave=clave, nombre=nombre, descripcion=descripcion, unidad=unidad, costo_unitario=costo, cantidad=cantidad,importe=importe, frente_id=frente_id)
        db.session.add(catalogo)
        db.session.commit()

        return redirect(url_for('listar_proyectos'))
    
    return render_template('registro_catalogo.html', frente=frente)


@app.route('/empresas')
def listar_empresas():
    empresas = Empresa.query.all()
    return render_template('empresas.html', empresas=empresas)

@app.route('/registro/empresa', methods=['GET', 'POST'])
def registro_empresas():
    if request.method == 'POST':
        nombre = request.form['nombre']
        razon_social = request.form['razon']
        rfc = request.form['rfc']
        numero_iva = request.form['no_iva']
        cmic= request.form['cmic']

        empresa = Empresa(nombre=nombre, razon_social=razon_social, rfc=rfc, numero_iva=numero_iva, cmic=cmic)
        db.session.add(empresa)
        db.session.commit()

        return redirect(url_for('listar_empresas'))

    return render_template('registro_empresas.html')

@app.route('/empresas/editar/<int:id>', methods=['GET', 'POST'])
def editar_empresa(id):
    empresa = Empresa.query.get(id)
    if request.method == 'POST':
        empresa.nombre=request.form['nombre']
        empresa.razon_social = request.form['razon']
        empresa.rfc = request.form['rfc']
        empresa.numero_iva = request.form['no_iva']
        empresa.cmic= request.form['cmic']
        db.session.commit()
        return redirect(url_for('listar_empresas'))
    
    return render_template('edit_empresas.html',empresa=empresa)
    

@app.route('/proyecto/<int:proyecto_id>/frente/<int:frente_id>/estimacion', methods=['GET', 'POST'])
def estimacion(proyecto_id, frente_id):
    proyecto = db.session.query(Proyecto).get(proyecto_id)
    frente = db.session.query(Frente).get(frente_id)
    estimacion_anterior = db.session.query(Estimacion).filter_by(frente_id=frente_id).order_by(Estimacion.fecha.desc()).first()

    if estimacion_anterior:
        # Datos de la carátula de estimación
        nombre_empresa = frente.empresa.nombre
        numero_contrato = frente.no_contrato
        fecha_contrato = frente.fecha_inicio
        razon_social = frente.empresa.razon_social
        fecha = date.today()

        # Obtener los datos de la estimación anterior
        importe_contrato = estimacion_anterior.importe_contrato
        importe_estimado_acumulado_anterior = estimacion_anterior.importe_estimado_acumulado_actual

        if request.method == 'POST':
            importe_estimado_actual = float(request.form['importe_estimado_actual'])
            numero_estimacion = request.form['numero_estimacion']
            periodo = request.form['periodo']
        else:
            importe_estimado_actual = 0

        importe_estimado_acum_actual = importe_estimado_acumulado_anterior + importe_estimado_actual
        saldo_por_estimar = importe_contrato - importe_estimado_acum_actual

        estimacion = Estimacion(
            numero_estimacion=numero_estimacion,
            fecha=fecha,
            importe_contrato=importe_contrato,
            importe_estimado_acum_anterior=importe_estimado_acumulado_anterior,
            importe_estimado_actual=importe_estimado_actual,
            importe_estimado_acum_actual=importe_estimado_acum_actual,
            saldo_por_estimar=saldo_por_estimar,
            numero_contrato=numero_contrato,
            razon_social=razon_social,
            periodo=periodo,
            frente=frente)

        db.session.add(estimacion)
        db.session.commit()

        return render_template('estimacion.html', frente=frente, proyecto=proyecto,
                               importe_estimado_acumulado_anterior=importe_estimado_acumulado_anterior,
                               importe_contrato=importe_contrato, saldo_por_estimar=saldo_por_estimar,
                               nombre_empresa=nombre_empresa, numero_contrato=numero_contrato,
                               fecha_contrato=fecha_contrato, razon_social=razon_social, fecha=fecha)
    else:
        # No hay estimación anterior, obtener datos del frente y calcular valores

        # Datos de la carátula de estimación
        nombre_empresa = frente.empresa.nombre
        numero_contrato = frente.no_contrato
        fecha_contrato = frente.fecha_inicio
        razon_social = frente.empresa.razon_social
        fecha = date.today()

        # Realizar los cálculos iniciales
        importe_contrato = 0

        for concepto in frente.catalogos_relacionados:
            importe_contrato += concepto.importe

        importe_estimado_acumulado_anterior = 0
        numero_estimacion = 0 
        periodo="000"

        if request.method == 'POST':
            importe_estimado_actual = float(request.form['importe_estimado_actual'])
            numero_estimacion = request.form['numero_estimacion']
            periodo = request.form['periodo']
            importe_estimado_acum_actual = importe_estimado_actual + importe_estimado_acumulado_anterior
            saldo_por_estimar = importe_contrato - importe_estimado_acum_actual
        else:
            importe_estimado_actual = 0
            importe_estimado_acum_actual = importe_estimado_actual + importe_estimado_acumulado_anterior
            saldo_por_estimar = importe_contrato - importe_estimado_actual

        estimacion = Estimacion(
            numero_estimacion=numero_estimacion,
            fecha=fecha,
            importe_contrato=importe_contrato,
            importe_estimado_acum_anterior=importe_estimado_acumulado_anterior,
            importe_estimado_actual=importe_estimado_actual,
            importe_estimado_acum_actual=importe_estimado_acum_actual,
            saldo_por_estimar=saldo_por_estimar,
            numero_contrato=numero_contrato,
            razon_social=razon_social,
            periodo=periodo,
            frente=frente)

        return render_template('estimacion.html', frente=frente, proyecto=proyecto,
                               importe_estimado_acumulado_anterior=importe_estimado_acumulado_anterior,
                               importe_contrato=importe_contrato, saldo_por_estimar=saldo_por_estimar,
                               nombre_empresa=nombre_empresa, numero_contrato=numero_contrato,
                               fecha_contrato=fecha_contrato, razon_social=razon_social,
                               importe_estimado_acum_actual=importe_estimado_acum_actual, fecha=fecha)





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
