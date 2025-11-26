import tkinter as tk
from tkinter import ttk
import math

from MetroMexico import coordenadas, conexiones, posiciones_dibujo, calcular_ruta,accesibilidad_mec,accesibilidad_asc

MARGEN = 40
FONDO_MAPA = "#D1D1D1"
COLOR_ESTACIONES = "#FFFFFF"
COLOR_TEXTO = "black"
COLOR_TRANSBORDO = "#888888"
COLOR_RUTA = "#0400FF"
RADIO_CURSOR = 6

ESCALA_X = 125
ESCALA_Y = 40
OFFSET_X = -90
OFFSET_Y = 0

COLOR_LINEA = {"L1": "#E71D73", "L3": "#A4C639", "L7": "#F5A623", "L9": "#8B5A2B", "L12": "#C9A100"}

# Variables globales
id_estacion = {}  
id_estacion_canva = {}
color_estaciones = {}
origen_actual = None
destino_actual = None
animacion_activa = False
modo_accesible = False

# Nombre de la estacion sin la linea
def obtener_nombre_base(nodo):
    return nodo.split("_")[0]
# Linea del metro sin el nombre de la estacion
def obtener_linea(nodo):
    return nodo.split("_")[1]
# Convierte coordenadas de la cuadricula a pixeles
def grid_a_pixeles(gx, gy):
    x = (gx * ESCALA_X) + OFFSET_X
    y = (gy * ESCALA_Y) + OFFSET_Y
    return x, y
# Verifica si dos estaciones son transbordo
def es_transbordo(nodo1, nodo2):
    return (obtener_nombre_base(nodo1) == obtener_nombre_base(nodo2) and obtener_linea(nodo1) != obtener_linea(nodo2))
# Dibuja el mapa del metro
def dibujar_mapa(canvas):
    global idestacion, id_estacion_canva,color_Estaciones
    idestacion = {}
    color_Estaciones={}
    id_estacion_canva = {}
    canvas.delete("all")
    
    h= canvas.winfo_height()
    w = canvas.winfo_width()
    
    canvas.create_rectangle(0,0,w,h,fill=FONDO_MAPA,outline=FONDO_MAPA)
    for a,b,_ in conexiones:
      if(a in posiciones_dibujo and b in posiciones_dibujo):
        nombre_a = obtener_nombre_base(a)
        linea_a = obtener_linea(a)
        nombre_b = obtener_nombre_base(b)
        gx,gy = posiciones_dibujo.get(a)
        gbx,gby = posiciones_dibujo.get(b)
        ax,ay = grid_a_pixeles(gx,gy)
        bx,by = grid_a_pixeles(gbx,gby)
        
        if(es_transbordo(a,b)):
            canvas.create_line(ax,ay,bx,by,fill=COLOR_TRANSBORDO,width=2)
        else:
            canvas.create_line(ax,ay,bx,by,fill=COLOR_LINEA.get(linea_a, "#B0B0B0"),width=5)
    for nodo,(gx,gy) in posiciones_dibujo.items():
        x,y = grid_a_pixeles(gx,gy)
        oid = canvas.create_oval(x-6,y-6,x+6,y+6,fill=COLOR_ESTACIONES,width=2)
        tid = canvas.create_text(x+10,y-10,text=obtener_nombre_base(nodo), anchor="w", font=("Segoe UI", 8, "bold"), fill=COLOR_TEXTO)
        
        idestacion[oid] = obtener_nombre_base(nodo)
        id_estacion_canva[idestacion[oid]] = oid
    
    resaltar_seleccion(canvas)
    dibujar_leyenda_lineas(canvas)
    dibujar_leyenda_accesibilidad(canvas)
# Leyenda de la linea del metro
def dibujar_leyenda_lineas(canvas):
    canvas.delete("leyenda_lineas")

    w = canvas.winfo_width()
    h = canvas.winfo_height()

    x0 = w - 180
    y0 = h - 160

    canvas.create_rectangle( x0 - 10, y0 - 20, x0 + 150, y0 + (len(COLOR_LINEA) * 18) + 20, fill="#FFFFFF", outline="black", width=1, tags="leyenda_lineas")

    canvas.create_text(x0, y0 - 10, text="Líneas del Metro:", anchor="w", font=("Segoe UI", 10, "bold"), fill="black", tags="leyenda_lineas")
    y0 += 12
    for linea, color in COLOR_LINEA.items():
        canvas.create_line( x0, y0, x0 + 30, y0,width=5, fill=color, tags="leyenda_lineas")
        canvas.create_text(x0 + 40, y0, text=linea, anchor="w", font=("Segoe UI", 9, "bold"), fill="black", tags="leyenda_lineas")
        y0 += 18
