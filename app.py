from flask import Flask, render_template, redirect, session, flash, request
from flask.templating import render_template
from bd import cargardatos, resgistrardato
from datetime import datetime
import math
import os
from werkzeug.security import check_password_hash, generate_password_hash
from markupsafe import escape
import traceback

app = Flask('__name__')

@app.errorhandler(404)
def e404(e):
    return render_template('error.html'), 404

@app.route('/')
@app.route('/home/')
@app.route('/index/')
def index():
    session['perfil']=None
    return render_template('index.html')



@app.route('/nosotros')
@app.route('/nosotros/')
def about():
    return render_template('sobreNosotros.html')



@app.route('/terminos')
@app.route('/terminos/')
def tercond():
    return render_template('terminosCondiciones.html')



@app.route('/contactanos')
@app.route('/contactanos/',methods=['GET', 'POST'])
def contact():
    if request.method=='GET':
        return render_template('contacto.html')
    else:
        nom = request.form['nombre']
        tel= request.form['telefono']
        correo= request.form['email']
        mensaje= request.form['mensaje']
        try:
            # Valido los datos 
            if nom==None or tel==None:
                msg = 'ERROR: SE DEBE INGRESAR EL NOMBRE'
            elif correo==None:
                msg = 'ERROR: SE DEBE INGRESAR UN CORREO'
            else:
                # Valido los datos 
                sql = f"INSERT INTO mensajes (nombre, telefono, email, mensaje) VALUES ('{nom}', '{tel}', '{correo}', '{mensaje}')"
                #print('arme a consulta')
                res = resgistrardato(sql)
                if res==0:
                    msg ='ERROR AL CARGAR LA INFORMACIÓN'
                else:
                    msg = 'Ok'
                    
        except Exception:
            msg = 'ERROR: Por favor intente luego'
            print(Exception)
        if msg == 'Ok':
            return redirect('/home/')
        else:
            return render_template('contacto.html',error=msg)



@app.route('/login')
@app.route('/login/',methods=['GET', 'POST'])
def login():
    #Si el metodo HTTP es GET devuelvo rederizado la  pagina de Login
    if request.method=='GET':
        return render_template('login.html')
    #Si el metodo es post tomo los valores de formulario
    else:
        usr = escape (request.form['email'])
        clave = escape (request.form['pwd'])
        msg=''
        #intento conectarme a la base de datos
        try:
            dat = None
            if usr==None:
                msg = 'ERROR: Se Debe suministrar un usuario'
            elif clave==None:
                msg = 'ERROR: Se Debe suministrar una clave'
            else:
                # Procedo a ubicar el usuario indicado
                #Armo la consulta SQL
                sql = f"SELECT nombre, perfil, contraseña, codigo, documento FROM usuarios WHERE email='{usr}'"
                #print('arme a consulta')
                #Ejecuto la consulta 
                dat = cargardatos(sql)
                #si los datos encontado son  quiere decir que el usuario o la clave son invalidos
                if len(dat)==0:
                    msg ='ERROR:: Usuario no valido'
                    print(msg)
                #De lo contrario capturo el perfil del usuario y creo las variables de sesion
                else:
                    cbd = dat[0][2] #EXTRAIGO CONTRASEÑA 
                    if check_password_hash(cbd,clave): #COMPARO CONTRASEÑA ENCIPTADA CON LA CONTRASEÑA PUESTA.
                        session.clear()
                        #print('LLegue hasta aca')
                        msg = 'Ok'
                        session['nombre']=(dat[0][0])
                        profile=dat[0][1]
                        session['perfil']=dat[0][1]
                        session['codigo']=dat[0][3]
                        session['cedula']=dat[0][4]
                        session['mensaje']=' '
                    else:
                        msg ='ERROR:: clave invalida'
                        
        except Exception:
            msg = 'ERROR: Por favor intente luego'
            print(Exception)
            dat = None

        #Si la consult fue exitosa verifico el tipo y devuelvo el menu correspondiente menu
        if msg =='Ok':
            if(profile == 'U'):
                return redirect('/menu/')
            elif(profile == 'A'):
                return redirect('/madmin/')
            elif(profile == 'P'):
                return redirect('/mpiloto/')
            else:
                return render_template('login.html',error='Usuario invalido, contacte al administrador')
        else:
            return render_template('login.html',error=msg)



