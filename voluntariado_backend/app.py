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




app = Flask(__name__)
db = MySQL(app)
CORS(app)



#-----------------------------------------METODOS DE ADMIN--------------------------------------------------
#buscar administrador
@app.route('/Admin/<string:nombre_Usuario>', methods=['GET'])
def obtenerAdmin(nombre_Usuario):
    admin = []
    try:
        #conexion con la base de datos
        cursor = db.connection.cursor() 
        sql = "SELECT * FROM admin"
        cursor.execute(sql) #se ejecuta el comando sql en la base de datos
        datos = cursor.fetchall() # Al ejecutar el sql nos devuelve una tupla de tuplas
        print(datos) #Ver el print para entender mejor cual es la devolución en datos.
        for admin in datos: # por esa tupla de tuplas hacemos un for donde vamos a recorrer los datos de la tupla en la tupla
            if admin[1] == nombre_Usuario: #admin[1] vendría siendo el nombre de cada tupla admin.
                objeto = {
                'id': admin[0],
                'nombre_Usuario': admin[1],  
                'contraseña': admin[2],
                'correo': admin[3]
                }
                return (jsonify(objeto)) # Se devuelve un json para mejor facilidad en javascript
        salida={"Mensaje":"No existe el administrador"}
        return(jsonify(salida))
    except Exception as error:
        salida={"Mensaje":"Error"}
        return (jsonify(error))

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