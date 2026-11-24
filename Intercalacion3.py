DESC = False


def clave(r):
    return r[0]


def texto(r):
    return f"${r[0]:.2f}"

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


def resolver(precios_a, precios_b):
    print("Tienda 1 vende a:", lista_txt(precios_a))
    print("Tienda 2 vende a:", lista_txt(precios_b))
    print("\nObjetivo: una sola lista con todos los precios, del más barato al más caro.")
    print("\nPaso a paso:")
    todos = intercalar(precios_a, precios_b, True, "   ", "tienda 1", "tienda 2")
    print("\nPrecios de menor a mayor")
    print("-" * 34)
    for pos, (precio, tienda) in enumerate(todos, 1):
        print(f"{pos:>2}. ${precio:<9.2f} (tienda {tienda})")
    barato = todos[0]
    print(f"\nEl más barato: ${barato[0]:.2f} en la tienda {barato[1]}")


def pedir_precios(numero):
    while True:
        texto_ingresado = input(f"Precios de la tienda {numero} (números separados por espacio, ej: 12.5 30 45.9): ")
        try:
            numeros = [float(x) for x in texto_ingresado.split()]
        except ValueError:
            print("  Escribe solo números separados por espacio.")
            continue
        if not numeros:
            print("  Escribe al menos un número.")
            continue
        return sorted((n, numero) for n in numeros)


def ejemplo():
    resolver([(12.5, 1), (30.0, 1), (45.9, 1), (80.0, 1)],
             [(9.99, 2), (30.0, 2), (52.5, 2), (60.0, 2), (99.0, 2)])


def propio():
    a = pedir_precios(1)
    b = pedir_precios(2)
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
        print("\n=== INTERCALACIÓN: PRECIOS DE DOS TIENDAS ===")
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
