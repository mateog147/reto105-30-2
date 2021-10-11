from flask import Flask
from flask.templating import render_template

server = Flask('__name__')

@server.route('/')
@server.route('/home/')
@server.route('/index/')
def index():
    sal = '<h1>PAGINA INICIO</h1>'
    sal +='<a href="/login">LOGIN</a>'
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

@server.route('/nosotros')
@server.route('/nosotros/')
def about():
    sal = '<h1>Sobre nosotros: </h1>'
    sal += '<p>info</p>'
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

@server.route('/menu')
@server.route('/menu/')
@server.route('/menu/<string:usr>')
def userMenu():
    return render_template('menuUsuario.html')

@server.route('/mpiloto')
@server.route('/mpiloto/')
@server.route('/mpiloto/<string:usr>')
def pilotMenu():
    return render_template('menuPiloto.html')

@server.route('/madmin')
@server.route('/madmin/')
@server.route('/madmin/<string:usr>')
def adminMenu():
    return render_template('menuAdmin.html')

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

if __name__=='__main__':
    server.run(debug=True,port=8080)