@app.route('/registro')
@app.route('/registro/',methods=['GET', 'POST'])
def register():
    #Si el metodo HTTP es GET devuelvo rederizado la  pagina de Registro
    if request.method == 'GET':
        return render_template('registro.html',error="")
    #De lo contrario tomo los valores del formulario 
    else:
        nombre=request.form['nombre']
        apellido=request.form['apellido']
        tipo=request.form['tipo']
        doc=request.form['documento']
        correo=request.form['email']
        pwd1=request.form['pwd']
        pwd2=request.form['pwd2']
        #print(nombre)
        try:
            dat = None
            # Valido los datos 
            if nombre==None or apellido==None:
                msg = 'ERROR: SE DEBE INGRESAR EL NOMBRE'
            elif correo==None:
                msg = 'ERROR: SE DEBE INGRESAR UN CORREO'
            elif pwd1 != pwd2:
                msg = 'LAS CONTRASEÑAS NO COINCIDEN'
            else:
                # Valido los datos 
                pwd = generate_password_hash(pwd1) #SE ENCRIPTA CONTRASEÑA DFRO
                sql = f"INSERT INTO usuarios (nombre, apellidos, tipodocumento, documento, email, contraseña) VALUES ('{nombre}', '{apellido}', '{tipo}', '{doc}', '{correo}', '{pwd}')"
                #print('arme a consulta')
                res = resgistrardato(sql)
                if res==0:
                    msg ='ERROR AL CARGAR LA INFORMACIÓN'
                else:
                    msg = 'Ok'
                    
        except Exception:
            msg = 'ERROR: Por favor intente luego'
            print(Exception)
        if msg == 'Ok':
            return redirect('/home/')
        else:
            return render_template('registro.html',error=msg)



@app.route('/recuperarpwd/')
def rpwd():
    sal = '<head><link rel="stylesheet" href="../static/css/style.css"></head>'
    sal +="<div class = 'main'>"
    sal += '<p>Se ha enviado un correo con las instrucciones</p>'
    sal +='<a href="/home">VOLVER AL HOME</a>'
    sal += '</div>'
    return sal



@app.route('/menu')
@app.route('/menu/')
@app.route('/menu/<string:usr>')
def userMenu(usr=None):
    if session['perfil']=='U':
        return render_template('menuUsuario.html',nombre=session['nombre'],mensaje=session['mensaje'])
    else:
        return render_template('error.html',mensaje='Acseso no permitido')



@app.route('/madmin')
@app.route('/madmin/')
@app.route('/madmin/<string:usr>')
def adminMenu(usr=None):
    if session['perfil']=='A':
        return render_template('menuAdmin.html')
    else:
        return render_template('error.html',mensaje='Acseso no permitido')
    


@app.route('/mpiloto')
@app.route('/mpiloto/')
@app.route('/mpiloto/<string:usr>')
def pilotMenu(usr=None):
    if session['perfil']=='P':
        return render_template('menuPiloto.html',nombre=session['nombre'])
    else:
        return render_template('error.html',mensaje='Acseso no permitido')