# Pinta azul el origen y rojo el destino     
def resaltar_seleccion(canvas):
    canvas.itemconfig("estacion", fill="white")
    if(modo_accesible):
        canvas.itemconfig("Escaleras_mec",fill="blue")
        canvas.itemconfig("Ascensor",fill="green")

    all_items = set()

    all_items = idestacion.keys()
    for item in all_items:
        nombre = idestacion.get(item)
        if nombre == origen_actual:
            canvas.itemconfig(item, fill="#7DFBFB")
        elif nombre == destino_actual:
            canvas.itemconfig(item, fill="#A02B16")
# Leyenda de accesibilidad
def dibujar_leyenda_accesibilidad(canvas):
    canvas.delete("leyenda_acc")
    if not modo_accesible:
        return

    w = canvas.winfo_width()
    h = canvas.winfo_height()

    x0 = 20
    y0 = h - 150

    rect = canvas.create_rectangle(x0 - 10, y0 - 20, x0 + 200, y0 + 60, fill="#FFFFFF", outline="black", width=1, tags="leyenda_acc")

    canvas.create_text(x0, y0 - 10, text="Accesibilidad:", anchor="w", fill="black", font=("Segoe UI", 10, "bold"), tags="leyenda_acc")

    canvas.create_oval(x0, y0, x0+12, y0+12, fill="blue", outline="black", tags="leyenda_acc")
    canvas.create_text(x0+20, y0+6, text="Escalera Mecánica", anchor="w", fill="black", font=("Segoe UI", 8), tags="leyenda_acc")

    y0 += 18

    canvas.create_oval(x0, y0, x0+12, y0+12, fill="green", outline="black", tags="leyenda_acc")
    canvas.create_text(x0+20, y0+6,text="Ascensor y Escalera Mecánica", anchor="w", fill="black", font=("Segoe UI", 8),tags="leyenda_acc")
    y0 += 18

# Mueve un punto azul entre la lista de estaciones y dibuja una linea por donde ha pasado
def animar_ruta(canvas, puntos, idx=0, t=0.0, cursor_id=None):

    global animacion_activa

    if not animacion_activa:
        return

    if idx >= len(puntos) - 1:
        animacion_activa = False
        canvas.delete(cursor_id)
        return

    x1, y1 = puntos[idx]
    x2, y2 = puntos[idx+1]

    x = x1 + (x2 - x1) * t
    y = y1 + (y2 - y1) * t

    if cursor_id is None:
        cursor_id = canvas.create_oval(x-RADIO_CURSOR, y-RADIO_CURSOR, x+RADIO_CURSOR, y+RADIO_CURSOR, fill=COLOR_RUTA, outline="white", width=2)
    else:
        canvas.coords(cursor_id, x-RADIO_CURSOR, y-RADIO_CURSOR, x+RADIO_CURSOR, y+RADIO_CURSOR)

    if t >= 1.0:
        canvas.create_line(x1, y1, x2, y2, fill=COLOR_RUTA, width=4)
        idx += 1
        t = 0.0
    else:
        t += 0.05 

    canvas.after(30, lambda: animar_ruta(canvas, puntos, idx, t, cursor_id))
# Interaccion con el mapa
def configurar_eventos(canvas, combo_origen, combo_destino):
    
    def zoom(event):
        scale = 1.1 if event.delta > 0 else 0.9
        canvas.scale("all", event.x, event.y, scale, scale)

    # Mover mapa
    canvas.bind("<ButtonPress-2>", lambda e: canvas.scan_mark(e.x, e.y))
    canvas.bind("<B2-Motion>", lambda e: canvas.scan_dragto(e.x, e.y, gain=1))
    canvas.bind("<ButtonPress-3>", lambda e: canvas.scan_mark(e.x, e.y))
    canvas.bind("<B3-Motion>", lambda e: canvas.scan_dragto(e.x, e.y, gain=1))
    canvas.bind("<MouseWheel>", zoom)

    # Seleccion de estacion con click izquierdo
    def clic_izquierdo(event):
        global origen_actual, destino_actual
        item = canvas.find_closest(canvas.canvasx(event.x), canvas.canvasy(event.y))[0]
        nombre = idestacion.get(item)
        if nombre:
            if origen_actual is None:
                origen_actual = nombre
            elif destino_actual is None:
                destino_actual = nombre
            else:
                origen_actual = nombre
                destino_actual = None
            resaltar_seleccion(canvas)
            combo_origen.set(origen_actual if origen_actual else "")
            combo_destino.set(destino_actual if destino_actual else "")
    canvas.bind("<ButtonPress-1>", clic_izquierdo)

