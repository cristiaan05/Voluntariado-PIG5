create database IF NOT EXISTS DBVoluntariadoG5;
use DBVoluntariadoG5;

DROP TABLE if exists admin;

CREATE TABLE if not exists admin(
	id_Admin INT not null UNIQUE,
    nombre_Admin varchar(100) UNIQUE not null primary key,
    contraseña_Admin varchar(100) not null,
    correo_Admin varchar(100) not null
)ENGINE=MyISAM;

DROP TABLE if exists ensenanza;

CREATE TABLE if not exists ensenanza(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    titulo varchar(8000),
    cuerpo varchar(8000)
)ENGINE=MyISAM;

DROP TABLE if exists noticias;

CREATE TABLE if not exists noticias(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    titulo varchar(8000),
    cuerpo varchar(8000)
)ENGINE=MyISAM;

INSERT INTO  admin VALUES(1,'admin','1234','admin@gmail.com');
# UPDATE admin SET nombre_Admin = "admins", contraseña_Admin = "123", correo_Admin = "@gmail.com" WHERE nombre_Admin = "admin";
#INSERT INTO ensenanza VALUES(NULL,"hola","mundo");
#INSERT INTO ensenanza VALUES(NULL,"hola3","mundo3");
#DELETE FROM ensenanza WHERE id = '1';
#INSERT INTO ensenanza VALUES(NULL,"hola2","mundo2");

SELECT * FROM ensenanza;
SELECT * FROM noticias;
SELECT * FROM admin;
