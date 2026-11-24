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


def intercalacion_sin_repetidos(a, b):
    r, i, j, paso = [], 0, 0, 1
    while i < len(a) and j < len(b):
        u, v = a[i], b[j]
        if clave(u) < clave(v):
            r.append(u)
            i += 1
            msg = f"sale {u} (A)"
        elif clave(u) > clave(v):
            r.append(v)
            j += 1
            msg = f"sale {v} (B)"
        else:
            r.append(u)
            i += 1
            j += 1
            msg = f"es el mismo libro, sale {u} una sola vez"
        print(f"   Paso {paso}: {u} vs {v} -> {msg}  =>  {lista_txt(r)}")
        paso += 1
    if i < len(a):
        print(f"   Sobran de A: {lista_txt(a[i:])} -> se copian al final")
    if j < len(b):
        print(f"   Sobran de B: {lista_txt(b[j:])} -> se copian al final")
    return r + a[i:] + b[j:]


def resolver(a, b):
    print("Biblioteca A:", lista_txt(a))
    print("Biblioteca B:", lista_txt(b))
    print("\nPaso a paso:")
    catalogo = intercalacion_sin_repetidos(a, b)
    print("\n" + "-" * 60)
    print(f"  RESULTADO FINAL: catálogo único de {len(catalogo)} títulos")
    for n, titulo in enumerate(catalogo, 1):
        print(f"   {n:>2}. {titulo}")
    print("-" * 60)


def pedir_catalogo(mensaje):
    t = input(mensaje)
    titulos = {x.strip() for x in t.split(",") if x.strip()}
    return sorted(titulos, key=clave)


def ejemplo():
    resolver(["Algoritmos", "Bases de Datos", "Cálculo", "Física", "Redes"],
             ["Álgebra", "Bases de Datos", "Estructuras de Datos", "Física", "Programación"])


def propio():
    a = pedir_catalogo("Títulos de la biblioteca A (separados por coma): ")
    b = pedir_catalogo("Títulos de la biblioteca B (separados por coma): ")
    if not a and not b:
        print("No capturaste títulos.")
        return
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
        print("\n=== INTERCALACIÓN: CATÁLOGO DE LIBROS ===")
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