@app.route('/calificar')
@app.route('/calificar/',methods=['GET', 'POST'])
@app.route('/calificar/<string:metodo>/',methods=['GET', 'POST'])
def calificarVuelo(metodo=None):
#valido que este logeado un usuario
    if session['perfil']=='U':
    #Si el metodo de la consulta HTTP  es get decuelvo el formulario limpio con los vuelos que tiene ewe pasajero
        if request.method == 'GET':
            dat=None
            try:
                # Procedo a ubicar el usuario indicado
                #Armo la consulta SQL
                sql = f"SELECT vuelo FROM reservas WHERE pasajero='{session['codigo']}'"
                #print('arme a consulta')
                #Ejecuto la consulta 
                dat = cargardatos(sql)
                #si los datos encontado son  quiere decir que el usuario o la clave son invalidos
                #print(dat)
                if len(dat)==0:
                    msg ='ERROR:: Codigo no valido'
                    print(msg)
                else:
                    msg='Ok'
                    print(dat)
                #De lo contrario capturo el perfil del usuario y creo las variables de sesio        
            except Exception:
                msg = 'ERROR: Por favor intente luego'
                print(Exception)
                traceback.print_exc()
            if msg == 'Ok':
                return render_template('calificarVuelo.html',vuelos=dat)
            else:
                return render_template('calificarVuelo.html',error = msg)

        #Si el metodo el post valido si en la url voy a buscar o guardar
        else:
            #si el metodo no es buscar
            if metodo==None:
                codvuelo=request.form['codigo']
                nota=request.form['nota']
                coment=request.form['coment']
                try:
                    if codvuelo==None:
                        msg = 'ERROR: Se Debe suministrar un codigo de vuelo'
                    else:
                        # Procedo a actualizar el usuario indicado
                        #Armo la consulta SQL
                        sql = f"INSERT INTO calificaciones (vuelo, pasajero, calificacion, comentarios) VALUES ('{codvuelo}', '{session['codigo']}', '{nota}', '{coment}')"
                        #Ejecuto la consulta 
                        res = resgistrardato(sql)
                        #si los datos encontado son  quiere decir que el usuario o la clave son invalidos
                        #print('estoy afuera del if')
                        #print(dat)
                        if res==0:
                            msg ='ERROR:: Usuario no valido'
                            print(msg)
                        #De lo contrario capturo el perfil del usuario y creo las variables de sesion
                        else:                    
                            msg = 'Ok'
                except Exception:
                    msg = 'ERROR: Por favor intente luego'
                    print(Exception)
                if msg == 'Ok':
                    session['mensaje']="Gracias por su calificación"
                    return redirect('/menu/')
                else:
                    return render_template('calificarVuelo.html',error = msg)
            
            #si el metodo es buscar
            else:
                codvuelo=request.form['codigo']
                try:
                    if codvuelo==None:
                        msg = 'ERROR: Se Debe suministrar un codigo de vuelo'
                    else:
                        # Procedo a ubicar el usuario indicado
                        #Armo la consulta SQL
                        sql = f"SELECT origen, destino, horasalida, horallegada FROM vuelos WHERE codigo='{codvuelo}'"
                        #print('arme a consulta')
                        #Ejecuto la consulta 
                        dat = cargardatos(sql)
                        #si los datos encontado son  quiere decir que el usuario o la clave son invalidos
                        #print('estoy afuera del if')
                        print(dat)
                        if len(dat)==0:
                            msg ='ERROR:: Codigo no valido'
                            print(msg)
                        else:
                            corigen= dat[0][0]
                            csalida = dat[0][1]
                            hsalida = dat[0][2]
                            hllegada = dat[0][3]
                            msg='Ok'
                        #De lo contrario capturo el perfil del usuario y creo las variables de sesio        
                except Exception:
                    msg = 'ERROR: Por favor intente luego'
                    print(Exception)
                    traceback.print_exc()
                if msg == 'Ok':
                    return render_template('calificarVuelo.html', codigo = codvuelo, origen = corigen, destino = csalida, horasalida = hsalida, horallegada = hllegada, vuelos=[(codvuelo,"bug")])
                else:
                    return render_template('error.html',error=msg)
    return "Hola no eres nadie"


@app.route('/separavuelo')
@app.route('/separavuelo/',methods=['GET', 'POST'])
@app.route('/separavuelo/<string:met>/',methods=['GET', 'POST'])
def separarVuelo(met=None):
    if session['perfil']=='U':
    #Si el metodo de la consulta HTTP  es get decuelvo el formulario limpio
        if request.method == 'GET':
            return render_template('separarVuelo.html')
        #Si el metodo el post valido si en la url voy a buscar o guardar
        else:
            #si el metodo es buscar 
            if met != None:
                fecha = request.form['fecha']
                origen=request.form['origen']
                destino=request.form['destino']
                op = request.form['op']
                #print(f"la opciones {op}")
                if fecha==None or origen==None or destino==None:
                    msg="ERROR::Suministre información"
                else:
                    #Armo la consulta SQL
                    try:
                        if op=='1':
                            sql = f"SELECT codigo, aerolinea, horasalida,capacidad, pasajeros FROM vuelos WHERE DATE(horasalida)='{fecha}' AND origen='{origen}' AND destino='{destino}'"
                        elif op=='0':
                            sql = f"SELECT codigo, aerolinea, horasalida,capacidad, pasajeros FROM vuelos WHERE origen='{origen}' AND destino='{destino}'"
                        #Ejecuto la consulta 
                        dat = cargardatos(sql)
                        #si los datos encontado son  quiere decir que el usuario o la clave son invalidos
                        if len(dat)==0:
                            msg ='ERROR:: No hay vuelos para los datos ingresados'
                            print(msg)
                        else:
                            msg='Ok'
                        #De lo contrario capturo el perfil del usuario y creo las variables de sesio        
                    except Exception:
                        msg = 'ERROR: Por favor intente luego'
                        print(Exception)
                        traceback.print_exc()
                if msg == 'Ok':
                    return render_template('separarVuelo.html', vuelos = dat, origen = origen, destino = destino)
                else:
                    return render_template('separarVuelo.html',error=msg)
            #si el metodo no es buscar
            else:
                vuelo=request.form['codigo']
                pasajero=session['codigo']
                if vuelo==None:
                    msg="Seleccione un vuelo valido"
                else:
                    try:
                        consulta=f"SELECT capacidad, pasajeros FROM vuelos WHERE codigo='{vuelo}'"
                        dat = cargardatos(consulta)
                        #si los datos encontado son  quiere decir que el usuario o la clave son invalidos
                        if len(dat)==0:
                            msg ='ERROR:: Inetnte nuevamente'
                            print(msg)
                        else:
                            if dat[0][0]<=dat[0][1]:
                                msg="Vuelo sin cupos disponibles"
                            else:
                                #De lo contrario capturo el perfil del usuario y creo las variables de sesio       
                                sql = f"INSERT INTO reservas (vuelo, pasajero) VALUES ('{vuelo}', '{pasajero}')"
                                #print('arme a consulta')
                                res = resgistrardato(sql)
                                sql2 = f"UPDATE vuelos SET pasajeros = '{dat[0][1]+1}' WHERE codigo='{vuelo}'"
                                #print('arme a consulta')
                                res2 = resgistrardato(sql2)
                                if res==0:
                                    msg ='ERROR AL CARGAR LA INFORMACIÓN'
                                else:
                                    msg = 'Ok'
                                    if(res2==0):
                                        print('ERROR NO SE RESTO EL CUPO')
                        
                    except Exception:
                        msg = 'ERROR: Por favor intente luego'
                        print(Exception)
                        traceback.print_exc()
                if msg == 'Ok':
                    session['mensaje']="Reservado tu proximo vuelo!"
                    return redirect('/menu/')
                else:
                    return render_template('separarVuelo.html',error=msg)
    else:
        print('no llegue a ninguna lado')
        return render_template('error.html',mensaje='Acceso no permitido')



