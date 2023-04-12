from flask import Flask
from flask import render_template, request, redirect, session
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory
import os

####
app=Flask(__name__)
app.secret_key="UPIIT"

mysql=MySQL()

app.config["MYSQL_DATABASE_HOST"]="localhost"
app.config["MYSQL_DATABASE_USER"]="root"
app.config["MYSQL_DATABASE_PASSWORD"]=""
app.config["MYSQL_DATABASE_DB"]="upiit_control_lab"
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
    _matricula=request.form['txtUsuario']
    _contraseña=request.form['txtPassword']
    print(_matricula)
    print(_contraseña)

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT id_usuario,contrasena FROM `usuario` WHERE id_usuario=%s",(_matricula))
    correcto=cursor.fetchall()
    conexion.commit()
    print(correcto)

    c="INCORRECTA"
    u="INCORRECTA"
    for a in correcto:
        u=a[0]
    for a in correcto:
        c=a[1]
    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT nombre FROM `usuario` WHERE id_usuario=%s",(_matricula))
    nombre=cursor.fetchall()
    conexion.commit()
    print(nombre)

    if str(_matricula)==str(u) and str(_contraseña)==str(c):
        session["login"]=True
        session["usuario"]=str(nombre[0][0])
        session["matricula"]=str(_matricula)
        return redirect("/")    

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

@app.route("/laboratorio2")
def laboratorio2():
    if not 'login' in session:
        return redirect("/login")
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `laboratorio`")
    computadoras=cursor.fetchall()
    conexion.commit()
    print(computadoras)
    return render_template("sitio/laboratorio2.html", computadoras=computadoras)


@app.route("/laboratorio1")
def laboratorio1():
    if not 'login' in session:
        return redirect("/login")
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `laboratorio`")
    computadoras=cursor.fetchall()
    conexion.commit()
    print(computadoras)
    print("---------------------------------------------------------------")
    print(computadoras)
    

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT disponible FROM `laboratorio`")
    color=cursor.fetchall()
    conexion.commit()

    return render_template("sitio/laboratorio1.html", computadoras=computadoras)

#------------------------------reservas------horarios

@app.route("/horarios")
def horarios():
    if not 'login' in session:
        return redirect("/login")
    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `solicitud` WHERE matricula=%s",(session["matricula"]))
    solicitud=cursor.fetchall()
    conexion.commit()

    return render_template("sitio/horarios.html",solicitud=solicitud)


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

    sql="INSERT INTO `solicitud` (`id`, `matricula`, `computadora`,`hora`) VALUES (NULL,%s,%s,%s);"
    datos=(_matricula,_computadora,_hora)
    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect("/horarios")
#------------------------------reservas------horarios

#---------administrador----------

@app.route("/admin/")
def admin_index():
    if not 'admin_login' in session:
        return redirect("/admin/login")
    return render_template("admin/index.html")

@app.route("/admin/login")
def admin_login():
    return render_template("admin/login.html")

@app.route("/admin/login", methods=['POST'])
def admin_login_post():
    _usuario=request.form['txtUsuario']
    _password=request.form['txtPassword']
    print(_usuario)
    print(_password)

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT matricula,contraseña,especialidad FROM `usuario` WHERE matricula=%s",(_usuario))
    correcto=cursor.fetchall()
    conexion.commit()
    print(correcto)

    c="INCORRECTA"
    u="INCORRECTA"
    admin="INCORRECTA"
    for a in correcto:
        u=a[0]
    for a in correcto:
        c=a[1]
    for a in correcto:
        admin=a[2]

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT nombre FROM `usuario` WHERE matricula=%s",(_usuario))
    nombre=cursor.fetchall()
    conexion.commit()
    print(nombre)
    


    if str(_usuario)==str(u) and str(_password)==str(c) and str(admin)=="Docente":
        session["admin_login"]=True
        session["usuario_admin"]=str(nombre[0][0])
        return redirect("/admin")

    return render_template("admin/login.html")

