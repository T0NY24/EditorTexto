# Importamos las bibliotecas necesarias
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

# Definimos la clase Nodo para la lista doblemente enlazada
class Nodo:
    def __init__(self, dato):
        self.dato = dato  # El dato que almacena el nodo
        self.siguiente = self.anterior = None  # Referencias al siguiente y anterior nodo

# Definimos la clase ListaDoblementeEnlazada
class ListaDoblementeEnlazada:
    def __init__(self):
        self.cabeza = self.cola = None  # Inicializamos la cabeza y cola como None
        self.longitud = 0  # Contador de elementos en la lista

    def insertar(self, dato, posicion):
        nuevo = Nodo(dato)  # Creamos un nuevo nodo
        if not self.cabeza:  # Si la lista está vacía
            self.cabeza = self.cola = nuevo
        elif posicion == 0:  # Si insertamos al inicio
            nuevo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo
            self.cabeza = nuevo
        elif posicion >= self.longitud:  # Si insertamos al final
            self.cola.siguiente = nuevo
            nuevo.anterior = self.cola
            self.cola = nuevo
        else:  # Si insertamos en medio
            actual = self.cabeza
            for _ in range(posicion):
                actual = actual.siguiente
            nuevo.anterior = actual.anterior
            nuevo.siguiente = actual
            actual.anterior.siguiente = nuevo
            actual.anterior = nuevo
        self.longitud += 1  # Aumentamos la longitud de la lista

    def eliminar(self, posicion):
        if not self.cabeza:  # Si la lista está vacía
            return None
        if posicion == 0:  # Si eliminamos el primer elemento
            dato = self.cabeza.dato
            self.cabeza = self.cabeza.siguiente
            if self.cabeza:
                self.cabeza.anterior = None
            else:
                self.cola = None
        elif posicion >= self.longitud - 1:  # Si eliminamos el último elemento
            dato = self.cola.dato
            self.cola = self.cola.anterior
            if self.cola:
                self.cola.siguiente = None
            else:
                self.cabeza = None
        else:  # Si eliminamos un elemento en medio
            actual = self.cabeza
            for _ in range(posicion):
                actual = actual.siguiente
            dato = actual.dato
            actual.anterior.siguiente = actual.siguiente
            actual.siguiente.anterior = actual.anterior
        self.longitud -= 1  # Disminuimos la longitud de la lista
        return dato  # Devolvemos el dato eliminado

# Definimos la clase EditorTexto
class EditorTexto:
    def __init__(self):
        self.texto = ListaDoblementeEnlazada()  # Usamos una lista doblemente enlazada para el texto
        self.cursor = 0  # Posición del cursor

    def insertar(self, caracter):
        self.texto.insertar(caracter, self.cursor)  # Insertamos un carácter en la posición del cursor
        self.cursor += 1  # Movemos el cursor

    def eliminar(self):
        if self.cursor > 0:  # Si no estamos al inicio del texto
            self.cursor -= 1  # Movemos el cursor hacia atrás
            return self.texto.eliminar(self.cursor)  # Eliminamos el carácter

    def mover_cursor(self, posicion):
        # Aseguramos que el cursor esté dentro de los límites del texto
        self.cursor = max(0, min(posicion, self.texto.longitud))

    def obtener_texto(self):
        actual = self.texto.cabeza
        texto = []
        while actual:  # Recorremos la lista
            texto.append(actual.dato)  # Añadimos cada carácter a la lista
            actual = actual.siguiente
        return ''.join(texto)  # Unimos todos los caracteres en una cadena

    def establecer_texto(self, texto):
        self.texto = ListaDoblementeEnlazada()  # Creamos una nueva lista
        self.cursor = 0
        for char in texto:  # Insertamos cada carácter del texto
            self.insertar(char)

