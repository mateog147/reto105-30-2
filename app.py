from flask import Flask, render_template, redirect, session, flash, request
from flask.templating import render_template
from bd import cargardatos, resgistrardato
from datetime import datetime
import math
import os
from werkzeug.security import check_password_hash, generate_password_hash
from markupsafe import escape

server = Flask('__name__')

@server.route('/')
@server.route('/home/')
@server.route('/index/')
def index():
    session['perfil']=None
    return render_template('index.html')

@server.route('/nosotros')
@server.route('/nosotros/')
def about():
    return render_template('sobreNosotros.html')


@server.route('/terminos')
@server.route('/terminos/')
def tercond():
    return render_template('terminosCondiciones.html')

@server.route('/contactanos')
@server.route('/contactanos/')
def contact():
    return render_template('contacto.html')

@server.route('/login')
@server.route('/login/',methods=['GET', 'POST'])

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
                sql = f"SELECT nombre, perfil, contraseña FROM usuarios WHERE email='{usr}'"
                #print('arme a consulta')
                #Ejecuto la consulta 
                dat = cargardatos(sql)
                #si los datos encontado son  quiere decir que el usuario o la clave son invalidos
                print('estoy afuera del if')
                print(dat)
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


@server.route('/registro')
@server.route('/registro/',methods=['GET', 'POST'])
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
        print(nombre)
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


@server.route('/recuperarpwd/')
def rpwd():
    sal = '<head><link rel="stylesheet" href="../static/css/style.css"></head>'
    sal +="<div class = 'main'>"
    sal += '<p>Se ha enviado un correo con las instrucciones</p>'
    sal +='<a href="/home">VOLVER AL HOME</a>'
    sal += '</div>'
    return sal

@server.route('/menu')
@server.route('/menu/')
@server.route('/menu/<string:usr>')
def userMenu(usr=None):
    if session['perfil']=='U':
        return render_template('menuUsuario.html',nombre=session['nombre'])
    else:
        return render_template('error.html',mensaje='Acseso no permitido')

@server.route('/madmin')
@server.route('/madmin/')
@server.route('/madmin/<string:usr>')
def adminMenu(usr=None):
    if session['perfil']=='A':
        return render_template('menuAdmin.html')
    else:
        return render_template('error.html',mensaje='Acseso no permitido')
    

@server.route('/mpiloto')
@server.route('/mpiloto/')
@server.route('/mpiloto/<string:usr>')
def pilotMenu(usr=None):
    if session['perfil']=='P':
        return render_template('menuPiloto.html',nombre=session['nombre'])
    else:
        return render_template('error.html',mensaje='Acseso no permitido')


@server.route('/calificar')
@server.route('/calificar/')
@server.route('/calificar/<string:cod>/<string:usr>')
def calificarVuelo(usr=None,cod=None):
    return render_template('calificarVuelo.html')

@server.route('/separavuelo')
@server.route('/separavuelo/')
@server.route('/separavuelo/<string:usr>')
def separarVuelo(usr=None):
    return render_template('separarVuelo.html')

@server.route('/vervuelos/')
@server.route('/vervuelos/<string:usr>')
def listarVuelos(usr=None):
    return render_template('verVuelos.html')

@server.route('/editarusuario/')
def editUser():
    return render_template('editarEliminarUsuario.html')

@server.route('/calificaciones/')
@server.route('/calificaciones/<string:usr>')
def verCal(usr=None):
    return render_template('comentarios.html')

@server.route('/roles')
@server.route('/roles/<string:met>/',methods=['GET', 'POST'])
@server.route('/roles/',methods=['GET', 'POST'])
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

@server.route('/registrovuelo/')
@server.route('/registrovuelo/',methods=['GET', 'POST'])
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

            #return(f"La fecha de salida es:{fhsalida}")
        
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
                sql = f"INSERT INTO vuelos (codigo, aerolinea, matricula, destino, origen, horasalida, horallegada, piloto) VALUES ('{codigo}', '{empresa}', '{tipo}', '{matricula}', '{destino}', '{origen}', '{fhsalida}', '{fhllegada}', '{piloto}')"
                #print('arme a consulta') 
                res = resgistrardato(sql)
                if res==0:
                    msg ='ERROR AL CARGAR LA INFORMACIÓN'
                else:
                    msg = 'Ok'
                    
        except Exception:
            msg = 'ERROR: Por favor intente luego'
            print(Exception.with_traceback)
        if msg == 'Ok':
            return redirect('/madmin/')
        else:
            return render_template('registroVuelo.html',error=msg)


@server.route('/editarvuelo/')
def editoVuelo():
    return render_template('editarEliminar.html')

@server.route('/verusuarios/')
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



if __name__=='__main__':
    server.secret_key=os.urandom(12)
    server.run(debug=True,port=8080)