@app.route("/admin/cerrar")
def admin_login_cerrar():
    session.clear()
    return redirect("/admin/login")


#---------------------------------lab1---------------------------------------------Lab1
@app.route("/admin/laboratorio1")
def admin_laboratorio1():
    if not 'admin_login' in session:
        return redirect("/admin/login")
    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute('SELECT * FROM `laboratorio`')
    computadoras=cursor.fetchall()
    conexion.commit()
    print(computadoras)

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute('SELECT * FROM `solicitud`')
    solicitud=cursor.fetchall()
    conexion.commit()

    return render_template("/admin/laboratorio1.html", computadoras=computadoras,solicitud=solicitud)

@app.route("/admin/laboratorio1/guardar", methods=["POST"])
def admin_laboratorio1_guardar():
    if not 'admin_login' in session:
        return redirect("/admin/login")

    _id=request.form["txtID"]
    _matricula=request.form["txtMatricula"]
    _uso=request.form["txtUso"]
    _disponible=request.form["txtDisponible"]

    tiempo=datetime.now()
    horaActual=tiempo.strftime('%Y%H%M%S')

#    if _archivo.filename!="":
#        nuevoNombre=horaActual+"_"+_archivo.filename
#        _archivo.save("templates/sitio/img/"+nuevoNombre)

    sql="INSERT INTO `laboratorio` (`id`, `matriculas`, `uso`, `disponible`) VALUES (%s,%s,%s,%s);"
    datos=(_id,_matricula,_uso,_disponible)
    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    print(_id)
    print(_matricula)
    print(_uso)
    print(_disponible)

    return redirect("/admin/laboratorio1")

@app.route("/admin/laboratorio1/habilitar", methods=["POST"])
def admin_laboratorio1_habilitar():
    if not 'admin_login' in session:
        return redirect("/admin/login")

    _id=request.form["txtID"]
#    tiempo=datetime.now()
#    horaActual=tiempo.strftime('%Y%H%M%S')

#    if _archivo.filename!="":
#        nuevoNombre=horaActual+"_"+_archivo.filename
#        _archivo.save("templates/sitio/img/"+nuevoNombre)

    sql="UPDATE `laboratorio` SET `disponible` = '2' WHERE `laboratorio`.`id` = %s;"
    dato=(_id)
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,dato)
    conexion.commit()
    print(_id)

    return redirect("/admin/laboratorio1")

@app.route("/admin/laboratorio1/desabilitar", methods=["POST"])
def admin_laboratorio1_desabilitar():
    if not 'admin_login' in session:
        return redirect("/admin/login")

    _id=request.form["txtID"]
#    tiempo=datetime.now()
#    horaActual=tiempo.strftime('%Y%H%M%S')

#    if _archivo.filename!="":
#        nuevoNombre=horaActual+"_"+_archivo.filename
#        _archivo.save("templates/sitio/img/"+nuevoNombre)

    sql="UPDATE `laboratorio` SET `disponible` = '1' WHERE `laboratorio`.`id` = %s;"
    dato=(_id)
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,dato)
    conexion.commit()
    print(_id)

    return redirect("/admin/laboratorio1")

@app.route("/admin/laboratorio1/borrar",methods=["POST"])
def admin_laboratorio1_borrar():
    if not 'admin_login' in session:
        return redirect("/admin/login")

    _id=request.form["txtID"]
    print(_id)

#    conexion=mysql.connect()
#    cursor=conexion.cursor()
#    cursor.execute("SELECT imagen FROM `laboratorio1` WHERE id=%s",(_id))
#    libro=cursor.fetchall()
#    conexion.commit()
#    print(libro)

#    if os.path.exists("templates/sitio/img/"+str(libro[0][0])):
#        os.unlink("templates/sitio/img/"+str(libro[0][0]))
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM laboratorio WHERE id=%s",(_id))
    conexion.commit()

    return redirect("/admin/laboratorio1")
