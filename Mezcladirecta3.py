import os
import shutil
from itertools import islice

DESC = False
ORIGEN = "edades.txt"
TRABAJO = "trabajo.txt"
AUX1, AUX2 = "aux1.txt", "aux2.txt"
RESULTADO = "edades_ordenadas.txt"


def clave(linea):
    return int(linea)


def texto(linea):
    return linea.strip()

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


def leer_bloques(ruta, longitud):
    bloques = []
    with open(ruta) as f:
        while True:
            b = list(islice(f, longitud))
            if not b:
                break
            bloques.append(b)
    return bloques


def mostrar_archivo(ruta, longitud):
    bloques = leer_bloques(ruta, longitud)
    print(f"    {ruta}: " + (" ".join(lista_txt(b) for b in bloques) or "(vacío)"))


def distribuir(origen, longitud):
    with open(origen) as f, open(AUX1, "w") as f1, open(AUX2, "w") as f2:
        destino = f1
        while True:
            bloque = list(islice(f, longitud))
            if not bloque:
                break
            destino.writelines(bloque)
            destino = f2 if destino is f1 else f1
    print("  Distribución en archivos auxiliares:")
    mostrar_archivo(AUX1, longitud)
    mostrar_archivo(AUX2, longitud)


def mezclar(destino, longitud):
    with open(AUX1) as f1, open(AUX2) as f2, open(destino, "w") as out:
        k = 1
        while True:
            b1 = list(islice(f1, longitud))
            b2 = list(islice(f2, longitud))
            if not b1 and not b2:
                break
            print(f"    Bloque {k}: {lista_txt(b1)} con {lista_txt(b2)}")
            if b2:
                m = intercalar(b1, b2, True, "      ", "aux1", "aux2")
            else:
                m = b1
                print("      (no tiene pareja en aux2, se copia igual)")
            out.writelines(m)
            k += 1


def mezcla_directa_archivo():
    shutil.copy(ORIGEN, TRABAJO)
    with open(TRABAJO) as f:
        n = sum(1 for _ in f)
    longitud, paso = 1, 1
    while longitud < n:
        print(f"\nPASO {paso}: bloques de {longitud} línea(s)")
        distribuir(TRABAJO, longitud)
        print("  Mezcla bloque por bloque:")
        mezclar(TRABAJO, longitud)
        with open(TRABAJO) as f:
            print(f"  Resultado del paso {paso}: {lista_txt(f.readlines())}")
        longitud *= 2
        paso += 1
    os.replace(TRABAJO, RESULTADO)
    for aux in (AUX1, AUX2):
        if os.path.exists(aux):
            os.remove(aux)


def resolver(edades):
    lineas = [f"{e}\n" for e in edades]
    with open(ORIGEN, "w") as f:
        f.writelines(lineas)
    print(f"Archivo {ORIGEN} (original): {lista_txt(lineas)}")
    print("Objetivo: ordenar las edades de menor a mayor usando archivos")
    mezcla_directa_archivo()
    with open(RESULTADO) as f:
        final = f.readlines()
    resultado_final(final)
    print(f"\nArchivo {RESULTADO}:")
    for pos, linea in enumerate(final, 1):
        print(f"{pos:>2}. {linea.strip()} años")


def pedir_edades():
    while True:
        t = input("Edades (números enteros separados por espacio, ej: 25 31 18 40): ")
        try:
            edades = [int(x) for x in t.split()]
        except ValueError:
            print("  Escribe solo números enteros separados por espacio.")
            continue
        if len(edades) < 2:
            print("  Escribe al menos 2 números.")
            continue
        return edades


def ejemplo():
    resolver([25, 31, 18, 40, 22, 35, 29, 19])


def propio():
    e = pedir_edades()
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
        print("\n=== MEZCLA DIRECTA: EDADES CON ARCHIVOS ===")
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
