import hashlib
import mysql.connector

import os
from flask import Flask, request, render_template, session
from datetime import datetime
from classes.generaCodigos import GeneraCodigo
import random
import string






class Grupos:
    def __init__(self) -> None:
        self.nombreG = ''
        self.cupoG = ''
        self.visibilidad = ''
        self.fechaInicio = ''
        self.fechaFin = ''
        self.descripcionG = ''
        self.db_config = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': '',
            'database': 'praxis'
        }

    def creaGrupo(self):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()
            parte1 = ''.join(random.choices(string.ascii_uppercase, k=2)) 
            parte2 = ''.join(random.choices(string.digits, k=2))            
            parte3 = ''.join(random.choices(string.ascii_uppercase, k=2)) 

            codigo = f"{parte1}-{parte2}-{parte3}"
            
            consulta = "INSERT INTO grupos (nombre_grupo, cupo, visibilidad, descripcion, profesor_id, estatus_grupo, fecha_inicio, fecha_fin,codigo) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)"
            
            datos_grupo = (self.nombreG, self.cupoG, self.visibilidad, self.descripcionG, 1, 'ACTIVO', self.fechaInicio, self.fechaFin,codigo)
            cursor.execute(consulta, datos_grupo)


            
            conexion.commit()

            return 1

        except mysql.connector.Error as err:
            return 2

        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()
                
    def obtener_grupos(self):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()

            
            consulta = "select * from grupos g where g.profesor_id=%s AND estatus_grupo='ACTIVO';"
            cursor.execute(consulta, (1,))  
            grupos = cursor.fetchall()
            gruposAll=[]
            for fila in grupos:                                
                respuesta={'idGrupo':fila[0],'nombreGrupo':fila[1],'cupo':fila[2], 'visibilidad':fila[3],'descripcion':fila[4],'profesorID':fila[5], 'estatusGrupo':fila[6],'fechaCreacion':fila[7],'fechaInicio':fila[8], 'fechaFin':fila[9], 'codigoGrupo':fila[10]}  
                print(respuesta)
                gruposAll.append(respuesta)
            return gruposAll
            

        except mysql.connector.Error as err:
            print(f"Error al obtener los grupos: {err}")
            return []

        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()
                
    def dameInscripciones(self):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()

            
            consulta = "select * from grupos g where g.profesor_id=%s AND estatus_grupo='ACTIVO';"
            cursor.execute(consulta, (session['idUsuario'],))  
            grupos = cursor.fetchall()
           
            return grupos
            

        except mysql.connector.Error as err:
            print(f"Error al obtener los grupos: {err}")
            return []

        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()
        
    