#---------------------------------lab1---------------------------------------------Lab1

#---------------------------------lab2---------------------------------------------Lab2
@app.route("/admin/laboratorio2")
def admin_laboratorio2():
    if not 'admin_login' in session:
        return redirect("/admin/login")
    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute('SELECT * FROM `laboratorio`')
    computadoras=cursor.fetchall()
    conexion.commit()
    
    return render_template("/admin/laboratorio2.html", computadoras=computadoras)

@app.route("/admin/laboratorio2/guardar", methods=["POST"])
def admin_laboratorio2_guardar():
    if not 'admin_login' in session:
        return redirect("/admin/login")

    _id=request.form["txtID"]
    _matricula=request.form["txtMatricula"]
    _uso=request.form["txtUso"]
    _disponible=request.form["txtDisponible"]

    tiempo=datetime.now()
    horaActual=tiempo.strftime('%Y%H%M%S')

#    if _archivo.filename!="":
#        nuevoNombre=horaActual+"_"+_archivo.filename
#        _archivo.save("templates/sitio/img/"+nuevoNombre)

    sql="INSERT INTO `laboratorio` (`id`, `matriculas`, `uso`, `disponible`) VALUES (%s,%s,%s,%s);"
    datos=(_id,_matricula,_uso,_disponible)
    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    print(_id)
    print(_matricula)
    print(_uso)
    print(_disponible)

    return redirect("/admin/laboratorio2")

@app.route("/admin/laboratorio2/habilitar", methods=["POST"])
def admin_laboratorio2_habilitar():
    if not 'admin_login' in session:
        return redirect("/admin/login")

    _id=request.form["txtID"]
#    tiempo=datetime.now()
#    horaActual=tiempo.strftime('%Y%H%M%S')

#    if _archivo.filename!="":
#        nuevoNombre=horaActual+"_"+_archivo.filename
#        _archivo.save("templates/sitio/img/"+nuevoNombre)

    sql="UPDATE `laboratorio` SET `disponible` = '2' WHERE `laboratorio`.`id` = %s;"
    dato=(_id)
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,dato)
    conexion.commit()
    print(_id)

    return redirect("/admin/laboratorio2")

@app.route("/admin/laboratorio2/desabilitar", methods=["POST"])
def admin_laboratorio2_desabilitar():
    if not 'admin_login' in session:
        return redirect("/admin/login")

    _id=request.form["txtID"]
#    tiempo=datetime.now()
#    horaActual=tiempo.strftime('%Y%H%M%S')

#    if _archivo.filename!="":
#        nuevoNombre=horaActual+"_"+_archivo.filename
#        _archivo.save("templates/sitio/img/"+nuevoNombre)

    sql="UPDATE `laboratorio` SET `disponible` = '1' WHERE `laboratorio`.`id` = %s;"
    dato=(_id)
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,dato)
    conexion.commit()
    print(_id)

    return redirect("/admin/laboratorio2")

@app.route("/admin/laboratorio2/borrar",methods=["POST"])
def admin_laboratorio2_borrar():
    if not 'admin_login' in session:
        return redirect("/admin/login")

    _id=request.form["txtID"]
    print(_id)

#    conexion=mysql.connect()
#    cursor=conexion.cursor()
#    cursor.execute("SELECT imagen FROM `laboratorio1` WHERE id=%s",(_id))
#    libro=cursor.fetchall()
#    conexion.commit()
#    print(libro)

#    if os.path.exists("templates/sitio/img/"+str(libro[0][0])):
#        os.unlink("templates/sitio/img/"+str(libro[0][0]))
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM laboratorio WHERE id=%s",(_id))
    conexion.commit()

    return redirect("/admin/laboratorio2")
#---------------------------------lab2---------------------------------------------Lab2

if __name__=="__main__":
    app.run(debug=True)