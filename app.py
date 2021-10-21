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
    return render_template('menuUsuario.html',nombre=session['nombre'])

@server.route('/madmin')
@server.route('/madmin/')
@server.route('/madmin/<string:usr>')
def adminMenu(usr=None):
    return render_template('menuAdmin.html')

@server.route('/mpiloto')
@server.route('/mpiloto/')
@server.route('/mpiloto/<string:usr>')
def pilotMenu(usr=None):
    return render_template('menuPiloto.html',nombre=session['nombre'])

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

@server.route('/roles/')
def permisosRoles():
    return render_template('permisosRoles.html')

@server.route('/registrovuelo/')
def registroVuelo():
    return render_template('registroVuelo.html')

@server.route('/editarvuelo/')
def editoVuelo():
    return render_template('editarEliminar.html')

@server.route('/verusuarios/')
def listarUsuario():
    return render_template('verUsuarios.html')



if __name__=='__main__':
    server.secret_key=os.urandom(12)
    server.run(debug=True,port=8080)