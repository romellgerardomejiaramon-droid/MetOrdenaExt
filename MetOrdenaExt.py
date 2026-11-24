
import tkinter as tk
from tkinter import ttk, messagebox
import re
import unicodedata


class AplicacionOrdenamiento:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Metodos de Ordenamiento")
        self.ventana.geometry("1200x780")
        self.ventana.minsize(950, 650)

        try:
            self.ventana.state("zoomed")
        except tk.TclError:
            pass

        self.ventana.configure(bg="#eef2f7")
        self.metodo = ""
        self.entradas_listas = []

        self.ejemplos = {
            "Intercalacion": [
                {
                    "nombre": "Ejemplo 1 - Numeros",
                    "listas": [
                        "8, 3, 12, 5",
                        "2, 10, 6, 15"
                    ]
                },
                {
                    "nombre": "Ejemplo 2 - Palabras",
                    "listas": [
                        "pera, manzana, uva, fresa",
                        "naranja, kiwi, sandia, melon"
                    ]
                },
                {
                    "nombre": "Ejemplo 3 - Nombres con valores",
                    "listas": [
                        "Ana=15, Luis=8, Pedro=20",
                        "Maria=12, Carlos=5, Sofia=18"
                    ]
                }
            ],
            "Mezcla Directa": [
                {
                    "nombre": "Ejemplo 1 - Numeros",
                    "listas": [
                        "38, 15, 27, 9, 42, 11, 5, 30"
                    ]
                },
                {
                    "nombre": "Ejemplo 2 - Tiempos",
                    "listas": [
                        "01:25, 00:48, 02:10, 00:35, 01:05"
                    ]
                },
                {
                    "nombre": "Ejemplo 3 - Palabras",
                    "listas": [
                        "rojo, azul, verde, amarillo, negro, blanco"
                    ]
                }
            ],
            "Mezcla Equilibrada": [
                {
                    "nombre": "Ejemplo 1 - Numeros",
                    "listas": [
                        "45, 12, 36, 8, 25, 19, 50, 3"
                    ]
                },
                {
                    "nombre": "Ejemplo 2 - Decimales",
                    "listas": [
                        "9.5, 2.3, 7.8, 1.4, 5.6, 3.2"
                    ]
                },
                {
                    "nombre": "Ejemplo 3 - Palabras",
                    "listas": [
                        "computadora, teclado, pantalla, mouse, impresora"
                    ]
                }
            ]
        }

        self.crear_encabezado()

        self.contenedor = tk.Frame(
            self.ventana,
            bg="#eef2f7"
        )
        self.contenedor.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=18
        )

        self.mostrar_menu_principal()

    # --------------------------------------------------
    # INTERFAZ GENERAL
    # --------------------------------------------------

    def crear_encabezado(self):

        encabezado = tk.Frame(
            self.ventana,
            bg="#172554",
            height=75
        )
        encabezado.pack(fill="x")
        encabezado.pack_propagate(False)

        tk.Label(
            encabezado,
            text="METODOS DE ORDENAMIENTO",
            font=("Arial", 22, "bold"),
            bg="#172554",
            fg="white"
        ).pack(expand=True)

    def limpiar_pantalla(self):

        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def crear_titulo(self, titulo, descripcion=""):

        tk.Label(
            self.contenedor,
            text=titulo,
            font=("Arial", 21, "bold"),
            bg="#eef2f7",
            fg="#172554"
        ).pack(pady=(10, 5))

        if descripcion:
            tk.Label(
                self.contenedor,
                text=descripcion,
                font=("Arial", 11),
                bg="#eef2f7",
                fg="#475569"
            ).pack(pady=(0, 15))

    def crear_boton(
        self,
        padre,
        texto,
        comando,
        color="#2563eb"
    ):

        return tk.Button(
            padre,
            text=texto,
            command=comando,
            font=("Arial", 10, "bold"),
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=11
        )

    # --------------------------------------------------
    # MENU PRINCIPAL
    # --------------------------------------------------

    def mostrar_menu_principal(self):

        self.limpiar_pantalla()

        self.crear_titulo(
            "MENU PRINCIPAL",
            "Selecciona el metodo de ordenamiento que deseas utilizar."
        )

        tarjeta = tk.Frame(
            self.contenedor,
            bg="white",
            padx=35,
            pady=25
        )
        tarjeta.pack(
            fill="both",
            expand=True,
            padx=100,
            pady=15
        )

        tk.Label(
            tarjeta,
            text="Selecciona una opcion",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#172554"
        ).pack(pady=(10, 25))

        opciones = [
            ("1. INTERCALACION", "Intercalacion"),
            ("2. MEZCLA DIRECTA", "Mezcla Directa"),
            ("3. MEZCLA EQUILIBRADA", "Mezcla Equilibrada")
        ]

        for texto, metodo in opciones:

            self.crear_boton(
                tarjeta,
                texto,
                lambda m=metodo: self.mostrar_menu_metodo(m)
            ).pack(
                fill="x",
                pady=9,
                padx=40
            )

        self.crear_boton(
            tarjeta,
            "4. SALIR DEL PROGRAMA",
            self.salir,
            "#b91c1c"
        ).pack(
            fill="x",
            pady=(25, 10),
            padx=40
        )

    # --------------------------------------------------
    # MENU DE CADA METODO
    # --------------------------------------------------

    def mostrar_menu_metodo(self, metodo):

        self.metodo = metodo
        self.limpiar_pantalla()

        self.crear_titulo(
            metodo.upper(),
            "Selecciona el ejercicio que deseas resolver."
        )

        tarjeta = tk.Frame(
            self.contenedor,
            bg="white",
            padx=25,
            pady=20
        )
        tarjeta.pack(
            fill="both",
            expand=True,
            padx=80,
            pady=10
        )

        tk.Label(
            tarjeta,
            text="EJERCICIOS DE EJEMPLO",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#172554"
        ).pack(pady=(5, 15))

        for i, ejemplo in enumerate(
            self.ejemplos[metodo],
            start=1
        ):

            texto = str(i) + ". " + ejemplo["nombre"]

            self.crear_boton(
                tarjeta,
                texto,
                lambda e=ejemplo: self.resolver_ejemplo(e)
            ).pack(
                fill="x",
                pady=5,
                padx=30
            )

        tk.Label(
            tarjeta,
            text="OTRAS OPCIONES",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#172554"
        ).pack(pady=(20, 10))

        self.crear_boton(
            tarjeta,
            "4. RESOLVER MI PROPIO EJERCICIO",
            self.mostrar_entrada_datos,
            "#15803d"
        ).pack(
            fill="x",
            pady=5,
            padx=30
        )

        botones = tk.Frame(
            tarjeta,
            bg="white"
        )
        botones.pack(
            fill="x",
            pady=(20, 5)
        )

        self.crear_boton(
            botones,
            "REGRESAR AL MENU PRINCIPAL",
            self.mostrar_menu_principal,
            "#475569"
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

        self.crear_boton(
            botones,
            "SALIR DEL PROGRAMA",
            self.salir,
            "#b91c1c"
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

    # --------------------------------------------------
    # INGRESAR DATOS
    # --------------------------------------------------

    def mostrar_entrada_datos(self):

        self.limpiar_pantalla()
        self.entradas_listas = []

        self.crear_titulo(
            "RESOLVER MI PROPIO EJERCICIO",
            "Primero indica cuantas listas deseas ingresar."
        )

        tarjeta = tk.Frame(
            self.contenedor,
            bg="white",
            padx=25,
            pady=20
        )
        tarjeta.pack(
            fill="both",
            expand=True,
            padx=60,
            pady=10
        )

        tk.Label(
            tarjeta,
            text="¿CUANTAS LISTAS DESEAS UTILIZAR?",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#172554"
        ).pack(pady=10)

        self.cantidad_listas = tk.Entry(
            tarjeta,
            font=("Arial", 13),
            justify="center",
            width=12
        )
        self.cantidad_listas.pack(
            pady=10,
            ipady=6
        )

        if self.metodo == "Intercalacion":
            texto = "Puedes utilizar dos o mas listas para intercalarlas."
        else:
            texto = (
                "Las listas se combinaran para formar una secuencia "
                "que sera ordenada por el metodo seleccionado."
            )

        tk.Label(
            tarjeta,
            text=texto,
            font=("Arial", 10),
            bg="white",
            fg="#475569",
            wraplength=700
        ).pack(pady=10)

        self.crear_boton(
            tarjeta,
            "CONTINUAR",
            self.crear_campos_listas,
            "#15803d"
        ).pack(
            fill="x",
            padx=80,
            pady=15
        )

        self.crear_boton(
            tarjeta,
            "REGRESAR AL MENU DEL METODO",
            lambda: self.mostrar_menu_metodo(self.metodo),
            "#475569"
        ).pack(
            fill="x",
            padx=80,
            pady=5
        )

        self.crear_boton(
            tarjeta,
            "SALIR DEL PROGRAMA",
            self.salir,
            "#b91c1c"
        ).pack(
            fill="x",
            padx=80,
            pady=5
        )

    def crear_campos_listas(self):

        try:

            cantidad = int(self.cantidad_listas.get())

            if cantidad < 1:
                raise ValueError

            if self.metodo == "Intercalacion" and cantidad < 2:
                raise ValueError(
                    "Para Intercalacion necesitas al menos dos listas."
                )

            if cantidad > 20:
                raise ValueError(
                    "Puedes ingresar como maximo 20 listas."
                )

        except ValueError as error:

            mensaje = str(error)

            if not mensaje:
                mensaje = "Ingresa una cantidad valida de listas."

            messagebox.showerror(
                "Cantidad incorrecta",
                mensaje
            )
            return

        self.limpiar_pantalla()
        self.entradas_listas = []

        self.crear_titulo(
            "INGRESAR LAS LISTAS",
            "Escribe los datos correspondientes a cada lista."
        )

        marco = tk.Frame(
            self.contenedor,
            bg="white",
            padx=15,
            pady=12
        )
        marco.pack(
            fill="both",
            expand=True
        )

        lienzo = tk.Canvas(
            marco,
            bg="white",
            highlightthickness=0
        )

        barra = ttk.Scrollbar(
            marco,
            orient="vertical",
            command=lienzo.yview
        )

        lienzo.configure(
            yscrollcommand=barra.set
        )

        barra.pack(side="right", fill="y")
        lienzo.pack(
            side="left",
            fill="both",
            expand=True
        )

        interior = tk.Frame(
            lienzo,
            bg="white"
        )

        ventana_interior = lienzo.create_window(
            (0, 0),
            window=interior,
            anchor="nw"
        )

        def actualizar_region(event):
            lienzo.configure(
                scrollregion=lienzo.bbox("all")
            )

        def ajustar_ancho(event):
            lienzo.itemconfigure(
                ventana_interior,
                width=event.width
            )

        interior.bind(
            "<Configure>",
            actualizar_region
        )

        lienzo.bind(
            "<Configure>",
            ajustar_ancho
        )

        for i in range(cantidad):

            tk.Label(
                interior,
                text="LISTA " + str(i + 1),
                font=("Arial", 11, "bold"),
                bg="white",
                fg="#172554"
            ).pack(
                anchor="w",
                pady=(12, 3)
            )

            entrada = tk.Entry(
                interior,
                font=("Arial", 11),
                relief="solid",
                bd=1
            )

            entrada.pack(
                fill="x",
                ipady=7,
                pady=(0, 8)
            )

            self.entradas_listas.append(entrada)

        tk.Label(
            interior,
            text=(
                "Separa los valores con comas, punto y coma "
                "o saltos de linea."
            ),
            font=("Arial", 9),
            bg="white",
            fg="#64748b"
        ).pack(
            anchor="w",
            pady=10
        )

        botones = tk.Frame(
            self.contenedor,
            bg="#eef2f7"
        )
        botones.pack(
            fill="x",
            pady=10
        )

        self.crear_boton(
            botones,
            "RESOLVER EJERCICIO",
            self.resolver_datos,
            "#15803d"
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

        self.crear_boton(
            botones,
            "REGRESAR AL MENU PRINCIPAL",
            self.mostrar_menu_principal,
            "#475569"
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

        self.crear_boton(
            botones,
            "SALIR",
            self.salir,
            "#b91c1c"
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

    # --------------------------------------------------
    # LECTURA Y CONVERSION DE DATOS
    # --------------------------------------------------

    def clave_texto(self, texto):

        normalizado = unicodedata.normalize(
            "NFKD",
            texto.casefold()
        )

        return "".join(
            caracter
            for caracter in normalizado
            if not unicodedata.combining(caracter)
        )

    def convertir_tiempo(self, valor):

        partes = valor.split(":")

        if len(partes) not in (2, 3):
            raise ValueError(
                "Formato de tiempo incorrecto: " + valor
            )

        if not all(p.isdigit() for p in partes):
            raise ValueError(
                "El tiempo debe contener numeros."
            )

        numeros = [int(p) for p in partes]

        if len(numeros) == 2:

            minutos, segundos = numeros

            if segundos >= 60:
                raise ValueError(
                    "Los segundos deben ser menores a 60."
                )

            return minutos * 60 + segundos

        horas, minutos, segundos = numeros

        if minutos >= 60 or segundos >= 60:
            raise ValueError(
                "Minutos y segundos deben ser menores a 60."
            )

        return horas * 3600 + minutos * 60 + segundos

    def convertir_valor(self, valor):

        if ":" in valor:
            return self.convertir_tiempo(valor), "tiempo"

        try:
            return float(valor), "numero"

        except ValueError:
            return self.clave_texto(valor), "texto"

    def interpretar_datos(self, texto):

        tokens = [
            x.strip()
            for x in re.split(r"[,;\n]+", texto)
            if x.strip()
        ]

        if not tokens:
            raise ValueError(
                "Debes ingresar al menos un dato en cada lista."
            )

        lista = []
        tipo_general = None

        for token in tokens:

            if "=" in token:

                nombre, valor = token.split("=", 1)
                nombre = nombre.strip()
                valor = valor.strip()

                if not nombre or not valor:
                    raise ValueError(
                        "Revisa el formato nombre=valor."
                    )

                clave, tipo = self.convertir_valor(valor)

                if tipo == "texto":
                    raise ValueError(
                        "En nombre=valor, el valor debe ser numerico o tiempo."
                    )

                etiqueta = nombre + "=" + valor

            else:

                clave, tipo = self.convertir_valor(token)
                etiqueta = token

            if tipo_general is None:
                tipo_general = tipo

            elif tipo_general != tipo:
                raise ValueError(
                    "No mezcles numeros, tiempos y palabras en una misma lista."
                )

            lista.append({
                "clave": clave,
                "etiqueta": etiqueta
            })

        return lista, tipo_general

    def mostrar_lista(self, lista):

        return "[" + ", ".join(
            elemento["etiqueta"]
            for elemento in lista
        ) + "]"

    # --------------------------------------------------
    # MEZCLA DE DOS LISTAS CON COMPARACIONES
    # --------------------------------------------------

    def mezclar(self, izquierda, derecha, mostrar=False):

        resultado = []
        i = 0
        j = 0
        comparacion = 1

        if mostrar:

            self.escribir("Se van a mezclar estas dos sublistas:")
            self.escribir("Izquierda: " + self.mostrar_lista(izquierda))
            self.escribir("Derecha:   " + self.mostrar_lista(derecha))
            self.escribir("")

        while i < len(izquierda) and j < len(derecha):

            valor_izquierdo = izquierda[i]
            valor_derecho = derecha[j]

            if mostrar:
                self.escribir(
                    "Comparacion " + str(comparacion) + ": " +
                    valor_izquierdo["etiqueta"] + " contra " +
                    valor_derecho["etiqueta"]
                )

            if valor_izquierdo["clave"] <= valor_derecho["clave"]:

                resultado.append(valor_izquierdo)
                i += 1

                if mostrar:
                    self.escribir(
                        "Se coloca " + valor_izquierdo["etiqueta"] +
                        " porque es menor o igual."
                    )

            else:

                resultado.append(valor_derecho)
                j += 1

                if mostrar:
                    self.escribir(
                        "Se coloca " + valor_derecho["etiqueta"] +
                        " porque es menor."
                    )

            if mostrar:
                self.escribir(
                    "Resultado parcial: " + self.mostrar_lista(resultado)
                )
                self.escribir("")

            comparacion += 1

        if i < len(izquierda):

            sobrantes = izquierda[i:]
            resultado.extend(sobrantes)

            if mostrar:
                self.escribir(
                    "Se agregan los elementos restantes de la izquierda: " +
                    self.mostrar_lista(sobrantes)
                )

        if j < len(derecha):

            sobrantes = derecha[j:]
            resultado.extend(sobrantes)

            if mostrar:
                self.escribir(
                    "Se agregan los elementos restantes de la derecha: " +
                    self.mostrar_lista(sobrantes)
                )

        if mostrar:

            self.escribir("Sublista ordenada despues de mezclar:")
            self.escribir(self.mostrar_lista(resultado))
            self.escribir("-" * 65)
            self.escribir("")

        return resultado

    # --------------------------------------------------
    # DIVISION RECURSIVA PARA INTERCALACION
    # --------------------------------------------------

    def ordenar_previo(self, lista, mostrar=False, nivel=1):

        if len(lista) <= 1:

            if mostrar:
                self.escribir(
                    "La sublista " + self.mostrar_lista(lista) +
                    " tiene un solo elemento; ya esta ordenada."
                )

            return lista[:]

        mitad = len(lista) // 2
        izquierda_original = lista[:mitad]
        derecha_original = lista[mitad:]

        if mostrar:

            self.escribir(
                "Division nivel " + str(nivel) + ": " +
                self.mostrar_lista(lista)
            )

            self.escribir(
                "  Mitad izquierda: " +
                self.mostrar_lista(izquierda_original)
            )

            self.escribir(
                "  Mitad derecha:   " +
                self.mostrar_lista(derecha_original)
            )

            self.escribir("")

        izquierda = self.ordenar_previo(
            izquierda_original, mostrar, nivel + 1
        )

        derecha = self.ordenar_previo(
            derecha_original, mostrar, nivel + 1
        )

        if mostrar:
            self.escribir(
                "Ahora se mezclan las mitades ordenadas del nivel " +
                str(nivel) + "."
            )

        return self.mezclar(izquierda, derecha, mostrar)

    # --------------------------------------------------
    # INTERCALACION DE VARIAS LISTAS
    # --------------------------------------------------

    def intercalacion(self, listas):

        self.escribir("METODO DE INTERCALACION")
        self.escribir("=" * 65)

        listas_ordenadas = []

        for i, lista in enumerate(listas, start=1):

            self.escribir(
                "Lista " + str(i) + " original: " +
                self.mostrar_lista(lista)
            )

            self.escribir(
                "PASO DE ORDENAMIENTO DE LA LISTA " + str(i) + ":"
            )

            self.escribir(
                "Se divide la lista en mitades hasta obtener "
                "sublistas individuales."
            )

            self.escribir("")

            ordenada = self.ordenar_previo(lista, mostrar=True)
            listas_ordenadas.append(ordenada)

            self.escribir(
                "Lista " + str(i) + " ordenada: " +
                self.mostrar_lista(ordenada)
            )

            self.escribir("")

        self.escribir("PASO FINAL. Intercalar todas las listas.")
        self.escribir("")

        resultado = listas_ordenadas[0]

        for i in range(1, len(listas_ordenadas)):

            self.escribir(
                "Intercalando resultado con lista " +
                str(i + 1)
            )

            resultado = self.mezclar(
                resultado,
                listas_ordenadas[i],
                True
            )

        self.escribir("RESULTADO FINAL:")
        self.escribir(self.mostrar_lista(resultado))

    # --------------------------------------------------
    # MEZCLA DIRECTA
    # --------------------------------------------------

    def mezcla_directa(self, lista):

        self.escribir("METODO DE MEZCLA DIRECTA")
        self.escribir("=" * 65)

        self.escribir(
            "La mezcla directa comienza con bloques de un elemento. "
            "En cada pasada duplica el tamano de los bloques y mezcla "
            "cada par de bloques vecinos."
        )

        self.escribir("")

        actual = lista[:]
        cantidad = len(actual)
        ancho = 1
        pasada = 1

        self.escribir("Lista original:")
        self.escribir(self.mostrar_lista(actual))
        self.escribir("")

        while ancho < cantidad:

            self.escribir("PASADA " + str(pasada))
            self.escribir("-" * 50)

            siguiente = []
            inicio = 0

            while inicio < cantidad:

                izquierda = actual[
                    inicio:inicio + ancho
                ]

                derecha = actual[
                    inicio + ancho:inicio + 2 * ancho
                ]

                self.escribir("Sublista izquierda:")
                self.escribir(self.mostrar_lista(izquierda))

                self.escribir("Sublista derecha:")
                self.escribir(self.mostrar_lista(derecha))

                mezcla = self.mezclar(
                    izquierda,
                    derecha,
                    True
                )

                siguiente.extend(mezcla)

                inicio += 2 * ancho

            actual = siguiente

            self.escribir("Lista despues de la pasada:")
            self.escribir(self.mostrar_lista(actual))
            self.escribir("")

            ancho *= 2
            pasada += 1

        self.escribir("RESULTADO FINAL:")
        self.escribir(self.mostrar_lista(actual))

    # --------------------------------------------------
    # MEZCLA EQUILIBRADA
    # --------------------------------------------------

    def mezcla_equilibrada(self, lista):

        self.escribir("METODO DE MEZCLA EQUILIBRADA")
        self.escribir("=" * 65)

        self.escribir(
            "La mezcla equilibrada inicia con corridas de un elemento. "
            "Las distribuye en dos grupos y despues combina las corridas "
            "por pares hasta obtener una sola lista ordenada."
        )

        self.escribir("")

        actual = [
            [elemento]
            for elemento in lista
        ]

        self.escribir("Lista original:")
        self.escribir(self.mostrar_lista(lista))
        self.escribir("")

        pasada = 1

        while len(actual) > 1:

            self.escribir("PASADA " + str(pasada))
            self.escribir("-" * 55)

            f1 = actual[0::2]
            f2 = actual[1::2]

            self.escribir("Distribucion de corridas:")

            self.escribir(
                "F1: " + str([
                    self.mostrar_lista(x) for x in f1
                ])
            )

            self.escribir(
                "F2: " + str([
                    self.mostrar_lista(x) for x in f2
                ])
            )

            self.escribir("")

            f3 = []
            f4 = []

            total = max(len(f1), len(f2))

            for i in range(total):

                izquierda = (
                    f1[i] if i < len(f1) else []
                )

                derecha = (
                    f2[i] if i < len(f2) else []
                )

                self.escribir(
                    "Mezclando corrida " + str(i + 1)
                )

                mezcla = self.mezclar(
                    izquierda,
                    derecha,
                    True
                )

                if i % 2 == 0:
                    f3.append(mezcla)
                else:
                    f4.append(mezcla)

            self.escribir("Corridas en F3:")
            self.escribir(
                str([self.mostrar_lista(x) for x in f3])
            )

            self.escribir("Corridas en F4:")
            self.escribir(
                str([self.mostrar_lista(x) for x in f4])
            )

            nuevas_corridas = []

            for i in range(max(len(f3), len(f4))):

                if i < len(f3):
                    nuevas_corridas.append(f3[i])

                if i < len(f4):
                    nuevas_corridas.append(f4[i])

            actual = nuevas_corridas

            self.escribir("")
            self.escribir("Corridas de la siguiente pasada:")

            for corrida in actual:
                self.escribir(self.mostrar_lista(corrida))

            self.escribir("")
            pasada += 1

        resultado = actual[0] if actual else []

        self.escribir("RESULTADO FINAL:")
        self.escribir(self.mostrar_lista(resultado))

    # --------------------------------------------------
    # RESOLVER EJEMPLOS
    # --------------------------------------------------

    def resolver_ejemplo(self, ejemplo):

        try:

            listas = []
            tipo_general = None

            for datos in ejemplo["listas"]:

                lista, tipo = self.interpretar_datos(datos)

                if tipo_general is None:
                    tipo_general = tipo

                elif tipo_general != tipo:
                    raise ValueError(
                        "Las listas deben tener el mismo tipo de datos."
                    )

                listas.append(lista)

            self.nombre_ejercicio = ejemplo["nombre"]
            self.mostrar_resultado(listas)

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    # --------------------------------------------------
    # RESOLVER DATOS PROPIOS
    # --------------------------------------------------

    def resolver_datos(self):

        try:

            listas = []
            tipo_general = None

            for i, entrada in enumerate(
                self.entradas_listas,
                start=1
            ):

                lista, tipo = self.interpretar_datos(
                    entrada.get()
                )

                if tipo_general is None:
                    tipo_general = tipo

                elif tipo_general != tipo:
                    raise ValueError(
                        "Todas las listas deben contener el mismo tipo de datos. "
                        "Error en la lista " + str(i) + "."
                    )

                listas.append(lista)

            self.nombre_ejercicio = "Ejercicio creado por el usuario"
            self.mostrar_resultado(listas)

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    # --------------------------------------------------
    # PANTALLA DE RESULTADOS
    # --------------------------------------------------

    def mostrar_resultado(self, listas):

        self.limpiar_pantalla()

        self.crear_titulo(
            "RESOLUCION DEL EJERCICIO",
            "Procedimiento detallado, comparaciones y resultado final."
        )

        marco = tk.Frame(
            self.contenedor,
            bg="white",
            padx=10,
            pady=10
        )
        marco.pack(
            fill="both",
            expand=True,
            pady=5
        )

        self.resultado = tk.Text(
            marco,
            font=("Consolas", 10),
            bg="#f8fafc",
            fg="#172554",
            wrap="word",
            relief="flat",
            padx=15,
            pady=12
        )

        barra = ttk.Scrollbar(
            marco,
            orient="vertical",
            command=self.resultado.yview
        )

        self.resultado.configure(
            yscrollcommand=barra.set
        )

        barra.pack(side="right", fill="y")

        self.resultado.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.escribir("DATOS DE ENTRADA")
        self.escribir("=" * 65)

        for numero, lista in enumerate(listas, start=1):

            self.escribir(
                "Lista " + str(numero) + ": " +
                self.mostrar_lista(lista)
            )

        self.escribir("")
        self.escribir("CRITERIO DE ORDENAMIENTO")

        self.escribir(
            "Los datos se ordenan de menor a mayor. "
            "En palabras se usa el orden alfabetico; "
            "en tiempos se comparan sus segundos."
        )

        self.escribir("")

        self.escribir(
            "EJERCICIO: " + getattr(
                self,
                "nombre_ejercicio",
                "Ejercicio ingresado"
            )
        )

        self.escribir("METODO: " + self.metodo)
        self.escribir("")

        if self.metodo == "Intercalacion":

            self.intercalacion(listas)

        else:

            lista_unica = []

            self.escribir(
                "LISTAS INGRESADAS: " + str(len(listas))
            )

            for i, lista in enumerate(listas, start=1):

                self.escribir(
                    "Lista " + str(i) + ": " +
                    self.mostrar_lista(lista)
                )

                lista_unica.extend(lista)

            self.escribir("")

            self.escribir(
                "Se combinan las listas para aplicar el metodo."
            )

            self.escribir(
                "Lista que sera ordenada: " +
                self.mostrar_lista(lista_unica)
            )

            self.escribir("")

            if self.metodo == "Mezcla Directa":

                self.mezcla_directa(lista_unica)

            elif self.metodo == "Mezcla Equilibrada":

                self.mezcla_equilibrada(lista_unica)

        self.escribir("")
        self.escribir("=" * 65)
        self.escribir("FIN DE LA RESOLUCION")

        self.escribir(
            "El resultado final aparece arriba. Cada comparacion muestra "
            "que elementos se evaluaron, cual se eligio y como fue creciendo "
            "la lista ordenada."
        )

        botones = tk.Frame(
            self.contenedor,
            bg="#eef2f7"
        )
        botones.pack(
            fill="x",
            pady=(12, 5)
        )

        self.crear_boton(
            botones,
            "REGRESAR AL MENU PRINCIPAL",
            self.mostrar_menu_principal,
            "#475569"
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=8
        )

        self.crear_boton(
            botones,
            "SALIR DEL PROGRAMA",
            self.salir,
            "#b91c1c"
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=8
        )

    # --------------------------------------------------
    # MOSTRAR PROCEDIMIENTO
    # --------------------------------------------------

    def escribir(self, mensaje):

        self.resultado.insert(
            "end",
            str(mensaje) + "\n"
        )

        self.resultado.see("end")
        self.ventana.update_idletasks()

    # --------------------------------------------------
    # SALIR
    # --------------------------------------------------

    def salir(self):

        respuesta = messagebox.askyesno(
            "Salir del programa",
            "¿Estas seguro de que deseas salir?"
        )

        if respuesta:
            self.ventana.destroy()


# --------------------------------------------------
# INICIO DEL PROGRAMA
# --------------------------------------------------

ventana = tk.Tk()
app = AplicacionOrdenamiento(ventana)
ventana.mainloop()
