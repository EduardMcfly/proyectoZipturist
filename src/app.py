from urllib import response
from flask import Flask, render_template, request,redirect,url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required,current_user
from flask_wtf.csrf import CSRFProtect
from config import config
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash
from random import sample
from io import BytesIO
from  flask import Flask, send_file
from werkzeug.datastructures import FileStorage
import os, re
from werkzeug.utils import secure_filename 
# Models:
from models.ModeloUsuario import ModeloUsuario

# Entities:
from models.entities.Usuario import Usuario

#Definición de archivos estaticos
app = Flask(__name__, static_folder='static', template_folder='templates')
#Conexion con la base de datos
db = MySQL(app)
#Manejo de sesiones
login_manager_app = LoginManager(app)



@login_manager_app.user_loader
def load_user(id):
    return ModeloUsuario.get_by_id(db, id)

#Para subir archivo tipo foto al servidor
import os
from werkzeug.utils import secure_filename 



#Creación de ruta para pagína inicial
@app.route('/health')
def health():
    cur = db.connection.cursor()
    # test db connection
    cur.execute("SELECT 2 + 2")
    row = cur.fetchone()
    print('result', row[0])
    return "OK"

#Función autenticación de usuario y definicón de ruta correspondiente al inicio de sesión.
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        usuario = Usuario(0,"", request.form['correo_Usuario'], request.form['contraseña_Usuario'])
        logged_user = ModeloUsuario.login(db, usuario)
        if logged_user != None:
            if logged_user.contraseña_Usuario:
                login_user(logged_user)
                return redirect(url_for('admin'))
            else:
                flash("Contraseña Incorrecta...")
                return render_template('auth/login.html')
        else:
            flash("Usuario No Encontrado...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

#Función generar ruta correspondiente a cerrar sesión y retorna al template de inicio de sesión
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

#Creación de ruta para pagína inicial
@app.route('/')
def inicio():
    return render_template('contenidoInicio.html')

#Creación de ruta para visualizar los tipos de sitios disponibles.
@app.route('/servicios')
def servicios():
    return render_template('paginaInicial.html')

# Definición de ruta para la creacion de la cuenta
@app.route('/singup')
def singup():
    return render_template('auth/singUp.html')

#Función para registrar un nuevo usuario en el sistema 
@app.route('/register', methods=["POST"])
def register():
    if request.method=="POST":
        contraseña=request.form['pass']
        patron = r'^(?=.*\d)(?=.*[a-z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,15}$'
        if re.match(patron, contraseña):
            flash("Registro correcto")
            texto_encriptado1 = generate_password_hash(contraseña)
            name=request.form['nombre']
            correo=request.form['email']
            contraseñaE=texto_encriptado1
            
            query =f"INSERT INTO usuario(nombre_Usuario,correo_Usuario,contraseña_Usuario) VALUES('{name}','{correo}','{contraseñaE}')"
            cursor=db.connection.cursor()
            cursor.execute(query)
            db.connection.commit()
            return redirect(url_for('login'))
        else: 
            flash("Contraseña insegura, tener en cuenta las recomendaciones dadas" )
            return redirect(url_for('singup'))
    else:
        return "nooooooo"  
     
#Función para definir la ruta del template formulario para registrar centros religiosos
@app.route('/formularioCentrosR')
@login_required
def formulario():
    return render_template('formlarioCentrosR.html')

#Función que permite agregar información de un centro religioso a la base de datos
@app.route('/registerCentrosR', methods=["POST"])
def registerCentrosR():
    if request.method=="POST":
        nombre=request.form['nombre']
        direccion=request.form['direccion']
        descripcion=request.form['descripcion']
        contacto=request.form['contacto']
        file = request.files['imagen'] #recibiendo el archivo
        nuevoNombreFile = recibeFoto(file) #Llamado la funcion que procesa la imagen
        usuario_Id=current_user.id
        cursor=db.connection.cursor()
        query =f"INSERT INTO centrosreligiosos(nombre_Centro,direccion_Centro,descipcion_Centro,contacto_Centro,imagen_Centro,usuario_Id) VALUES('{nombre}','{direccion}','{descripcion}','{contacto}','{nuevoNombreFile}',{usuario_Id})"
        cursor=db.connection.cursor()
        cursor.execute(query)
        db.connection.commit()
        return redirect(url_for('admin'))
    else:
        return "nooooooo"

#Función para definir la ruta del template formulario para registrar actividades representativas 
@app.route('/formularioActividadesR')
@login_required
def formularioActividadesR():
    return render_template('formularioActividadesR.html')

#Función que permite agregar información de una actividad representativa a la base de datos
@app.route('/registerActividadesR', methods=["POST"])
def registerActividadesR():
    if request.method=="POST":
        nombre=request.form['nombre']
        lugar=request.form['lugar']
        descripcion=request.form['descripcion']
        contacto=request.form['contacto']
        file = request.files['imagen'] #recibiendo el archivo
        nuevoNombreFile = recibeFoto(file)
        usuario_Id=current_user.id
        cursor=db.connection.cursor()
        query =f"""INSERT INTO actividadesreprecentativas(nombre_Actividad,lugar_Actividad,descipcion_Actividad,
        contacto_Actividad,imagen_Actividad,usuario_Id) 
        VALUES('{nombre}','{lugar}','{descripcion}','{contacto}','{nuevoNombreFile}'
        ,{usuario_Id})"""
        cursor=db.connection.cursor()
        cursor.execute(query)
        db.connection.commit()
        return redirect(url_for('admin'))
    else:
        return "nooooooo"

#Función para definir la ruta del template formulario para registrar hoteles 
@app.route('/formularioHotel')
@login_required
def formularioHotel():
    return render_template('formularioHoteles.html')

#Función que permite agregar información de una actividad representativa a la base de datos
@app.route('/registerHotel', methods=["POST"])
def registerHotel():
    if request.method=="POST":
        nombre=request.form['nombre']
        direccion=request.form['direccion']
        descripcion=request.form['descripcion']
        contacto=request.form['contacto']
        file = request.files['imagen'] #recibiendo el archivo
        nuevoNombreFile = recibeFoto(file) #Llamado la funcion que procesa la imagen
        usuario_Id=current_user.id
        cursor=db.connection.cursor()
        query =f"""INSERT INTO hoteles(nombre_hotel,direccion_hotel,descipcion_hotel,
        contacto_hotel,imagen_hotel,usuario_Id) 
        VALUES('{nombre}','{direccion}','{descripcion}','{contacto}','{nuevoNombreFile}',{usuario_Id})"""
        cursor=db.connection.cursor()
        cursor.execute(query)
        db.connection.commit()
        return redirect(url_for('admin'))
    else:
        return "nooooooo"

#Función para definir la ruta del template formulario para registrar sitios turisticos
@app.route('/formularioSitio')
@login_required
def formularioSitio():
    return render_template('formularioSitio.html')

#Función que permite agregar información de un sitio turistco a la base de datos
@app.route('/registerSitio', methods=["POST"])
def registerSitio():
    if request.method=="POST":
        nombre=request.form['nombre']
        direccion=request.form['direccion']
        descripcion=request.form['descripcion']
        contacto=request.form['contacto']
        file = request.files['imagen'] #recibiendo el archivo
        nuevoNombreFile = recibeFoto(file) #Llamado la funcion que procesa la imagen
        usuario_Id=current_user.id
        cursor=db.connection.cursor()
        query =f"""INSERT INTO sitiosturisticos(nombre_sitiosT,direccion_sitiosT,descipcion_sitiosT,
        contacto_sitiosT,imagen_sitiosT,usuario_Id) 
        VALUES('{nombre}','{direccion}','{descripcion}','{contacto}','{nuevoNombreFile}',{usuario_Id})"""
        cursor=db.connection.cursor()
        cursor.execute(query)
        db.connection.commit()
        return redirect(url_for('admin'))
    else:
        return "nooooooo"

#Función para definir la ruta del template formulario para registrar restaurantes
@app.route('/formularioRestaurantes')
@login_required
def formularioRestaurantes():
    return render_template('formularioRestaurantes.html')

#Función que permite agregar información de un restaurante a la base de datos
@app.route('/registerRestaurantes', methods=["POST"])
def registerRestaurantes():
    if request.method=="POST":
        nombre=request.form['nombre']
        direccion=request.form['direccion']
        descripcion=request.form['descripcion']
        contacto=request.form['contacto']
        file = request.files['imagen'] #recibiendo el archivo
        nuevoNombreFile = recibeFoto(file) #Llamado la funcion que procesa la imagen
        usuario_Id=current_user.id
        cursor=db.connection.cursor()
        query =f"""INSERT INTO restaurantes(nombre_restaurante,direccion_restaurante,descipcion_restaurante,
        contacto_restaurante,imagen_restaurante,usuario_Id) 
        VALUES('{nombre}','{direccion}','{descripcion}','{contacto}','{nuevoNombreFile}',{usuario_Id})"""
        cursor=db.connection.cursor()
        cursor.execute(query)
        db.connection.commit()
        return redirect(url_for('admin'))
    else:
        return "nooooooo"

#Función para definir la ruta del template formulario para registrar artesanias
@app.route('/formularioArtesanias')
@login_required
def formularioArtesanias():
    return render_template('formularioArtesanias.html')

#Función que permite agregar información de las artesanias a la base de datos
@app.route('/registerArtesanias', methods=["POST"])
def registerArtesanias():
    if request.method=="POST":
        nombre=request.form['nombre']
        direccion=request.form['direccion']
        descripcion=request.form['descripcion']
        contacto=request.form['contacto']
        file = request.files['imagen'] #recibiendo el archivo
        nuevoNombreFile = recibeFoto(file) #Llamado la funcion que procesa la imagen
        usuario_Id=current_user.id
        cursor=db.connection.cursor()
        query =f"""INSERT INTO artesanias(nombre_artesanias,direccion_artesanias,descipcion_artesanias,
        contacto_artesanias,imagen_artesanias,usuario_Id) 
        VALUES('{nombre}','{direccion}','{descripcion}','{contacto}','{nuevoNombreFile}',{usuario_Id})"""
        cursor=db.connection.cursor()
        cursor.execute(query)
        db.connection.commit()
        return redirect(url_for('admin'))
    else:
        return "nooooooo"

#Función para editar informacion correspondiente a una artesania en especico
@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    nombre = request.form['nombre']
    direccion = request.form['direccion']
    descripcion = request.form['descripcion']
    contacto = request.form['contacto']
    if (request.files['imagen']):
        file = request.files['imagen']
        nuevoNombreFile = recibeFoto(file)
    else:
        cursor = db.connection.cursor()
        sql = "SELECT imagen_artesanias FROM Artesanias WHERE id_artesanias=%s"
        data = (id,)
        cursor.execute(sql, data)
        db.connection.commit()
        myresultados1 = cursor.fetchall()
        nuevoNombreFile=myresultados1
    if nombre and direccion and descripcion and contacto and nuevoNombreFile:
        cursor = db.connection.cursor()
        query = """UPDATE artesanias 
                   SET nombre_artesanias = %s,
                       direccion_artesanias = %s,
                       descipcion_artesanias = %s,
                       contacto_artesanias = %s,
                       imagen_artesanias = %s 
                   WHERE id_artesanias= %s"""
        cursor.execute(query, (nombre, direccion, descripcion, contacto, nuevoNombreFile, id))
        db.connection.commit()
    return redirect(url_for('admin'))

#Función para editar informacion correspondiente a una actividad Reprecentativa en especico
@app.route('/editAr/<string:id>', methods=['POST'])
def editAr(id):
    nombre = request.form['nombre']
    direccion = request.form['direccion']
    descripcion = request.form['descripcion']
    contacto = request.form['contacto']
    if (request.files['imagen']):
        file = request.files['imagen']
        nuevoNombreFile = recibeFoto(file)
    else:
        cursor = db.connection.cursor()
        sql = "SELECT imagen_Actividad  FROM actividadesReprecentativas WHERE id_Actividad =%s"
        data = (id,)
        cursor.execute(sql, data)
        db.connection.commit()
        myresultados1 = cursor.fetchall()
        nuevoNombreFile=myresultados1
    if nombre and direccion and descripcion and contacto and nuevoNombreFile:
        cursor = db.connection.cursor()
        query = """UPDATE actividadesReprecentativas 
                   SET nombre_Actividad = %s,
                       lugar_Actividad = %s,
                       descipcion_Actividad = %s,
                       contacto_Actividad = %s,
                       imagen_Actividad = %s 
                   WHERE id_Actividad= %s"""
        cursor.execute(query, (nombre, direccion, descripcion, contacto, nuevoNombreFile, id))
        db.connection.commit()
    return redirect(url_for('admin'))


#Función para editar informacion correspondiente a un centro religioso en especico
@app.route('/editCr/<string:id>', methods=['POST'])
def editCr (id):
    nombre = request.form['nombre']
    direccion = request.form['direccion']
    descripcion = request.form['descripcion']
    contacto = request.form['contacto']
    if (request.files['imagen']):
        file = request.files['imagen']
        nuevoNombreFile = recibeFoto(file)
    else:
        cursor = db.connection.cursor()
        sql = "SELECT imagen_Centro  FROM CentrosReligiosos WHERE id_Centro =%s"
        data = (id,)
        cursor.execute(sql, data)
        db.connection.commit()
        myresultados1 = cursor.fetchall()
        nuevoNombreFile=myresultados1
    if nombre and direccion and descripcion and contacto and nuevoNombreFile:
        cursor = db.connection.cursor()
        query = """UPDATE CentrosReligiosos 
                   SET nombre_Centro = %s,
                       direccion_Centro = %s,
                       descipcion_Centro = %s,
                       contacto_Centro = %s,
                       imagen_Centro = %s 
                   WHERE id_Centro= %s"""
        cursor.execute(query, (nombre, direccion, descripcion, contacto, nuevoNombreFile, id))
        db.connection.commit()
    return redirect(url_for('admin'))

#Función para editar informacion correspondiente a un sitio turistico en especico
@app.route('/editSt/<string:id>', methods=['POST'])
def editSt(id):
    nombre = request.form['nombre']
    direccion = request.form['direccion']
    descripcion = request.form['descripcion']
    contacto = request.form['contacto']
    if (request.files['imagen']):
        file = request.files['imagen']
        nuevoNombreFile = recibeFoto(file)
    else:
        cursor = db.connection.cursor()
        sql = "SELECT imagen_sitiosT  FROM sitiosTuristicos  WHERE id_sitiosT =%s"
        data = (id,)
        cursor.execute(sql, data)
        db.connection.commit()
        myresultados1 = cursor.fetchall()
        nuevoNombreFile=myresultados1
    if nombre and direccion and descripcion and contacto and nuevoNombreFile:
        cursor = db.connection.cursor()
        query = """UPDATE sitiosTuristicos 
                   SET nombre_sitiosT = %s,
                       direccion_sitiosT = %s,
                       descipcion_sitiosT = %s,
                       contacto_sitiosT = %s,
                       imagen_sitiosT = %s 
                   WHERE id_sitiosT= %s"""
        cursor.execute(query, (nombre, direccion, descripcion, contacto, nuevoNombreFile, id))
        db.connection.commit()
    return redirect(url_for('admin'))


#Función para editar informacion correspondiente a un restaurante en especico
@app.route('/editR/<string:id>', methods=['POST'])
def editR(id):
    nombre = request.form['nombre']
    direccion = request.form['direccion']
    descripcion = request.form['descripcion']
    contacto = request.form['contacto']
    if (request.files['imagen']):
        file = request.files['imagen']
        nuevoNombreFile = recibeFoto(file)
    else:
        cursor = db.connection.cursor()
        sql = "SELECT imagen_restaurante FROM restaurantes  WHERE id_restaurante=%s"
        data = (id,)
        cursor.execute(sql, data)
        db.connection.commit()
        myresultados1 = cursor.fetchall()
        nuevoNombreFile=myresultados1
    if nombre and direccion and descripcion and contacto and nuevoNombreFile:
        cursor = db.connection.cursor()
        query = """UPDATE restaurantes 
                   SET nombre_restaurante = %s,
                       direccion_restaurante = %s,
                       descipcion_restaurante = %s,
                       contacto_restaurante = %s,
                       imagen_restaurante = %s 
                   WHERE id_restaurante= %s"""
        cursor.execute(query, (nombre, direccion, descripcion, contacto, nuevoNombreFile, id))
        db.connection.commit()
    return redirect(url_for('admin'))

#Función para editar informacion correspondiente a un hotel en especico
@app.route('/editH/<string:id>', methods=['POST'])
def editH(id):
    nombre = request.form['nombre']
    direccion = request.form['direccion']
    descripcion = request.form['descripcion']
    contacto = request.form['contacto']
    if (request.files['imagen']):
        file = request.files['imagen']
        nuevoNombreFile = recibeFoto(file)
    else:
        cursor = db.connection.cursor()
        sql = "SELECT imagen_hotel FROM hoteles  WHERE id_hotel=%s"
        data = (id,)
        cursor.execute(sql, data)
        db.connection.commit()
        myresultados1 = cursor.fetchall()
        nuevoNombreFile=myresultados1
    if nombre and direccion and descripcion and contacto and nuevoNombreFile:
        cursor = db.connection.cursor()
        query = """UPDATE hoteles 
                   SET nombre_hotel = %s,
                       direccion_hotel = %s,
                       descipcion_hotel = %s,
                       contacto_hotel = %s,
                       imagen_hotel = %s 
                   WHERE id_hotel= %s"""
        cursor.execute(query, (nombre, direccion, descripcion, contacto, nuevoNombreFile, id))
        db.connection.commit()
    return redirect(url_for('admin'))

#Función pagína de administrador que recopila las consultas de los datos de cada uno de los registros por categoria
@app.route('/admin')
@login_required
def admin():
    cursor=db.connection.cursor()
    cursor.execute("SELECT * FROM centrosreligiosos")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()

    cursor=db.connection.cursor()
    cursor.execute("SELECT * FROM restaurantes")
    myresultado = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObjecto = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresultado:
        insertObjecto.append(dict(zip(columnNames, record)))
    cursor.close()

    cursor=db.connection.cursor()
    cursor.execute("SELECT * FROM hoteles")
    myresultados = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObjectos = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresultados:
        insertObjectos.append(dict(zip(columnNames, record)))
    cursor.close()

    cursor=db.connection.cursor()
    cursor.execute("SELECT * FROM sitiosturisticos")
    myresultados2 = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObjectos2 = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresultados2:
        insertObjectos2.append(dict(zip(columnNames, record)))
    cursor.close()

    cursor=db.connection.cursor()
    cursor.execute("SELECT * FROM actividadesreprecentativas")
    myresultados1 = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObjectos1 = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresultados1:
        insertObjectos1.append(dict(zip(columnNames, record)))
    cursor.close()

    cursor=db.connection.cursor()
    cursor.execute("SELECT * FROM artesanias")
    myresultados3 = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObjectos3 = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresultados3:
        insertObjectos3.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('admin.html', data=insertObject, dato=insertObjecto, datos=insertObjectos,datos1=insertObjectos1,datos2=insertObjectos2,datos3=insertObjectos3)

#Función para eliminar un registro en especifico de los entros religiosos 
@app.route('/delete/<string:id>')
def delete(id):
    cursor=db.connection.cursor()
    sql = "DELETE FROM centrosreligiosos WHERE id_Centro=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.connection.commit()
    return redirect(url_for('admin'))

#Función para eliminar un registro en especifico de los entros religiosos 
@app.route('/deleteR/<string:id>')
def deleteR(id):
    cursor=db.connection.cursor()
    sql = "DELETE FROM restaurantes WHERE id_restaurante=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.connection.commit()
    return redirect(url_for('admin')) 

#Función para eliminar un registro en especifico de los entros religiosos 
@app.route('/deleteH/<string:id>')
def deleteH(id):
    cursor=db.connection.cursor()
    sql = "DELETE FROM hoteles WHERE id_hotel=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.connection.commit()
    return redirect(url_for('admin')) 

#Función para eliminar un registro en especifico de los entros religiosos 
@app.route('/deleteS/<string:id>')
def deleteS(id):
    cursor=db.connection.cursor()
    sql = "DELETE FROM sitiosturisticos WHERE id_sitiosT=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.connection.commit()
    return redirect(url_for('admin')) 

#Función para eliminar un registro en especifico de los entros religiosos 
@app.route('/deleteAr/<string:id>')
def deleteAr(id):
    cursor=db.connection.cursor()
    sql = "DELETE FROM actividadesreprecentativas WHERE id_Actividad=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.connection.commit()
    return redirect(url_for('admin')) 

#Función para eliminar un registro en especifico de los entros religiosos 
@app.route('/deleteA/<string:id>')
def deleteA(id):
    cursor=db.connection.cursor()
    sql = "DELETE FROM artesanias WHERE id_artesanias=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.connection.commit()
    return redirect(url_for('admin')) 

#Funcion para guardar el nombre de la imagen en la base de datos y el  archivo en la carpeta correspondiente
def recibeFoto(file):
    print(file)
    basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actual
    filename = secure_filename(file.filename) #Nombre original del archivo

    #capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
    extension           = os.path.splitext(filename)[1]
    nuevoNombreFile     = stringAleatorio() + extension
    upload_path = os.path.join (basepath, 'static/fotos_turismo', nuevoNombreFile) 
    file.save(upload_path)

    return nuevoNombreFile

#Función para renombrar lo sarchivos de las imagenes de una forma aleatiria
def stringAleatorio():
    string_aleatorio = "0123456789abcdefghijklmnopqrstuvwxyz_"
    longitud         = 20
    secuencia        = string_aleatorio.upper()
    resultado_aleatorio  = sample(secuencia, longitud)
    string_aleatorio     = "".join(resultado_aleatorio)
    return string_aleatorio

#Función consulta de las actividades representativas guardadas 
@app.route('/actividadesRepresentativas')
def actividadesRepresentativas():
    cursor=db.connection.cursor()
    cursor.execute("SELECT * FROM actividadesreprecentativas")
    myresultados1 = cursor.fetchall()
    #Convertir los datos a diccionario
    actividades = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresultados1:
        actividades.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('actividadesRepresentativas.html', data=actividades)

#Función consulta de las artesanias  guardadas 
@app.route('/artesanias')
def artesanias():
    cursor=db.connection.cursor()
    cursor.execute("SELECT * FROM artesanias")
    myresultados3 = cursor.fetchall()
    #Convertir los datos a diccionario
    artesanias = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresultados3:
        artesanias.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('artesanias.html', data=artesanias)

#Función consulta de los hoteles guardados 
@app.route('/hoteles')
def hoteles():
    cursor=db.connection.cursor()
    cursor.execute("SELECT * FROM hoteles")
    myresultados3 = cursor.fetchall()
    #Convertir los datos a diccionario
    hotel = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresultados3:
        hotel.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('hoteles.html', data=hotel)

#Función consulta de los restaurantes guardados 
@app.route('/restaurantes')
def restaurantes():
    cursor=db.connection.cursor()
    cursor.execute("SELECT * FROM restaurantes")
    myresultados3 = cursor.fetchall()
    #Convertir los datos a diccionario
    restaurante = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresultados3:
        restaurante.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('restaurantes.html', data=restaurante)

#Función consulta de los centros religiosos guardados 
@app.route('/centrosReligiosos')
def centrosReligiosos():
    cursor=db.connection.cursor()
    cursor.execute("SELECT * FROM centrosreligiosos")
    myresultados3 = cursor.fetchall()
    #Convertir los datos a diccionario
    centro = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresultados3:
        centro.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('centrosReligiosos.html', data=centro)

#Función consulta de los sitios turisticos guardados  
@app.route('/sitiosTuristicos')
def sitiosTuristicos():
    cursor=db.connection.cursor()
    cursor.execute("SELECT * FROM sitiosTuristicos")
    myresultados3 = cursor.fetchall()
    #Convertir los datos a diccionario
    sitio = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresultados3:
        sitio.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('sitiosTuristicos.html', data=sitio)

#Función para visualizar la informacion de una actividad representativa en especifico
@app.route('/verActividad/<string:id>')
def verActividad(id):
    cursor=db.connection.cursor()
    query="SELECT * FROM actividadesreprecentativas WHERE id_Actividad=%s"
    data=(id)
    cursor.execute(query,data)
    myresultados1 = cursor.fetchall()
    #Convertir los datos a diccionario
    actividad = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresultados1:
        actividad.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('verActividad.html', data=actividad)

#Función para visualizar la informacion de un sitio turistico en especifico
@app.route('/verSitio/<string:id>')
def verSitio(id):
    cursor=db.connection.cursor()
    query="SELECT * FROM sitiosturisticos WHERE id_sitiosT=%s"
    data=(id)
    cursor.execute(query,data)
    myresultados1 = cursor.fetchall()
    #Convertir los datos a diccionario
    sitio = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresultados1:
        sitio.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('verSitio.html', data=sitio)

#Función para visualizar la informacion de una artesania en especifico
@app.route('/verArtesania/<string:id>')
def verArtesania(id):
    cursor=db.connection.cursor()
    query="SELECT * FROM artesanias WHERE id_artesanias=%s"
    data=(id)
    cursor.execute(query,data)
    myresultados1 = cursor.fetchall()
    #Convertir los datos a diccionario
    artesanias = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresultados1:
        artesanias.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('verArtesania.html', data=artesanias)

#Función para visualizar la informacion de un hotel en especifico
@app.route('/verHotel/<string:id>')
def verHotel(id):
    cursor=db.connection.cursor()
    query="SELECT * FROM hoteles WHERE id_hotel=%s"
    data=(id)
    cursor.execute(query,data)
    myresultados1 = cursor.fetchall()
    #Convertir los datos a diccionario
    hotel = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresultados1:
        hotel.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('verHotel.html', data=hotel)

#Función para visualizar la informacion de un restaurante en especifico
@app.route('/verRestaurante/<string:id>')
def verRestaurante(id):
    cursor=db.connection.cursor()
    query="SELECT * FROM restaurantes WHERE id_restaurante=%s"
    data=(id)
    cursor.execute(query,data)
    myresultados1 = cursor.fetchall()
    #Convertir los datos a diccionario
    restaurante = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresultados1:
        restaurante.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('verRestaurante.html', data=restaurante)

#Función para visualizar la informacion de un centro religioso en especifico
@app.route('/verCentro/<string:id>')
def verCentro(id):
    cursor=db.connection.cursor()
    query="SELECT * FROM centrosreligiosos WHERE id_Centro=%s"
    data=(id)
    cursor.execute(query,data)
    myresultados1 = cursor.fetchall()
    #Convertir los datos a diccionario
    centro = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresultados1:
        centro.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('verCentro.html', data=centro)

def status_401(error):
    return redirect(url_for('login'))
    
def status_404(error):
    return render_template('404.html')


#iniciación de la aplicacion en flask.
if __name__ == '__main__' or __name__ == 'app':
    app.config.from_object(config['development'])
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)

    app.run()