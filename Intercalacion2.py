DESC = False


def clave(r):
    return r[0]


def texto(r):
    return str(r[0])

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


def resolver(turnos_a, turnos_b):
    print("Ventanilla 1 tiene los turnos:", lista_txt(turnos_a))
    print("Ventanilla 2 tiene los turnos:", lista_txt(turnos_b))
    print("\nObjetivo: una sola lista con todos los turnos, del número más chico al más grande.")
    print("\nPaso a paso:")
    orden = intercalar(turnos_a, turnos_b, True, "   ", "ventanilla 1", "ventanilla 2")
    print("\nOrden de atención")
    print("-" * 34)
    for pos, (turno, ventanilla) in enumerate(orden, 1):
        print(f"{pos:>2}. Turno {turno:<5} (ventanilla {ventanilla})")


def pedir_turnos(numero):
    while True:
        texto_ingresado = input(f"Turnos de la ventanilla {numero} (números separados por espacio, ej: 3 8 15): ")
        try:
            numeros = [int(x) for x in texto_ingresado.split()]
        except ValueError:
            print("  Escribe solo números enteros separados por espacio.")
            continue
        if not numeros:
            print("  Escribe al menos un número.")
            continue
        return sorted((n, numero) for n in numeros)


def ejemplo():
    resolver([(3, 1), (8, 1), (15, 1), (22, 1), (40, 1)],
             [(1, 2), (9, 2), (16, 2), (27, 2), (35, 2), (50, 2)])


def propio():
    a = pedir_turnos(1)
    b = pedir_turnos(2)
    print()
    resolver(a, b)


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
        print("\n=== INTERCALACIÓN: TURNOS DE VENTANILLAS ===")
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
