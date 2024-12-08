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

class Desinscribe:
    def __init__(self) -> None:
        self.matricula = ''
        self.password = ''
        self.idCiclo = ''
        self.aciertos = 0 
        self.incorrectas = 0
        self.tiempo = 0
        self.db_config = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': '',
            'database': 'praxis'
        }
    def realizaDesinscripcion(self):
        objPts = Desinscribe()
        objPts.matricula= self.matricula
        idInscripcion = objPts.dameInscripcion() 
        
        
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()
            parametros = (idInscripcion,)
            
            cursor.callproc('realizaDesincripcion',parametros)
            
            conexion.commit()
            
            return str(202)
            
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
            conexion.commit()
            result = next(cursor.stored_results()) 
            resultado = result.fetchone()  
            
            if resultado:                
                idCiclo = resultado[0]  
                return str(idCiclo)          
            else:
                return str(404)

            cursor.close()
            conexion.close()

        except mysql.connector.Error as err:
           
            return(f"Error: {err}")
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()
        
    def dameInscripcion(self):
        matricula = self.matricula
        objPts = Desinscribe()
        idCiclo = objPts.dameCiclo()
        
        
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()
            parametros = (matricula,idCiclo)
            cursor.callproc('dameInscripcionActual',parametros)
            result = next(cursor.stored_results()) 
            resultado = result.fetchone()  
           
            if resultado:                
                idInscripcion = resultado[0]  
                return str(idInscripcion)          
            else:
                return str(404)

            cursor.close()
            conexion.close()

        except mysql.connector.Error as err:
           
            return(f"Error: {err}")
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()
        
        