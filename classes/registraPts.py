import hashlib
import mysql.connector

import os
from flask import Flask, jsonify, request, render_template, session





class RegistraPts:
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
    def registraPts(self):
        objPts = RegistraPts()
        objPts.matricula= self.matricula
        idInscripcion = objPts.dameInscripcion() 
        
        aciertos = self.aciertos 
        incorrectas = self.incorrectas
        tiempo = self.tiempo
        puntaje = 0
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()
            parametros = (idInscripcion ,aciertos ,incorrectas ,tiempo ,puntaje)
            
            cursor.callproc('registraPuntaje',parametros)
            
            conexion.commit()
            
            return 202
            
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
        objPts = RegistraPts()
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
                return idInscripcion          
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
        
        