def interfaz():
    global animacion_activa, origen_actual, destino_actual, modo_accesible

    root = tk.Tk()
    root.title("Metro CDMX - A*")
    root.geometry("1400x800")

    panel = tk.Frame(root, bg="#DDD", pady=5)
    panel.pack(side="top", fill="x")

    estaciones = sorted(list(set([obtener_nombre_base(k) for k in coordenadas.keys()])))

    # Comboboxes
    tk.Label(panel, text="Origen:", bg="#DDD").pack(side="left", padx=5)
    cb_origen = ttk.Combobox(panel, values=estaciones)
    cb_origen.pack(side="left")

    tk.Label(panel, text="Destino:", bg="#DDD").pack(side="left", padx=5)
    cb_destino = ttk.Combobox(panel, values=estaciones)
    cb_destino.pack(side="left")

    # Botones

    # Boton calcular
    def accion_calcular():
        global animacion_activa, origen_actual, destino_actual
        
        origen_actual = cb_origen.get()
        destino_actual = cb_destino.get()

        if not origen_actual or not destino_actual:
            return

        animacion_activa = False
        dibujar_mapa(canvas) 
        camino = calcular_ruta(origen_actual, destino_actual)
        if camino:
            puntos_pantalla = []
            for nodo in camino:
                if nodo in posiciones_dibujo:
                    gx, gy = posiciones_dibujo[nodo]
                    px, py = grid_a_pixeles(gx, gy)
                    puntos_pantalla.append((px, py))
            
            animacion_activa = True
            animar_ruta(canvas, puntos_pantalla)
        else:
            print("No se encontró ruta")
    # Boton limpiar
    def accion_limpiar():
        global origen_actual, destino_actual, animacion_activa
        animacion_activa = False
        origen_actual = None
        destino_actual = None
        cb_origen.set("")
        cb_destino.set("")
        dibujar_mapa(canvas)
    # Boton accesibilidad
    def toggle_accesibilidad():
        global modo_accesible,btn_acc
        modo_accesible = not modo_accesible
        if (modo_accesible):
          btn_acc.config(text ="Accesibilidad: ON",bg="green", fg="white")
          for esta in accesibilidad_mec.keys():
              if(id_estacion_canva[esta]):
                canvas.itemconfig(id_estacion_canva[esta],fill="blue")
                canvas.addtag_withtag("Escaleras_mec", id_estacion_canva[esta])
                canvas.dtag(id_estacion_canva[esta],"estacion")
          for est in accesibilidad_asc:
              if(id_estacion_canva[est]):
                  canvas.itemconfig(id_estacion_canva[est],fill="green")
                  canvas.addtag_withtag("Ascensor", id_estacion_canva[est])
                  canvas.dtag(id_estacion_canva[esta],"estacion")
        else:
          btn_acc.config(text = "Accesibilidad: OFF",bg="#DDD",fg="black")
          for estac in accesibilidad_mec.keys():
           if(id_estacion_canva[estac]):
             canvas.itemconfig(id_estacion_canva[estac],fill="white")
             canvas.dtag(id_estacion_canva[estac],"Escaleras_mec")
             canvas.addtag_withtag("estacion",id_estacion_canva[estac])
          for es in accesibilidad_asc:
              if(id_estacion_canva[es]):
                  canvas.itemconfig(id_estacion_canva[es],fill="white")
                  canvas.dtag(id_estacion_canva[es],"Ascensor")
                  canvas.addtag_withtag("estacion",id_estacion_canva[estac])
        dibujar_leyenda_accesibilidad(canvas)

    tk.Button(panel, text="Calcular", command=accion_calcular, bg="#4CAF50", fg="white").pack(side="left", padx=10)
    tk.Button(panel, text="Limpiar", command=accion_limpiar).pack(side="left")
    
    global btn_acc
    btn_acc = tk.Button(panel, text="Accesibilidad: OFF", command=toggle_accesibilidad)
    btn_acc.pack(side="right", padx=10)

    # Canvas
    canvas = tk.Canvas(root, bg=FONDO_MAPA)
    canvas.pack(fill="both", expand=True)

    # Inicializar
    dibujar_mapa(canvas)
    configurar_eventos(canvas, cb_origen, cb_destino)
    root.after(100, lambda: (dibujar_leyenda_lineas(canvas), dibujar_leyenda_accesibilidad(canvas)))

    root.mainloop()

if __name__ == "__main__":
    interfaz()