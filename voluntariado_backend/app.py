#importando nuestras librerías es útil recordar que hay que instalarlas usando loas pip install y así para poder hacer uso de flask
from re import S
from types import MethodDescriptorType
from flask import Flask, jsonify, request
from flask_cors import CORS 
import json
#Modulo para conectar a la base de datos
from flask_mysqldb import MySQL
#Librerías implementadas
from config import config
from Admin import Admin
#Librería utilizada para el envío de email
#En Python, el módulo smtplib define un objeto de sesión de cliente SMTP 
#que se puede usar para enviar correo a cualquier máquina de Internet con un daemon de escucha SMTP o ESMTP.
import smtplib



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
    try:
        print(nombre_Usuario)
        #conexion con la base de datos
        cursor = db.connection.cursor() 
        sql = 'UPDATE admin SET nombre_Admin = "{1}", contraseña_Admin = "{2}", correo_Admin = "{3}" WHERE nombre_Admin = "{0}";'.format(nombre_Usuario, request.json['nombre_Usuario'], request.json['contraseña'], request.json['correo'])
        cursor.execute(sql) #se ejecuta el comando sql en la base de datos
        db.connection.commit() # Confirma la acción de inserción
        
        print(nombre_Usuario, request.json['nombre_Usuario'], request.json['contraseña'], request.json['correo'])
        print(type(nombre_Usuario), type(request.json['nombre_Usuario']), type(request.json['contraseña']), type(request.json['correo']))
        salida={"Mensaje":"Actualización realizada con éxito"}

        return(jsonify(salida))

    except Exception as error:
        salida={"Mensaje": f"Error: {error}"}
        return (jsonify(error))


def pagina_no_encontrada(error):
    return "<h1>La página que intentas buscar no existe...</h1>"


#-----------------------------------------METODOS DE PETICIONES--------------------------------------------------
@app.route('/send-email', methods = ['POST'])
def send_mail():
    try:
        nombre = request.json['nombre']
        apellido = request.json['apellido']
        asunto = request.json['asunto']
        #Recordar email es el correo al cual se envía el mensaje
        email = request.json['email']
        cuerpoMensaje = request.json['message']
        
        #aquí va el contenido del email: asunto, cuerpo y así.
        message = f'''Subject: {asunto}\nContent-type: text/html\n
                    <h1>Peticion solicitada por: {nombre} {apellido} </h1>
                    <h1>correo: {email}</h1><h1>Cuerpo del mensaje</h1><h2>{cuerpoMensaje}</h2>''' 
        #Establecemos conexión al servidor SMTP mediante el Host y puerto SMTP de Gmail 
        server = smtplib.SMTP("smtp.gmail.com", 587)  
        #Protocolo de cifrado de datos utilizado por gmail - Encriptación TLS
        server.starttls() #Esto solo aplica por el puerto que estamos utilizando 587 de otra forma solo se asigna por default
        #Iniciar sesión en el servidor SMTP
        server.login("voluntariadog5@gmail.com", "voluntariadoG5$")
        #Enviando el correo con el cuerpo y todo
        server.sendmail("voluntariadog5@gmail.com", "voluntariadog5@gmail.com", message)

        #Desconectar del servidor SMTP
        server.quit()

        salida={"Mensaje":"Email enviado con éxito"}
        return(jsonify(salida))

    except Exception as err:
        print(err)

if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()