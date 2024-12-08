import hashlib
import mysql.connector

import os
from flask import Flask, request, render_template, session, jsonify
from datetime import datetime
from classes.generaCodigos import GeneraCodigo
import random
import string
class RegistraData:
    def __init__(self) -> None:
        self.direccion = ''
        self.idCliente = ''
        self.passw = ''
        self.cliente = ''
        self.email = ''
        self.telefono = ''
        self.rol = 0
        self.nombre = ''
        self.nickname = ''
        self.descripcionG = ''
        self.descripcion = ''
        self.monto = ''
        self.fechaV = ''
        self.db_config = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': '',
            'database': 'praxis'
        }
    def ingresaRegistros(self):
       
        try:
            conexion = mysql.connector.connect(**self.db_config)

            cursor = conexion.cursor()
            consulta = """
                INSERT INTO clientes 
                ( nombre, email, telefono, direccion, fechaRegistro,estatus_cliente) 
                VALUES (%s, %s, %s, %s, now(),'ACTIVO')
            """

            datos_grupo = (self.nombre, self.email, self.telefono, self.direccion)
            cursor.execute(consulta, datos_grupo)
            print("HOLAAAAAAAAAAAAAAAAAAAAAA",datos_grupo)
            conexion.commit()
            return jsonify({"mensaje":"Se inserto colegio","exito":True})

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return jsonify({"mensaje":"No se inserto colegio","exito":False})

        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()
    def obtenerUsuarios(self):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()

            
            consulta = "select u.id,nickusuario,u.nombre,r.nombre as rol,estatus_usuario from usuarios u inner join roles r on rol_id=r.id;"
            cursor.execute(consulta)  
            Ventas = cursor.fetchall()
            print(Ventas)
            ventasAll=[]
            for fila in Ventas:                                
                respuesta={'id':fila[0],'nickname':fila[1],'nombreUsuario':fila[2],'rol':fila[3],'estatusUsuario':fila[4]}  
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
    def dameCargos(self):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()

            
            consulta = "select ClienteID, nombre, id_cargo,descripcion,fecha_cargo,monto_cargo,saldo_cargo from clientes c inner join cargos car on car.id_cliente=c.ClienteID where nombre=%s"
            cursor.execute(consulta,(self.nombre,))  
            Ventas = cursor.fetchall()
            print(Ventas)
            ventasAll=[]
            for fila in Ventas:                                
                respuesta={'idCliente':fila[0],'nombre':fila[1],'id_cargo':fila[2],'descripcion':fila[3],'fecha_cargo':fila[4],'monto_cargo':fila[5],'saldo_cargo':fila[6]}  
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
    def actualizaUsuario(self):
        print(self.nombre,self.idCliente,self.rol)
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()

            
            consulta = "UPDATE usuarios SET nombre=%s,rol_id=%s WHERE id=%s"
            
            cursor.execute(consulta,(self.nombre,self.rol,self.idCliente,))  
            conexion.commit()
            print(self.nombre,self.idCliente,self.rol)
            return jsonify({"mensaje":"Se inserto colegio","exito":True})

        except mysql.connector.Error as err:
            print(f"Error al obtener las ventas: {err}")
            return jsonify({"mensaje":"Se actualizo usuario","exito":False})

        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()  
    def registraUsuario(self):
        
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()

            passw = hashlib.sha1(self.passw.encode()).hexdigest()
            
            consulta = "INSERT INTO usuarios (id, nickusuario, nombre, email, pass, telefono, direccion, fecha_nacimiento, fecha_ultimo_inicio_sesion, email_verificado, rol_id, fecha_creacion, fecha_actualizacion, estatus_usuario) VALUES (null, %s, %s, %s, %s, '123456789', 'Calle Falsa 123', '1990-01-01', '2024-12-01 17:16:23', '0', %s, '2024-06-03 10:45:37', '2024-12-01 17:16:23', '1');"
            
            cursor.execute(consulta,(self.nickname,self.nombre,self.email,passw,self.rol,))  
            conexion.commit()
            print(self.nombre,self.idCliente,self.rol)
            return jsonify({"mensaje":"Se inserto colegio","exito":True})

        except mysql.connector.Error as err:
            print(f"Error al obtener las ventas: {err}")
            return jsonify({"mensaje":"Se actualizo usuario","exito":False})

        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()  
    def registraCargo(self):
        
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()

            passw = hashlib.sha1(self.passw.encode()).hexdigest()
            consulta = "INSERT INTO cargos (id_cargo, id_cliente, descripcion, fecha_cargo, monto_cargo, saldo_cargo, fecha_registro) VALUES (null, %s, %s, %s, %s, %s, now());"
            cursor.execute(consulta,(self.idCliente,self.descripcion,self.fechaV,self.monto,self.monto,))  
            
            conexion.commit()
            print(self.nombre,self.idCliente,self.rol)
            return jsonify({"mensaje":"Se inserto colegio","exito":True})

        except mysql.connector.Error as err:
            print(f"Error al obtener las ventas: {err}")
            return jsonify({"mensaje":"Se actualizo usuario","exito":False})

        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()  

        