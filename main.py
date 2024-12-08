from flask import  Flask, session, redirect, url_for, request, render_template, jsonify
from classes.login import Login
from classes.loginGame import LoginGame
from classes.registraPts import RegistraPts
from classes.estadisticas import Estadisticas
from classes.ventas import Ventas
from classes.registros import RegistraData
#Sfrom dotenv import load_dotenv
import os
from classes.grupos import Grupos
import mysql.connector
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import io
import base64
from classes.realizaInscripcion import RealizaInscripcion
from flask_cors import CORS
from classes.realizaDesinscripcion import Desinscribe
matplotlib.use('Agg')
db_config = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': '',
            'database': 'praxis'
        }
app=Flask(__name__)
app.secret_key = "Secret" 
CORS(app,resources={r"/*": {"origins":"http://localhost:4200"}})
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        objLogin = Login()
        objLogin.usuario = request.json["inpUsuario"]
        objLogin.password = request.json["inpPass"]
        res=objLogin.iniciaLoggeo()
        return res
    
@app.route('/loginGame', methods=['GET', 'POST'])
def loginGame():
    if request.method == 'POST':
        objLogin = LoginGame()
        objLogin.usuario = request.form.get("inpUsuario")
        objLogin.password = request.form.get("inpPass")
        res=objLogin.iniciaLoggeo()
       
        if res:
            
            return res
        else:
            
            mensaje_respuesta = 'Usuario o contraseña incorrectos'
            return 404

    return render_template('login.html')
@app.route('/dameGrupos', methods=['GET','POST'])
def dameGrupos():
    if request.method == 'GET':
        objGrupo = Grupos()
        mis_grupos = objGrupo.obtener_grupos()
        print(mis_grupos)
        return mis_grupos
@app.route('/dameVentas', methods=['GET','POST'])
def dameVentas():
    if request.method == 'GET':
        objVentas = Ventas()
        ventas = objVentas.obtener_ventas()
        print(ventas)
        return ventas
@app.route('/dameUsuarios', methods=['GET','POST'])
def dameUsuarios():
    if request.method == 'GET':
        objUsuarios = RegistraData()
        ventas = objUsuarios.obtenerUsuarios()
        
        return ventas
@app.route('/actualizaUsuario', methods=['GET','POST'])
def actualizaUsuario():
    if request.method =='POST':
        objUsuarios = RegistraData()
        rol=request.json['rol']
        if rol=='Administrador':
            rolFinal=3
        elif rol == 'Finanzas':
            rolFinal=4
        elif rol == 'Profesor':
            rolFinal=1

        objUsuarios.idCliente=request.json['idUsuario']
        objUsuarios.nombre=request.json['nombre']
        objUsuarios.rol=rolFinal
        
        actualiza = objUsuarios.actualizaUsuario()
        
        return actualiza
@app.route('/registraUsuario', methods=['GET','POST'])
def registraUsuario():
    if request.method =='POST':
        objUsuarios = RegistraData()
        rol=request.json['rol']
        if rol=='Administrador':
            rolFinal=3
        elif rol == 'Finanzas':
            rolFinal=4
        elif rol == 'Profesor':
            rolFinal=1

        
        objUsuarios.nombre=request.json['nombre']
        objUsuarios.passw=request.json['pass']
        objUsuarios.email=request.json['email']
        objUsuarios.nickname=request.json['nickname']
        objUsuarios.rol=rolFinal

        actualiza = objUsuarios.registraUsuario()
@app.route('/registraCargo', methods=['GET','POST'])
def registraCargo():
    if request.method =='POST':
        objUsuarios = RegistraData()
               
        objUsuarios.idCliente=request.json['idCliente']
        objUsuarios.descripcion=request.json['descripcion']
        objUsuarios.monto=request.json['cargo']
        objUsuarios.fechaV=request.json['fechaV']
        

        actualiza = objUsuarios.registraCargo()
        
        return actualiza
@app.route('/dameCargos', methods=['GET','POST'])
def dameCargos():
    if request.method =='POST':
        objUsuarios = RegistraData() 
        objUsuarios.nombre=request.json['nombre']         

        actualiza = objUsuarios.dameCargos()
        
        return actualiza
        
@app.route('/dameLicencias', methods=['GET','POST'])
def dameLicencias():
    if request.method == 'GET':
        objLicencias = Ventas()
        licencia =objLicencias.dameLicenciasXCliente()
        print(licencia)
        return licencia
@app.route('/dameClientesTotal', methods=['GET','POST'])
def dameCliente():
    if request.method == 'GET':
        objCliente = Ventas()
        licencia =objCliente.dameClienteXCliente()
        print(licencia)
        return licencia
@app.route('/dameMetas', methods=['GET','POST'])
def dameMetas():
    if request.method == 'GET':
        objMetas = Ventas()
        metas =objMetas.dameMetas()
        print(metas)
        return metas
