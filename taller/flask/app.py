from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import json

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'una-clave-secreta-000001'

# Configuración de cabeceras con el Token
token = 'c7113110d24ef19be08e0c33565f94db0de3325e'
headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json"
}

@app.route("/")
def hello_world():
    return "<p>Hola mundo - Gestión de Edificios y Departamentos</p>"


# VISTAS PARA EDIFICIOS

@app.route("/los/edificios")
def los_edificios():
    """
    Lista todos los edificios consumidos desde la API de Django
    """
    r = requests.get("http://localhost:8000/api/edificios/", headers=headers)
    
    print("---------------------")
    print(r.content)
    print("---------------------")
    
    edificios = json.loads(r.content)['results']
    numero_edificios = json.loads(r.content)['count']
    
    return render_template("losedificios.html", 
                           edificios=edificios,
                           numero_edificios=numero_edificios)


@app.route("/crear/edificio", methods=['GET', 'POST'])
def crear_edificio():
    """
    Formulario y acción para crear un nuevo Edificio
    """
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        ciudad = request.form['ciudad']
        tipo = request.form['tipo'] # residencial o comercial

        # Mapea perfectamente con tu clase Edificio
        edificio_data = {
            'nombre': nombre,
            'direccion': direccion,
            'ciudad': ciudad,
            'tipo': tipo
        }

        r = requests.post("http://localhost:8000/api/edificios/",
                          json=edificio_data,
                          headers=headers)

        print(f"Status Code (Crear Edificio): {r.status_code}")
        
        nuevo_edificio = json.loads(r.content)
        flash(f"Edificio '{nuevo_edificio['nombre']}' creado exitosamente!", 'success')
        return redirect(url_for('los_edificios'))

    return render_template("crear_edificio.html")


# VISTAS PARA DEPARTAMENTOS

@app.route("/los/departamentos")
def los_departamentos():
    """
    Lista los departamentos y resuelve el nombre del edificio usando la función de ayuda
    """
    r = requests.get("http://localhost:8000/api/departamentos/", headers=headers)
    datos = json.loads(r.content)['results']
    numero = json.loads(r.content)['count']
    
    datos2 = []
    for d in datos:
        # CORRECCIÓN: Se lee usando exactamente las llaves generadas por el modelo de Django
        datos2.append({
            'nombre_completo_propietario': d['nombre_completo_propietario'], 
            'costo_departamento': d['costo_departamento'],
            'numero_cuartos': d['numero_cuartos'], 
            'edificio': obtener_nombre_edificio(d['edificio']) 
        })
        
    return render_template("losdepartamentos.html", datos=datos2, numero=numero)


@app.route("/crear/departamento", methods=['GET', 'POST'])
def crear_departamento():
    """
    Formulario y acción para crear un departamento asociado a un edificio
    """
    edificios_disponibles = []

    # Consumimos los edificios para llenar el select del formulario
    r_edificios = requests.get("http://localhost:8000/api/edificios/", headers=headers)
    edificios_disponibles = json.loads(r_edificios.content)['results']

    if request.method == 'POST':
        # Mapeamos lo que viene del formulario HTML
        propietario_completo = request.form['propietario_completo']
        costo = float(request.form['costo'])
        cuartos_num = int(request.form['cuartos_num'])
        edificio_url = request.form['edificio'] 

        # CORRECCIÓN: Estructura JSON adaptada a los campos idénticos de tu modelo de Django
        departamento_data = {
            'nombre_completo_propietario': propietario_completo,
            'costo_departamento': costo,
            'numero_cuartos': cuartos_num,
            'edificio': edificio_url 
        }

        r = requests.post("http://localhost:8000/api/departamentos/",
                          json=departamento_data,
                          headers=headers)

        print(f"Status Code (Crear Departamento): {r.status_code}")

        nuevo_depto = json.loads(r.content)
        # CORRECCIÓN: Se lee la respuesta usando la llave correcta de Django
        flash(f"Departamento de '{nuevo_depto['nombre_completo_propietario']}' creado exitosamente!", 'success')
        return redirect(url_for('los_departamentos'))

    return render_template("crear_departamento.html",
                           edificios=edificios_disponibles)


# FUNCIONES DE AYUDA (HELPERS)

def obtener_nombre_edificio(url):
    """
    Recibe la URL del edificio (ej: http://127.0.0.1:8000/api/edificios/1/) 
    y retorna su nombre para mostrarlo amigablemente en la tabla.
    """
    if not url:
        return "Sin Edificio"
    r = requests.get(url, headers=headers)
    nombre_edificio = json.loads(r.content)['nombre']
    return nombre_edificio


if __name__ == "__main__":
    app.run(debug=True)