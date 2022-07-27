#Nota: recordar que si quiero que todo funcione, tengo que inicializar un entorno virtual correcto. 
#Dicho entorno debe crearse en la carpeta que se va a ejecutar el servidor y activarse
#luego instalar las librerias con: pip install flask flask_cors flask_mysqldb

#importando nuestras librerías es útil recordar que hay que instalarlas usando loas pip install y así para poder hacer uso de flask
from flask import Flask, jsonify, request
from flask.wrappers import Request
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
#Mail de peticiones
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

#Mail de contactos
@app.route('/send-email-contacto', methods = ['POST'])
def send_mail_contacto():
    try:
        nombre = request.json['nombre']
        #Recordar email es el correo al cual se envía el mensaje
        email = request.json['email']
        cuerpoMensaje = request.json['message']
        
        #aquí va el contenido del email: asunto, cuerpo y así.
        message = f'''Subject: MENSAJE DE CONTACTO\nContent-type: text/html\n
                    <h1>Mensaje enviado por: {nombre} </h1>
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



#-----------------------------------------METODOS DE ENSEÑANZA---------------------------------------------------
#Mostrar ensenanzas
@app.route('/Ensenanza', methods=['GET'])
def mostrarEnsenanzas():
    try:
        #conexion con la base de datos
        cursor = db.connection.cursor() 
        sql = "SELECT * FROM ensenanza"
        cursor.execute(sql) #se ejecuta el comando sql en la base de datos
        datos = cursor.fetchall() # Al ejecutar el sql nos devuelve una tupla de tuplas
        print(datos) #Ver el print para entender mejor cual es la devolución en datos.
        return (jsonify(datos)) # Se devuelve un json para mejor facilidad en javascript
    except Exception as error:
        salida={"Mensaje":"Error"}
        return (jsonify(error))


#Buscar ensenanza
@app.route('/Ensenanza/<string:id>', methods=['GET'])
def obtenerEnsenanza(id):
    ensenanza = []
    try:
        #conexion con la base de datos
        cursor = db.connection.cursor() 
        sql = "SELECT * FROM ensenanza"
        cursor.execute(sql) #se ejecuta el comando sql en la base de datos
        datos = cursor.fetchall() # Al ejecutar el sql nos devuelve una tupla de tuplas
        print(datos) #Ver el print para entender mejor cual es la devolución en datos.
        for ensenanza in datos: # por esa tupla de tuplas hacemos un for donde vamos a recorrer los datos de la tupla en la tupla
            if ensenanza[0] == int(id): #ensenanza[1] vendría siendo el nombre de cada tupla ensenanza.
                objeto = {
                'titulo': ensenanza[1],  
                'cuerpo': ensenanza[2]
                }
                return (jsonify(objeto)) # Se devuelve un json para mejor facilidad en javascript
        salida={"Mensaje":"No existe la enseñanza seleccionada."}
        return(jsonify(salida))
    except Exception as error:
        salida={"Mensaje":"Error"}
        return (jsonify(error))


#Modificar ensenanza
@app.route('/Ensenanza/<string:id>', methods=['PUT'])
def actualizarEnsenanza(id):
    try:
        print(id)
        #conexion con la base de datos
        cursor = db.connection.cursor() 
        sql = 'UPDATE ensenanza SET titulo = "{1}", cuerpo = "{2}" WHERE id = "{0}";'.format(id, request.json['titulo'], request.json['cuerpo'])
        cursor.execute(sql) #se ejecuta el comando sql en la base de datos
        db.connection.commit() # Confirma la acción de inserción
        
        print(id, request.json['titulo'], request.json['cuerpo'])
        salida={"Mensaje":"Actualización realizada con éxito"}

        return(jsonify(salida))

    except Exception as error:
        salida={"Mensaje": f"Error: {error}"}
        return (jsonify(error))


#Eliminar ensenanza
@app.route('/Ensenanza/<string:id>', methods=['DELETE'])
def eliminarEnsenanza(id):
    try:
        print(id)
        #conexion con la base de datos
        cursor = db.connection.cursor() 
        sql = 'DELETE FROM ensenanza WHERE id = "{0}";'.format(id)
        cursor.execute(sql) #se ejecuta el comando sql en la base de datos
        db.connection.commit() # Confirma la acción de inserción
        
        print(id)
        salida={"Mensaje":"Eliminación realizada con éxito"}

        return(jsonify(salida))

    except Exception as error:
        salida={"Mensaje": f"Error: {error}"}
        return (jsonify(error))


#Agregar enseñanza
@app.route('/Ensenanza', methods=['POST'])
def agregarEnsenanza():
    try:
        print(id)
        #conexion con la base de datos
        cursor = db.connection.cursor() 
        sql = 'INSERT INTO ensenanza VALUES(NULL, "{0}", "{1}");'.format(request.json['titulo'], request.json['cuerpo'])
        cursor.execute(sql) #se ejecuta el comando sql en la base de datos
        db.connection.commit() # Confirma la acción de inserción
        
        print(id)
        salida={"Mensaje":"Enseñanza agregada con éxito"}

        return(jsonify(salida))

    except Exception as error:
        salida={"Mensaje": f"Error: {error}"}
        return (jsonify(error))


#-----------------------------------------METODOS DE NOTICIAS---------------------------------------------------
#Mostrar Noticias
@app.route('/Noticia', methods=['GET'])
def mostrarNoticias():
    try:
        #conexion con la base de datos
        cursor = db.connection.cursor()
        sql = "SELECT * FROM noticias"
        cursor.execute(sql) #se ejecuta el comando sql en la base de datos
        datos = cursor.fetchall() # Al ejecutar el sql nos devuelve una tupla de tuplas
        print(datos) #Ver el print para entender mejor cual es la devolución en datos.
        return (jsonify(datos)) # Se devuelve un json para mejor facilidad en javascript
    except Exception as error:
        salida={"Mensaje":"Error"}
        return (jsonify(error))


#Buscar Noticias
@app.route('/Noticia/<string:id>', methods=['GET'])
def obtenerNoticia(id):
    noticias = []
    try:
        #conexion con la base de datos
        cursor = db.connection.cursor() 
        sql = "SELECT * FROM noticias"
        cursor.execute(sql) #se ejecuta el comando sql en la base de datos
        datos = cursor.fetchall() # Al ejecutar el sql nos devuelve una tupla de tuplas
        print(datos) #Ver el print para entender mejor cual es la devolución en datos.
        for noticias in datos: # por esa tupla de tuplas hacemos un for donde vamos a recorrer los datos de la tupla en la tupla
            if noticias[0] == int(id): #noticias[1] vendría siendo el nombre de cada tupla noticias.
                objeto = {
                'titulo': noticias[1],  
                'cuerpo': noticias[2]
                }
                return (jsonify(objeto)) # Se devuelve un json para mejor facilidad en javascript
        salida={"Mensaje":"No existe la enseñanza seleccionada."}
        return(jsonify(salida))
    except Exception as error:
        salida={"Mensaje":"Error"}
        return (jsonify(error))


#Modificar noticias
@app.route('/Noticia/<string:id>', methods=['PUT'])
def actualizarNoticia(id):
    try:
        print(id)
        #conexion con la base de datos
        cursor = db.connection.cursor() 
        sql = 'UPDATE noticias SET titulo = "{1}", cuerpo = "{2}" WHERE id = "{0}";'.format(id, request.json['titulo'], request.json['cuerpo'])
        cursor.execute(sql) #se ejecuta el comando sql en la base de datos
        db.connection.commit() # Confirma la acción de inserción
        
        print(id, request.json['titulo'], request.json['cuerpo'])
        salida={"Mensaje":"Actualización realizada con éxito"}

        return(jsonify(salida))

    except Exception as error:
        salida={"Mensaje": f"Error: {error}"}
        return (jsonify(error))

#Eliminar noticias
@app.route('/Noticia/<string:id>', methods=['DELETE'])
def eliminarNoticia(id):
    try:
        print(id)
        #conexion con la base de datos
        cursor = db.connection.cursor() 
        sql = 'DELETE FROM noticias WHERE id = "{0}";'.format(id)
        cursor.execute(sql) #se ejecuta el comando sql en la base de datos
        db.connection.commit() # Confirma la acción de inserción
        
        print(id)
        salida={"Mensaje":"Eliminación realizada con éxito"}

        return(jsonify(salida))

    except Exception as error:
        salida={"Mensaje": f"Error: {error}"}
        return (jsonify(error))

#Agregar noticia
@app.route('/Noticia', methods=['POST'])
def agregarNoticia():
    try:
        print(id)
        #conexion con la base de datos
        cursor = db.connection.cursor() 
        sql = 'INSERT INTO noticias VALUES(NULL, "{0}", "{1}");'.format(request.json['titulo'], request.json['cuerpo'])
        cursor.execute(sql) #se ejecuta el comando sql en la base de datos
        db.connection.commit() # Confirma la acción de inserción
        
        print(id)
        salida={"Mensaje":"Noticia agregada con éxito"}

        return(jsonify(salida))

    except Exception as error:
        salida={"Mensaje": f"Error: {error}"}
        return (jsonify(error))



if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()