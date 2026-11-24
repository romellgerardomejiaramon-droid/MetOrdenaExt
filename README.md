# MetOrdenaExt

# Ordenamiento Externo en Python

Intercalación, Mezcla Directa y Mezcla Equilibrada, resueltas **paso a paso** en la terminal.

---

## 1. Descripción

Este proyecto contiene **10 programas en Python** que implementan tres métodos de ordenamiento externo:

1. **Intercalación**: combina dos secuencias que ya están ordenadas en una sola.
2. **Mezcla Directa**: ordena repartiendo los datos en dos archivos auxiliares por bloques de tamaño 1, 2, 4, 8... y mezclándolos.
3. **Mezcla Equilibrada**: ordena con 2N archivos (N de entrada y N de salida) que se alternan en cada pasada, aprovechando los tramos que ya vienen ordenados.

Cada programa trae un **ejemplo ya resuelto** y permite **resolver tu propio ejercicio**. En todos se muestra el procedimiento completo, no solo el resultado.

---

## 2. Contenido del proyecto

| # | Archivo | Método | Ejercicio | Orden |
|---|---------|--------|-----------|-------|
| 1 | `intercalacion_1_catalogo_libros.py` | Intercalación | Catálogo de dos bibliotecas, sin libros repetidos | A a Z (ignora acentos) |
| 2 | `intercalacion_2_turnos_ventanillas.py` | Intercalación | Turnos de dos ventanillas de un banco | Menor a mayor |
| 3 | `intercalacion_3_precios_tiendas.py` | Intercalación | Precios de dos tiendas | Menor a mayor |
| 4 | `mezcla_directa_1_calificaciones.py` | Mezcla Directa | Calificaciones de un grupo | Mayor a menor |
| 5 | `mezcla_directa_2_nombres_asistencia.py` | Mezcla Directa | Lista de asistencia | A a Z (ignora acentos) |
| 6 | `mezcla_directa_3_edades_archivo.py` | Mezcla Directa | Edades, con **archivos reales** | Menor a mayor |
| 7 | `mezcla_equilibrada_1_puntajes_videojuego.py` | Mezcla Equilibrada (2 vías) | Puntajes de un videojuego | Mayor a menor |
| 8 | `mezcla_equilibrada_2_temperaturas_semana.py` | Mezcla Equilibrada (3 vías) | Temperaturas de la semana | Menor a mayor |
| 9 | `mezcla_equilibrada_3_estaturas_archivos.py` | Mezcla Equilibrada (2 vías) | Estaturas, con **archivos reales** | Menor a mayor |
| 10 | `programa_final_todos_los_metodos.py` | Los tres | Menú con ejemplos y ejercicio propio de cada método | Menor a mayor |

---

## 3. Requisitos y ejecución

- **Python 3.8 o superior.**
- No necesita instalar librerías: solo usa módulos que vienen con Python (`os`, `shutil`, `itertools`, `contextlib`, `unicodedata`, `datetime`).

Para ejecutar cualquier programa, abre una terminal en la carpeta del proyecto y escribe:

```
python nombre_del_archivo.py
```

Por ejemplo:

```
python programa_final_todos_los_metodos.py
```

> En algunos sistemas el comando es `python3` en lugar de `python`.

Los programas 6 y 9 crean archivos `.txt` en la carpeta donde los ejecutes, así que conviene correrlos desde una carpeta propia.

---

## 4. Conceptos básicos

- **Ordenamiento externo:** técnica para ordenar datos que no caben completos en memoria, usando archivos auxiliares. Se ordenan por partes y se mezclan.
- **Tramo (run):** secuencia de datos consecutivos que ya están en orden. Por ejemplo, en `[17, 31, 5, 59]` hay dos tramos: `[17, 31]` y `[5, 59]`.
- **Intercalar:** mezclar dos secuencias ordenadas comparando siempre sus primeros elementos y sacando el que corresponda.
- **F1 y F2:** los dos archivos auxiliares de la mezcla directa.
- **Vías:** cantidad de archivos de entrada (y de salida) en la mezcla equilibrada.

En los programas 1 a 5, 7, 8 y 10 los "archivos" se **simulan con listas de Python** para que el proceso se vea claro. En los programas 6 y 9 se usan **archivos de texto reales**.

---

## 5. Funcionamiento interno (parte por parte)

### 5.1 Estructura general de un programa

Todos los programas tienen las mismas capas:

```
Configuración   ->  DESC, clave(), texto()
Presentación    ->  lista_txt(), resultado_final()
Comparación     ->  antes()
Método          ->  intercalar() / mezcla_directa() / mezcla_equilibrada()
Ejercicio       ->  resolver(), pedir_...(), ejemplo(), propio()
Menú            ->  volver(), menu()
```

Los métodos (intercalación, mezcla directa y mezcla equilibrada) son **iguales en todos los programas**. Lo único que cambia entre un programa y otro es la configuración (qué dato se ordena y cómo) y la parte de captura del ejercicio.

### 5.2 Configuración: `DESC`, `clave()` y `texto()`

Estas tres piezas hacen que el mismo método sirva para cualquier tipo de dato:

```python
DESC = False

def clave(x):
    return x

def texto(x):
    return str(x)
```

- **`DESC`**: si es `False`, ordena de menor a mayor (o de A a Z). Si es `True`, de mayor a menor.
- **`clave(x)`**: devuelve el valor por el que se compara. Para números es el mismo número. Para nombres, es el texto en minúsculas y sin acentos, así "Álvaro" queda junto a "Ana".
- **`texto(x)`**: devuelve cómo se muestra el dato en pantalla. Por ejemplo, un precio se muestra como `$12.50`.

### 5.3 Funciones de presentación

```python
def lista_txt(lista):
    return "[" + ", ".join(texto(x) for x in lista) + "]"
```

Convierte una lista en texto legible, usando `texto()` en cada elemento. Es la que permite imprimir `[3, 8, 15]` o `[$9.99, $12.50]` según el programa.

`resultado_final(lista)` imprime el resultado dentro de un recuadro de guiones. En el programa final también existe `banner(t)`, que dibuja el encabezado de cada método con líneas de `=`.

### 5.4 La comparación: `antes()`

```python
def antes(x, y):
    return clave(x) >= clave(y) if DESC else clave(x) <= clave(y)
```

Responde: *¿`x` debe salir antes que `y`?* Si dos datos son iguales, sale primero el de la izquierda (el de la lista A o el primer tramo).

### 5.5 Método 1: Intercalación (`intercalar`)

**Idea:** se tienen dos listas ya ordenadas, `a` y `b`. Se compara el primer elemento que queda de cada una. El que deba ir antes pasa al resultado y se avanza en esa lista. Se repite hasta que una se acabe; lo que sobre de la otra se copia al final.

```python
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
        ...imprime el paso si visible...
        paso += 1
    ...imprime lo que sobra si visible...
    return r + a[i:] + b[j:]
```

Partes del código:

| Parte | Qué hace |
|-------|----------|
| `i`, `j` | Posición actual en `a` y en `b`. |
| `u, v = a[i], b[j]` | Los dos elementos que se comparan. |
| `antes(u, v)` | Decide cuál sale. |
| `r.append(x)` | Agrega el ganador al resultado. |
| `return r + a[i:] + b[j:]` | Une el resultado con lo que sobró de la lista que aún tenía elementos. |
| `visible=True` | Imprime cada comparación con el resultado parcial. |
| `na`, `nb` | Nombres que se muestran para indicar de dónde salió el elemento (A y B, F1 y F2, tramo izq y tramo der, etc.). |

**Caso especial (programa 1):** `intercalacion_sin_repetidos()` hace lo mismo, pero si los dos elementos son iguales (es el mismo libro en las dos bibliotecas), lo escribe **una sola vez** y avanza en ambas listas.

**Complejidad:** cada elemento se compara y se copia una sola vez, así que es O(n + m).

### 5.6 Método 2: Mezcla Directa (`mezcla_directa`)

**Idea:** se empieza con bloques de tamaño 1 (cada dato es un bloque ordenado). En cada pasada se reparten los bloques alternadamente en dos archivos, F1 y F2, y se mezcla el bloque 1 de F1 con el bloque 1 de F2, el bloque 2 con el bloque 2, etc. Después el tamaño de bloque se duplica. Se repite hasta que el bloque abarca todos los datos.

```python
def mezcla_directa(datos):
    datos = list(datos)
    n, longitud, paso = len(datos), 1, 1
    while longitud < n:
        bloques = [datos[i:i + longitud] for i in range(0, n, longitud)]
        f1, f2 = bloques[0::2], bloques[1::2]
        ...
        resultado = []
        for k, b1 in enumerate(f1):
            b2 = f2[k] if k < len(f2) else []
            mezcla = intercalar(b1, b2, True, ...) if b2 else b1
            resultado += mezcla
        datos = resultado
        longitud *= 2
        paso += 1
    return datos
```

