import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import mariadb
import logging

# Configurar el logger
logging.basicConfig(filename='app.log', level=logging.ERROR)

# Función para conectar a la base de datos
def conectar_db():
    try:
        con = mariadb.connect(
            host="localhost",
            user="root",
            password="pro01#",
            database="tu_luis",
            port=3307
        )
        return con, con.cursor()
    except mariadb.Error as error:
        messagebox.showerror("Error de conexión", f"Error de conexión: {error}")
        logging.error(f"Error de conexión: {error}")
        return None, None

# Función para insertar datos en la base de datos
def insertar(datos):
    con, cursor = conectar_db()
    if con is None or cursor is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return
    
    sql = """
    INSERT INTO clientes (name_cl, apellido_cl, Nit, DPI, Productos01, Cantidad01, Precio01, Productos02, Cantidad02, Precio02, Productos03, Cantidad03, Precio03, Productos04, Cantidad04, Precio04, Productos05, Cantidad05, Precio05, Productos06, Cantidad06, Precio06, Productos07, Cantidad07, Precio07, Productos08, Cantidad08, Precio08, Productos09, Cantidad09, Precio09, Productos10, Cantidad10, Precio10) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    try:
        cursor.execute(sql, datos)
        con.commit()
        messagebox.showinfo("Éxito", "Los datos se han insertado correctamente.")
    except mariadb.Error as error:
        messagebox.showerror("Error al insertar", f"Error al insertar datos: {error}")
        logging.error(f"Error al insertar datos: {error}")
    finally:
        cursor.close()
        con.close()

# Función que se llama cuando se hace clic en "Enviar otro"
def enviar_datos():
    name_cl = entry_name.get()
    apellido_cl = entry_apellido.get()
    Nit = entry_nit.get()
    DPI = entry_dpi.get()

    # Recoger todos los productos, cantidades y precios agregados dinámicamente
    productos = [entry.get() for entry in producto_entries]
    cantidades = [quantity_entry.get() for quantity_entry in cantidad_entries]
    precios = [price_entry.get() for price_entry in precio_entries]

    # Limitar los productos, cantidades y precios a los primeros 10, por si hay más
    productos = productos[:10]
    cantidades = cantidades[:10]
    precios = precios[:10]

    # Rellenar con None si hay menos de 10 productos, cantidades o precios
    while len(productos) < 10:
        productos.append(None)
    while len(cantidades) < 10:
        cantidades.append(None)
    while len(precios) < 10:
        precios.append(None)

    # Preparar los datos para insertar, incluyendo todos los productos, cantidades y precios
    datos = (name_cl, apellido_cl, Nit, DPI, *[item for sublist in zip(productos, cantidades, precios) for item in sublist])
    
    insertar(datos)

    # Limpiar los campos del formulario
    entry_name.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_nit.delete(0, tk.END)
    entry_dpi.delete(0, tk.END)
    
    for entry in producto_entries:
        entry.delete(0, tk.END)
    for entry in cantidad_entries:
        entry.delete(0, tk.END)
    for entry in precio_entries:
        entry.delete(0, tk.END)

# Función para cerrar la aplicación
def terminar_inventario():
    root.quit()
    root.destroy()

# Función para agregar un nuevo producto en la misma ventana
def agregar_producto():
    global producto_count
    
    if producto_count >= 10:
        messagebox.showerror("Error", "No puedes agregar más de 10 productos.")
        return

    # Crear una nueva entrada para el producto, la cantidad y el precio dentro del frame de productos
    producto_label = tk.Label(productos_frame, text=f"Producto {producto_count+1}:")
    producto_label.grid(row=producto_count, column=0, padx=5, pady=5, sticky='w')
    
    entry_producto = tk.Entry(productos_frame)
    entry_producto.grid(row=producto_count, column=1, padx=5, pady=5, sticky='ew')

    cantidad_label = tk.Label(productos_frame, text="Cantidad:")
    cantidad_label.grid(row=producto_count, column=2, padx=5, pady=5, sticky='w')
    
    entry_cantidad = tk.Entry(productos_frame)
    entry_cantidad.grid(row=producto_count, column=3, padx=5, pady=5, sticky='ew')

    precio_label = tk.Label(productos_frame, text="Precio:")
    precio_label.grid(row=producto_count, column=4, padx=5, pady=5, sticky='w')
    
    entry_precio = tk.Entry(productos_frame)
    entry_precio.grid(row=producto_count, column=5, padx=5, pady=5, sticky='ew')
    
    producto_entries.append(entry_producto)
    cantidad_entries.append(entry_cantidad)
    precio_entries.append(entry_precio)
    producto_count += 1

# Función para agregar el logo en la esquina superior derecha
def agregar_logo(ruta_logo):
    try:
        # Cargar la imagen usando PIL
        imagen = Image.open(ruta_logo)
        imagen = imagen.resize((200, 100), Image.LANCZOS)  # Redimensionar si es necesario
        logo = ImageTk.PhotoImage(imagen)

        # Crear un label para mostrar el logo
        label_logo = tk.Label(root, image=logo)
        label_logo.image = logo  # Guardar una referencia para evitar el garbage collection
        label_logo.grid(row=0, column=3, padx=10, pady=10, sticky='ne')  # Posicionar en la esquina superior derecha
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar el logo: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Ingreso de Datos")

# Configurar la ventana para pantalla completa
root.attributes('-fullscreen', True)

# Llamar a la función para agregar el logo
ruta_logo = r"C:\Users\Camazotz\Pictures\intecap.png"
agregar_logo(ruta_logo)

# Crear un marco gris para la sección de información
info_frame = tk.Frame(root, bg='gray', padx=100, pady=10)
info_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky='ew')

tk.Label(info_frame, text="Nombre:", bg='gray').grid(row=0, column=0, padx=5, pady=5, sticky='w')
entry_name = tk.Entry(info_frame)
entry_name.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

tk.Label(info_frame, text="Apellido:", bg='gray').grid(row=1, column=0, padx=5, pady=5, sticky='w')
entry_apellido = tk.Entry(info_frame)
entry_apellido.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

tk.Label(info_frame, text="NIT:", bg='gray').grid(row=2, column=0, padx=5, pady=5, sticky='w')
entry_nit = tk.Entry(info_frame)
entry_nit.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

tk.Label(info_frame, text="DPI:", bg='gray').grid(row=3, column=0, padx=5, pady=5, sticky='w')
entry_dpi = tk.Entry(info_frame)
entry_dpi.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

# Frame con scroll para los productos
frame_scroll = tk.Frame(root)
frame_scroll.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

canvas = tk.Canvas(frame_scroll)
scrollbar = ttk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
productos_frame = tk.Frame(canvas)

productos_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=productos_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Listas para almacenar las entradas de los productos, precios y cantidades
producto_entries = []
precio_entries = []
cantidad_entries = []

# Variable para contar los productos agregados
producto_count = 0

# Botones
btn_width = 50  # Ancho fijo para los botones, ajusta según sea necesario
btn_height = 2  # Altura fija para los botones

tk.Button(root, text="Enviar otro", command=enviar_datos, width=btn_width, height=btn_height).grid(row=5, column=0, padx=10, pady=10, sticky='ew')
tk.Button(root, text="Agregar otro producto", command=agregar_producto, width=btn_width, height=btn_height).grid(row=5, column=1, padx=10, pady=10, sticky='ew')
tk.Button(root, text="Terminar inventario", command=terminar_inventario, width=btn_width, height=btn_height).grid(row=5, column=3, padx=10, pady=10, sticky='ew')

# Configurar el comportamiento de la cuadrícula
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(5, weight=1)

# Ejecutar el loop principal
root.mainloop()