# Definimos la clase principal NotePadApp
class NotePadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bloc de Notas")  # Título de la ventana
        self.editor = EditorTexto()  # Creamos una instancia de EditorTexto
        self.setup_ui()  # Configuramos la interfaz de usuario
        self.root.bind('<Control-v>', lambda e: self.pegar())

    def setup_ui(self):
        # Configuramos el tamaño de la ventana
        self.root.rowconfigure(0, minsize=600, weight=1)
        self.root.columnconfigure(1, minsize=800, weight=1)

        # Creamos el widget de texto
        self.txt_edit = tk.Text(self.root)
        self.txt_edit.grid(row=0, column=1, sticky="nsew")
        self.txt_edit.bind('<Key>', self.on_key)  # Vinculamos el evento de teclado

        # Creamos el frame para los botones
        fr_buttons = tk.Frame(self.root, relief=tk.RAISED, bd=2)
        # Creamos los botones
        btn_abrir = tk.Button(fr_buttons, text="Abrir", command=self.abrir_archivo)
        btn_guardar = tk.Button(fr_buttons, text="Guardar Como", command=self.guardar_archivo)
        btn_deshacer = tk.Button(fr_buttons, text="Deshacer", command=self.deshacer)
        btn_rehacer = tk.Button(fr_buttons, text="Rehacer", command=self.rehacer)
        btn_pegar = tk.Button(fr_buttons, text="Pegar", command=self.pegar)

        # Posicionamos los botones
        btn_abrir.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        btn_guardar.grid(row=1, column=0, sticky="ew", padx=5)
        btn_deshacer.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        btn_rehacer.grid(row=3, column=0, sticky="ew", padx=5)
        btn_pegar.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

        # Posicionamos el frame de botones
        fr_buttons.grid(row=0, column=0, sticky="ns")

        # Inicializamos las listas para deshacer y rehacer
        self.historial = []
        self.pila_rehacer = []

    def abrir_archivo(self):
        # Abrimos un diálogo para seleccionar un archivo
        filepath = askopenfilename(filetypes=[("Archivos de Texto", "*.txt"), ("Todos los Archivos", "*.*")])
        if not filepath:
            return
        with open(filepath, "r") as input_file:
            text = input_file.read()
            self.editor.establecer_texto(text)  # Establecemos el texto en el editor
            self.actualizar_widget_texto()  # Actualizamos el widget de texto
        self.root.title(f"Bloc de Notas - {filepath}")  # Actualizamos el título de la ventana

    def guardar_archivo(self):
        # Abrimos un diálogo para guardar el archivo
        filepath = asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de Texto", "*.txt"), ("Todos los Archivos", "*.*")])
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = self.editor.obtener_texto()  # Obtenemos el texto del editor
            output_file.write(text)  # Escribimos el texto en el archivo
        self.root.title(f"Bloc de Notas - {filepath}")  # Actualizamos el título de la ventana

    def on_key(self, event):
        if event.char and ord(event.char) >= 32:  # Si es un carácter imprimible
            self.agregar_a_historial()
            index = self.txt_edit.index(tk.INSERT)
            row, col = map(int, index.split('.'))
            self.editor.mover_cursor(col)
            self.editor.insertar(event.char)  # Insertamos el carácter
        elif event.keysym == 'BackSpace':  # Si es la tecla de borrar
            self.agregar_a_historial()
            index = self.txt_edit.index(tk.INSERT)
            row, col = map(int, index.split('.'))
            if col > 0:
                self.editor.mover_cursor(col)
                self.editor.eliminar()  # Eliminamos un carácter
        self.actualizar_widget_texto()  # Actualizamos el widget de texto
        return "break"  # Evitamos que el evento se propague

    def actualizar_widget_texto(self):
        self.txt_edit.delete("1.0", tk.END)  # Borramos todo el texto
        self.txt_edit.insert(tk.END, self.editor.obtener_texto())  # Insertamos el nuevo texto

    def agregar_a_historial(self):
        self.historial.append(self.editor.obtener_texto())  # Añadimos el texto actual al historial
        self.pila_rehacer.clear()  # Limpiamos la pila de rehacer

    def deshacer(self):
        if len(self.historial) > 0:
            self.pila_rehacer.append(self.editor.obtener_texto())  # Guardamos el estado actual para rehacer
            text = self.historial.pop()  # Obtenemos el estado anterior
            self.editor.establecer_texto(text)  # Establecemos el texto anterior
            self.actualizar_widget_texto()  # Actualizamos el widget de texto

    def rehacer(self):
        if len(self.pila_rehacer) > 0:
            self.historial.append(self.editor.obtener_texto())  # Guardamos el estado actual para deshacer
            text = self.pila_rehacer.pop()  # Obtenemos el estado siguiente
            self.editor.establecer_texto(text)  # Establecemos el texto siguiente
            self.actualizar_widget_texto()  # Actualizamos el widget de texto

    def pegar(self):
        try:
            texto = self.root.clipboard_get()
            index = self.txt_edit.index(tk.INSERT)
            row, col = map(int, index.split('.'))
            self.editor.mover_cursor(col)
            for char in texto:
                self.editor.insertar(char)
            self.actualizar_widget_texto()
            self.agregar_a_historial()
        except tk.TclError:
            pass  # El portapapeles está vacío

# Creamos la ventana principal y ejecutamos la aplicación
root = tk.Tk()
app = NotePadApp(root)
root.mainloop()