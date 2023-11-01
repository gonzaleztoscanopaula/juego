import mysql.connector
from datetime import datetime

# Función para conectar a la base de datos
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        port=3305,  # Asegúrate de usar el puerto correcto
        password="12345678",  # Cambia la contraseña según tu configuración
        database="trivia"
    )

# Función para crear un nuevo usuario
def create_user(nombre, instagram):
    try:
        db = connect_to_db()
        cursor = db.cursor()

        # Consulta SQL para insertar un nuevo usuario
        insert_query = "INSERT INTO usuarios (nombre, instagram) VALUES (%s, %s)"
        cursor.execute(insert_query, (nombre, instagram))
        db.commit()

        return cursor.lastrowid  # Obtén el ID del usuario recién creado
    except mysql.connector.Error as err:
        print(f"Error al crear usuario: {err}")
    finally:
        cursor.close()
        db.close()


# Función para obtener respuestas para una pregunta específica
def get_answers(pregunta_id):
    try:
        db = connect_to_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT respuesta, es_correcta FROM respuestas WHERE pregunta_id = %s", (pregunta_id,))
        answers = cursor.fetchall()

        return answers
    except mysql.connector.Error as err:
        print(f"Error al obtener respuestas: {err}")
    finally:
        cursor.close()
        db.close()

# Función para obtener la lista de preguntas
def get_preguntas():
    try:
        db = connect_to_db()
        cursor = db.cursor()

        cursor.execute("SELECT id, pregunta FROM preguntas")
        preguntas = cursor.fetchall()

        cursor.close()  # Cerrar el cursor después de leer los resultados

        return preguntas
    except mysql.connector.Error as err:
        print(f"Error al obtener preguntas: {err}")
    finally:
        db.close()

# Función para obtener la respuesta correcta para una pregunta
def get_respuesta_correcta(pregunta_id):
    try:
        db = connect_to_db()
        cursor = db.cursor()

        cursor.execute("SELECT respuesta FROM respuestas WHERE pregunta_id = %s AND es_correcta = 1", (pregunta_id,))
        respuesta_correcta = cursor.fetchone()
        if respuesta_correcta:
            return respuesta_correcta[0]
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Error al obtener respuesta correcta: {err}")
    finally:
        cursor.close()
        db.close()

# Función para obtener respuestas incorrectas para una pregunta
def get_respuestas_incorrectas(pregunta_id):
    try:
        db = connect_to_db()
        cursor = db.cursor()

        cursor.execute("SELECT respuesta FROM respuestas WHERE pregunta_id = %s AND es_correcta = 0", (pregunta_id,))
        respuestas_incorrectas = [row[0] for row in cursor.fetchall()]

        return respuestas_incorrectas
    except mysql.connector.Error as err:
        print(f"Error al obtener respuestas incorrectas: {err}")
    finally:
        cursor.close()
        db.close()

# Función para insertar un puntaje en la base de datos
def insertar_puntaje(usuario_id, pregunta_id, respuesta_id, tiempo_respondido):
    try:
        db = connect_to_db()
        cursor = db.cursor()

        # Consulta SQL para insertar un puntaje
        insert_query = "INSERT INTO respuestas_usuario (usuario_id, pregunta_id, respuesta_id, tiempo_respondido) " \
                       "VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (usuario_id, pregunta_id, respuesta_id, tiempo_respondido))
        db.commit()
    except mysql.connector.Error as err:
        print(f"Error al insertar puntaje: {err}")
    finally:
        cursor.close()
        db.close()

# Función para obtener la grilla de puntajes
def obtener_puntajes():
    try:
        db = connect_to_db()
        cursor = db.cursor()

        cursor.execute("SELECT usuarios.id, usuarios.nombre, usuarios.instagram, SUM(respuestas_usuario.respuesta_id), MIN(respuestas_usuario.tiempo_respondido) FROM usuarios INNER JOIN respuestas_usuario ON usuarios.id = respuestas_usuario.usuario_id GROUP BY usuarios.id, usuarios.nombre, usuarios.instagram ORDER BY SUM(respuestas_usuario.respuesta_id) DESC, MIN(respuestas_usuario.tiempo_respondido) ASC")

        puntajes = cursor.fetchall()

        cursor.close()  # Cerrar el cursor después de leer los resultados

        return puntajes
    except mysql.connector.Error as err:
        print(f"Error al obtener puntajes: {err}")
    finally:
        db.close()

