import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import mysql.connector

class Estadisticas:
    def __init__(self) -> None:
        self.usuario = ''
        self.password = ''
        self.db_config = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': '',
            'database': 'praxis'
        }
        
    def obtener_grupo(self,grupo_id):
        connection = mysql.connector.connect(**self.db_config)
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
        SELECT *
        FROM grupos g
        WHERE g.id = %s AND estatus_grupo = 'ACTIVO'
        """, (grupo_id,))

        grupo = cursor.fetchone()

        cursor.close()
        connection.close()

        if grupo:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
            SELECT a.nombre AS Nombre, 
               r.aciertos AS Aciertos,
               errores AS Errores
                
            FROM resultados r
            inner join inscripciones i on r.inscripcion_id=i.id
            INNER JOIN alumnos a on i.alumno_id=a.id
            WHERE i.grupo_id = %s AND estatus_inscripcion='ACTIVO'
            GROUP BY nombre 
            """, (grupo_id,))

            aciertos = cursor.fetchall()

            cursor.close()
            connection.close()

            data = {
                'Nombre': ['Juan Pérez', 'Ana López', 'Carlos Martínez'],
                'Matemáticas': [85, 95, 70],
                'Español': [90, 88, 75],
                'Ciencias': [78, 92, 80]
            }
            df = pd.DataFrame(aciertos)
            df.set_index('Nombre', inplace=True)

            fig, ax = plt.subplots(figsize=(10, 6))
            df.plot(kind='bar', ax=ax)
            ax.set_title('Calificaciones de Estudiantes')
            ax.set_ylabel('Calificación')
            ax.set_xlabel('Estudiantes')
            ax.set_ylim(0, 10)
            plt.xticks(rotation=45)
            plt.tight_layout()

            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            bar_img_base64 = base64.b64encode(img.getvalue()).decode('utf8')

            fig, axs = plt.subplots(1, 3, figsize=(18, 6))

            for i, subject in enumerate(df.columns):
                df[subject].plot.pie(
                    ax=axs[i],
                    autopct='%1.1f%%',
                    startangle=90,
                    title=f'Distribución de {subject}'
                )
                axs[i].set_ylabel('') 

            plt.tight_layout()

            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            pie_img_base64 = base64.b64encode(img.getvalue()).decode('utf8')

            fig, ax = plt.subplots(figsize=(10, 6))
            df['Aciertos'].plot(kind='hist', bins=10, ax=ax)
            ax.set_title('Distribución de Calificaciones en Matemáticas')
            ax.set_xlabel('Calificación')
            ax.set_ylabel('Frecuencia')
            plt.tight_layout()

            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            hist_img_base64 = base64.b64encode(img.getvalue()).decode('utf8')

            return grupo, bar_img_base64, pie_img_base64, hist_img_base64
    
        else:
            return None, None