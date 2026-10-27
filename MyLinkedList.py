import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ==========================================
# PALETA ESMERALDA / VERDE OSCURO
# ==========================================

FONDO = "#09120E"
PANEL = "#11221A"
PANEL_CLARO = "#1B382B"
ESMERALDA = "#059669"
ESMERALDA_OSCURO = "#047857"
MENTA = "#6EE7B7"
MENTA_CLARO = "#0F2A1E"
MENTA_SELECCION = "#A7F3D0"
TEXTO = "#ECFDF5"
TEXTO_SECUNDARIO = "#A7F3D0"
ROJO = "#E11D48"


# ==========================================
# CLASE NODO
# ==========================================

class Nodo:
    __slots__ = ('id', 'dato', 'liga')
    
    def __init__(self, identificador, dato):
        self.id = identificador
        self.dato = dato
        self.liga = None


# ==========================================
# CLASE LISTA ENLAZADA
# ==========================================

class ListaEnlazada:
    def __init__(self):
        self.inicio = None
        self.nodos = {}
        self.siguiente_id = 1

    def nuevo(self, dato):
        nodo = Nodo(self.siguiente_id, dato)
        self.nodos[nodo.id] = nodo
        self.siguiente_id += 1
        return nodo

    def recorrido(self):
        resultado = []
        actual = self.inicio
        vistos = set()

        while actual and actual.id not in vistos:
            vistos.add(actual.id)
            resultado.append(actual)
            actual = actual.liga

        return resultado

    def hay_ciclo(self):
        actual = self.inicio
        vistos = set()
        while actual:
            if actual.id in vistos:
                return True
            vistos.add(actual.id)
            actual = actual.liga
        return False

    def cantidad(self):
        return len(self.recorrido())

    def insertar_inicio(self, dato):
        nuevo = self.nuevo(dato)
        nuevo.liga = self.inicio
        self.inicio = nuevo
        return nuevo

    def insertar_final(self, dato):
        if not self.inicio:
            return self.insertar_inicio(dato)

        if self.hay_ciclo():
            raise ValueError(
                "La lista tiene un ciclo. Modifica la conexión antes de insertar al final."
            )

        nuevo = self.nuevo(dato)
        self.recorrido()[-1].liga = nuevo
        return nuevo

    def insertar_posicion(self, dato, posicion):
        ruta = self.recorrido()

        if not 1 <= posicion <= len(ruta) + 1:
            raise ValueError(f"Posiciones válidas para insertar: 1 a {len(ruta) + 1}.")

        if posicion == 1:
            return self.insertar_inicio(dato)

        if posicion == len(ruta) + 1 and self.hay_ciclo():
            raise ValueError("No se puede insertar al final de una lista con ciclo.")

        previo = ruta[posicion - 2]
        nuevo = self.nuevo(dato)
        nuevo.liga = previo.liga
        previo.liga = nuevo
        return nuevo

    def buscar(self, dato):
        return [(i, n) for i, n in enumerate(self.recorrido(), 1) if n.dato == dato]

    def eliminar_posicion(self, posicion):
        ruta = self.recorrido()

        if not 1 <= posicion <= len(ruta):
            raise ValueError(f"Posiciones válidas para eliminar: 1 a {len(ruta)}.")

        nodo = ruta[posicion - 1]
        sucesor = nodo.liga if nodo.liga is not nodo else None

        if self.inicio is nodo:
            self.inicio = sucesor

        for otro in self.nodos.values():
            if otro is not nodo and otro.liga is nodo:
                otro.liga = None if sucesor is otro else sucesor

        del self.nodos[nodo.id]
        nodo.liga = None
        return nodo

    def invertir(self):
        if self.hay_ciclo():
            raise ValueError("No se puede invertir una lista que contiene ciclos.")
        
        ruta = self.recorrido()
        if len(ruta) <= 1:
            return  

        anterior = None
        actual = self.inicio
        while actual:
            siguiente_nodo = actual.liga
            actual.liga = anterior
            anterior = actual
            actual = siguiente_nodo
            
        self.inicio = anterior

    def conectar(self, origen_id, destino_id):
        origen = self.nodos.get(origen_id)
        destino = self.nodos.get(destino_id)

        if not origen:
            raise ValueError(f"No existe el nodo de origen con ID {origen_id}.")
        if not destino:
            raise ValueError(f"No existe el nodo de destino con ID {destino_id}.")
        if origen is destino:
            raise ValueError("No se permite que un nodo apunte a sí mismo.")

        origen.liga = destino
        return origen, destino

    def desconectar(self, origen_id):
        origen = self.nodos.get(origen_id)
        if not origen:
            raise ValueError(f"No existe el nodo con ID {origen_id}.")
        origen.liga = None
        return origen

    def limpiar(self):
        self.inicio = None
        self.nodos.clear()
        self.siguiente_id = 1


