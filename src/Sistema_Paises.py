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

#Opción 2 del menu: Actualizar
def actualizar_pais(inventario):
    
    nombre = input("Ingrese el nombre del país a actualizar: ").strip().lower().replace(" ", "")

    #Búsqueda secuencial
    pais_encontrado = None
    for pais in inventario:
        if pais["nombre"] == nombre:
            pais_encontrado = pais
            break

    #País no encontrado
    if pais_encontrado is None:
        print("País no encontrado.")
        print("Por favor, revise si lo escribió bien o intente con otro nombre.")
        return

    print("\n" + "="*50)
    print(f"Datos del pais: {pais_encontrado['nombre'].upper()}")
    print("="*50)
    print(f"Población Actual  : {pais_encontrado['poblacion']} habitantes")
    print(f" Superficie Actual : {pais_encontrado['superficie']} km²")
    print("="*50)

    print("\n¿Qué datos desea modificar?")
    print("1 - Población")
    print("2 - Superficie")
    opcion = input("Seleccione una opción (1 o 2): ").strip()

    if opcion not in ["1", "2"]:
        print("Opción incorrecta. Elija la opción 1 o 2.")
        return

    try:
        if opcion == "1":
            nueva_poblacion = int(input("Ingrese la nueva población, debe ser un entero positivo: ").strip())
            if nueva_poblacion <= 0:
                raise ValueError("La población no puede ser menor o igual a cero.")
            pais_encontrado["poblacion"] = nueva_poblacion

        elif opcion == "2":
            nueva_superficie = int(input("Ingrese la nueva superficie, km² positivos: ").strip())
            if nueva_superficie <= 0:
                raise ValueError("La extensión territorial debe ser mayor a cero.")
            pais_encontrado["superficie"] = nueva_superficie

        #Datos guardados correctamente
        guardar_csv(inventario)
        print(f"\nEl país '{nombre.upper()}' fue actualizado y guardado correctamente.")
        print(f"Nueva Población : {pais_encontrado['poblacion']:,} habitantes")
        print(f"Nueva Superficie: {pais_encontrado['superficie']:,} km²")

    except ValueError as error:
        if "int()" in str(error):
            mensaje_amigable = "Debe ingresar un número entero válido sin letras ni símbolos."
        else:
            mensaje_amigable = str(error)

        print(f"\nAlgo no coincidió con lo esperado: {mensaje_amigable}")
        print("Operación cancelada. El archivo no sufrió cambios.")

#Opcion 3 del menu: Buscar
def buscar_paises(inventario):
    
    # Bucle para pedir y validar los datos que ingresa el usuario
    while True:
        try:
            
            #limpia los espacios y los pasa a minúscula 
            pais_a_buscar = input("Ingrese el nombre del pais: ").strip().lower().replace(" ", "")
            
            # Validación 1: Si el usuario apretó enter sin escribir nada
            if pais_a_buscar == "":
                raise ValueError("El campo de búsqueda no puede estar vacío.")
            
            # Validación 2: Si ingresó números o símbolos raros
            if not pais_a_buscar.isalpha():
                raise ValueError("El nombre solo debe contener letras, sin números ni símbolos.")
            
            # Si los datos están perfectos, rompemos el bucle 'while' para pasar a buscar
            break
            
        except ValueError as error:
            # si hay un error, mostramos el aviso y el 'while' vuelve a pedir el dato
            print(f"Error: {error} Intente nuevamente.")
    
    # 2 búsqueda lineal
    coincidencias = []
    for pais in inventario:
        # El 'in' busca coincidencias parciales
        if pais_a_buscar in pais["nombre"]:
            coincidencias.append(pais)
            
    # 3. Control de resultados
    if len(coincidencias) == 0:
        print(f"\nNo se encontró ningún país que coincida con '{pais_a_buscar.upper()}'.")
        return  # Corta la función de forma segura y vuelve al menú

    # 4. Mostrar los resultados en una tabla prolija
    print("\n" + "="*75)
    print(f"Coincidencias: {len(coincidencias)}")
    print(f"{'PAÍS':<20} | {'POBLACIÓN':<15} | {'SUPERFICIE (km²)':<18} | {'CONTINENTE':<12}")
    
    
    # Recorremos la lista de aciertos para mostrarlos en pantalla
    for p in coincidencias:
        print(f"{p['nombre'].upper():<20} | {p['poblacion']:<15,} | {p['superficie']:<18,} | {p['continente'].title():<12}")
        
    print("="*75)
    
#Opcion 5 del menu: Ordenar
def ordenar_paises(inventario):
    
    if len(inventario) == 0:
        print("No hay países cargados en el sistema para ordenar.")
        return

    # 1. MENÚ INTERNO DE SELECCIÓN 
    while True:
        try:
            print("\nOrdenar los países por: ")
            print("1 - Nombre, de la A-Z")
            print("2 - Población, de mayor a menor")
            print("3 - Superficie, ascendente/descendente)")
            
            criterio = input("Seleccione una opción (1, 2 o 3): ").strip()
            
            if criterio not in ["1", "2", "3"]:
                raise ValueError("La opción elegida no es válida. Debe ser 1, 2 o 3.")
            
            # Si la opción es correcta, rompemos el bucle para avanzar
            break
            
        except ValueError as error:
            print(f"El dato no es correcto: {error}. Intente de nuevo.")

    
    
    # Por Nombre
    if criterio == "1":
        # sorted() genera una nueva lista ordenada sin romper la lista original si no queremos
        # lambda p: p["nombre"] le dice a Python que mire la clave "nombre" para ordenar
        lista_ordenada = sorted(inventario, key=lambda p: p["nombre"], reverse=False)
        titulo_reporte = "ORDENADO POR NOMBRE"

    #Por Población
    elif criterio == "2":
        # reverse=True hace que el ordenamiento vaya de mayor a menor 
        lista_ordenada = sorted(inventario, key=lambda p: p["poblacion"], reverse=True)
        titulo_reporte = "ORDENADO POR POBLACIÓN"

    #Por superficie
    elif criterio == "3":
        #para validar el sentido de la superficie
        while True:
            try:
                print("\nOrdenar en sentido:")
                print("A - Ascendente")
                print("D - Descendente")
                sentido = input("Seleccione el sentido (A o D): ").strip().upper()
                
                if sentido not in ["A", "D"]:
                    raise ValueError("Sentido incorrecto. Ingrese estrictamente 'A' o 'D'.")
                break
            except ValueError as error:
                print(f"Datos invalidos: {error} Intente de nuevo.")
        
        # Aplicamos el ordenamiento según el sentido elegido
        if sentido == "A":
            lista_ordenada = sorted(inventario, key=lambda p: p["superficie"], reverse=False)
            titulo_reporte = "ORDENADO POR SUPERFICIE - SENTIDO ASCENDENTE"
        else:
            lista_ordenada = sorted(inventario, key=lambda p: p["superficie"], reverse=True)
            titulo_reporte = "ORDENADO POR SUPERFICIE - SENTIDO DESCENDENTE"


    print("\n" + "="*75)
    print(f" REPORTE: {titulo_reporte}")
    print("="*75)
    print(f"{'PAÍS':<20} | {'POBLACIÓN':<15} | {'SUPERFICIE (km²)':<18} | {'CONTINENTE':<12}")
    print("-"*75)
    
    
    for p in lista_ordenada:
        print(f"{p['nombre'].upper():<20} | {p['poblacion']:<15,} | {p['superficie']:<18,} | {p['continente'].title():<12}")
        
    print("="*75)
    



    


inventario = leer_csv()

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
