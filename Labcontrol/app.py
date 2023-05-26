from flask import Flask
from flask import render_template, request, redirect, session
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory
import os
from datetime import date
import calendar
####
app=Flask(__name__)
app.secret_key="UPIIT"

mysql=MySQL()

app.config["MYSQL_DATABASE_HOST"]="localhost"
app.config["MYSQL_DATABASE_USER"]="root"
app.config["MYSQL_DATABASE_PASSWORD"]=""
app.config["MYSQL_DATABASE_DB"]="control_lab_upiit"
mysql.init_app(app)


@app.route("/")
def inicio():
    if not 'login' in session:
        return redirect("/login")
    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `usuario`")
    usuarios=cursor.fetchall()
    conexion.commit()
    
    return render_template("sitio/index.html", usuarios=usuarios)

#-----------------

@app.route("/login")
def login():
    return render_template("sitio/login.html")

@app.route("/login", methods=['POST'])
def login_post():
    _usuario=request.form['txtUsuario']
    _password=request.form['txtPassword']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT id_usuario,contrasena FROM `usuario` WHERE id_usuario=%s",(_usuario))
    correcto=cursor.fetchall()
    conexion.commit()

    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT id_curso FROM grupo WHERE usuario=%s",(_usuario))
    cursos=cursor.fetchall()
    conexion.commit()

    c="INCORRECTA"
    u="INCORRECTA"
    for a in correcto:
        u=a[0]
    for a in correcto:
        c=a[1]
    admin = False
    for a in cursos:
        if(str(a[0]) == "ADMI"):
            admin = True

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT nombre FROM `usuario` WHERE id_usuario=%s",(_usuario))
    nombre=cursor.fetchall()
    conexion.commit()
    
    if str(_usuario)==str(u) and str(_password)==str(c) and admin:
        session["login"]=True
        session["usuario"]=str(nombre[0][0])
        session["matricula"]=str(_usuario)
        session["admin"]=int(1)
        return redirect("/")
    elif str(_usuario)==str(u) and str(_password)==str(c):
        session["login"]=True
        session["usuario"]=str(nombre[0][0])
        session["matricula"]=str(_usuario)
        session["admin"]=int(0)
        return redirect("/")

    return render_template("sitio/login.html")

@app.route("/signup")
def signup():
    return render_template("sitio/signup.html")


@app.route("/signup", methods=['POST'])
def signup_post():
    _matricula=request.form['txtUsuario']
    _nombre=request.form['txtNombre']
    _contraseña=request.form['txtPassword']
    _contraseñaV=request.form['txtPasswordV']

    if _contraseña != _contraseñaV:
        print("la contraseña no coincide")
        return redirect("/signup")
    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `usuario` WHERE id_usuario=%s",(_matricula))
    usuario=cursor.fetchall()
    conexion.commit()
    print(usuario)

    a = "matricula"
    b = "nombre"
    c = "contraseña"

    for i in usuario:
        a = i[0]
        b = i[1]
        c = i[2]

    if str(_matricula) != str (a):
        print("la matricula no está en la base")
        print(_matricula)
        print(usuario)
        return redirect("/signup")
    
    if str(b) == "" and str(c) == "":
        sql="UPDATE `usuario` SET `nombre` = %s, `contrasena` = %s WHERE `usuario`.`id_usuario` = %s"
        datos=(_nombre,_contraseña,_matricula)

        conexion=mysql.connect()
        cursor=conexion.cursor()
        cursor.execute(sql,datos)
        conexion.commit()
    else:
        return redirect("/signup")
    

    return render_template("sitio/login.html")



@app.route("/cerrar")
def login_cerrar():
    session.clear()
    return redirect("/login")

#-----------------

