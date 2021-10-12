from flask import Flask
from flask.templating import render_template

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
@server.route('/login/')
def login():
    return render_template('login.html')

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