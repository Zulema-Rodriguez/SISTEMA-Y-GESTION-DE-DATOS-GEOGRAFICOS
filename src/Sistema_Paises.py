# Archivo principal del sistema de gestión de países
import csv
import os
import unicodedata

#Funcion quitar acentos 
def quitar_acentos(texto):
    """
    Recibe un texto y devuelve el mismo texto sin acentos.
    Ejemplo: 'Japón' -> 'Japon'
    """
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

#   FUNCION LECTURA DE ARCHIVO CSV
def leer_csv():
    paises = []  # Lista donde vamos a guardar cada país como diccionario

    try:
        # Abrimos el archivo CSV en modo lectura
        with open("datos/datos_geograficos.csv", "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)  # Lee cada fila como diccionario

            # Recorremos cada fila del CSV
            for fila in lector:
                try:
                    # Convertimos los valores numéricos a int
                    paises.append({
                        "nombre": fila["nombre"],
                        "poblacion": int(fila["poblacion"]),
                        "superficie": int(fila["superficie"]),
                        "continente": fila["continente"]
                    })
                except (ValueError, KeyError) as e:
                    # Si la fila tiene un dato inválido o le falta una columna, la saltamos
                    print(f"Fila inválida en el CSV, se omite: {e}")

    except FileNotFoundError:
        # Si el archivo todavía no existe, avisamos y seguimos con la lista vacía
        print("No se encontró el archivo de datos. Se comenzará con una lista vacía.")
    except Exception as e:
        # Cualquier otro error al leer el archivo se muestra, pero no rompe el programa
        print(f"Error inesperado al leer el archivo CSV: {e}")

    return paises  # Devolvemos la lista completa de países (puede quedar vacía si hubo error)

#   FUNCION GUARDAR ARCHIVO CSV
def guardar_csv(lista_paises):
    # Intentamos crear la carpeta (si no existe) y guardar el archivo
    try:
        # Nos aseguramos de que exista la carpeta "datos"
        os.makedirs("datos", exist_ok=True)

        # Abrimos el archivo CSV en modo escritura (reescribe todo)
        with open("datos/datos_geograficos.csv", "w", newline="", encoding="utf-8") as archivo:

            # Definimos los nombres de las columnas del CSV
            campos = ["nombre", "poblacion", "superficie", "continente"]

            # Creamos un escritor de diccionarios
            escritor = csv.DictWriter(archivo, fieldnames=campos)

            escritor.writeheader()  # Escribimos la fila de encabezados

            # Escribimos cada país (diccionario) como una fila del CSV
            for pais in lista_paises:
                escritor.writerow(pais)

    except Exception as e:
        # Capturamos cualquier error al escribir el archivo (permisos, disco lleno, etc.)
        print(f"Error al guardar el archivo CSV: {e}")

#Funcion eleccion de continentes validos
def elegir_continente():
    """
    Muestra una lista numerada de continentes y devuelve el seleccionado.
    Evita errores de tipeo, acentos y validaciones innecesarias.
    """
    continentes = ["América", "Europa", "Asia", "África", "Oceanía"]

    print("Seleccione un continente:")
    for i, cont in enumerate(continentes, start=1):
        print(f"{i}) {cont}")

    opcion = input("Ingrese el número del continente: ").strip()

    # Validamos que sea un número válido dentro del rango
    while not opcion.isdigit() or int(opcion) < 1 or int(opcion) > len(continentes):
        print("Opción inválida. Intente nuevamente.")
        opcion = input("Ingrese el número del continente: ").strip()

    # Devolvemos el continente elegido
    return continentes[int(opcion) - 1]

#Funcion al elegir #1 en el menu-
def agregar_pais():
    try:
        paises = leer_csv()   # ← LEER CSV

        # Pedir nombre
        nombre = input("Nombre del país: ").strip()
        while nombre == "":
            print("No puede estar vacío.")
            nombre = input("Nombre del país: ").strip()

        # VALIDAR QUE NO TENGA NÚMEROS NI SÍMBOLOS
        while not nombre.replace(" ", "").isalpha():
            print("El nombre no puede contener números ni símbolos.")
            nombre = input("Nombre del país: ").strip()

        # Validar duplicado (comparación sin acentos)
        nombre_normalizado = quitar_acentos(nombre.lower().replace(" ", ""))

        for p in paises:
            nombre_csv_normalizado = quitar_acentos(p["nombre"].lower().replace(" ", ""))
            if nombre_normalizado == nombre_csv_normalizado:
                print("Ese país ya existe.")
                return

        # Población
        while True:
            poblacion = input("Población: ")
            try:
                poblacion = int(poblacion)
                break
            except ValueError:
                print("Debe ser un número entero.")

        # Superficie
        while True:
            superficie = input("Superficie: ")
            try:
                superficie = int(superficie)
                break
            except ValueError:
                print("Debe ser un número entero.")

        # Continente
        continente_seleccionado = elegir_continente()

        # Agregar a la lista
        paises.append({
            "nombre": nombre,
            "poblacion": poblacion,
            "superficie": superficie,
            "continente": continente_seleccionado
        })

        guardar_csv(paises)   # ← GUARDAR CSV

        print("País agregado correctamente.")

    except Exception as e:
        print(f"Ocurrió un error inesperado al agregar el país: {e}")

#Funcion al elegir #4 en el menu-
def filtrar_paises():
    # un error inesperado cierre el programa
    try:
        # Leemos todos los países desde el archivo CSV
        paises = leer_csv()

        # Si la lista está vacía, no hay nada para filtrar
        if len(paises) == 0:
            print("No hay datos cargados en el sistema.")
            return

        # Mostramos el menú de filtros disponibles
        print("=== FILTRO DE PAÍSES ===")
        print("1) Filtrar por continente")
        print("2) Filtrar por rango de población")

        # Leemos la opción elegida por el usuario
        opcion = input("Elija una opción: ").strip()

        # OPCIÓN 1  FILTRAR POR CONTINENTE
        if opcion == "1":
            # Usamos la función elegir_continente() para evitar errores de tipeo
            print("Seleccione el continente:")
            continente = elegir_continente()

            # Normalizamos el continente elegido para comparar correctamente
            cont_normalizado = quitar_acentos(continente.lower())

            resultados = []

            # Recorremos todos los países buscando coincidencias exactas de continente
            for pais in paises:
                # Normalizamos también el continente del país
                cont_pais = quitar_acentos(pais["continente"].lower())

                # Si coinciden, lo agregamos a la lista de resultados
                if cont_pais == cont_normalizado:
                    resultados.append(pais)

            # Si no se encontró ningún país, avisamos
            if len(resultados) == 0:
                print("No se encontraron países en ese continente.")
                return

            # Mostramos los países encontrados
            print(f"Países en el continente {continente}:")
            for p in resultados:
                print(f"- {p['nombre']} (Población: {p['poblacion']}, Superficie: {p['superficie']})")

        # OPCIÓN 2  FILTRAR POR RANGO DE POBLACIÓN
        elif opcion == "2":
            try:
                # Pedimos los límites del rango
                minimo = int(input("Población mínima: "))
                maximo = int(input("Población máxima: "))
            except ValueError:
                # Si el usuario ingresa algo que no es número
                print("Debe ingresar números enteros.")
                return

            # Validamos que el rango sea correcto
            if minimo > maximo:
                print("El rango es inválido (mínimo mayor que máximo).")
                return

            resultados = []

            # Recorremos todos los países buscando los que estén dentro del rango
            for pais in paises:
                if minimo <= pais["poblacion"] <= maximo:
                    resultados.append(pais)

            # Si no se encontró ningún país, avisamos
            if len(resultados) == 0:
                print("No se encontraron países en ese rango de población.")
                return

            # Mostramos los países encontrados
            print(f"Países con población entre {minimo} y {maximo}:")
            for p in resultados:
                print(f"- {p['nombre']} (Población: {p['poblacion']}, Superficie: {p['superficie']}, Continente: {p['continente']})")

        # OPCIÓN INVÁLIDA
        else:
            print("Opción de filtro inválida.")

    except Exception as e:
        # Capturamos cualquier error inesperado y evitamos que el programa se cierre
        print(f"Ocurrió un error inesperado al filtrar países: {e}")

#Funcion al elegir #6 en el menu
def estadisticas():
    try:
        # Leemos todos los países desde el archivo CSV
        paises = leer_csv()

        # Si no hay datos cargados, no se puede calcular nada
        if len(paises) == 0:
            print("No hay datos cargados en el sistema.")
            return

        # Inicializamos mayor y menor con el primer país
        mayor = paises[0]
        menor = paises[0]

        # Acumuladores para promedios
        total_poblacion = 0
        total_superficie = 0

        # Diccionario para contar países por continente
        continentes = {}

        # Recorremos todos los países
        for pais in paises:

            # Mayor población
            if pais["poblacion"] > mayor["poblacion"]:
                mayor = pais

            # Menor población
            if pais["poblacion"] < menor["poblacion"]:
                menor = pais

            # Acumular población y superficie
            total_poblacion += pais["poblacion"]
            total_superficie += pais["superficie"]

            # Contar continentes
            cont = pais["continente"]
            if cont not in continentes:
                continentes[cont] = 0
            continentes[cont] += 1

        # Calcular promedios
        promedio_poblacion = total_poblacion / len(paises)
        promedio_superficie = total_superficie / len(paises)

        # Mostrar resultados
        print("=== ESTADÍSTICAS ===")
        print(f"País con mayor población: {mayor['nombre']} ({mayor['poblacion']})")
        print(f"País con menor población: {menor['nombre']} ({menor['poblacion']})")
        print(f"Promedio de población: {promedio_poblacion:.2f}")
        print(f"Promedio de superficie: {promedio_superficie:.2f}")

        print("\nCantidad de países por continente:")
        for cont in continentes:
            print(f"- {cont}: {continentes[cont]}")

    except Exception as e:
        # Captura cualquier error inesperado
        print(f"Ocurrió un error inesperado al calcular las estadísticas: {e}")

#Funcion al elegir #2 en el menu
def actualizar_pais():
    try:
        paises = leer_csv()

        if len(paises) == 0:
            print("No hay datos cargados en el sistema.")
            return

        # Pedimos el nombre del país a actualizar
        nombre = input("Ingrese el nombre del país a actualizar: ").strip()
        while nombre == "":
            print("El nombre no puede estar vacío.")
            nombre = input("Ingrese el nombre del país a actualizar: ").strip()

        # Normalizamos para buscar sin acentos
        nombre_normalizado = quitar_acentos(nombre.lower().replace(" ", ""))

        pais_encontrado = None

        for pais in paises:
            nombre_csv_normalizado = quitar_acentos(pais["nombre"].lower().replace(" ", ""))
            if nombre_normalizado == nombre_csv_normalizado:
                pais_encontrado = pais
                break

        if pais_encontrado is None:
            print("No se encontró un país con ese nombre.")
            return

        # Mostramos datos actuales
        print("Datos actuales del país:")
        print(f"1) Nombre: {pais_encontrado['nombre']}")
        print(f"2) Población: {pais_encontrado['poblacion']}")
        print(f"3) Superficie: {pais_encontrado['superficie']}")
        print(f"4) Continente: {pais_encontrado['continente']}")
        print("0) Cancelar actualización")

        # Menú de selección
        opcion = input("Seleccione el dato que desea modificar: ").strip()

        if opcion == "0":
            print("Actualización cancelada.")
            return

        # -------------------------
        # MODIFICAR NOMBRE
        # -------------------------
        if opcion == "1":
            nuevo_nombre = input("Nuevo nombre: ").strip()
            while nuevo_nombre == "":
                print("El nombre no puede estar vacío.")
                nuevo_nombre = input("Nuevo nombre: ").strip()
            pais_encontrado["nombre"] = nuevo_nombre

        # -------------------------
        # MODIFICAR POBLACIÓN
        # -------------------------
        elif opcion == "2":
            while True:
                nuevo_poblacion = input("Nueva población: ").strip()
                try:
                    nuevo_poblacion = int(nuevo_poblacion)
                    pais_encontrado["poblacion"] = nuevo_poblacion
                    break
                except:
                    print("Debe ser un número entero.")

        # -------------------------
        # MODIFICAR SUPERFICIE
        # -------------------------
        elif opcion == "3":
            while True:
                nuevo_superficie = input("Nueva superficie: ").strip()
                try:
                    nuevo_superficie = int(nuevo_superficie)
                    pais_encontrado["superficie"] = nuevo_superficie
                    break
                except:
                    print("Debe ser un número entero.")

        # -------------------------
        # MODIFICAR CONTINENTE
        # -------------------------
        elif opcion == "4":
            print("Seleccione el nuevo continente:")
            nuevo_continente = elegir_continente()
            pais_encontrado["continente"] = nuevo_continente

        else:
            print("Opción inválida.")
            return

        # Guardamos cambios
        guardar_csv(paises)
        print("País actualizado correctamente.")

    except Exception as e:
        print("Ocurrió un error:", e)

#Funcion al elegir #3 en el menu
def buscar_paises():
    try:
        # Leemos todos los países desde el archivo CSV
        paises = leer_csv()

        # Si no hay datos cargados, no se puede buscar nada
        if len(paises) == 0:
            print("No hay datos cargados en el sistema.")
            return

        # Pedimos el texto de búsqueda al usuario
        texto = input("Ingrese parte del nombre del país a buscar: ").strip()
        while texto == "":
            print("El texto no puede estar vacío.")
            texto = input("Ingrese parte del nombre del país a buscar: ").strip()

        # Normalizamos el texto ingresado:
        # - pasamos a minúsculas
        # - quitamos espacios
        # - quitamos acentos (para que "japon" coincida con "Japón")
        texto_normalizado = quitar_acentos(texto.lower().replace(" ", ""))

        resultados = []

        # Recorremos todos los países buscando coincidencias parciales
        for pais in paises:
            # Normalizamos también el nombre del país del CSV
            # Esto permite buscar correctamente países con acentos
            nombre_normalizado = quitar_acentos(pais["nombre"].lower().replace(" ", ""))

            # Si el texto ingresado aparece dentro del nombre del país, lo agregamos
            if texto_normalizado in nombre_normalizado:
                resultados.append(pais)

        # Si no se encontró ningún país, avisamos
        if len(resultados) == 0:
            print("No se encontró ningún país que coincida con la búsqueda.")
            return

        # Mostramos todos los resultados encontrados
        print("=== RESULTADOS DE LA BÚSQUEDA ===")
        for p in resultados:
            print(f"- {p['nombre']} (Población: {p['poblacion']}, Superficie: {p['superficie']}, Continente: {p['continente']})")

    except Exception as e:
        # Captura cualquier error inesperado
        print("Ocurrió un error:", e)

#Funcion al elegir #5 en el menu
def ordenar_paises():
    try:
        # Leemos todos los países desde el archivo CSV
        paises = leer_csv()

        # Si no hay datos cargados, no se puede ordenar nada
        if len(paises) == 0:
            print("No hay datos cargados en el sistema.")
            return

        # Mostramos las opciones de ordenamiento disponibles
        print("=== ORDENAR PAÍSES ===")
        print("1 - Ordenar por nombre (A-Z)")
        print("2 - Ordenar por población (menor a mayor)")
        print("3 - Ordenar por superficie (menor a mayor)")

        opcion = input("Elija una opción: ").strip()

        # Validamos que la opción sea correcta
        if opcion not in ["1", "2", "3"]:
            print("Opción inválida.")
            return

        # ORDENAMIENTO BURBUJA (bubble sort)
        # Recorremos la lista varias veces para ordenar
        for i in range(len(paises) - 1):
            for j in range(len(paises) - 1 - i):

                # Ordenar por nombre
                if opcion == "1":
                    nombre1 = paises[j]["nombre"].lower()
                    nombre2 = paises[j + 1]["nombre"].lower()

                    # Si están en el orden incorrecto, los intercambiamos
                    if nombre1 > nombre2:
                        paises[j], paises[j + 1] = paises[j + 1], paises[j]

                # Ordenar por población
                elif opcion == "2":
                    if paises[j]["poblacion"] > paises[j + 1]["poblacion"]:
                        paises[j], paises[j + 1] = paises[j + 1], paises[j]

                # Ordenar por superficie
                elif opcion == "3":
                    if paises[j]["superficie"] > paises[j + 1]["superficie"]:
                        paises[j], paises[j + 1] = paises[j + 1], paises[j]

        # Mostramos el resultado del ordenamiento
        print("=== LISTA ORDENADA ===")
        for p in paises:
            print(f"- {p['nombre']} (Población: {p['poblacion']}, Superficie: {p['superficie']}, Continente: {p['continente']})")

    except Exception as e:
        # Captura cualquier error inesperado
        print("Ocurrió un error:", e)

#        MENÚ PRINCIPAL

while True:
    # Envolvemos todo el ciclo del menú para que un error inesperado no cierre el programa
    try:
        print("===== MENÚ PRINCIPAL =====")
        print("1) Agregar país")
        print("2) Actualizar país")
        print("3) Buscar países por nombre")
        print("4) Filtrar países")
        print("5) Ordenar países")
        print("6) Mostrar estadísticas")
        print("0) Salir")
        print("==========================")

        # Leemos la opción elegida por el usuario
        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            # Llama a la función para agregar un país nuevo
            agregar_pais()
            #pass
        elif opcion == "2":
            actualizar_pais()
            #pass
        elif opcion == "3":
            buscar_paises()
            #pass
        elif opcion == "4":
            # Llama a la función para filtrar países por continente o población
            filtrar_paises()
            #pass
        elif opcion == "5":
            ordenar_paises()
            #pass
        elif opcion == "6":
            # Llama a la función que muestra las estadísticas generales
            estadisticas()
            #pass
        elif opcion == "0":
            # Termina el programa
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida. Intente nuevamente.")

    except (KeyboardInterrupt, EOFError):
        # Si el usuario interrumpe la entrada (Ctrl+C / Ctrl+D), salimos prolijamente
        print("\nEntrada interrumpida. Saliendo del sistema...")
        break
    except Exception as e:
        # Cualquier otro error inesperado se muestra y el menú vuelve a aparecer
        print(f"Ocurrió un error inesperado: {e}")
