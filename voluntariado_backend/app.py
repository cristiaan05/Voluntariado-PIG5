#importando nuestras librerías es útil recordar que hay que instalarlas usando loas pip install y así para poder hacer uso de flask
from types import MethodDescriptorType
from flask import Flask, jsonify, request
from flask_cors import CORS 
import json
#Modulo para conectar a la base de datos
from flask_mysqldb import MySQL
#Librerías implementadas
from config import config
from Admin import Admin


admin = []

app = Flask(__name__)
db = MySQL(app)
CORS(app)

#Agregando administradores
admin.append(Admin('1','admin','1234','admin@gmail.com'))

#-----------------------------------------METODOS DE ADMIN--------------------------------------------------
#buscar administrador
@app.route('/Admin/<string:nombre_Usuario>', methods=['GET'])
def obtenerAdmin(nombre_Usuario):
    try:
        cursor = db.connection.cursor()
        sql = "SELECT * FROM admin"
        cursor.execute(sql)
        datos = cursor.fetchall()
        print(datos)
        return "Ok"
    except Exception as error:
        return "Error"
    # global admin
    # for adminBuscado in admin:
    #     if adminBuscado.nombre_Usuario == nombre_Usuario:
    #         objeto = {
    #             'id': adminBuscado.id,
    #             'nombre_Usuario': adminBuscado.nombre_Usuario,  
    #             'contraseña': adminBuscado.contraseña,
    #             'correo': adminBuscado.correo
    #         }
    #         return(jsonify(objeto))

    # salida={"Mensaje":"No existe el administrador"}
    # return(jsonify(salida))
    

#Modificar administrador
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

def pagina_no_encontrada(error):
    return "<h1>La página que intentas buscar no existe...</h1>"


if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()