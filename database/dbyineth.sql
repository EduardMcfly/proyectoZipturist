create database turismoZ;
use turismoZ;
create table usuario(
id_Usuario int not null primary key auto_increment,
nombre_Usuario varchar(50),
correo_Usuario varchar(50),
contraseña_Usuario varchar(200) 
 );
 
 create table CentrosReligiosos(
id_Centro int not null primary key auto_increment,
nombre_Centro varchar(100),
direccion_Centro varchar(100),
descipcion_Centro varchar(500),
contacto_Centro numeric(11),
imagen_Centro varchar(50),
usuario_Id int not null ,
CONSTRAINT fk_usuario FOREIGN KEY (usuario_Id) REFERENCES usuario(id_Usuario)
 );
 
 create table actividadesReprecentativas(
id_Actividad int not null primary key auto_increment,
nombre_Actividad varchar(100),
lugar_Actividad varchar(100),
descipcion_Actividad varchar(500),
contacto_Actividad numeric(11),
imagen_Actividad varchar(50),
usuario_Id int not null ,
CONSTRAINT fk_usuarios FOREIGN KEY (usuario_Id) REFERENCES usuario(id_Usuario)
 );
 
  create table hoteles(
id_hotel int not null primary key auto_increment,
nombre_hotel varchar(100),
direccion_hotel varchar(100),
descipcion_hotel varchar(500),
contacto_hotel numeric(11),
imagen_hotel varchar(50),
usuario_Id int not null ,
CONSTRAINT fk_usuario1 FOREIGN KEY (usuario_Id) REFERENCES usuario(id_Usuario)
 );
 
 create table restaurantes(
id_restaurante int not null primary key auto_increment,
nombre_restaurante varchar(100),
direccion_restaurante varchar(100),
descipcion_restaurante varchar(500),
contacto_restaurante numeric(11),
imagen_restaurante varchar(50),
usuario_Id int not null ,
CONSTRAINT fk_usuario2 FOREIGN KEY (usuario_Id) REFERENCES usuario(id_Usuario)
 );
 
 create table sitiosTuristicos(
id_sitiosT int not null primary key auto_increment,
nombre_sitiosT varchar(100),
direccion_sitiosT varchar(100),
descipcion_sitiosT varchar(500),
contacto_sitiosT numeric(11),
imagen_sitiosT varchar(50),
usuario_Id int not null ,
CONSTRAINT fk_usuario3 FOREIGN KEY (usuario_Id) REFERENCES usuario(id_Usuario)
 );

  create table Artesanias(
id_artesanias int not null primary key auto_increment,
nombre_artesanias varchar(100),
direccion_artesanias varchar(100),
descipcion_artesanias varchar(500),
contacto_artesanias numeric(11),
imagen_artesanias varchar(50),
usuario_Id int not null ,
CONSTRAINT fk_usuario4 FOREIGN KEY (usuario_Id) REFERENCES usuario(id_Usuario)
 );
 