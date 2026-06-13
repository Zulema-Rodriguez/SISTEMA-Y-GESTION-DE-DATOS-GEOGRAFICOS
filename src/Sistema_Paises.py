# Archivo principal del sistema de gestión de países
import csv

#   FUNCIONES DE ARCHIVO CSV

def leer_csv():
    paises = []  # Lista donde vamos a guardar cada país como diccionario

    # Abrimos el archivo CSV en modo lectura
    with open("datos/datos_geograficos.csv", "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)  # Lee cada fila como diccionario

        # Recorremos cada fila del CSV
        for fila in lector:
            # Convertimos los valores numéricos a int
            paises.append({
                "nombre": fila["nombre"],
                "poblacion": int(fila["poblacion"]),
                "superficie": int(fila["superficie"]),
                "continente": fila["continente"]
            })

    return paises  # Devolvemos la lista completa de países

def guardar_csv(lista_paises):
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

def agregar_pais():
    paises = leer_csv()   # ← LEER CSV

    # Pedir nombre
    nombre = input("Nombre del país: ").strip()
    while nombre == "":
        print("No puede estar vacío.")
        nombre = input("Nombre del país: ").strip()

    # Validar duplicado
    for p in paises:
        if p["nombre"].lower() == nombre.lower():
            print("Ese país ya existe.")
            return

    # Población
    while True:
        poblacion = input("Población: ")
        try:
            poblacion = int(poblacion)
            break
        except:
            print("Debe ser un número entero.")

    # Superficie
    while True:
        superficie = input("Superficie: ")
        try:
            superficie = int(superficie)
            break
        except:
            print("Debe ser un número entero.")

    # Continente
    continente = input("Continente: ").strip()
    while continente == "":
        print("No puede estar vacío.")
        continente = input("Continente: ").strip()

    # Agregar a la lista
    paises.append({
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    })

    guardar_csv(paises)   #  GUARDAR CSV

    print("País agregado correctamente.")

#        MENÚ PRINCIPAL

while True:
    print("===== MENÚ PRINCIPAL =====")
    print("1) Agregar país")
    print("2) Actualizar país")
    print("3) Buscar países por nombre")
    print("4) Filtrar países")
    print("5) Ordenar países")
    print("6) Mostrar estadísticas")
    print("0) Salir")
    print("==========================")

    opcion = input("Ingrese una opción: ")

    if opcion == "1":
        agregar_pais()
        pass
    elif opcion == "2":
       # actualizar_pais()   
        pass
    elif opcion == "3":
       # buscar_paises()     
        pass
    elif opcion == "4":
       # filtrar_paises()    
        pass
    elif opcion == "5":
       # ordenar_paises()    
        pass
    elif opcion == "6":
       # estadisticas()      
        pass
    elif opcion == "0":
        print("Saliendo del sistema...")
        break

    else:
        print("Opción inválida. Intente nuevamente.")