@app.route('/inactivaColegio/<clg>', methods=['GET','POST'])
def inactivaColegio(clg):
    if request.method == 'POST' or request.method == 'GET':
        objVentas = Ventas()
        objVentas.idCliente=clg
        metas =objVentas.inactivaColegio()
        
        return metas
@app.route('/activaColegio/<clg>', methods=['GET','POST'])
def activaColegio(clg):
    if request.method == 'POST' or request.method == 'GET':
        objVentas = Ventas()
        objVentas.idCliente=clg
        metas =objVentas.activaColegio()
        
        return metas
    
@app.route('/registraCliente', methods=['GET','POST'])
def registraCliente():    
    if request.method == 'POST':
        objClientes = RegistraData()
        objClientes.nombre=request.json["nombre"]
        objClientes.email=request.json["email"]
        objClientes.telefono=request.json["telefono"]
        objClientes.direccion=request.json["direccion"]
        metas =objClientes.ingresaRegistros()
       
        return metas
@app.route('/inscribeAlumno', methods=['GET', 'POST'])
def inscribeAlumno():
    if request.method == 'POST':
        objInscripcion = RealizaInscripcion()
        
        objInscripcion.codigo = request.form.get("codigoGrupo")
        
        objInscripcion.matricula = request.form.get("inpUsuario")
        res=objInscripcion.registraInscripcion()
        
       
        if res:
            try:
                conexion = mysql.connector.connect(**db_config)
                cursor = conexion.cursor()

            
                consulta = "select nombre_grupo from grupos g where g.codigo=%s AND estatus_grupo='ACTIVO';"
                cursor.execute(consulta, (objInscripcion.codigo,))  
                grupos = cursor.fetchone()
                datos_usuario = {
                        "grupo": grupos[0]
                        
                        #"contraseña": resultado[2]
                     }
                return jsonify(datos_usuario)
            

            except mysql.connector.Error as err:
                print(f"Error al obtener los grupos: {err}")
                return []

            
        else:
            
            mensaje_respuesta = 'Usuario o contraseña incorrectos'
            return 404
    
@app.route('/desinscribeAlumno', methods=['GET', 'POST'])
def desinscribeAlumno():
    if request.method == 'POST':
        objInscripcion = Desinscribe()
        objInscripcion.matricula = request.form.get("inpUsuario")
        res=objInscripcion.realizaDesinscripcion()
        
        if res:
            return jsonify({
        "grupo": 0})
        else:
            
            mensaje_respuesta = 'Usuario o contraseña incorrectos'
            return 404
@app.route('/inscribeWeb' , methods=['GET', 'POST'])
def inscribeWeb():
    session.pop('usuario', None)
    return redirect(url_for('index'))    
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))

@app.route('/grupo', methods=['GET', 'POST'])
def grupo():
    
    objGrupo = Grupos()
    objGrupo.nombreG = request.form.get('nombreG')
    objGrupo.cupoG = request.form.get('cupoG')
    objGrupo.visibilidad = request.form.get('visibleG')
    objGrupo.fechaInicio = request.form.get('inicioFech')
    objGrupo.fechaFin = request.form.get('finFech')
    objGrupo.descripcionG = request.form.get('descripcionG')
    resp=objGrupo.creaGrupo()
    mis_grupos = objGrupo.obtener_grupos()
    if resp==1:
        mensajeResp = f"Grupo {objGrupo.nombreG} ha sido creado con éxito"
        return redirect(url_for('index', mensajeResp=mensajeResp))
  
        
    else :
        return render_template('index.html', errorResp='No se pudo crear el grupo '+request.form.get('nombreG'),mis_grupos=mis_grupos) 
@app.route('/registraPts', methods=['GET', 'POST'])
def registraPts():
    objRegistra = RegistraPts()
    objRegistra.matricula = request.form.get('matricula')
    objRegistra.aciertos = request.form.get('aciertos')
    objRegistra.incorrectas = request.form.get('incorrectas')
    objRegistra.tiempo = request.form.get('tiempo')
    
    isInscrito = objRegistra.registraPts() 
    
    if isInscrito == 202:
        return 'Registro con exito'
    else :
        return 'Hubo un problema al registrar'
    return isInscrito   
@app.route('/grupo/<int:grupo_id>')
def obtener_grupo(grupo_id):
    objEst = Estadisticas()
    grupo, grafico, graficoPie,otroGrafico = objEst.obtener_grupo(grupo_id)
    if grupo is None :
        return jsonify({"error": "No se encontraron alumnos activos para este grupo."}), 404
    
    return jsonify({
        "grupo": grupo,
        "grafico": grafico,
        "graficoPie": graficoPie,
        "otroGrafico": otroGrafico
    })
            
if __name__=="__main__":
    app.run(debug=True)
    