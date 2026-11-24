DESC = True


def clave(x):
    return x


def texto(x):
    return str(x)

def lista_txt(lista):
    return "[" + ", ".join(texto(x) for x in lista) + "]"


def resultado_final(lista):
    print("\n" + "-" * 60)
    print("  RESULTADO FINAL: " + lista_txt(lista))
    print("-" * 60)

def antes(x, y):
    return clave(x) >= clave(y) if DESC else clave(x) <= clave(y)


def intercalar(a, b, visible=False, sangria="   ", na="A", nb="B"):
    r, i, j, paso = [], 0, 0, 1
    while i < len(a) and j < len(b):
        u, v = a[i], b[j]
        if antes(u, v):
            x, de = u, na
            i += 1
        else:
            x, de = v, nb
            j += 1
        r.append(x)
        if visible:
            print(f"{sangria}Paso {paso}: {texto(u)} vs {texto(v)} -> sale {texto(x)} ({de})  =>  {lista_txt(r)}")
        paso += 1
    if visible:
        if i < len(a):
            print(f"{sangria}Sobran de {na}: {lista_txt(a[i:])} -> se copian al final")
        if j < len(b):
            print(f"{sangria}Sobran de {nb}: {lista_txt(b[j:])} -> se copian al final")
    r = r + a[i:] + b[j:]
    if visible:
        print(f"{sangria}Resultado: {lista_txt(r)}")
    return r

def dividir_en_runs(datos):
    runs, actual = [], [datos[0]]
    for x in datos[1:]:
        if antes(actual[-1], x):
            actual.append(x)
        else:
            runs.append(actual)
            actual = [x]
    runs.append(actual)
    return runs


def mostrar_archivos(archivos):
    for i, f in enumerate(archivos, 1):
        print(f"    Archivo {i}: " + (" ".join(lista_txt(r) for r in f) or "(vacío)"))


def mezcla_equilibrada(datos, vias=2):
    datos = list(datos)
    print("Datos originales:", lista_txt(datos))
    runs = dividir_en_runs(datos)
    print(f"\nPASO 0: detectar los tramos que ya están ordenados ({len(runs)} tramos)")
    entrada = [[] for _ in range(vias)]
    for k, run in enumerate(runs):
        print(f"    Tramo {k + 1}: {lista_txt(run)} -> Archivo {k % vias + 1}")
        entrada[k % vias].append(run)
    print("  Archivos de entrada:")
    mostrar_archivos(entrada)
    paso = 0
    while sum(len(f) for f in entrada) > 1:
        paso += 1
        salida = [[] for _ in range(vias)]
        print(f"\nPASO {paso}: mezclar un tramo de cada archivo de entrada")
        destino, ronda = 0, 1
        while any(entrada):
            tomados, partes = [], []
            for idx, f in enumerate(entrada):
                if f:
                    t = f.pop(0)
                    tomados.append(t)
                    partes.append(f"{lista_txt(t)} (archivo {idx + 1})")
            print(f"  Ronda {ronda}: se toman " + " y ".join(partes))
            mezclado = tomados[0]
            if len(tomados) == 1:
                print("      (queda un solo tramo, se copia igual)")
            for t in tomados[1:]:
                mezclado = intercalar(mezclado, t, True, "      ", "tramo izq", "tramo der")
            print(f"    => se escribe en el archivo de salida {destino + 1}")
            salida[destino].append(mezclado)
            destino = (destino + 1) % vias
            ronda += 1
        entrada = salida
        print("  Archivos de salida (serán la entrada del siguiente paso):")
        mostrar_archivos(entrada)
    final = next(f[0] for f in entrada if f)
    print(f"\n  Pasadas realizadas: {paso}")
    return final


def resolver(puntajes):
    print("Puntajes:", lista_txt(puntajes))
    print("Objetivo: ordenarlos del más alto al más bajo, con 2 vías\n")
    ordenados = mezcla_equilibrada(puntajes, 2)
    resultado_final(ordenados)
    print("\nTabla de posiciones")
    print("-" * 24)
    for pos, p in enumerate(ordenados, 1):
        print(f"{pos:>2}. {p} puntos")


def pedir_puntajes():
    while True:
        t = input("Puntajes (números enteros separados por espacio, ej: 1500 320 980 2200): ")
        try:
            numeros = [int(x) for x in t.split()]
        except ValueError:
            print("  Escribe solo números enteros separados por espacio.")
            continue
        if len(numeros) < 2:
            print("  Escribe al menos 2 números.")
            continue
        return numeros


def ejemplo():
    resolver([1500, 320, 980, 2200, 760, 1800, 450, 2600, 1100, 90])


def propio():
    p = pedir_puntajes()
    print()
    resolver(p)


def volver():
    while True:
        print("\n1. Regresar al menú principal")
        print("2. Salir del programa")
        r = input("Elige una opción: ").strip()
        if r == "1":
            return True
        if r == "2":
            return False
        print("Opción inválida.")


def menu():
    while True:
        print("\n=== MEZCLA EQUILIBRADA: PUNTAJES DE VIDEOJUEGO ===")
        print("1. Resolver tu propio ejercicio")
        print("2. Resolver el ejemplo")
        print("3. Salir")
        opcion = input("Elige una opción: ").strip()
        if opcion == "1":
            propio()
        elif opcion == "2":
            ejemplo()
        elif opcion == "3":
            break
        else:
            print("Opción inválida.")
            continue
        if not volver():
            break
    print("\nPrograma terminado.")


if __name__ == "__main__":
    menu()
