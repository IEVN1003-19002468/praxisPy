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

class RealizaInscripcion:
    def __init__(self) -> None:
        self.matricula = ''
        self.password = ''
        self.idCiclo = ''
        self.aciertos = 0 
        self.incorrectas = 0
        self.tiempo = 0
        self.codigoGrupo = ''  # Asignar valor adecuado antes de usar
        self.db_config = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': '',
            'database': 'praxis'
        }

    def registraInscripcion(self):
        objGrupo = RealizaInscripcion()
        objGrupo.codigoGrupo=self.codigo
        idGrupo = objGrupo.dameGrupo()
        idCiclo = self.dameCiclo()
        matricula = self.matricula
        
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()
            parametros = (idGrupo, idCiclo, matricula)
            cursor.callproc('registraInscripcion', parametros)
            conexion.commit()
            return matricula
        except mysql.connector.Error as err:
            return(f"Error: {err}")
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

    def dameCiclo(self):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()
            cursor.callproc('dameCicloActual')
            result = next(cursor.stored_results()) 
            resultado = result.fetchone()  
            if resultado:                
                idCiclo = resultado[0]  
                return idCiclo          
            else:
                return str(404)
        except mysql.connector.Error as err:
            return(f"Error: {err}")
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

    def dameGrupo(self):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()
            codigo = self.codigoGrupo
            parametro = (codigo,)
            cursor.callproc('dameGrupoXCodigo',parametro )
            result = next(cursor.stored_results()) 
            resultado = result.fetchone()  
            
            if resultado:                
                idGrupo = resultado[0]  
                return str(idGrupo)         
            else:
                return str(404)
        except mysql.connector.Error as err:
            return(f"Error: {err}")
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()
