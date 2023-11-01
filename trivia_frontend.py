import tkinter as tk
import trivia_backend
import random
from datetime import datetime


class TriviaGame:
    def __init__(self, root):
        self.root = root 
        self.root.title("Trivia Game") 
        self.usuario_id = None
        self.indice_pregunta_actual = 0
        self.preguntas = trivia_backend.get_preguntas()
        self.respuesta_correcta_actual = None  # Almacena la respuesta correcta actual
        self.puntaje = 0
        self.respondiendo = True  # Variable para rastrear si el usuario está respondiendo


        # Estilo básico
        self.root.configure(bg='#f5f5f5') 
        self.root.geometry('600x400') 

        self.crear_formulario_usuario() 

    def crear_formulario_usuario(self): 
        nombre_label = tk.Label(self.root, text="Nombre:")
        nombre_label.pack()
        self.nombre_entry = tk.Entry(self.root)
        self.nombre_entry.pack()

        instagram_label = tk.Label(self.root, text="Instagram:")
        instagram_label.pack()
        self.instagram_entry = tk.Entry(self.root)
        self.instagram_entry.pack()

        jugar_button = tk.Button(self.root, text="Jugar", command=self.comenzar_juego)
        jugar_button.pack()


    def comenzar_juego(self):
        nombre = self.nombre_entry.get() 
        instagram = self.instagram_entry.get() 

        if nombre and instagram:
            self.usuario_id = trivia_backend.create_user(nombre, instagram)
            self.cargar_pregunta() 
        else:
            error_label = tk.Label(self.root, text="Por favor, complete todos los campos.")
            error_label.pack()


    def cargar_pregunta(self):
        if self.indice_pregunta_actual < len(self.preguntas):
            pregunta_id, pregunta = self.preguntas[self.indice_pregunta_actual]
            self.respuestas_correctas = []  # Limpia la lista de respuestas correctas
            # Obtiene la lista de respuestas para la pregunta actual
            respuestas = trivia_backend.get_answers(pregunta_id) 
            # Separa las respuestas correctas e incorrectas
            respuestas_correctas = [respuesta['respuesta'] for respuesta in respuestas if respuesta['es_correcta'] == 1]
            respuestas_incorrectas = [respuesta['respuesta'] for respuesta in respuestas if respuesta['es_correcta'] == 0]
            

            self.root.title(f"Trivia Game - Pregunta {self.indice_pregunta_actual + 1}")

            # Resto del código para cargar la pregunta y las respuestas
            pregunta_label = tk.Label(self.root, text=pregunta)
            pregunta_label.pack(pady=10)

            todas_respuestas = respuestas_incorrectas
            random.shuffle(todas_respuestas)

            for respuesta in todas_respuestas:
                respuesta_button = tk.Button(self.root, text=respuesta, command=lambda r=respuesta: self.verificar_respuesta(r))
                respuesta_button.pack()

            self.indice_pregunta_actual += 1

    def verificar_respuesta(self, respuesta_usuario):
        respuesta_correcta_actual = trivia_backend.get_respuesta_correcta(self.preguntas[self.indice_pregunta_actual - 1][0])

        if respuesta_usuario == respuesta_correcta_actual:
            self.puntaje += 100
            tiempo_respuesta = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            trivia_backend.insertar_puntaje(self.usuario_id, self.preguntas[self.indice_pregunta_actual - 1][0], respuesta_usuario, tiempo_respuesta)

            if self.indice_pregunta_actual == len(self.preguntas):
                self.mostrar_puntaje_final()
            else:
                self.cargar_pregunta()

    def mostrar_puntaje_final(self):
        self.limpiar_pregunta()
        self.root.title("Trivia Game - Puntajes Finales")

        puntaje_label = tk.Label(self.root, text=f"Tu puntaje final: {self.puntaje}")
        puntaje_label.pack(pady=10)

        puntajes = trivia_backend.obtener_puntajes()
        puntajes.sort(key=lambda x: x[3])  # Ordena por tiempo

        puntajes_label = tk.Label(self.root, text="Puntajes Finales")
        puntajes_label.pack()

        puntajes_frame = tk.Frame(self.root)
        puntajes_frame.pack()

        for usuario_id, usuario_nombre, usuario_instagram, usuario_puntaje, tiempo_respuesta in puntajes:
            puntaje_texto = f"{usuario_nombre} ({usuario_instagram}): {usuario_puntaje} puntos, Tiempo: {tiempo_respuesta}"
            puntaje_entry = tk.Label(puntajes_frame, text=puntaje_texto)
            puntaje_entry.pack()
        # Botón para pasar a la siguiente pregunta o salir del juego
        if self.indice_pregunta_actual < len(self.preguntas):
            siguiente_pregunta_button = tk.Button(self.root, text="Siguiente Pregunta", command=self.cargar_pregunta)
            siguiente_pregunta_button.pack()
        else:
            salir_button = tk.Button(self.root, text="Salir del Juego", command=self.root.quit)
            salir_button.pack()



    def limpiar_pregunta(self): # Limpia la pantalla de la pregunta
        for widget in self.root.winfo_children(): # Recorre todos los widgets
            widget.destroy() # Destruye todos los widgets



if __name__ == "__main__":
    root = tk.Tk()
    juego = TriviaGame(root)
    root.mainloop()
