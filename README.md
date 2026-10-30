# Metro CDMX: búsqueda de rutas con A*

Aplicación de escritorio en Python que representa un subconjunto de estaciones de
las líneas 1, 3, 7, 9 y 12 del Metro de Ciudad de México. Permite seleccionar
estaciones de origen y destino, calcular una ruta y mostrarla animada sobre un
mapa esquemático.

## Requisitos

- Python 3.10 o posterior.
- Tkinter, incluido normalmente con Python para Windows.
- NetworkX 3.x.

## Instalación

Desde la carpeta del proyecto, instala la dependencia de Python:

```powershell
python -m pip install -r requirements.txt
```

Si Tkinter no está disponible en tu instalación de Python, instala una versión
de Python para Windows que incluya Tcl/Tk.

## Ejecución

Inicia la interfaz gráfica desde la carpeta del proyecto:

```powershell
python tkin.py
```

Selecciona el origen y el destino en las listas y pulsa **Calcular**. También
puedes seleccionar estaciones haciendo clic en el mapa. **Limpiar** restablece
la selección. El mapa admite zoom con la rueda del ratón y desplazamiento con
el botón central o el derecho.

El botón **Accesibilidad** resalta las estaciones que el proyecto tiene
marcadas con escaleras mecánicas o ascensor. Esta indicación es visual: no
cambia el cálculo de rutas ni garantiza el estado actual de las instalaciones.

## Cómo funciona

- `MetroMexico.py` contiene las estaciones, coordenadas, conexiones y el grafo
  de NetworkX, además de `calcular_ruta`.
- `tkin.py` implementa la interfaz gráfica con Tkinter, el mapa y la animación.
- Las conexiones entre estaciones consecutivas tienen un peso en metros; los
  transbordos tienen un peso fijo de 150.
- `calcular_ruta(origen, destino)` busca la ruta de menor coste mediante A*.
  Los nombres de las estaciones se pasan sin el sufijo de línea, por ejemplo:
  `calcular_ruta("Universidad", "Polanco")`. Devuelve la lista de nodos de la
  ruta o `None` si no encuentra estaciones válidas.

## Comprobaciones

Comprueba que los módulos compilan:

```powershell
python -m py_compile MetroMexico.py tkin.py
```

Ejecuta una comprobación sencilla del cálculo de rutas:

```powershell
python -c "from MetroMexico import calcular_ruta; assert calcular_ruta('Universidad', 'Polanco'); assert calcular_ruta('NoExiste', 'Polanco') is None; print('Comprobaciones correctas')"
```

## Alcance y limitaciones

- El grafo incluye solo una selección de estaciones de cinco líneas; no es un
  mapa completo de la red.
- Las distancias, coordenadas y datos de accesibilidad están definidos
  directamente en `MetroMexico.py` y no se actualizan automáticamente.
- La accesibilidad solo se representa mediante colores en la interfaz; no se
  usa como condición para encontrar rutas.
- El proyecto no incluye todavía una suite automatizada de pruebas.
