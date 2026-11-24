import os
from contextlib import ExitStack

DESC = False
ORIGEN = "estaturas.txt"
RESULTADO = "estaturas_ordenadas.txt"
VIAS = 2
ARCH_A = [f"entrada{i}.txt" for i in range(1, VIAS + 1)]
ARCH_B = [f"salida{i}.txt" for i in range(1, VIAS + 1)]


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


def leer_runs(ruta):
    run = []
    with open(ruta) as f:
        for linea in f:
            linea = linea.strip()
            if linea == "#":
                yield run
                run = []
            elif linea:
                run.append(int(linea))


def distribuir_inicial():
    total = 0
    with ExitStack() as pila:
        salidas = [pila.enter_context(open(r, "w")) for r in ARCH_A]
        destino, previo, run = 0, None, []
        with open(ORIGEN) as f:
            for linea in f:
                valor = int(linea)
                if previo is not None and valor < previo:
                    salidas[destino].write("#\n")
                    total += 1
                    print(f"    Tramo {total}: {lista_txt(run)} -> {ARCH_A[destino]}")
                    destino = (destino + 1) % VIAS
                    run = []
                salidas[destino].write(f"{valor}\n")
                run.append(valor)
                previo = valor
        if previo is not None:
            salidas[destino].write("#\n")
            total += 1
            print(f"    Tramo {total}: {lista_txt(run)} -> {ARCH_A[destino]}")
    return total


def pasada(entradas, salidas):
    total = 0
    with ExitStack() as pila:
        out = [pila.enter_context(open(r, "w")) for r in salidas]
        gens = [leer_runs(r) for r in entradas]
        destino, ronda = 0, 1
        while True:
            tomados, partes = [], []
            for idx, g in enumerate(gens):
                r = next(g, None)
                if r is not None:
                    tomados.append(r)
                    partes.append(f"{lista_txt(r)} ({entradas[idx]})")
            if not tomados:
                break
            print(f"  Ronda {ronda}: se toman " + " y ".join(partes))
            mezclado = tomados[0]
            if len(tomados) == 1:
                print("      (queda un solo tramo, se copia igual)")
            for t in tomados[1:]:
                mezclado = intercalar(mezclado, t, True, "      ", "tramo izq", "tramo der")
            out[destino].writelines(f"{v}\n" for v in mezclado)
            out[destino].write("#\n")
            print(f"    => se escribe en {salidas[destino]}")
            destino = (destino + 1) % VIAS
            ronda += 1
            total += 1
    return total


def mostrar(rutas):
    for r in rutas:
        runs = [lista_txt(run) for run in leer_runs(r)]
        print(f"    {r}: {' '.join(runs) if runs else '(vacío)'}")


def resolver(estaturas):
    with open(ORIGEN, "w") as f:
        f.write("\n".join(map(str, estaturas)) + "\n")
    print(f"Archivo {ORIGEN} (original):", lista_txt(estaturas))
    print("Objetivo: ordenar las estaturas (cm) de menor a mayor usando 4 archivos")
    print(f"\nPASO 0: detectar los tramos ya ordenados y repartirlos en {VIAS} archivos")
    total = distribuir_inicial()
    print(f"  Se detectaron {total} tramos. Archivos de entrada:")
    mostrar(ARCH_A)

    entradas, salidas, paso = ARCH_A, ARCH_B, 0
    while total > 1:
        paso += 1
        print(f"\nPASO {paso}: mezclar un tramo de cada archivo de entrada")
        total = pasada(entradas, salidas)
        print("  Archivos de salida (serán la entrada del siguiente paso):")
        mostrar(salidas)
        entradas, salidas = salidas, entradas

    final = next(r for r in entradas if os.path.getsize(r) > 0)
    ordenadas = next(leer_runs(final))
    with open(RESULTADO, "w") as out:
        out.writelines(f"{v}\n" for v in ordenadas)
    for r in ARCH_A + ARCH_B:
        if os.path.exists(r):
            os.remove(r)
    print(f"\n  Pasadas realizadas: {paso}")
    resultado_final(ordenadas)
    print(f"Guardado en {RESULTADO}")
    for pos, e in enumerate(ordenadas, 1):
        print(f"{pos:>2}. {e} cm")


def pedir_estaturas():
    while True:
        t = input("Estaturas en cm (números enteros separados por espacio, ej: 165 172 158 180): ")
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
    resolver([165, 172, 158, 180, 169, 175, 160, 183, 170, 155, 178, 162])


def propio():
    e = pedir_estaturas()
    print()
    resolver(e)


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
        print("\n=== MEZCLA EQUILIBRADA: ESTATURAS CON ARCHIVOS ===")
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