@app.route('/vervuelos/')
@app.route('/vervuelos/<string:usr>/',methods=['GET', 'POST'])
@app.route('/vervuelos/',methods=['GET', 'POST'])

def listarVuelos(usr=None):
    if session['perfil']==None or session['perfil']=='I':
        return render_template('error.html',mensaje='Acseso no permitido')
    #si el usuario es piloto 
    elif session['perfil']=='P':
        try:
            #Armo la consulta SQL
            sql = f"SELECT * FROM vuelos WHERE estadovuelo <> 'CERRADO' AND piloto='{session['cedula']}'"
            #print('arme a consulta')
            #Ejecuto la consulta 
            dat = cargardatos(sql)
            #si los datos encontado son  quiere decir que el usuario o la clave son invalidos
            #print('estoy afuera del if')
            #print(dat)
            if len(dat)==0:
                msg ='No hay vuelosregistrados'
                print(msg)
            #De lo contrario capturo el perfil del usuario y creo las variables de sesion
            else:                   
                msg = 'Ok'
                    
        except Exception:
            msg = 'ERROR: Por favor intente luego'
            print(Exception)
            traceback.print_exc()
        if msg == 'Ok':
            return render_template('verVuelos.html',vuelos=dat)
        else:
            return render_template('error.html',mensaje=msg)
    #si no es piloto
    else:
        try:
            #Armo la consulta SQL
            if usr==None:
                sql = f"SELECT * FROM vuelos WHERE estadovuelo <> 'CERRADO'"
            else:
                sql = f"SELECT * FROM vuelos INNER JOIN reservas ON vuelos.codigo = reservas.vuelo WHERE reservas.pasajero='{session['codigo']}'"
            #print('arme a consulta')
            #Ejecuto la consulta 
            dat = cargardatos(sql)
            #si los datos encontado son  quiere decir que el usuario o la clave son invalidos
            #print('estoy afuera del if')
            #print(dat)
            if len(dat)==0:
                msg ='No hay vuuelos registrados'
                print(msg)
            #De lo contrario capturo el perfil del usuario y creo las variables de sesion
            else:                   
                msg = 'Ok'
                    
        except Exception:
            msg = 'ERROR: Por favor intente luego'
            print(Exception)
            traceback.print_exc()
        if msg == 'Ok':
            return render_template('verVuelos.html',vuelos=dat)
        else:
            return render_template('error.html',mensaje=msg)