Fases de cada pasada:

1. **Dividir en bloques:** `bloques` corta la lista en trozos de tamaño `longitud`.
2. **Distribución:** `bloques[0::2]` (los de posición par) van a **F1** y `bloques[1::2]` (los de posición impar) van a **F2**.
3. **Mezcla:** cada bloque de F1 se intercala con su pareja de F2. Si F2 se quedó sin pareja, el bloque se copia igual.
4. **Duplicar:** `longitud *= 2` para la siguiente pasada.
5. **Condición de paro:** el ciclo termina cuando `longitud >= n`.

**Ejemplo con 8 datos:** bloques de 1, luego de 2, luego de 4 → **3 pasadas**.

**Complejidad:** el número de pasadas es ⌈log₂ n⌉ y en cada una se recorren los n datos, así que es O(n log n).

### 5.7 Método 3: Mezcla Equilibrada (`mezcla_equilibrada`)

**Idea:** se detectan los tramos que ya vienen ordenados y se reparten por turnos entre N archivos de entrada. En cada pasada se toma **un tramo de cada archivo de entrada**, se mezclan y el resultado se escribe en uno de los N archivos de salida, por turnos. Al terminar la pasada, los archivos de salida pasan a ser la entrada de la siguiente. Se repite hasta que queda un solo tramo.

Partes del código:

**a) Detectar tramos: `dividir_en_runs(datos)`**

```python
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
```

Recorre los datos. Mientras cada dato pueda ir después del anterior, sigue en el mismo tramo. Cuando se rompe el orden, cierra el tramo y empieza otro.

**b) Distribución inicial**

```python
entrada = [[] for _ in range(vias)]
for k, run in enumerate(runs):
    entrada[k % vias].append(run)
```

`k % vias` reparte los tramos por turnos: tramo 1 al archivo 1, tramo 2 al archivo 2, tramo 3 al archivo 1, etc.

**c) Ciclo de pasadas**

```python
while sum(len(f) for f in entrada) > 1:
    salida = [[] for _ in range(vias)]
    destino = 0
    while any(entrada):
        tomados = [f.pop(0) for f in entrada if f]
        mezclado = tomados[0]
        for t in tomados[1:]:
            mezclado = intercalar(mezclado, t, True, ...)
        salida[destino].append(mezclado)
        destino = (destino + 1) % vias
    entrada = salida
```

| Parte | Qué hace |
|-------|----------|
| `while sum(len(f) ...) > 1` | Sigue mientras queden 2 o más tramos en total. |
| `while any(entrada)` | Cada vuelta es una **ronda**: mientras algún archivo tenga tramos. |
| `f.pop(0)` | Saca el primer tramo de cada archivo de entrada que aún tenga. |
| `intercalar(...)` | Mezcla los tramos tomados. Con más de 2 vías, mezcla de dos en dos de forma sucesiva. |
| `destino = (destino + 1) % vias` | El resultado se escribe en el siguiente archivo de salida, por turnos. |
| `entrada = salida` | Las salidas se vuelven la entrada de la siguiente pasada. |

**d) Resultado:** cuando solo queda un tramo, ese es la lista ordenada: `next(f[0] for f in entrada if f)`.

**Complejidad:** con N vías, el número de pasadas es aproximadamente ⌈log_N(tramos)⌉. **Más vías significan menos pasadas.** Por eso el programa 8 usa 3 vías.

### 5.8 Versiones con archivos reales (programas 6 y 9)

Hacen lo mismo que las versiones simuladas, pero leen y escriben archivos `.txt`.

**Programa 6, mezcla directa con archivos:**

| Función | Qué hace |
|---------|----------|
| `distribuir(origen, longitud)` | Lee bloques de `longitud` líneas con `islice` y los escribe alternadamente en `aux1.txt` y `aux2.txt`. |
| `mezclar(destino, longitud)` | Lee un bloque de cada auxiliar, los intercala y escribe el resultado en `destino`. |
| `mezcla_directa_archivo()` | Copia `edades.txt` a `trabajo.txt`, repite distribuir y mezclar duplicando el bloque, y al final renombra a `edades_ordenadas.txt` y borra los auxiliares. |

**Programa 9, mezcla equilibrada con archivos:**

Como un archivo de texto no tiene "tramos" por sí solo, cada tramo termina con una línea que contiene `#`. Así se sabe dónde acaba uno y empieza otro.