# ==========================================
# INTERFAZ GRÁFICA OPTIMIZADA
# ==========================================

class Aplicacion:
    def __init__(self, ventana):
        self.ventana = ventana
        self.lista = ListaEnlazada()
        self.resaltados = set()
        self.registros = []
        self.ventana_historial = None
        self.lista_historial = None

        ventana.title("LinkedList")
        ventana.geometry("1210x770")
        ventana.minsize(870, 620)
        ventana.configure(bg=FONDO)

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("TEntry", fieldbackground=MENTA_CLARO, foreground=TEXTO, padding=5)
        estilo.configure("TCombobox", fieldbackground=MENTA_CLARO, foreground=TEXTO, padding=5)

        self.construir()
        self.registrar("INICIO", "Aplicación iniciada")
        self.actualizar()

    def boton(self, padre, texto, accion, color=ESMERALDA):
        return tk.Button(
            padre, text=texto, command=accion, bg=color, fg="white",
            activebackground=ESMERALDA_OSCURO, activeforeground="white",
            font=("Segoe UI", 9, "bold"), relief="flat", padx=10, pady=8, cursor="hand2"
        )

    def etiqueta(self, padre, texto, fila, columna):
        tk.Label(padre, text=texto, bg=PANEL, fg=TEXTO, font=("Segoe UI", 10)).grid(row=fila, column=columna, padx=5, sticky="w")

    def construir(self):
        cabecera = tk.Frame(self.ventana, bg=FONDO, padx=18, pady=13)
        cabecera.pack(fill="x")

        tk.Label(cabecera, text="⛓ LinkedList Studio", fg=MENTA, bg=FONDO, font=("Segoe UI", 23, "bold")).pack(side="left")
        self.boton(cabecera, "Invertir lista", self.accion_invertir, "#065F46").pack(side="right", padx=5)
        self.boton(cabecera, "Historial separado", self.abrir_historial, ESMERALDA_OSCURO).pack(side="right")

        # Panel de Operaciones
        panel = tk.Frame(self.ventana, bg=PANEL, padx=12, pady=10)
        panel.pack(fill="x", padx=14, pady=6)

        self.etiqueta(panel, "Dato", 0, 0)
        self.etiqueta(panel, "Insertar", 0, 1)
        self.etiqueta(panel, "Posición", 0, 2)

        self.entrada_dato = ttk.Entry(panel, width=14)
        self.entrada_dato.grid(row=1, column=0, padx=5)

        self.operacion = ttk.Combobox(panel, width=17, state="readonly", values=["Al inicio", "Al final", "En una posición"])
        self.operacion.current(0)
        self.operacion.grid(row=1, column=1, padx=5)

        self.entrada_posicion = ttk.Entry(panel, width=10)
        self.entrada_posicion.grid(row=1, column=2, padx=5)

        self.boton(panel, "Insertar", self.insertar).grid(row=1, column=3, padx=4)
        self.boton(panel, "Buscar dato", self.buscar, "#047857").grid(row=1, column=4, padx=4)
        self.boton(panel, "Eliminar posición", self.eliminar, ROJO).grid(row=1, column=5, padx=4)
        self.boton(panel, "Limpiar", self.limpiar, PANEL_CLARO).grid(row=1, column=6, padx=4)

        self.ayuda = tk.Label(panel, text="", bg=PANEL, fg=TEXTO_SECUNDARIO, font=("Segoe UI", 9))
        self.ayuda.grid(row=2, column=0, columnspan=7, sticky="w", pady=(9, 0))
        self.operacion.bind("<<ComboboxSelected>>", lambda _: self.actualizar_ayuda())

        # Panel de Conexiones
        links = tk.LabelFrame(self.ventana, text="Conexiones: reemplazar la secuencia", bg=PANEL, fg=MENTA, padx=12, pady=9, font=("Segoe UI", 11, "bold"))
        links.pack(fill="x", padx=14, pady=8)

        self.etiqueta(links, "ID origen", 0, 0)
        self.origen = ttk.Entry(links, width=9)
        self.origen.grid(row=0, column=1, padx=5)

        self.etiqueta(links, "ID destino", 0, 2)
        self.destino = ttk.Entry(links, width=9)
        self.destino.grid(row=0, column=3, padx=5)

        self.boton(links, "Conectar / sustituir", self.conectar).grid(row=0, column=4, padx=5)
        self.boton(links, "Quitar conexión del origen", self.desconectar, PANEL_CLARO).grid(row=0, column=5, padx=5)

        tk.Label(links, text="Usa los ID sobre cada nodo. Dos nodos pueden apuntar al mismo destino.", bg=PANEL, fg=TEXTO_SECUNDARIO, font=("Segoe UI", 9)).grid(row=1, column=0, columnspan=6, sticky="w", pady=(8, 0))

        # Área de Visualización (Canvas)
        tk.Label(self.ventana, text="Vista de los nodos (las flechas son las ligas reales)", bg=FONDO, fg=TEXTO, font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=14, pady=(8, 5))

        lienzo = tk.Frame(self.ventana, bg=FONDO)
        lienzo.pack(fill="both", expand=True, padx=14, pady=4)

        self.canvas = tk.Canvas(lienzo, bg=MENTA_CLARO, highlightthickness=0)
        horizontal = ttk.Scrollbar(lienzo, orient="horizontal", command=self.canvas.xview)
        vertical = ttk.Scrollbar(lienzo, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=horizontal.set, yscrollcommand=vertical.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        horizontal.grid(row=1, column=0, sticky="ew")
        vertical.grid(row=0, column=1, sticky="ns")
        lienzo.grid_rowconfigure(0, weight=1)
        lienzo.grid_columnconfigure(0, weight=1)

        self.estado = tk.Label(self.ventana, bg=FONDO, fg=MENTA, font=("Segoe UI", 10, "bold"), anchor="w")
        self.estado.pack(fill="x", padx=14, pady=(2, 10))

    def registrar(self, accion, detalle):
        registro = f"[{datetime.now():%H:%M:%S}] {accion}: {detalle}"
        self.registros.append(registro)
        if self.ventana_historial and self.ventana_historial.winfo_exists():
            self.lista_historial.insert(tk.END, registro)
            self.lista_historial.see(tk.END)

    def registrar_extremos(self):
        ruta = self.lista.recorrido()
        if not ruta:
            self.registrar("ESTADO", "Sin nodos alcanzables")
        else:
            self.registrar("EXTREMOS", f"Primero={ruta[0].dato}; último visible={ruta[-1].dato}")

    def abrir_historial(self):
        if self.ventana_historial and self.ventana_historial.winfo_exists():
            self.ventana_historial.lift()
            return

        v = tk.Toplevel(self.ventana)
        self.ventana_historial = v
        v.title("Historial | LinkedList Studio")
        v.geometry("820x440")
        v.configure(bg=FONDO)

        tk.Label(v, text="Historial de operaciones", bg=FONDO, fg=MENTA, font=("Segoe UI", 19, "bold")).pack(anchor="w", padx=15, pady=12)

        marco = tk.Frame(v, bg=PANEL)
        marco.pack(fill="both", expand=True, padx=15)

        self.lista_historial = tk.Listbox(marco, bg=PANEL, fg=TEXTO, font=("Consolas", 10), relief="flat", selectbackground=ESMERALDA)
        self.lista_historial.pack(side="left", fill="both", expand=True)

        sb = ttk.Scrollbar(marco, command=self.lista_historial.yview)
        sb.pack(side="right", fill="y")
        self.lista_historial.configure(yscrollcommand=sb.set)

        for registro in self.registros:
            self.lista_historial.insert(tk.END, registro)
        self.lista_historial.see(tk.END)

        pie = tk.Frame(v, bg=FONDO)
        pie.pack(fill="x", padx=15, pady=12)
        self.boton(pie, "Borrar historial", self.borrar_historial, ROJO).pack(side="left")
        self.boton(pie, "Cerrar", v.destroy, ESMERALDA_OSCURO).pack(side="right")

    def borrar_historial(self):
        self.registros.clear()
        if self.ventana_historial and self.ventana_historial.winfo_exists():
            self.lista_historial.delete(0, tk.END)
        self.registrar("HISTORIAL", "Se borraron los registros anteriores")

    def leer_entero(self, entrada, nombre):
        valor = entrada.get().strip()
        if not valor:
            raise ValueError(f"Escribe {nombre}.")
        try:
            return int(valor)
        except ValueError:
            raise ValueError(f"{nombre.capitalize()} debe ser un número entero.")

    def insertar(self):
        try:
            dato = self.leer_entero(self.entrada_dato, "un dato")
            modo = self.operacion.get()

            if modo == "Al inicio":
                nodo = self.lista.insertar_inicio(dato)
            elif modo == "Al final":
                nodo = self.lista.insertar_final(dato)
            else:
                posicion = self.leer_entero(self.entrada_posicion, "una posición")
                nodo = self.lista.insertar_posicion(dato, posicion)

            self.resaltados = {nodo.id}
            self.registrar("INSERCIÓN", f"Dato={dato}, ID={nodo.id}, modo={modo}")
            self.registrar_extremos()
            self.entrada_dato.delete(0, tk.END)
            self.actualizar()
        except ValueError as error:
            messagebox.showerror("No se pudo insertar", str(error))

    def buscar(self):
        try:
            dato = self.leer_entero(self.entrada_dato, "un dato")
            resultados = self.lista.buscar(dato)
            self.resaltados = {n.id for _, n in resultados}

            if resultados:
                posiciones = ", ".join(str(p) for p, _ in resultados)
                self.registrar("BÚSQUEDA", f"Dato={dato}, posiciones={posiciones}")
                messagebox.showinfo("Búsqueda", f"{dato} aparece en las posiciones: {posiciones}.")
            else:
                self.registrar("BÚSQUEDA", f"Dato={dato}, no encontrado desde INICIO")
                messagebox.showinfo("Búsqueda", f"No se encontró {dato} desde INICIO.")

            self.actualizar()
        except ValueError as error:
            messagebox.showerror("Búsqueda", str(error))

    def eliminar(self):
        try:
            posicion = self.leer_entero(self.entrada_posicion, "una posición")
            nodo = self.lista.eliminar_posicion(posicion)
            self.resaltados = set()
            self.registrar("ELIMINACIÓN", f"Posición={posicion}, dato eliminado={nodo.dato}")
            self.registrar_extremos()
            self.entrada_posicion.delete(0, tk.END)
            self.actualizar()
        except ValueError as error:
            messagebox.showerror("No se pudo eliminar", str(error))

    def accion_invertir(self):
        try:
            self.lista.invertir()
            self.resaltados = set()
            self.registrar("INVERTIR", "Se invirtió el orden de los nodos de la lista")
            self.registrar_extremos()
            self.actualizar()
        except ValueError as error:
            messagebox.showerror("No se pudo invertir", str(error))

    def conectar(self):
        try:
            origen_id = self.leer_entero(self.origen, "un ID de origen")
            destino_id = self.leer_entero(self.destino, "un ID de destino")
            self.lista.conectar(origen_id, destino_id)
            self.resaltados = {origen_id, destino_id}
            self.registrar("CONEXIÓN", f"Origen ID {origen_id} apunta a ID {destino_id}")
            self.registrar_extremos()
            self.origen.delete(0, tk.END)
            self.destino.delete(0, tk.END)
            self.actualizar()
        except ValueError as error:
            messagebox.showerror("No se pudo conectar", str(error))

    def desconectar(self):
        try:
            origen_id = self.leer_entero(self.origen, "un ID de origen")
            self.lista.desconectar(origen_id)
            self.resaltados = {origen_id}
            self.registrar("DESCONEXIÓN", f"Se quitó la liga del ID {origen_id}")
            self.registrar_extremos()
            self.origen.delete(0, tk.END)
            self.actualizar()
        except ValueError as error:
            messagebox.showerror("No se pudo desconectar", str(error))

    def limpiar(self):
        self.lista.limpiar()
        self.resaltados.clear()
        self.registrar("LIMPIEZA", "Se vació la lista")
        self.actualizar()

    def actualizar_ayuda(self):
        modo = self.operacion.get()
        textos = {
            "Al inicio": "Inserta un nodo nuevo al comienzo de la lista.",
            "Al final": "Inserta un nodo nuevo al final (requiere lista sin ciclos).",
            "En una posición": "Inserta en la posición indicada (1 = inicio)."
        }
        self.ayuda.config(text=textos.get(modo, ""))

    def actualizar(self):
        self.actualizar_ayuda()
        self.canvas.delete("all")

        ruta = self.lista.recorrido()
        total_memoria = len(self.lista.nodos)
        hay_ciclo = self.lista.hay_ciclo()

        if hay_ciclo:
            self.estado.config(text=f"⚠️ CICLO DETECTADO | Nodos visibles: {len(ruta)} | Total en memoria: {total_memoria}", fg=ROJO)
        else:
            self.estado.config(text=f"✨ Lista normal | Elementos: {len(ruta)} | Total en memoria: {total_memoria}", fg=MENTA)

        if not self.lista.inicio:
            self.canvas.create_text(40, 40, anchor="nw", text="La lista está vacía. Agrega elementos arriba.", fill="#4B5563", font=("Segoe UI", 11, "italic"))
            self.canvas.config(scrollregion=(0, 0, 800, 200))
            return

        x, y, ancho, alto, espacio = 40, 50, 130, 80, 60
        self.canvas.config(scrollregion=(0, 0, x + (len(ruta) * (ancho + espacio)) + 100, 250))

        for nodo in ruta:
            color_fondo = ESMERALDA if nodo.id in self.resaltados else PANEL
            color_borde = MENTA if nodo.id not in self.resaltados else MENTA_SELECCION

            self.canvas.create_rectangle(x, y, x + ancho, y + alto, fill=color_fondo, outline=color_borde, width=2)
            self.canvas.create_text(x + 10, y + 20, anchor="w", text=f"ID: {nodo.id}", fill=TEXTO_SECUNDARIO, font=("Segoe UI", 9, "bold"))
            self.canvas.create_text(x + 10, y + 50, anchor="w", text=f"Dato: {nodo.dato}", fill=TEXTO, font=("Segoe UI", 11, "bold"))

            sig_x, sig_y, fin_x = x + ancho, y + (alto / 2), x + ancho + espacio
            if nodo.liga:
                self.canvas.create_line(sig_x, sig_y, fin_x, sig_y, fill=ESMERALDA_OSCURO, width=3, arrow=tk.LAST, arrowshape=(10, 12, 5))
            else:
                self.canvas.create_line(sig_x, sig_y, fin_x, sig_y, fill=ROJO, width=2, arrow=tk.LAST)
                self.canvas.create_text(fin_x - 20, sig_y - 15, text="NIL", fill=ROJO, font=("Segoe UI", 9, "bold"))

            x += ancho + espacio


if __name__ == "__main__":
    ventana = tk.Tk()
    app = Aplicacion(ventana)
    ventana.mainloop()