@app.route('/editarusuario/')
@app.route('/editarusuario/',methods=['GET', 'POST'])
@app.route('/editarusuario/<string:met>/',methods=['GET', 'POST'])
def editUser(met=None):
    #Valido el perfil del usuario logeado.
    #Si el usuario no tiene privilegios de administrado
    if session['perfil']=='U' or session['perfil']=='P': 
        if request.method == 'GET':
            cod=session['codigo'] #capturo el codigo del usuario logeado
            try:
                if cod==None:
                    msg = 'ERROR: Se Debe suministrar un usuario'
                else:
                    #armo la consulta 
                    sql = f"SELECT nombre, apellidos, documento, email FROM usuarios WHERE codigo='{cod}'"
                    #Ejecuto la consulta 
                    dat = cargardatos(sql)

                    #si no encuentro informacion
                    if len(dat)==0:
                        msg ='ERROR:: Usuario no valido'
                        #print(msg)
                    #De lo contario si hay datos encontrados
                    else:                    
                        msg = 'Ok'
                            
            except Exception:
                msg = 'ERROR: Por favor intente luego'
                print(Exception)
            #Si encontre datos renderizo la pantalla de editar usuario con los datos del usuario
            if msg == 'Ok':
                return render_template('editarEliminarUsuario.html',nombre = dat[0][0], apellido = dat[0][1], cedula = dat[0][2], correo = dat[0][3])
            #si algo salio mal rederizo la pantalla con el mensaje de error
            else:
                return render_template('editarEliminarUsuario.html',error = msg)
        elif request.method == 'POST':
            cod=session['codigo']
            nombre=request.form['nombre']
            apellido=request.form['apellido']
            tipo=request.form['tipo']
            doc=request.form['documento']
            correo=request.form['email']
            try:
                if cod==None:
                    msg = 'ERROR: Se Debe suministrar un usuario'
                else:
                    # Procedo a actualizar el usuario indicado
                    #Armo la consulta SQL
                    sql = f"UPDATE usuarios SET nombre = '{nombre}', apellidos = '{apellido}', tipodocumento = '{tipo}', documento = '{doc}', email = '{correo}' WHERE codigo='{cod}'"
                    #Ejecuto la consulta 
                    res = resgistrardato(sql)
                    if res==0:
                        msg ='ERROR:: Usuario no valido'
                        print(msg)
                    #De lo contrario capturo el perfil del usuario y creo las variables de sesion
                    else:                    
                        msg = 'Ok'
                            
            except Exception:
                msg = 'ERROR: Por favor intente luego'
                print(Exception)
            if msg == 'Ok':
                if session['perfil']=='P':
                    return redirect('/mpiloto/')
                else:
                    return redirect('/menu/')
            else:
                return render_template('editarEliminarUsuario.html',error = msg)

    #si el usuario si tiene privilegios de admin
    elif session['perfil']=='A':
        if request.method == 'GET':
            return render_template('editarUsuarioAdmin.html')
        else:
            #si el metodo no es buscar
            if met==None:
                cod=request.form['codigo']
                nombre=request.form['nombre']
                apellido=request.form['apellido']
                tipo=request.form['tipo']
                doc=request.form['cedula']
                correo=request.form['email']
                try:
                    if cod==None:
                        msg = 'ERROR: Se Debe suministrar un usuario'
                    else:
                        # Procedo a actualizar el usuario indicado
                        #Armo la consulta SQL
                        sql = f"UPDATE usuarios SET nombre = '{nombre}', apellidos = '{apellido}', tipodocumento = '{tipo}', documento = '{doc}', email = '{correo}' WHERE codigo='{cod}'"
                        #Ejecuto la consulta 
                        res = resgistrardato(sql)
                        #si los datos encontado son  quiere decir que el usuario o la clave son invalidos
                        if res==0:
                            msg ='ERROR:: Usuario no valido'
                            print(msg)
                        else:                    
                            msg = 'Ok'
                except Exception:
                    msg = 'ERROR: Por favor intente luego'
                    print(Exception)
                if msg == 'Ok':
                    return redirect('/madmin/')
                else:
                    return render_template('editarUsuarioAdmin.html',error = msg)
            #si el metodo es buscar
            else:
                cc=request.form['cedula']
                try:
                    if cc==None:
                        msg = 'ERROR: Se Debe suministrar un usuario'
                    else:
                        # Procedo a ubicar el usuario indicado
                        #Armo la consulta SQL
                        sql = f"SELECT nombre, apellidos, codigo, documento, email FROM usuarios WHERE documento='{cc}'"
                        #Ejecuto la consulta 
                        dat = cargardatos(sql)
                        #si los datos encontado son  quiere decir que el usuario o la clave son invalidos
                        if len(dat)==0:
                            msg ='ERROR:: Usuario no valido'
                            print(msg)
                        #De lo contrario capturo el perfil del usuario y creo las variables de sesion
                        else:              
                            msg = 'Ok'
                                
                except Exception:
                    msg = 'ERROR: Por favor intente luego'
                    print(Exception)
                if msg == 'Ok':
                    return render_template('editarUsuarioAdmin.html',nombre=dat[0][0], apellido=dat[0][1],codigo=dat[0][2], cedula=dat[0][3], correo=dat[0][4] )
                else:
                    return render_template('editarUsuarioAdmin.html',error = msg)
    else:
        return render_template('error.html',mensaje='Acceso no permitido')