| Función | Qué hace |
|---------|----------|
| `leer_runs(ruta)` | Generador que entrega un tramo a la vez leyendo hasta encontrar `#`. |
| `distribuir_inicial()` | Detecta los tramos de `estaturas.txt` y los escribe por turnos en `entrada1.txt` y `entrada2.txt`. |
| `pasada(entradas, salidas)` | Hace una pasada completa: toma un tramo de cada entrada, los mezcla y escribe en las salidas por turnos. |
| `ExitStack` | Permite abrir varios archivos a la vez y cerrarlos todos al terminar. |

Al final se guarda el resultado en `estaturas_ordenadas.txt` y se borran los archivos temporales.

### 5.9 Captura y validación de datos

Cada programa tiene una función `pedir_...()` con un ciclo `while True` que repite la pregunta hasta que el dato sea válido:

```python
def pedir_calificaciones():
    while True:
        t = input("Calificaciones (números separados por espacio, ej: 8 6.5 9 7): ")
        try:
            numeros = [float(x) for x in t.split()]
        except ValueError:
            print("  Escribe solo números separados por espacio.")
            continue
        if len(numeros) < 2:
            print("  Escribe al menos 2 números.")
            continue
        return numeros
```

- `t.split()` separa lo que escribes por espacios.
- `float(x)` (o `int(x)`) convierte cada dato; si falla, `ValueError` activa el mensaje de error.
- Si hay muy pocos datos, también avisa y vuelve a preguntar.

En el programa final, `tipo(tokens)` detecta automáticamente si los datos son enteros, decimales o texto, y `pedir_tokens()` y `pedir_vias()` hacen la captura y validación.

### 5.10 Menú y control de flujo

Cada programa individual tiene dos funciones que definen su ejercicio:

- **`ejemplo()`**: llama a `resolver(...)` con datos ya escritos en el código.
- **`propio()`**: pide los datos con `pedir_...()` y llama al mismo `resolver(...)`.

Y dos funciones controlan el recorrido:

```python
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
        ...muestra las 3 opciones...
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
```

`menu()` repite el ciclo hasta que eliges salir. Después de cada resultado llama a `volver()`: si devuelve `True`, se muestra de nuevo el menú; si devuelve `False`, el programa termina.

### 5.11 El programa final (`programa_final_todos_los_metodos.py`)

Reúne los tres métodos en un solo programa de 291 líneas. Además de las funciones de las secciones anteriores tiene:

| Función | Qué hace |
|---------|----------|
| `banner(t)` | Dibuja el encabezado de cada método. |
| `metodo_intercalacion(a, b)` | Muestra el encabezado, las listas, el paso a paso y el resultado. |
| `metodo_mezcla_directa(datos)` | Igual, para la mezcla directa. |
| `metodo_mezcla_equilibrada(datos, vias)` | Igual, para la mezcla equilibrada. |
| `ejemplo_intercalacion()`, `ejemplo_mezcla_directa()`, `ejemplo_mezcla_equilibrada()`, `ejemplo_todos()` | Ejemplos ya resueltos de cada método. |
| `propio_intercalacion()`, `propio_mezcla_directa()`, `propio_mezcla_equilibrada()` | Piden tus datos y resuelven con el método elegido. |
| `OPCIONES` | Diccionario que relaciona cada número del menú con la función que se ejecuta. |
| `mostrar_menu()` | Dibuja el menú principal de 8 opciones. |

Para ejecutar la opción elegida, `menu()` hace simplemente `OPCIONES[opcion]()`.

---

## 6. Funcionamiento externo (al ejecutarlo en la terminal)

### 6.1 Programas individuales (1 al 9)

Al ejecutar cualquiera de ellos aparece este menú:

```
=== MEZCLA DIRECTA: CALIFICACIONES ===
1. Resolver tu propio ejercicio
2. Resolver el ejemplo
3. Salir
Elige una opción:
```

| Opción | Qué pasa |
|--------|----------|
| **1** | El programa te pide tus datos en **una sola línea** (con un ejemplo en la misma pregunta) y los resuelve paso a paso. |
| **2** | Resuelve el ejemplo que ya trae, mostrando todos los pasos. |
| **3** | Termina el programa. |
| Otra cosa | Muestra `Opción inválida.` y vuelve a mostrar el menú. |

Después de mostrar cualquier resultado aparece:

```
1. Regresar al menú principal
2. Salir del programa
Elige una opción:
```

Con `1` vuelves al menú principal; con `2` el programa termina con el mensaje `Programa terminado.`

### 6.2 Programa final (10)

Al ejecutarlo se ve este menú:

```
################################################################
            ORDENAMIENTO EXTERNO - TODOS LOS MÉTODOS
################################################################

  EJEMPLOS YA RESUELTOS (paso a paso)
    1. Ejemplo de Intercalación
    2. Ejemplo de Mezcla Directa
    3. Ejemplo de Mezcla Equilibrada
    4. Ver los tres ejemplos

  RESUELVE TU PROPIO EJERCICIO (paso a paso)
    5. Con Intercalación
    6. Con Mezcla Directa
    7. Con Mezcla Equilibrada

    8. Salir

Elige una opción (1-8):
```

| Opción | Qué pasa |
|--------|----------|
| **1, 2, 3** | Resuelve un ejemplo del método elegido. |
| **4** | Resuelve los tres ejemplos, uno después de otro. |
| **5, 6, 7** | Eliges el método y escribes tus datos (números o palabras separados por espacio). La opción 7 también te pide el número de vías (2 a 5). |
| **8** | Termina el programa. |

Después de cada resultado puedes **regresar al menú principal** o **salir**.

### 6.3 Cómo se ve la resolución

**Intercalación** (opción 1 del programa final):

```
================================================================
                    MÉTODO 1: INTERCALACIÓN
================================================================
Lista A: [3, 8, 15, 22, 40]
Lista B: [1, 9, 16, 27, 35, 50]

Se comparan los primeros elementos de A y B; el menor sale al resultado.
Paso a paso:
   Paso 1: 3 vs 1 -> sale 1 (B)  =>  [1]
   Paso 2: 3 vs 9 -> sale 3 (A)  =>  [1, 3]
   Paso 3: 8 vs 9 -> sale 8 (A)  =>  [1, 3, 8]
   ...
   Paso 10: 40 vs 50 -> sale 40 (A)  =>  [1, 3, 8, 9, 15, 16, 22, 27, 35, 40]
   Sobran de B: [50] -> se copian al final
   Resultado: [1, 3, 8, 9, 15, 16, 22, 27, 35, 40, 50]

------------------------------------------------------------
  RESULTADO FINAL: [1, 3, 8, 9, 15, 16, 22, 27, 35, 40, 50]
------------------------------------------------------------
```

**Mezcla Directa** (opción 2, primera pasada):

```
================================================================
                    MÉTODO 2: MEZCLA DIRECTA
================================================================
Datos originales: [38, 27, 43, 3, 9, 82, 10, 55]

PASO 1: bloques de tamaño 1
  Distribución:
    F1: [38] [43] [9] [10]
    F2: [27] [3] [82] [55]
  Mezcla bloque por bloque:
    Bloque 1: [38] con [27]
      Paso 1: 38 vs 27 -> sale 27 (F2)  =>  [27]
      Sobran de F1: [38] -> se copian al final
      Resultado: [27, 38]
    ...
  Resultado del paso 1: [27, 38, 3, 43, 9, 82, 10, 55]
```

Después siguen el PASO 2 (bloques de 2) y el PASO 3 (bloques de 4), hasta el resultado final.

**Mezcla Equilibrada** (opción 3, inicio):

```
================================================================
             MÉTODO 3: MEZCLA EQUILIBRADA (2 VÍAS)
================================================================
Datos originales: [17, 31, 5, 59, 13, 41, 43, 67, 11, 23, 29, 47, 3, 7]

PASO 0: detectar los tramos que ya están ordenados (5 tramos)
    Tramo 1: [17, 31] -> Archivo 1
    Tramo 2: [5, 59] -> Archivo 2
    Tramo 3: [13, 41, 43, 67] -> Archivo 1
    Tramo 4: [11, 23, 29, 47] -> Archivo 2
    Tramo 5: [3, 7] -> Archivo 1
  Archivos de entrada:
    Archivo 1: [17, 31] [13, 41, 43, 67] [3, 7]
    Archivo 2: [5, 59] [11, 23, 29, 47]

PASO 1: mezclar un tramo de cada archivo de entrada
  Ronda 1: se toman [17, 31] (archivo 1) y [5, 59] (archivo 2)
      Paso 1: 17 vs 5 -> sale 5 (tramo der)  =>  [5]
      ...
      Resultado: [5, 17, 31, 59]
    => se escribe en el archivo de salida 1
```

### 6.4 Leyenda: cómo leer la salida