@app.route('/img/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(os.path.join("templates/sitio/img"),imagen)


#------------------------------reservas------horarios

@app.route("/horarios")
def horarios():
    if not 'login' in session:
        return redirect("/login")
    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `reserva` WHERE id_responsable=%s",(session["matricula"]))
    solicitud=cursor.fetchall()
    conexion.commit()

    now = date.today()
    ano = int(str(now)[0])*1000 + int(str(now)[1])*100 + int(str(now)[2])*10 + int(str(now)[3])
    #print(ano)
    dia = int(str(now)[8])*10 + int(str(now)[9])
    #print(dia)
    mes = int(str(now)[5])*10 + int(str(now)[6])
    #print(mes)

    cal= calendar.Calendar()
    Horario = []
    semanas_vacia = 2

    for j in cal.monthdayscalendar(ano,mes):
        for i in j:
            if(i<dia):
                Horario.append("")
            if(i>=dia):
                Horario.append(i)
    for j in cal.monthdayscalendar(ano,mes+1):
        for i in j:
            if(i<1):
                Horario.append("")
            if(i>=1):
                Horario.append(i)
    i = 0
    while Horario[i] != dia:
        semanas_vacia = semanas_vacia + 1
        i = i+1
    
    vacia = True
    for k in range(0,int(semanas_vacia/7)*5):
        if(Horario[k] != ""):
            vacia = False

    if(vacia == True):
        for k in range(0,int(semanas_vacia/7)*7):
            Horario.remove(Horario[0])

    return render_template("sitio/horarios.html",solicitud=solicitud,Horario=Horario,tamano=len(Horario))


@app.route("/horarios/solicitar", methods=["POST"])
def solicitar_pc():
    if not 'login' in session:
        return redirect("/login")
    matricula=""
    for m in session:
        matricula=m
    print(matricula)
    _matricula=session["matricula"]
    _hora=request.form["txtHora"]
    _computadora=request.form["txtComputadora"]

    tiempo=datetime.now()
    horaActual=tiempo.strftime('%Y%H%M%S')

    sql="INSERT INTO `reserva` (`id_reserva`, `id_laboratorio`, `id_responsable`, `fecha`) VALUES (NULL,%s,%s,%s);"
    datos=(_computadora,_matricula,_hora)
    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect("/horarios")
#------------------------------reservas------horarios

#---------administrador----------




@app.route("/admin/")
def admin_index():
    if not 'login' in session:
        return redirect("/login")
    return render_template("sitio/index.html")

@app.route("/admin/login")
def admin_login():
    return render_template("admin/login.html")

@app.route("/admin/login", methods=['POST'])
def admin_login_post():
    _usuario=request.form['txtUsuario']
    _password=request.form['txtPassword']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT id_usuario,contrasena FROM `usuario` WHERE id_usuario=%s",(_usuario))
    correcto=cursor.fetchall()
    conexion.commit()

    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT id_curso FROM grupo WHERE usuario=%s",(_usuario))
    cursos=cursor.fetchall()
    conexion.commit()

    c="INCORRECTA"
    u="INCORRECTA"
    for a in correcto:
        u=a[0]
    for a in correcto:
        c=a[1]
    admin = False
    for a in cursos:
        if(str(a[0]) == "ADMI"):
            admin = True

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT nombre FROM `usuario` WHERE id_usuario=%s",(_usuario))
    nombre=cursor.fetchall()
    conexion.commit()
    
    if str(_usuario)==str(u) and str(_password)==str(c) and admin:
        session["admin_login"]=True
        session["usuario_admin"]=str(nombre[0][0])
        return redirect("/admin")

    return render_template("admin/login.html")

@app.route("/admin/cerrar")
def admin_login_cerrar():
    session.clear()
    return redirect("/login")

#---------------------------------Usuarios---------------------------------------------Usuarios Admin

@app.route("/usuarios")
def admin_usuarios():
    if not 'login' in session:
        return redirect("/login")

    return render_template("admin/usuarios.html")

@app.route("/buscar", methods=["POST"])
def admin_usuarios_buscar():
    if not 'login' in session:
        return redirect("/login")
    
    
    _matricula=request.form['txtUsuario']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `usuario` WHERE id_usuario=%s",(_matricula))
    usuario=cursor.fetchall()
    conexion.commit()

    print(usuario)
    matricula = ""
    nombre = ""
    contraseña = ""
    for i in usuario:
        matricula = i[0]
        nombre = i[1]
        contraseña = i[2]
    print(matricula)
    print(nombre)
    print(contraseña)

    return render_template("admin/usuarios.html",matricula=matricula,nombre=nombre,contraseña=contraseña)


@app.route("/crear", methods=["POST"])
def admin_laboratorio1_guardar():
    if not 'login' in session:
        return redirect("/login")

    _matricula=request.form["txtUsuario"]

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT id_usuario FROM `usuario` WHERE id_usuario=%s",(_matricula))
    usuario=cursor.fetchall()
    conexion.commit()

    print(usuario)

    a = "usuario"
    for i in usuario:
        a = i[0]
    print(a)

    if _matricula == a:
        return redirect("/usuarios")

    sql="INSERT INTO `usuario` (`id_usuario`, `nombre`, `contrasena`) VALUES (%s,%s,%s);"
    datos=(_matricula,"","")
    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect("/usuarios")

@app.route("/editar", methods=["POST"])
def admin_laboratorio1_desabilitar():
    if not 'login' in session:
        return redirect("/login")

    _matricula=request.form["txtMatricula"]
    _nombre=request.form["txtNombre"]
    _contraseña=request.form["txtUsuario"]

    sql="UPDATE `usuario` SET `id_usuario` = %s, `nombre` = %s, `contrasena` = %s  WHERE `usuario`.`id_usuario` = %s;"
    dato=(_matricula,_nombre,_contraseña,_matricula)
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,dato)
    conexion.commit()

    return redirect("/usuarios")

@app.route("/borrar",methods=["POST"])
def admin_usuarios_borrar():
    if not 'login' in session:
        return redirect("/login")

    _id=request.form["txtID"]
    print(_id)

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM usuario WHERE id_usuario=%s",(_id))
    conexion.commit()

    return redirect("/usuarios")
#---------------------------------Usuarios---------------------------------------------Usuarios Admin




if __name__=="__main__":
    app.run(debug=True)