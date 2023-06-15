from flask import Flask
from flask import render_template, request, redirect, session, jsonify
from flaskext.mysql import MySQL
from flask import send_from_directory
import os
import calendar
from datetime import datetime, date


from flask import current_app
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
    cursor.execute("SELECT id_reserva, fecha, id_hora FROM `reserva` WHERE id_responsable=%s",(session["matricula"]))
    reservas=cursor.fetchall()
    conexion.commit()

    now = date.today()

    fecha_actual = now.strftime("%d / %m / %Y")

    diccionario_horas = [
        '7:00 - 8:30',
        '8:30 - 10:00',
        '10:00 - 11:30',
        '11:30 - 1:00',
        '1:00 - 2:30',
        '2:30 - 4:00',
        '4:00 - 5:30',
        '5:30 - 7:00',
    ]

    reservas_modificadas = []
    for reserva in reservas:
        fecha_reserva = datetime.strptime(reserva[1], "%d / %m / %Y").date()
        if fecha_reserva >= now:
            reserva_lista = list(reserva)
            numero = reserva[2]
            hora = diccionario_horas[numero-1]
            reserva_lista[2] = hora
            reservas_modificadas.append(tuple(reserva_lista))

    return render_template("sitio/index.html", reservas=reservas_modificadas)

#------------

@app.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('favicon.ico')




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
                Horario.append(str(i)+" / "+str(mes)+" / "+str(ano))
    for j in cal.monthdayscalendar(ano,mes+1):
        for i in j:
            if(i<1):
                Horario.append("")
            if(i>=1):
                Horario.append(str(i)+" / "+str(mes+1)+" / "+str(ano))
    i = 0
    while Horario[i] != str(dia)+" / "+str(mes)+" / "+str(ano):
        semanas_vacia = semanas_vacia + 1
        i = i+1
    
    vacia = True
    for k in range(0,int(semanas_vacia/7)*5):
        if(Horario[k] != ""):
            vacia = False

    if(vacia == True):
        for k in range(0,int(semanas_vacia/7)*7):
            Horario.remove(Horario[0])

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT COUNT(DISTINCT id_laboratorio) AS cantidad_laboratorios FROM compu;")
    labs=cursor.fetchone()[0]
    conexion.commit()

    return render_template("sitio/horarios.html",solicitud=solicitud,Horario=Horario,tamano=len(Horario),labs=labs)


@app.route("/reservas/crear", methods=["POST"])
def crear_reserva():
    responsable = request.form.get('responsable')
    fecha = request.form.get('fecha')
    hora = request.form.get('hora')
    tipo = request.form.get('tipo')
    laboratorio = request.form.get('laboratorio')
    computadora = request.form.get('computadora')

    sql="INSERT INTO `reserva` (`id_responsable`, `fecha`, `id_hora`,`id_lab`,`id_compu`,`id_materia`) VALUES (%s,%s,%s,%s,%s,%s);"
    datos=(responsable,fecha,hora,laboratorio,computadora,"1")
    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()


    return jsonify({'success': True})

@app.route("/horarios/mostrar", methods=["POST"])
def mostrar_disponibles():
    fecha_seleccionada = request.form['fecha']
    modo = request.form['modo']
    laboratorio = request.form['laboratorio']

    conexion = mysql.connect()
    cursor = conexion.cursor()

    cursor.execute("SELECT id_hora FROM `reserva` WHERE fecha=%s AND id_lab=%s", (fecha_seleccionada,laboratorio))
    resultados = cursor.fetchall()

    horas_reservadas = [resultado[0] for resultado in resultados]

    diccionario_horas = {
        1: '7:00 - 8:30',
        2: '8:30 - 10:00',
        3: '10:00 - 11:30',
        4: '11:30 - 1:00',
        5: '1:00 - 2:30',
        6: '2:30 - 4:00',
        7: '4:00 - 5:30',
        8: '5:30 - 7:00',
    }

    horas_totales = [1, 2, 3, 4, 5, 6, 7, 8]

    if(modo == "grupal"):
        horas_disponibles = [
            {'valor': hora, 'texto': diccionario_horas[hora]}
            for hora in horas_totales
            if hora not in horas_reservadas
        ]
    if(modo == "unico"):
        horas_disponibles = [
            {'valor': hora, 'texto': diccionario_horas[hora]}
            for hora in horas_totales
        ]

    conexion.commit()

    return jsonify(horas_disponibles)



@app.route("/horarios/PC_disponible", methods=["POST"])
def pc_dispobiles():
    fecha_seleccionada = request.form['fecha']
    hora_seleccionada = request.form['hora']
    laboratorio = request.form['laboratorio']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT id_compu FROM `reserva` WHERE fecha=%s AND id_hora=%s AND id_lab=%s", (fecha_seleccionada, hora_seleccionada, laboratorio))
    pcs_uso=cursor.fetchall()
    conexion.commit()

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT id_compu FROM `compu` WHERE id_laboratorio=%s",(laboratorio))
    pcs_disponibles=cursor.fetchall()
    conexion.commit()

    pcs_dict = {}  # Diccionario para almacenar la información de las computadoras

    # Agregar las computadoras disponibles al diccionario
    for pc in pcs_disponibles:
        pc_id = pc[0]
        pcs_dict[pc_id] = {"disponible": "Disponible"}

    # Actualizar el estado de disponibilidad de las computadoras en uso
    for pc in pcs_uso:
        pc_id = pc[0]
        if pc_id in pcs_dict:
            pcs_dict[pc_id]["disponible"] = "No disponible"

    # Convertir el diccionario en una lista de diccionarios
    pcs_disponibles_list = []
    for pc_id, pc_info in pcs_dict.items():
        pc_dict = {"computadora": pc_id, "disponible": pc_info["disponible"]}
        pcs_disponibles_list.append(pc_dict)

    
    return jsonify(pcs_disponibles_list)

#------------------------------reservas------horarios


@app.route("/reservas")
def reservas():
    if not 'login' in session:
        return redirect("/login")

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT id_reserva, fecha, id_hora FROM `reserva`")
    reservas=cursor.fetchall()
    conexion.commit()

    now = date.today()

    fecha_actual = now.strftime("%d / %m / %Y")

    diccionario_horas = [
        '7:00 - 8:30',
        '8:30 - 10:00',
        '10:00 - 11:30',
        '11:30 - 1:00',
        '1:00 - 2:30',
        '2:30 - 4:00',
        '4:00 - 5:30',
        '5:30 - 7:00',
    ]

    reservas_modificadas = []
    for reserva in reservas:
        fecha_reserva = datetime.strptime(reserva[1], "%d / %m / %Y").date()
        if fecha_reserva >= now:
            reserva_lista = list(reserva)
            numero = reserva[2]
            hora = diccionario_horas[numero-1]
            reserva_lista[2] = hora
            reservas_modificadas.append(tuple(reserva_lista))

    
    return render_template("admin/reservas.html", reservas=reservas_modificadas)



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