| Texto en pantalla | Significa |
|-------------------|-----------|
| `PASO n` (mayúsculas) | Una pasada completa del método (distribuir y mezclar). |
| `Paso n` (con sangría) | Una comparación dentro de una intercalación. |
| `F1`, `F2` | Los dos archivos auxiliares de la mezcla directa. |
| `Bloque k` | La pareja de bloques que se mezcla en ese momento. |
| `Tramo k` | Un tramo ya ordenado detectado en los datos. |
| `Ronda k` | Una vuelta dentro de una pasada de mezcla equilibrada: se toma un tramo de cada archivo. |
| `Archivo n` | Un archivo de entrada o de salida de la mezcla equilibrada. |
| `=>` | Cómo va quedando el resultado parcial. |
| `Sobran de X ... se copian al final` | Una lista se acabó y el resto de la otra pasa completo. |
| `RESULTADO FINAL` | La lista ya ordenada. |

### 6.5 Cómo capturar tu propio ejercicio

Elige la opción para resolver tu propio ejercicio y escribe los datos en **una línea, separados por espacio**:

| Programa | Qué escribir | Ejemplo |
|----------|--------------|---------|
| 1. Catálogo de libros | Títulos de cada biblioteca, separados por **coma** | `Redes,Cálculo,Álgebra` |
| 2. Turnos de ventanillas | Números enteros por ventanilla | `3 8 15` |
| 3. Precios de tiendas | Números (acepta decimales) por tienda | `12.5 30 45.9` |
| 4. Calificaciones | Números (acepta decimales) | `8 6.5 9 7` |
| 5. Nombres de asistencia | Nombres separados por espacio | `Mario Ana Zoe Luis` |
| 6. Edades (archivos) | Números enteros | `25 31 18 40` |
| 7. Puntajes de videojuego | Números enteros | `1500 320 980 2200` |
| 8. Temperaturas | Números (acepta decimales y negativos) | `28 31.5 26 30` |
| 9. Estaturas (archivos) | Números enteros | `165 172 158 180` |
| 10. Programa final | Números o palabras separados por espacio; en mezcla equilibrada, además el número de vías (2 a 5) | `9 4 7 1 8 2` o `mango pera uva` |

En los programas de intercalación (1, 2, 3 y la opción 5 del final) **no necesitas escribir las listas en orden**: el programa las ordena antes de intercalarlas.

### 6.6 Mensajes y validaciones

Si escribes algo incorrecto, el programa no se cierra: te avisa y vuelve a pedir el dato.

| Situación | Mensaje |
|-----------|---------|
| Letras donde van números | `Escribe solo números separados por espacio.` |
| Muy pocos datos | `Escribe al menos 2 números.` |
| Opción de menú que no existe | `Opción inválida.` |
| Número de vías fuera de 2 a 5 | `Escribe un número entre 2 y 5.` |

### 6.7 Archivos que se generan

Solo los programas con archivos reales crean archivos en la carpeta donde se ejecutan:

| Programa | Archivos de datos | Temporales (se borran al terminar) |
|----------|-------------------|------------------------------------|
| 6. Edades | `edades.txt` (original), `edades_ordenadas.txt` (resultado) | `trabajo.txt`, `aux1.txt`, `aux2.txt` |
| 9. Estaturas | `estaturas.txt` (original), `estaturas_ordenadas.txt` (resultado) | `entrada1.txt`, `entrada2.txt`, `salida1.txt`, `salida2.txt` |

Los demás programas no crean ningún archivo.

---

## 7. Complejidad de los métodos

| Método | Pasadas | Tiempo |
|--------|---------|--------|
| Intercalación | 1 | O(n + m) |
| Mezcla Directa | ⌈log₂ n⌉ | O(n log n) |
| Mezcla Equilibrada (N vías) | ≈ ⌈log_N(tramos)⌉ | O(n log_N t), con t = tramos |

Donde n es la cantidad de datos. En la mezcla equilibrada, mientras más vías y más tramos ya ordenados haya, menos pasadas se necesitan.

---

## 8. Notas

- Como los programas muestran **cada comparación**, con listas muy largas la salida es extensa. Para clase conviene usar de 8 a 15 elementos.
- Cuando dos datos son iguales, sale primero el de la lista A (o del tramo izquierdo). Así el orden es estable.
- Los programas fueron probados con ejemplos y con cientos de listas aleatorias para comprobar que el resultado siempre queda bien ordenado.

---

## 9. Programa gráfico de los tres métodos (Tkinter)

Además de los programas que funcionan desde la terminal, el proyecto incluye un programa con **interfaz gráfica desarrollado en Python con Tkinter**, que reúne los tres métodos de ordenamiento externo en una sola aplicación:

1. Intercalación.
2. Mezcla Directa.
3. Mezcla Equilibrada.

El programa permite seleccionar el método que se desea utilizar, resolver ejercicios de ejemplo o ingresar datos propios. A diferencia de los programas de terminal, toda la interacción se realiza mediante ventanas, botones, campos de texto y áreas donde se muestra el procedimiento.

### 9.1 Funcionamiento interno

El programa está organizado mediante la clase `AplicacionOrdenamiento`, que contiene las funciones necesarias para crear la interfaz, recibir los datos, aplicar los métodos de ordenamiento y mostrar los resultados.

| Función | Qué hace |
|---------|----------|
| `__init__()` | Inicializa la aplicación, configura la ventana principal y prepara la interfaz. |
| `crear_encabezado()` | Construye el encabezado visual de la aplicación. |
| `limpiar_pantalla()` | Limpia el contenido anterior para mostrar una nueva pantalla. |
| `crear_titulo()` | Coloca los títulos correspondientes a cada sección. |
| `crear_boton()` | Crea los botones que permiten navegar y ejecutar las opciones. |
| `mostrar_menu_principal()` | Presenta los tres métodos de ordenamiento y la opción para salir. |
| `mostrar_menu_metodo()` | Muestra las opciones correspondientes al método seleccionado. |
| `mostrar_entrada_datos()` | Presenta la pantalla donde el usuario indica cuántas listas desea ingresar. |
| `crear_campos_listas()` | Genera dinámicamente los campos de texto según la cantidad de listas indicada. |
| `clave_texto()` | Prepara los textos para compararlos alfabéticamente, sin distinguir mayúsculas ni acentos. |
| `convertir_tiempo()` | Convierte los tiempos a segundos para poder compararlos correctamente. |
| `convertir_valor()` | Identifica y convierte los datos al tipo correspondiente para ordenarlos. |
| `interpretar_datos()` | Separa y analiza los valores ingresados por el usuario. |
| `mostrar_lista()` | Da formato a las listas para presentarlas en pantalla. |
| `mezclar()` | Combina dos secuencias ordenadas mediante comparaciones entre sus elementos. |
| `ordenar_previo()` | Ordena previamente los datos cuando es necesario para preparar las secuencias. |
| `intercalacion()` | Aplica el método de intercalación y muestra cómo se combinan las listas. |
| `mezcla_directa()` | Divide los datos en bloques, los distribuye y los mezcla en pasadas sucesivas. |
| `mezcla_equilibrada()` | Distribuye las corridas entre archivos auxiliares simulados y realiza las mezclas hasta obtener una secuencia ordenada. |
| `resolver_ejemplo()` | Ejecuta el ejercicio de ejemplo seleccionado para el método correspondiente. |
| `resolver_datos()` | Recibe los datos propios del usuario y ejecuta el método seleccionado. |
| `mostrar_resultado()` | Presenta el procedimiento realizado y el resultado final. |
| `escribir()` | Muestra la información del procedimiento en el área de resultados. |
| `salir()` | Cierra la aplicación. |

**Captura y procesamiento de datos**

El usuario puede trabajar con diferentes tipos de información:

- Números enteros.
- Números decimales.
- Palabras y nombres.
- Tiempos en formato `mm:ss` o `hh:mm:ss`.
- Datos con nombre y valor, por ejemplo: `Ana=15, Luis=8`.

El programa identifica el tipo de información ingresada y utiliza el valor correspondiente para realizar las comparaciones. En el caso de los tiempos, los convierte a segundos; cuando se utilizan nombres con valores, conserva el nombre y ordena de acuerdo con el valor numérico o temporal.

Las listas deben contener un mismo tipo de dato y los datos de las diferentes listas también deben ser compatibles entre sí. Para separar los elementos se pueden utilizar comas, punto y coma o saltos de línea. Los números decimales se escriben utilizando punto.

**Aplicación de los métodos**

- **Intercalación:** recibe las listas ingresadas, las prepara para que estén ordenadas y después combina sus elementos comparando los valores correspondientes hasta formar una sola lista ordenada.
- **Mezcla Directa:** reúne los datos ingresados en una secuencia, forma bloques de tamaño progresivo y realiza las mezclas necesarias hasta ordenar todos los elementos.
- **Mezcla Equilibrada:** trabaja con corridas ordenadas que se distribuyen alternadamente entre F1 y F2. Después combina las corridas y coloca los resultados en F3 y F4. Este proceso se repite en diferentes pasadas hasta obtener una sola corrida ordenada.

