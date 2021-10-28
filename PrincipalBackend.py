#importando nuestras librerías es útil recordar que hay que instalarlas usando loas pip install y así para poder hacer uso de flask
from types import MethodDescriptorType
from flask import Flask, jsonify, request
from flask_cors import CORS 
import json

from voluntariado_backend.Admin import Admin

admin = []

app = Flask(__name__)
CORS(app)

#Agregando administradores
admin.append(Admin('admin','1234','admin@gmail.com'))

#-----------------------------------------METODOS DE ADMIN--------------------------------------------------
#buscar un solo dato
@app.route('/Admin/<string:nombre_Usuario>', methods=['GET'])
def obtenerAdmin(nombre_Usuario):
    global admin
    for adminBuscado in admin:
        if adminBuscado.nombre_Usuario == nombre_Usuario:
            objeto = {
                'nombre_Usuario': adminBuscado.nombre_Usuario,
                'contraseña': adminBuscado.contraseña,
                'correo': adminBuscado.correo
            }
            return(jsonify(objeto))

    salida={"Mensaje":"No existe el administrador"}
    return(jsonify(salida))

#Modificar medicamento
@app.route('/Admin/<string:nombre_Usuario>', methods=['PUT'])
def actualizarAdmin(nombre_Usuario):
    global admin
    for recorrer in range(len(admin)):
        if nombre_Usuario == admin[recorrer].nombre_Usuario:
            admin[recorrer].nombre_Usuario = request.json['nombre_Usuario']
            admin[recorrer].contraseña = request.json['contraseña']
            admin[recorrer].correo = request.json['correo']
            return jsonify({"Mensaje":"Datos de administrador actualizados con éxito!!!"})
    return jsonify({"Mensaje":"El registro no existe"})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)