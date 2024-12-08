import hashlib, jsonify
import mysql.connector
#from dotenv import load_dotenv
import os
from flask import Flask, request, render_template, session
from flask_cors import CORS

#load_dotenv()
#DB_HOST = os.getenv("DB_HOST")
#DB_PORT = os.getenv("DB_PORT")
#DB_NAME = os.getenv("DB_NAME")
#DB_USER = os.getenv("DB_USER")
#DB_PASSWORD = os.getenv("DB_PASSWORD")

class Login:
    def __init__(self) -> None:
        self.usuario = ''
        self.password = ''
        self.db_config = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': '',
            'database': 'praxis'
        }

    def encriptar_contraseña(self, contraseña):
        
        sha_signature = hashlib.sha1(contraseña.encode()).hexdigest()
        return sha_signature

    def iniciaLoggeo(self):
        print("Hola me estoy loggeando")
        usuario = self.usuario
        password = self.password

        password_encriptada = self.encriptar_contraseña(password)

        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()

            consulta = "SELECT u.id as idUsuario,pass,u.nombre as nombreUsuario, r.nombre as rol FROM usuarios u left join roles r on u.rol_id=r.id WHERE nickusuario = %s"
            cursor.execute(consulta, (usuario,))
            resultado = cursor.fetchone()
            
            if resultado:
                contraseña_almacenada = resultado[1]
                idUsuario = resultado[0]
                nombreUsuario = resultado[2]
                rolUsuario = resultado[3]
                

                if password_encriptada == contraseña_almacenada:
                    respuesta={'usuario':usuario,'idUsuario':idUsuario,'nombre':nombreUsuario, 'rol':rolUsuario,'respuesta':True}
                    session['usuario'] = usuario 
                    session['idUsuario'] = idUsuario
                    session['nombre'] = nombreUsuario
                    session['rolUsuario'] = rolUsuario
                    return respuesta
                else:
                    respuesta={'respuesta':False}
                    return respuesta
            else:
                respuesta={'respuesta':False}
                return respuesta
                

            cursor.close()
            conexion.close()

        except mysql.connector.Error as err:
            # Manejar errores de la base de datos
            return(f"Error: {err}")
            