En esta versión gráfica, los archivos auxiliares se representan mediante listas de Python para mostrar visualmente el procedimiento, sin crear archivos físicos en la computadora.

### 9.2 Funcionamiento externo (interfaz gráfica)

Al ejecutar el programa aparece una ventana principal con el nombre del proyecto y un menú para seleccionar el método de ordenamiento.

**Menú principal**

El usuario puede elegir entre las siguientes opciones:

| Opción | Qué pasa |
|--------|----------|
| Intercalación | Abre el menú de ejercicios de intercalación. |
| Mezcla Directa | Abre el menú de ejercicios de mezcla directa. |
| Mezcla Equilibrada | Abre el menú de ejercicios de mezcla equilibrada. |
| Salir del programa | Cierra la aplicación. |

**Menú de cada método**

Después de seleccionar un método, aparece un segundo menú con las opciones disponibles:

| Opción | Qué pasa |
|--------|----------|
| Ejemplo 1 | Ejecuta el primer ejercicio ya preparado. |
| Ejemplo 2 | Ejecuta el segundo ejercicio ya preparado. |
| Ejemplo 3 | Ejecuta el tercer ejercicio ya preparado. |
| Resolver mi propio ejercicio | Permite ingresar los datos que se desean ordenar. |
| Regresar al menú principal | Vuelve a la pantalla donde se selecciona el método. |
| Salir del programa | Cierra la aplicación. |

**Resolución de un ejercicio propio**

Cuando el usuario selecciona la opción para resolver su propio ejercicio, el programa solicita primero la cantidad de listas que desea ingresar. Después genera automáticamente los campos necesarios para capturar cada lista.

Por ejemplo, si el usuario indica que utilizará tres listas, aparecen tres campos de entrada:

```text
Cantidad de listas: 3

Lista 1: 23, 15, 8
Lista 2: 42, 31, 19
Lista 3: 56, 12, 35
```

Una vez ingresados los datos, el usuario puede ejecutar el método seleccionado. El programa procesa las listas y presenta el procedimiento paso a paso.

**Visualización de resultados**

La pantalla de resultados muestra la información del ejercicio realizado, incluyendo:

- Cantidad de listas ingresadas.
- Contenido de cada lista.
- Datos que se utilizarán para aplicar el método.
- Distribución de bloques o corridas, cuando corresponde.
- Comparaciones realizadas durante las mezclas.
- Pasadas del método.
- Resultado final ordenado.

El área de resultados permite consultar el procedimiento completo, incluso cuando ocupa más espacio que el disponible inicialmente en la ventana.

**Regreso y salida**

Después de resolver un ejemplo o un ejercicio propio, el usuario puede elegir entre dos opciones:

1. **Regresar al menú principal:** vuelve a la pantalla inicial para seleccionar otro método.
2. **Salir del programa:** cierra la aplicación.

De esta manera, el usuario puede resolver diferentes ejercicios sin tener que cerrar y ejecutar nuevamente el programa.

### 9.3 Diferencias entre la versión de terminal y la versión gráfica

| Característica | Programas de terminal | Programa gráfico |
|----------------|-----------------------|------------------|
| Interfaz | Texto en consola. | Ventanas con Tkinter. |
| Selección de métodos | Mediante números escritos. | Mediante botones. |
| Captura de datos | Mediante la terminal. | Mediante campos de entrada. |
| Cantidad de listas | Depende de cada programa. | El usuario indica cuántas listas necesita. |
| Ejercicios | Ejemplos definidos en cada archivo. | Tres ejemplos seleccionables por método. |
| Procedimiento | Se imprime en la terminal. | Se muestra en un área de resultados. |
| Tipos de datos | Dependen de cada ejercicio. | Enteros, decimales, palabras, tiempos y datos con nombre y valor. |
| Navegación | Menús escritos. | Botones para regresar o salir. |

### 9.4 Ejecución del programa gráfico

Para ejecutar la aplicación se necesita Python 3.8 o superior. Tkinter forma parte de la instalación estándar de Python en la mayoría de las instalaciones de escritorio.

Abre una terminal en la carpeta donde se encuentra el archivo del programa y ejecuta:

```bash
python nombre_del_programa.py
```

En caso de que el sistema utilice el comando `python3`, se puede ejecutar de la siguiente manera:

```bash
python3 nombre_del_programa.py
```

Una vez iniciado, se abrirá la ventana principal y se podrá comenzar a utilizar la aplicación.

