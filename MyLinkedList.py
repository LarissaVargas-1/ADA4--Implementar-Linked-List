class Nodo:
    """Representa un nodo con los campos INFO y LIGA según el algoritmo."""
    def __init__(self, info):
        self.INFO = info  # Campo de datos
        self.LIGA = None  # Puntero al siguiente nodo

class MyLinkedList:
    def __init__(self):
        self.cabeza = None  # Puntero P que apunta al inicio de la lista

    def crea_inicio_algoritmo(self):
        """
        Implementación textual del Algoritmo 5.1 (Crea_inicio):
        Agrega cada nuevo nodo al inicio de la lista[cite: 2].
        """
        # 1. Crear (P) y 2. Leer P^.INFO
        info_inicial = input("Ingrese la información (INFO) para el primer nodo: ")
        self.cabeza = Nodo(info_inicial)
        
        # 3. Hacer P^.LIGA <- NIL
        self.cabeza.LIGA = None
        
        # 4. Escribir y 5. Leer RES
        res = int(input("¿Desea ingresar más nodos a la lista? Sí: 1, No: 0: "))
        
        # 6. Mientras (RES = 1) Repetir
        while res == 1:
            # Crear (Q) y leer Q^.INFO
            q = Nodo(None)
            q.INFO = input("Ingrese la información (INFO) para el nuevo nodo: ")
            
            # Hacer Q^.LIGA <- P y P <- Q (Se inserta al inicio)
            q.LIGA = self.cabeza
            self.cabeza = q
            
            # Escribir y leer RES
            res = int(input("¿Desea ingresar más nodos a la lista? Sí: 1, No: 0: "))
        
        # 7. Fin del ciclo

    def cargar_datos_ejemplo(self, lista_datos):
        """
        Simula la inserción con los datos del ejemplo del libro: 
        García, Pérez, López y Santos[cite: 2].
        Como se insertan al inicio, el orden final quedará invertido[cite: 2].
        """
        if not lista_datos:
            return

        # Paso 1, 2 y 3: Primer nodo
        self.cabeza = Nodo(lista_datos[0])
        self.cabeza.LIGA = None

        # Pasos 6: Inserción de los elementos restantes al inicio
        for dato in lista_datos[1:]:
            q = Nodo(dato)
            q.LIGA = self.cabeza
            self.cabeza = q  # P pasa a apuntar a Q

    def mostrar(self):
        """Imprime la lista enlazada visualmente hasta NIL."""
        actual = self.cabeza
        elementos = []
        while actual:
            elementos.append(str(actual.INFO))
            actual = actual.LIGA
        print(" -> ".join(elementos) + " -> NIL")


# --- Demostración ---
if __name__ == "__main__":
    print("=== 1. Demostración con los datos del ejemplo (García, Pérez, López, Santos) ===")
    print("Nota: Al agregarse cada elemento al inicio, la lista resultante queda en orden inverso.")
    
    ejemplo_datos = ["García", "Pérez", "López", "Santos"]
    lista = MyLinkedList()
    lista.cargar_datos_ejemplo(ejemplo_datos)
    
    print("Resultado:")
    lista.mostrar()
    
    print("\n=== 2. Ejecución interactiva  ===")
    lista_interactiva = MyLinkedList()
    lista_interactiva.crea_inicio_algoritmo()
    
    print("\nLista interactiva resultante:")
    lista_interactiva.mostrar()