@app.route('/calificaciones/')
@app.route('/calificaciones/<string:usr>')
def verCal(usr=None):
    if session['perfil']==None or session['perfil']=='I' or session['perfil']=='U':
        return render_template('error.html',mensaje='Acseso no permitido')
    #si el usuario es piloto 
    elif session['perfil']=='P':
        try:
            #Armo la consulta SQL
            sql = f"SELECT vuelo, pasajero, calificacion, comentarios FROM calificaciones INNER JOIN vuelos ON vuelos.codigo = calificaciones.vuelo WHERE vuelos.piloto='{session['cedula']}'"
            #print('arme a consulta')
            #Ejecuto la consulta 
            dat = cargardatos(sql)
            #si los datos encontado son  quiere decir que el usuario o la clave son invalidos
            #print('estoy afuera del if')
            #print(dat)
            if len(dat)==0:
                msg ='No hay vuelosregistrados'
                print(msg)
            #De lo contrario capturo el perfil del usuario y creo las variables de sesion
            else:                   
                msg = 'Ok'
                    
        except Exception:
            msg = 'ERROR: Por favor intente luego'
            print(Exception)
            traceback.print_exc()
        if msg == 'Ok':
            return render_template('comentarios.html',comentarios=dat)
        else:
            return render_template('error.html',mensaje=msg)
    #si no es piloto
    else:
        try:
            #Armo la consulta SQL
            sql = f"SELECT * FROM calificaciones"
            #print('arme a consulta')
            #Ejecuto la consulta 
            dat = cargardatos(sql)
            #si los datos encontado son  quiere decir que el usuario o la clave son invalidos
            #print('estoy afuera del if')
            #print(dat)
            if len(dat)==0:
                msg ='No hay comentarios registrados'
                print(msg)
            #De lo contrario capturo el perfil del usuario y creo las variables de sesion
            else:                   
                msg = 'Ok'
                    
        except Exception:
            msg = 'ERROR: Por favor intente luego'
            print(Exception)
            traceback.print_exc()
        if msg == 'Ok':
            return render_template('comentarios.html',comentarios=dat)
        else:
            return render_template('error.html',mensaje=msg)
    



