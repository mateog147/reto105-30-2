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
    sal = '<h1>Sobre nosotros: </h1>'
    sal += '<p>info</p>'
    sal +='<a href="/home">HOME</a>'
    return sal

@server.route('/terminos')
@server.route('/terminos/')
def tercond():
    sal = '<h1>Terminos y condiciones</h1>'
    sal +='<a href="/home">HOME</a>'
    return sal

@server.route('/contactanos')
@server.route('/contactanos/')
def contact():
    sal = '<h1>Folmulario contacto</h1>'
    sal +='<a href="/home">HOME</a>'
    return sal

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
    sal = '<p>pagina para recuperar tu clave vía correo</p>'
    sal +='<a href="/home">HOME</a>'
    return sal

@server.route('/menu')
@server.route('/menu/')
@server.route('/menu/<string:usr>')
def userMenu():
    return render_template('menuUsuario.html')

@server.route('/madmin')
@server.route('/madmin/')
@server.route('/madmin/<string:usr>')
def adminMenu():
    return render_template('menuAdmin.html')

@server.route('/mpiloto')
@server.route('/mpiloto/')
@server.route('/mpiloto/<string:usr>')
def pilotMenu():
    return render_template('menuPiloto.html')

@server.route('/calificar')
@server.route('/calificar/')
@server.route('/calificar/<string:cod>/<string:usr>')
def calificarVuelo():
    return render_template('calificarVuelo.html')

@server.route('/separavuelo')
@server.route('/separavuelo/')
@server.route('/separavuelo/<string:usr>')
def separarVuelo():
    return render_template('separarVuelo.html')

@server.route('/vervuelos/')
@server.route('/vervuelos/<string:usr>')
def listarVuelos():
    return render_template('verVuelos.html')

@server.route('/editarusuario/')
def editUser():
    sal = '<p>Pantalla para editar usuario</p>'
    sal +='<a href="/menu/">atras</a>'
    return sal

@server.route('/calificaciones/')
@server.route('/calificaciones/<string:usr>')
def verCal():
    return render_template('comentarios.html')

@server.route('/roles/')
def permisosRoles():
    return render_template('permisosRoles.html')

@server.route('/registrovuelo/')
def registroVuelo():
    sal = '<p>Pantalla para crear un vuelo</p>'
    sal +='<a href="/madmin/">atras</a>'
    return sal

@server.route('/editarvuelo/')
def editoVuelo():
    sal = '<p>Pantalla para editar un vuelo</p>'
    sal +='<a href="/madmin/">atras</a>'
    return sal

@server.route('/verusuarios/')
def listarUsuario():
    return render_template('verUsuarios.html')





if __name__=='__main__':
    server.run(debug=True,port=8080)