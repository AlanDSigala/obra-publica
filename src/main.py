from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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
    return render_template('registro_proyecto.html')
    """accion = request.form['accion']
    if accion == 'registrar':
        return render_template('registro_proyecto.html')
    else:
        return redirect(url_for('consultar'))"""
    
@app.route('/registro/frentes', methods=['POST'])
def registroFrentes():
    return render_template('frentes_obra.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)

    """name = request.form['txtNombre']
    print(name)
    return redirect(url_for('index'))"""