#Bienvenido al archivo de configuracion de la app flask
from flask_mysqldb import MySQL


class DevelopmentConfig():
    DEBUG = True
    HOST = "0.0.0.0"
    PORT = 5000
    #parametros de conexion
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '1234'
    MYSQL_DB = 'DBVoluntariadoG5'
    

#Aqui voy a tener las configuraciones del proyectos
config = {
    'development': DevelopmentConfig
}