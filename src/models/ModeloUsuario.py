from .entities.Usuario import Usuario

#Creación del modelo de usuario
class ModeloUsuario():

    @classmethod
    def login(self, db, usuario):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id_Usuario , nombre_Usuario, correo_Usuario , contraseña_Usuario FROM usuario 
                    WHERE correo_Usuario = '{}'""".format(usuario.correo_Usuario)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                usuario = Usuario(row[0], row[1],row[2],Usuario.check_password(row[3], usuario.contraseña_Usuario), )
                return usuario
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
            try:
                cursor = db.connection.cursor()
                sql = "SELECT id_Usuario , nombre_Usuario, correo_Usuario FROM usuario WHERE id_Usuario  = {}".format(id)
                cursor.execute(sql)
                row = cursor.fetchone()
                if row != None:
                    return Usuario(row[0], row[1], row[2],None)
                    
                else:
                    return None
            except Exception as ex:
                raise Exception(ex)       