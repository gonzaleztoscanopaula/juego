import tkinter as tk
from tkinter import messagebox
import time
from tkinter import ttk
import random
import threading
from tkinter import font
from tkinter import simpledialog
from PIL import Image, ImageTk
import tkinter.messagebox as msgbox
from funcionestrivia import *

class TriviaGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Trivia Game")
        self.root.attributes('-fullscreen', True)
        self.root.configure (bg="#B8AFE4")
        
        
        self.root.withdraw()

        self.nombre_usuario = ""

        self.mostrar_formulario_usuario()


    def mostrar_formulario_usuario(self):
        # Crear una nueva ventana para el formulario
        self.nombre_usuario = None  # Agrega esta línea para definir nombre_usuario como atributo de la clase
        self.red_social = None
        self.formulario_window = tk.Toplevel(self.root)
        self.formulario_window.title("Formulario de Usuario")
        self.formulario_window.attributes('-fullscreen', True)
        self.formulario_window.config (bg="#B8AFE4")


        # Etiqueta y campo de entrada para el nombre
        tk.Label(self.formulario_window, text="Nombre:", wraplength=800, font=("Comic Sans", 20), bg= "#B8AFE4", fg= "black").pack(padx=10, pady=50)
        self.nombre_usuario_entry = tk.Entry(self.formulario_window, width=40, bd=5, justify="center")
        self.nombre_usuario_entry.pack(padx=10, pady=50)

        # Etiqueta y campo de entrada para la red social
        tk.Label(self.formulario_window, text="Instagram:", wraplength=800, font=("Comic Sans", 20),  bg=  "#B8AFE4", fg= "black").pack(padx=10, pady=50)
        self.red_social_entry = tk.Entry(self.formulario_window, width=40, bd=5, justify="center" )
        self.red_social_entry.pack(padx=10, pady=50)

        # Botón para enviar el formulario
        tk.Button(self.formulario_window, text="Comencemos!", wraplength=800, font=("Arial", 30), borderwidth= 10 , bg= "#2E378A", fg= "black", command=self.iniciar_juego_desde_formulario).pack(padx=10, pady=50)

       

    def iniciar_juego_desde_formulario(self):
    # Obtener el nombre y la red social ingresados por el usuario
        nombre_usuario = self.nombre_usuario_entry.get()
        red_social = self.red_social_entry.get()

        if nombre_usuario and red_social:
        # Los datos se ingresaron, ahora guarda los datos en la base de datos
            self.nombre_usuario = nombre_usuario  # Actualiza el atributo de la clase
            self.red_social = red_social
            guardar_datos_usuario(nombre_usuario, red_social)

        # Luego, muestra la ventana principal de "Trivia Game"
            self.root.deiconify()

        # Luego, puedes mostrar la pantalla de inicio
            self.formulario_window.destroy()  # Cierra la ventana del formulario
            self.mostrar_pantalla_inicio(nombre_usuario, red_social)
        else:
        # Si no se ingresaron datos, puedes mostrar un mensaje de error o manejarlo como desees
            tk.messagebox.showerror("ERROR!!", "Necesitas loggearte para comenzar la trivia, pd: ya recorriste el ingreso para responder bien?.")

        
    def mostrar_pantalla_inicio(self, nombre_usuario, red_social):
        # Ventana de inicio
        self.frame_inicio = tk.Frame(self.root)
        self.frame_inicio.pack(fill="both", expand=True)
        self.frame_inicio.configure(bg="#6A9ACD")

        self.mi_fuente = font.Font(family="Comic Sans", size=50, weight="bold", slant="italic")
        self.etiqueta_bienvenida = tk.Label(self.frame_inicio, text="¡Bienvenido a la Trivia !", font=self.mi_fuente, bg="#6A9ACD")
        self.etiqueta_bienvenida.pack(padx=20, pady=200)

        # Cargar la imagen del botón "Play"
        img_play = Image.open("play.png")  
        img_play = img_play.resize((350, 150))  # Ajusta el tamaño de la imagen
        img_play = ImageTk.PhotoImage(img_play)

        # Crear un botón personalizado con la imagen
        boton_play = tk.Button(self.frame_inicio, image=img_play, command=self.iniciar_juego, bg="#C2AD47", borderwidth= 10)
        boton_play.image = img_play  # Mantiene una referencia a la imagen para evitar que sea recolectada por el recolector de basura
        boton_play.pack(pady=20)




    def cambiar_color(self):
        if self.etiqueta_bienvenida is not None:
            color = self.colores.pop(0)
            self.colores.append(color)
            self.etiqueta_bienvenida.config(fg=color)
            self.root.after(1000, self.cambiar_color)  # Cambiar de color cada segundo




    def iniciar_juego(self):
        # Inicia el juego
        self.frame_inicio.destroy()  # Cierra la ventana de inicio
        self.etiqueta_bienvenida = None  # Elimina la referencia a la etiqueta de bienvenida

        self.preguntas = obtener_preguntas()
        self.preguntas_seleccionadas = self.preguntas
        self.respuestas_correctas = 0

        self.pregunta_actual = 0
        self.tiempo_inicial = time.time()
        self.tiempo_transcurrido = 0

        # Etiqueta de pregunta
        self.pregunta_label = tk.Label(self.root, text="", wraplength=800, font=("Arial", 20), borderwidth= 10 , bg= "#B8AFE4", fg= "black")
        self.pregunta_label.pack(padx=20, pady=20)

        # Frame para las respuestas
        self.respuestas_frame = tk.Frame(self.root)
        self.respuestas_frame.pack(padx=20, pady=20)
        self.respuestas_frame.configure (bg= "#B8AFE4")

        self.botones_respuestas = []
        for i in range(3):
            boton = tk.Button(self.respuestas_frame, text="", font=("Arial", 16), borderwidth= 10 , bg= "#C6E0A3", fg= "black")
            boton.pack(pady=10)
            boton.config(command=lambda btn=boton: self.verificar_respuesta(btn.cget("text")))
            self.botones_respuestas.append(boton)

        # Etiqueta de feedback
        self.feedback_label = tk.Label(self.root, text="", font=("Arial", 16), fg="#C6E0A3",bg= "#B8AFE4")
        self.feedback_label.pack(pady=20)

        # Etiqueta de tiempo
        self.tiempo_label = tk.Label(self.root, text="Tiempo: 0 segundos", font=("Arial", 16), bg= "#B8AFE4", fg= "black")
        self.tiempo_label.pack(pady=20)

        # Hilo para el tiempo
        self.thread = threading.Thread(target=self.actualizar_tiempo)
        self.thread.daemon = True
        self.thread.start()

        self.actualizar_pregunta()

        # Botón para cerrar con icono de puerta
        img = Image.open("salir.png")  # Reemplaza "door_icon.png" con el nombre de tu archivo de imagen
        img = img.resize((50, 50))
        img = ImageTk.PhotoImage(img)
        cerrar_boton = tk.Button(self.root, image=img, command=self.cerrar_ventana)
        cerrar_boton.image = img
        cerrar_boton.pack(side="right", padx=20, pady=20)

        # Botón "Siguiente"
        self.boton_siguiente = tk.Button(self.root, text="Siguiente", font=("Arial", 16), state="disabled", command=self.siguiente_pregunta)
        self.boton_siguiente.pack(side="right", padx=20, pady=20)

    def cerrar_ventana(self):
        self.root.destroy()  # Cierra la ventana


    def actualizar_tiempo(self):
        while True:
            self.tiempo_transcurrido += 1
            tiempo_formateado = f"Tiempo: {self.tiempo_transcurrido} segundos"
            self.tiempo_label.config(text=tiempo_formateado)
            time.sleep(1)

    def verificar_respuesta(self, respuesta):
        # Verifica la respuesta
        if respuesta == self.preguntas_seleccionadas[self.pregunta_actual][1]:
            self.respuestas_correctas += 1
            self.feedback_label.config(text="¡Respuesta correcta!", fg="#C6E0A3")
        else:
            self.feedback_label.config(text="Respuesta incorrecta", fg="red")

        # Habilita el botón "Siguiente"
        self.boton_siguiente.config(state="active")

        # Deshabilita los botones de respuesta
        for boton in self.botones_respuestas:
            boton.config(state="disabled")

    def siguiente_pregunta(self):
    # Realiza acciones para pasar a la siguiente pregunta
        if self.pregunta_actual < len(self.preguntas_seleccionadas) - 1:
            self.pregunta_actual += 1
            self.actualizar_pregunta()
        else:
        # Se han agotado las preguntas
            self.feedback_label.config(text=f"Juego terminado. Preguntas correctas: {self.respuestas_correctas}")
            self.finalizar_juego()  # Llama al método para mostrar los resultados al finalizar el juego


        # Deshabilita el botón "Siguiente"
        self.boton_siguiente.config(state="disabled")

        # Habilita los botones de respuesta para la nueva pregunta
        for boton in self.botones_respuestas:
            boton.config(state="active")

    def generar_respuestas(self):
        # Obtener la pregunta actual
        pregunta, respuesta_correcta = self.preguntas_seleccionadas[self.pregunta_actual]

        # Generar una lista de respuestas que incluye la respuesta correcta y dos respuestas incorrectas
        respuestas = [respuesta_correcta]
        while len(respuestas) < 3:
            respuesta_incorrecta = random.choice(self.preguntas)[1]
            if respuesta_incorrecta not in respuestas:
                respuestas.append(respuesta_incorrecta)

        # Mezclar las respuestas para que no estén en orden
        random.shuffle(respuestas)
        return respuestas

    def actualizar_pregunta(self):
        self.respuestas = self.generar_respuestas()
        pregunta, _ = self.preguntas_seleccionadas[self.pregunta_actual]
        self.pregunta_label.config(text=pregunta)
        for i, boton in enumerate(self.botones_respuestas):
            # Usa una función lambda para pasar la respuesta como argumento
            boton.config(text=self.respuestas[i], command=lambda respuesta=self.respuestas[i]: self.verificar_respuesta(respuesta))

    
    def finalizar_juego(self):
        tiempo_total = round(time.time() - self.tiempo_inicial, 2)
        puntaje = calcular_puntaje(self.respuestas_correctas)

        registrar_resultado_usuario(self.nombre_usuario, self.red_social, puntaje, tiempo_total)
        cerrar_db()

        mensaje = f"Juego terminado\nTiempo total: {tiempo_total} segundos\nPuntaje: {puntaje} puntos"
        messagebox.showinfo("Resultado", mensaje)

        # Llama al método para mostrar los resultados al finalizar el juego
        self.mostrar_resultados()

    def mostrar_resultados(self):
    # Crea una nueva ventana emergente para mostrar los resultados
        resultados_window = tk.Toplevel(self.root)
        resultados_window.title("Resultados del Juego")

    # Crea un Treeview (tabla) para mostrar los resultados con scrollbar
        tree = ttk.Treeview(resultados_window, columns=("Nombre", "Puntaje", "Tiempo"))
        tree.heading("#1", text="Nombre")
        tree.heading("#2", text="Puntaje")
        tree.heading("#3", text="Tiempo")

    # Obtiene los resultados de la base de datos (asegúrate de que esta función funcione correctamente)
        resultados = obtener_resultados()

    # Agrega los resultados de los jugadores a la tabla
        for resultado in resultados:
            tree.insert("", "end", values=resultado)

        tree.pack()


def main():
    root = tk.Tk()
    app = TriviaGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()