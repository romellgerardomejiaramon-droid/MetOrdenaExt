import unicodedata

DESC = False


def clave(t):
    base = unicodedata.normalize("NFD", t.lower())
    return "".join(c for c in base if unicodedata.category(c) != "Mn")


def texto(x):
    return x

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

def mezcla_directa(datos):
    datos = list(datos)
    n, longitud, paso = len(datos), 1, 1
    print("Datos originales:", lista_txt(datos))
    while longitud < n:
        bloques = [datos[i:i + longitud] for i in range(0, n, longitud)]
        f1, f2 = bloques[0::2], bloques[1::2]
        print(f"\nPASO {paso}: bloques de tamaño {longitud}")
        print("  Distribución:")
        print("    F1:", " ".join(lista_txt(b) for b in f1))
        print("    F2:", " ".join(lista_txt(b) for b in f2) or "(vacío)")
        print("  Mezcla bloque por bloque:")
        resultado = []
        for k, b1 in enumerate(f1):
            b2 = f2[k] if k < len(f2) else []
            print(f"    Bloque {k + 1}: {lista_txt(b1)} con {lista_txt(b2)}")
            if b2:
                mezcla = intercalar(b1, b2, True, "      ", "F1", "F2")
            else:
                mezcla = b1
                print("      (no tiene pareja en F2, se copia igual)")
            resultado += mezcla
        datos = resultado
        print(f"  Resultado del paso {paso}: {lista_txt(datos)}")
        longitud *= 2
        paso += 1
    return datos


def resolver(nombres):
    print("Nombres:", lista_txt(nombres))
    print("Objetivo: ordenarlos alfabéticamente (A a Z)\n")
    ordenados = mezcla_directa(nombres)
    resultado_final(ordenados)
    print("\nLista de asistencia")
    print("-" * 24)
    for pos, n in enumerate(ordenados, 1):
        print(f"{pos:>2}. {n}")


def pedir_nombres():
    while True:
        nombres = input("Nombres (separados por espacio, ej: Mario Ana Zoe Luis): ").split()
        if len(nombres) >= 2:
            return nombres
        print("  Escribe al menos 2 nombres.")


def ejemplo():
    resolver(["Mario", "Ana", "Zoe", "Luis", "Beto", "Sofía", "Carlos", "Diana"])


def propio():
    n = pedir_nombres()
    print()
    resolver(n)


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
        print("\n=== MEZCLA DIRECTA: LISTA DE ASISTENCIA ===")
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
