import hashlib
import mysql.connector

import os
from flask import Flask, request, render_template, session, jsonify
from datetime import datetime
from classes.generaCodigos import GeneraCodigo
import random
import string






class Ventas:
    def __init__(self) -> None:
        self.nombreG = ''
        self.cupoG = ''
        self.visibilidad = ''
        self.fechaInicio = ''
        self.fechaFin = ''
        self.descripcionG = ''
        self.idCliente=0
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
    def inactivaColegio(self):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()

            
            consulta = "UPDATE clientes SET estatus_cliente='INACTIVO' WHERE ClienteID=%s"
            
            cursor.execute(consulta,(self.idCliente,))  
            conexion.commit()
            return jsonify({"mensaje":"Se inserto colegio","exito":True})

        except mysql.connector.Error as err:
            print(f"Error al obtener las ventas: {err}")
            return jsonify({"mensaje":"Se inserto colegio","exito":False})

        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()      
    def activaColegio(self):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()

            
            consulta = "UPDATE clientes SET estatus_cliente='ACTIVO' WHERE ClienteID=%s"
            
            cursor.execute(consulta,(self.idCliente,))  
            conexion.commit()
            return jsonify({"mensaje":"Se inserto colegio","exito":True})

        except mysql.connector.Error as err:
            print(f"Error al obtener las ventas: {err}")
            return jsonify({"mensaje":"Se inserto colegio","exito":False})

        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()      
    def actualizaCol(self):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()

            
            consulta = "UPDATE clientes SET nombre=%s WHERE ClienteID=%s"
            
            cursor.execute(consulta,(self.idCliente,))  
            conexion.commit()
            return jsonify({"mensaje":"Se inserto colegio","exito":True})

        except mysql.connector.Error as err:
            print(f"Error al obtener las ventas: {err}")
            return jsonify({"mensaje":"Se inserto colegio","exito":False})

        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()      
    def obtener_ventas(self):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()

            
            consulta = "select nombre, MontoTotal from clientes c inner join ventas v on v.clienteID=c.ClienteID"
            cursor.execute(consulta)  
            Ventas = cursor.fetchall()
            print(Ventas)
            ventasAll=[]
            for fila in Ventas:                                
                respuesta={'cliente':fila[0],'venta':fila[1]}  
                print(respuesta)
                ventasAll.append(respuesta)
            return ventasAll
            

        except mysql.connector.Error as err:
            print(f"Error al obtener las ventas: {err}")
            return []

        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()
                
    def dameLicenciasXCliente(self):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()

            
            consulta = "SELECT c.nombre,estatus_cliente,c.ClienteId, COUNT(*) AS total_licencias FROM LICENCIASALUMNOS lc INNER JOIN clientes c ON lc.clienteid = c.clienteid GROUP BY c.clienteid, c.nombre;"
            cursor.execute(consulta)  
            licencias = cursor.fetchall()
            ventasAll=[]
            for fila in licencias:                                
                respuesta={'cliente':fila[0],'estatus':fila[1],'noLicencias':fila[3],'ClienteId':fila[2]}  
                print(respuesta)
                ventasAll.append(respuesta)
            return ventasAll
        except mysql.connector.Error as err:
            print(f"Error al obtener los grupos: {err}")
            return []
    def dameClienteXCliente(self):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()

            
            consulta = "SELECT nombre,estatus_cliente FROM clientes;"
            cursor.execute(consulta)  
            licencias = cursor.fetchall()
            ventasAll=[]
            for fila in licencias:                                
                respuesta={'cliente':fila[0],'estatus':fila[1]}  
                print(respuesta)
                ventasAll.append(respuesta)
            return ventasAll
        except mysql.connector.Error as err:
            print(f"Error al obtener los grupos: {err}")
            return []
        
    def dameMetas(self):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()

            
            consulta = "SELECT count(*) FROM clientes"
            cursor.execute(consulta)  
            respuesta = cursor.fetchall()            
                
            return respuesta
            
            

        except mysql.connector.Error as err:
            print(f"Error al obtener los grupos: {err}")
            return []

        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()
        
    
