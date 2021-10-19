from flask import Flask, render_template, redirect, session, flash, request
from flask.templating import render_template
from bd import cargardatos

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
    if request.method=='GET':
        return render_template('login.html')
    else:
        usr = request.form['email']
        clave = request.form['pwd']
        print(f'me pidieron el menu para {usr}')
        #intento conectarme
        try:
            dat = None
            if usr==None:
                msg = 'ERROR: Se Debe suministrar un usuario'
            elif clave==None:
                msg = 'ERROR: Se Debe suministrar una clave'
            else:
                # Procedo a ubicar el usuario indicado
                sql = f"SELECT nombre, perfil FROM usuarios WHERE email='{usr}' AND contraseña='{clave}'"
                #print('arme a consulta')
                dat = cargardatos(sql)
                if len(dat)==0:
                    msg ='ERROR:: Usuario o clave no validos'
                else:
                    msg = 'Ok'
                    profile = dat[0][1]
                    
        except Exception:
            msg = 'ERROR: Por favor intente luego'
            print(Exception)
            dat = None
        sal = '<h2>Se realizó la consulta</h2><p>'
        sal += msg
        sal += '</p>'
        if msg=="Ok":
            if(profile == 'U'):
                return redirect('/menu/')
            elif(profile == 'A'):
                return redirect('/madmin/')
            elif(profile == 'P'):
                return redirect('/mpiloto/')

        return sal


@server.route('/registro')
@server.route('/registro/')
def register():
    return render_template('registro.html')

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
    return render_template('menuUsuario.html')

@server.route('/madmin')
@server.route('/madmin/')
@server.route('/madmin/<string:usr>')
def adminMenu(usr=None):
    return render_template('menuAdmin.html')

@server.route('/mpiloto')
@server.route('/mpiloto/')
@server.route('/mpiloto/<string:usr>')
def pilotMenu(usr=None):
    return render_template('menuPiloto.html')

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
    server.run(debug=True,port=8080)