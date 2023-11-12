import mysql.connector
import random

# Conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    port=3305,
    password="12345678",
    database="Trivia"
    )
# Crear cursor para ejecutar consultas
cursor = db.cursor()

# Obtener preguntas y respuestas desde la base de datos
def obtener_preguntas():
    query = "SELECT pregunta, respuesta FROM Preguntas"
    cursor.execute(query)
    preguntas = cursor.fetchall()
    return preguntas

# Función para mezclar y seleccionar preguntas
def seleccionar_preguntas(preguntas, cantidad):
    random.shuffle(preguntas)
    return preguntas[:cantidad]

# Comprobar si la respuesta del usuario es correcta
def comprobar_respuesta(pregunta, respuesta_usuario):
    pregunta, respuesta_correcta = pregunta
    return respuesta_usuario == respuesta_correcta

# Calcular puntaje
def calcular_puntaje(respuestas_correctas):
    return respuestas_correctas * 100

# Registrar tiempo en la base de datos
def registrar_tiempo(tiempo):
    cursor.execute("UPDATE Usuarios SET tiempo_respondido = %s WHERE id = 1", (tiempo,))
    db.commit()

def guardar_datos_usuario(nombre_usuario, red_social):
    insert_query = "INSERT INTO usuarios (nombre, redes) VALUES (%s, %s)"
    data = (nombre_usuario, red_social)
    cursor.execute(insert_query, data)
    db.commit()

def registrar_resultado_usuario(nombre_usuario, red_social, puntaje, tiempo_total):
    try:
        # Insertar los datos del usuario y el resultado en la tabla de resultados (ajusta la consulta SQL según tu esquema)
        insert_query = "INSERT INTO usuarios (nombre, redes, puntaje, tiempo_respondido) VALUES (%s, %s, %s, %s)"
        data = (nombre_usuario, red_social, puntaje, tiempo_total)
        cursor.execute(insert_query, data)
        db.commit()
    except Exception as e:
        print("Error al guardar resultado en la base de datos:", str(e))

def obtener_resultados():
    db = mysql.connector.connect(
    host="localhost",
    port=3305,
    user="root",
    password="12345678",
    database="Trivia"
)
    cursor = db.cursor()
    try:
        # Verificar si la conexión y el cursor están disponibles
        if cursor is not None and db.is_connected():
            # Ejecuta una consulta para obtener los resultados
            cursor.execute("SELECT nombre, puntaje, tiempo_respondido FROM Usuarios")
            resultados = cursor.fetchall()
            db.commit()
            return resultados
        else:
            # Manejar el caso en el que no haya una conexión válida
            print("No hay una conexión válida a la base de datos.")
            return []
    except Exception as e:
        print("Error al obtener resultados:", str(e))
        return []


def cerrar_db():
    cursor.close()
    db.close()