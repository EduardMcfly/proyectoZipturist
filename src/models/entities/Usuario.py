from werkzeug.security import check_password_hash
from flask_login import UserMixin


class Usuario(UserMixin):
    def __init__(self,id_Usuario , nombre_Usuario, correo_Usuario , contraseña_Usuario) -> None:
        self.id= id_Usuario
        self.nombre_Usuario = nombre_Usuario
        self.correo_Usuario = correo_Usuario
        self.contraseña_Usuario = contraseña_Usuario

#función de encriptar y desencriptar la contraseña
    @classmethod
    def check_password(self, hashed_contraseña_Usuario, contraseña_Usuario):
        return check_password_hash(hashed_contraseña_Usuario, contraseña_Usuario)