@app.route('/roles')
@app.route('/roles/<string:met>/',methods=['GET', 'POST'])
@app.route('/roles/',methods=['GET', 'POST'])
def permisosRoles(met=None):
    #valido que este logeado un admin
    if session['perfil']=='A':
    #Si el metodo de la consulta HTTP  es get decuelvo el formulario limpio
        if request.method == 'GET':
            return render_template('permisosRoles.html')

        #Si el metodo el post valido si en la url voy a buscar o guardar
        else:
            #si el metodo no es buscar
            if met==None:
                cc=request.form['cedula']
                nom=request.form['nombre']
                per=request.form['perfil']
                if per == 'Usuario':
                    perfil = 'U'
                elif per == 'Administrador':
                    perfil = 'A'
                elif per == 'Piloto':
                    perfil = 'P'
                elif per == 'Inactivo':
                    perfil = 'I'
                try:
                    if cc==None:
                        msg = 'ERROR: Se Debe suministrar un usuario'
                    else:
                        # Procedo a actualizar el usuario indicado
                        #Armo la consulta SQL
                        sql = f"UPDATE usuarios SET perfil = '{perfil}' WHERE documento='{cc}' AND nombre='{nom}'"
                        #print('arme a consulta')
                        #Ejecuto la consulta 
                        res = resgistrardato(sql)
                        #si los datos encontado son  quiere decir que el usuario o la clave son invalidos
                        #print('estoy afuera del if')
                        #print(dat)
                        if res==0:
                            msg ='ERROR:: Usuario no valido'
                            print(msg)
                        #De lo contrario capturo el perfil del usuario y creo las variables de sesion
                        else:                    
                            msg = 'Ok'
                                
                except Exception:
                    msg = 'ERROR: Por favor intente luego'
                    print(Exception)
                if msg == 'Ok':
                    return redirect('/madmin/')
                else:
                    return render_template('permisosRoles.html',nombre = msg)

                return "Hola no eres nadie"
            #si el metodo es buscar
            else:
                cc=request.form['cedula']
                try:
                    if cc==None:
                        msg = 'ERROR: Se Debe suministrar un usuario'
                    else:
                        # Procedo a ubicar el usuario indicado
                        #Armo la consulta SQL
                        sql = f"SELECT nombre, perfil, contraseña FROM usuarios WHERE documento='{cc}'"
                        #print('arme a consulta')
                        #Ejecuto la consulta 
                        dat = cargardatos(sql)
                        #si los datos encontado son  quiere decir que el usuario o la clave son invalidos
                        #print('estoy afuera del if')
                        #print(dat)
                        if len(dat)==0:
                            msg ='ERROR:: Usuario no valido'
                            print(msg)
                        #De lo contrario capturo el perfil del usuario y creo las variables de sesion
                        else:
                            nom = dat[0][0]
                            if dat[0][1] == 'U':
                                per = 'Usuario'
                            elif dat[0][1] == 'A':
                                per = 'Administrador'
                            elif dat[0][1] == 'P':
                                per = 'Piloto'
                            elif dat[0][1] == 'I':
                                per = 'Inactivo'                     
                            msg = 'Ok'
                                
                except Exception:
                    msg = 'ERROR: Por favor intente luego'
                    print(Exception)
                if msg == 'Ok':
                    return render_template('permisosRoles.html', nombre = nom, perfil = per, cedula = cc)
                else:
                    return render_template('permisosRoles.html',nombre = msg)
    else:
        return render_template('error.html',mensaje='Acseso no permitido')



@app.route('/registrovuelo/')
@app.route('/registrovuelo/',methods=['GET', 'POST'])
def registroVuelo():
    if session['perfil']!='A':
        return render_template('error.html',mensaje='Acseso no permitido')
    else:
        if request.method == 'GET':
            return render_template('registroVuelo.html')
        else:
            codigo=request.form['codigo']
            empresa=request.form['empresa']
            matricula=request.form['matricula']
            fsalida=request.form['fechaSalida']
            hsalida=request.form['horaSalida']
            fllegada=request.form['fechaLlegada']
            hllegada=request.form['horaLlegada']
            origen=request.form['origen']
            destino=request.form['destino']
            piloto=request.form['piloto']

        try:
            # Valido los datos 
            if codigo==None or empresa==None:
                msg = 'ERROR: VALIDE LOS DATOS DE ENTRADA'
            elif origen==None or destino==None:
                msg = 'ERROR: VALIDE LOS DATOS DE ENTRADA'
            else:
                # Valido los datos            
                fhsalida=datetime.fromisoformat(fsalida+' '+hsalida)
                fhllegada=datetime.fromisoformat(fllegada+' '+hllegada) 
                sql = f"INSERT INTO vuelos (codigo, aerolinea, matricula, destino, origen, horasalida, horallegada, piloto) VALUES ('{codigo}', '{empresa}', '{matricula}', '{destino}', '{origen}', '{fhsalida}', '{fhllegada}', '{piloto}')"
                #print('arme a consulta') 
                res = resgistrardato(sql)
                if res==0:
                    msg ='ERROR AL CARGAR LA INFORMACIÓN'
                else:
                    msg = 'Ok'
                    
        except Exception:
            msg = 'ERROR: Por favor intente luego'
            print(Exception)
            traceback.print_exc()
        if msg == 'Ok':
            return redirect('/madmin/')
        else:
            return render_template('registroVuelo.html',error=msg)



