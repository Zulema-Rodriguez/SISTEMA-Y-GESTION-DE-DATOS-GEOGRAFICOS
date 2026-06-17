## SISTEMA Y GESTIÓN DE DATOS GEOGRÁFICOS

##TRABAJO PRACTICO INTEGRADOR PROGRAMACION 

##PARTICIPANTES:
	-Alvarez, Maximiliano.
	-Zulema, Rodriguez.

Este proyecto es una aplicación en Python  que permite gestionar información de países utilizando listas, diccionarios, funciones, filtros, ordenamientos y estadísticas básicas. El sistema trabaja a partir de un archivo CSV que contiene datos reales de países.

---

##  Funcionalidades principales

- Cargar datos desde un archivo CSV.
- Agregar un nuevo país con validación de campos.
- Actualizar población y superficie de un país existente.
- Buscar países por nombre (coincidencia parcial o exacta).
- Filtrar países por continente, rango de población o rango de superficie.
- Ordenar países por nombre, población o superficie (ascendente o descendente).
- Mostrar estadísticas:
  - País con mayor y menor población
  - Promedio de población
  - Promedio de superficie
  - Cantidad de países por continente

---

##  Estructura del Repositorio

/proyecto_paises
│── datos/
│     └── datos_geograficos.csv
│
│── src/
│     └── Sistema_Paises.py
│
└── README.md


---

## Dataset utilizado

El archivo `datos_geograficos.csv` contiene los siguientes campos:

    "nombre": str,       # Identificador alfabético (Ej: "argentina") (Se guarda sin espacios y todo en minúscula)
    "poblacion": int,    # Magnitud demográfica (Número entero positivo)
    "superficie": int,   # Extensión territorial en kilómetros cuadrados (int)
    "continente": str    # Dados por defectos (america/asia/africa/oceania/europa)

## Video Demostrativo
Enlace del video: https://www.youtube.com/watch?v=XokzrS1OL5o 


