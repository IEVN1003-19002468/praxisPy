import hashlib
import mysql.connector
#from dotenv import load_dotenv
import os
from flask import Flask, jsonify, request, render_template, session

#load_dotenv()
#DB_HOST = os.getenv("DB_HOST")
#DB_PORT = os.getenv("DB_PORT")
#DB_NAME = os.getenv("DB_NAME")
#DB_USER = os.getenv("DB_USER")
#DB_PASSWORD = os.getenv("DB_PASSWORD")

class LoginGame:
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
        usuario = self.usuario
        password = self.password

        password_encriptada = password

        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()

            consulta = "SELECT id,contraseña,nombre FROM alumnos WHERE id = %s"
            cursor.execute(consulta, (usuario,))
            resultado = cursor.fetchone()

            if resultado:
                contraseña_almacenada = resultado[1]
                idUsuario = resultado[0]
                

                
                if password_encriptada == contraseña_almacenada:
                    consulta = "select nombre_grupo as grupo from inscripciones i inner join grupos g on i.grupo_id=g.id inner join ciclo_escolar ce on i.id_ciclo=ce.id_ciclo where ce.fecha_inicio<=now() and ce.fecha_fin>=now() and i.alumno_id=%s and estatus_inscripcion='ACTIVO'"
                    cursor.execute(consulta, (resultado[0],))
                    resultadoInscrpcion = cursor.fetchone()
                    if resultadoInscrpcion is None:
                        resultadoInscrpcion=[0]
                    datos_usuario = {
                        "id": resultado[0],
                        "grupo": resultadoInscrpcion[0]
                        #"contraseña": resultado[2]
                     }

                
                    return jsonify(datos_usuario)
                else:
                    return 2
            else:
                return usuario

            cursor.close()
            conexion.close()

        except mysql.connector.Error as err:
            
            return(f"Error: {err}")
            