@app.route('/editarvuelo/',methods=['GET', 'POST'])
@app.route('/editarvuelo/<string:met>/',methods=['GET', 'POST'])
def editoVuelo(met=None):
    if session['perfil']=='A':
        if request.method == 'GET':
            return render_template('editarEliminar.html',var=" ")
        else:
            #si el metodo no es buscar
            if met==None:
                cod=request.form['code']
                estado=request.form['estado']
                airline=request.form['empresa']
                matricula=request.form['matricula']
                piloto=request.form['piloto']
                fsalida=request.form['fechaSalida']
                hsalida=request.form['horaSalida']
                fllegada=request.form['fechaLlegada']
                hllegada=request.form['horaLlegada']
                origen=request.form['origen']
                destino=request.form['destino']
                try:
                    if cod==None:
                        msg = 'ERROR: Se Debe suministrar un usuario'
                    else:
                        fhsalida=datetime.fromisoformat(fsalida+' '+hsalida)
                        fhllegada=datetime.fromisoformat(fllegada+' '+hllegada) 
                        # Procedo a actualizar el usuario indicado
                        #Armo la consulta SQL
                        sql = f"UPDATE vuelos SET aerolinea = '{airline}', matricula = '{matricula}', destino = '{destino}', origen = '{origen}', piloto = '{piloto}', horasalida='{fhsalida}', horallegada='{fhllegada}', estadovuelo='{estado}' WHERE codigo='{cod}'"
                        #Ejecuto la consulta 
                        res = resgistrardato(sql)
                        #si los datos encontado son  quiere decir que el usuario o la clave son invalidos
                        if res==0:
                            msg ='ERROR:: Usuario no valido'
                            print(msg)
                        else:                    
                            msg = 'Ok'
                except Exception:
                    msg = 'ERROR: Por favor intente luego'
                    print(Exception)
                if msg == 'Ok':
                    return redirect('/madmin/')
                else:
                    return render_template('editarUsuarioAdmin.html',error = msg)
            #si el metodo es buscar
            else:
                cod=request.form['code']
                try:
                    if cod==None:
                        msg = 'ERROR: Se Debe suministrar un codigo de vuelo'
                    else:
                        # Procedo a ubicar el usuario indicado
                        #Armo la consulta SQL
                        sql = f"SELECT aerolinea, matricula, destino, origen, estadovuelo, piloto,horasalida, horallegada FROM vuelos WHERE codigo='{cod}'"
                        #Ejecuto la consulta 
                        dat = cargardatos(sql)
                        #si los datos encontado son  quiere decir que el usuario o la clave son invalidos
                        if len(dat)==0:
                            msg ='ERROR:: Usuario no valido'
                            print(msg)
                        #De lo contrario capturo el perfil del usuario y creo las variables de sesion
                        else:              
                            msg = 'Ok'
                                
                except Exception:
                    msg = 'ERROR: Por favor intente luego'
                    print(Exception)
                if msg == 'Ok':
                    return render_template('editarEliminar.html',empresa=dat[0][0], matricula=dat[0][1],destino=dat[0][2], origen=dat[0][3], estado=dat[0][4],piloto=dat[0][5],fhsalida=dat[0][6],fhllegada=dat[0][7],codigo=cod,var='None' )
                else:
                    return render_template('editarEliminar.html',error = msg)
    else:
        return render_template('error.html',mensaje='Acceso no permitido')




@app.route('/verusuarios/')
def listarUsuario():
    if session['perfil']!='A':
        return render_template('error.html',mensaje='Acseso no permitido')
    else:
        try:
            #Armo la consulta SQL
            sql = f"SELECT * FROM usuarios"
            #print('arme a consulta')
            #Ejecuto la consulta 
            dat = cargardatos(sql)
            #si los datos encontado son  quiere decir que el usuario o la clave son invalidos
            #print('estoy afuera del if')
            #print(dat)
            if len(dat)==0:
                msg ='No hay usuarios registrados'
                print(msg)
            #De lo contrario capturo el perfil del usuario y creo las variables de sesion
            else:                   
                msg = 'Ok'
                    
        except Exception:
            msg = 'ERROR: Por favor intente luego'
            print(Exception)
        if msg == 'Ok':
            return render_template('verUsuarios.html',usuarios=dat)
        else:
            return render_template('error.html',mensaje=msg)


@app.route('/vermensajes/')
def listarMensaje():
    if session['perfil']!='A':
        return render_template('error.html',mensaje='Acseso no permitido')
    else:
        try:
            #Armo la consulta SQL
            sql = f"SELECT * FROM mensajes"
            #print('arme a consulta')
            #Ejecuto la consulta 
            dat = cargardatos(sql)
            #si los datos encontado son  quiere decir que el usuario o la clave son invalidos
            #print('estoy afuera del if')
            #print(dat)
            if len(dat)==0:
                msg ='No hay mensajes registrados'
                print(msg)
            #De lo contrario capturo el perfil del usuario y creo las variables de sesion
            else:                   
                msg = 'Ok'
                    
        except Exception:
            msg = 'ERROR: Por favor intente luego'
            print(Exception)
        if msg == 'Ok':
            return render_template('verMensajes.html',mensajes=dat)
        else:
            return render_template('error.html',mensaje=msg)

if __name__=='__main__':
    app.secret_key=os.urandom(12)
    app.run(debug=True,port=8080)