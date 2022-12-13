from tkinter import ttk, messagebox # tiene los componentes gráficos pro no tiene el constructor, por lo que hay que importarlo entero

from tkinter import * #tkinter viene instalado con python, por lo que no hay que instalarlo
import sqlite3

class Producto:

    db = "database/productos.db"

    def __init__(self, root):#vinculamos la class con la interfaz gráfica, enviándolo por parametro. Además hemos de elegir una clase como la clase principal o elemento central del problema
        self.ventana = root #con esta var dentro del constructor de la clase podemos diseñar o configurar la ventana
        self.ventana.title("App Gestor de Productos")
        self.ventana.resizable(1, 1)#redimensionado ancho y largo es true o 1. Viene por defecto, x lo q no haría falta
        self.ventana.geometry("605x670") #Indicamos la dimensión por defecto de la ventana principal

        #Varias opciones para establecer un icono de la ventana de la app pero ninguna me funciona, no sé si por estar usando Linux, pero no encuentro la solución
        #img = self.ventana.tk.PhotoImage(file='/home/nacho/Escritorio/Tokyo_Python/Modulo 6/appescritorio/recursos/icono1.ico')
        #self.ventana.iconbitmap("/recursos/icono.ico")
        #self.ventana.wm_iconbitmap("/recursos/icono.ico")#no todas las instrucciones son validas en todos los SO, esta es una de ellas, este comando es para windows
        #self.ventana.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='/home/nacho/Escritorio/Tokyo_Python/Modulo 6/appescritorio/recursos/icono.ico'))
        #self.ventana.tk.call('wm', 'iconbitmap', self.ventana._w, img)
        #self.ventana.gui.iconbitmap('@/home/nacho/Escritorio/Tokyo_Python/Modulo 6/appescritorio/recursos/icono.xbm')

        #Tkinter siempre tiene una estructura de filas y columnas, tipo excel, llamada grid, aunque podemos redimensionarlo para establecer el número de filas y columnas que queremos. Así se accederá a ellas, empiezan en 0, por sus coordenadas
        #en ella se insertan los widgets, q son cualquier cosa que queramos, pero para posicionarlo hay q darle unas coordenadas y pueden ocupar varias celdas, pasándole el tamaño que queramos en coordenadas
        #tb podemos generar un grupo de widgets encapsulándolos en un frame


        #creacion del contenedor frame principal
        frame = LabelFrame(self.ventana, text="Registrar un nuevo producto", font=('Calibri', 16, 'bold')) #pasamos la ventana en q queremos insertarlo y un titulo, no se ejecuta, o no se pinta, hasta que no tiene nada dentro
        frame.pack(fill="both", expand="True") #He intentado que al redimensionar la ventana el frame también lo hiciese pero no me funciona
        frame.grid(row=0, column=0, columnspan=3, pady=20) #la ubicación en filas y col, tamaño(en este caso de 3 columnas) y separación del margen

        """He intentado implementar otra forma para redimensionar el frame pero tampoco me funciona.
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)"""

        #label de nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ", font=('Calibri', 13)) #creamos la etiqueta y q ponga Nombre:
        self.etiqueta_nombre.grid(row=1, column=0)
        #Entry de nombre
        self.nombre = Entry(frame, font=('Calibri', 13)) #pasamos dónde se crea el objeto cajon de texto
        self.nombre.focus() #autofocus
        self.nombre.grid(row=1, column=1) #posicionamiento en el grid

        #label de precio
        self.etiqueta_precio = Label(frame, text="Precio: ", font=('Calibri', 13))
        self.etiqueta_precio.grid(row=2, column=0)
        #Entry de precio
        self.precio = Entry(frame, font=('Calibri', 13))
        self.precio.grid(row=2, column=1)

        # label de categoria
        self.etiqueta_categoria = Label(frame, text="Categoría: ", font=('Calibri', 13))
        self.etiqueta_categoria.grid(row=3, column=0)
        # Entry de precio
        self.categoria = ttk.Combobox(frame, width=26)
        self.categoria.grid(row=3, column=1)

        opciones = ["Informática", "Electrónica"]
        self.categoria['values'] = opciones


        #Boton guardar
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        #self.boton_guardar = Button(frame, text="Añadir producto: ") #podria ser así, de la libreria Tk, pero lo vamos a hacer con el boton de ttk:
        self.boton_guardar = ttk.Button(frame, text="Añadir producto", command=self.add_producto, style='my.TButton') #aquí no hay q poner los parentesis de la funcion de add_producto xq el comando command sobreentiende q va a leer una funcion. esto es para los botones de Tkinter
        self.boton_guardar.grid(row=4, columnspan=3, sticky=W+E) #para que ocupe dos columnas primero columnspan y después con sticky, que funciona con coordenadas geográficas, es decir de Oeste a este, en este caso, ocupamos el espacio entero de las dos columnas
        self.mensaje = Label(text="", fg='red') #fg=forground es para poner algo en un color, bg sería para poner un fondo de color
        self.mensaje.grid(row=3, column=2, columnspan=2, sticky=W+E)

        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))  # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))  # Se modifica la fuente de las cabeceras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Eliminamos los bordes

        #Tabla de productos, lo haremos con el elemento treeview, al final es una tabla
        self.tabla = ttk.Treeview(frame, height=20, columns=('#1', '#2'), style="mystyle.Treeview") #hay que darle altura y anchura en numero de celdas, con style le damos un formato más bonito, el cual podemos a su vez dar formato
        self.tabla.grid(row=5, column=0, columnspan=3) #ubicacion
        self.tabla.heading("#0", text="Nombre", anchor=CENTER)#nombre de las columnas de la tabla, tienen un identificador alfanumerico #0 es el primero..
        self.tabla.heading("#1", text="Precio", anchor=CENTER)
        self.tabla.heading("#2", text="Categoría", anchor=CENTER)

        #Boton eliminar y Editar
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))

        boton_eliminar = ttk.Button(text="ELIMINAR", style='my.TButton', command=self.del_producto)
        boton_eliminar.grid(row=6, column=0, sticky=W+E)
        boton_editar = ttk.Button(text="EDITAR", style='my.TButton', command=self.ventana_edicion)
        boton_editar.grid(row=6, column=1, columnspan=2, sticky=W+E)

        self.get_productos()

    def db_consulta(self, consulta, parametros=()): #consulta seria un select, definimos parametros como una tupla vacía que será algun parametro adicional de la consulta. Esto es xq el metodo execute está preparado para recibir dos parametros un string y una tupla
        with sqlite3.connect(self.db) as con: #establecemos la conexion con la BD
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_productos(self):
        registros_tabla = self.tabla.get_children() #primero obtenemos los valores ya pintados en la app
        for fila in registros_tabla: #iteramos sobre ellos
            self.tabla.delete(fila) #para borrarlos, así no habrá problema al introducir nuevos registros, ya q como se introducirán desde laposición 0, tendría que pisar los registros ya pintados, lo que daría error

        query = "SELECT * FROM producto ORDER BY categoria, nombre" #Aquí tengo un problema ya que por consola sí me los ordena como yo quiero pero en la app no lo hace
        registros = self.db_consulta(query)
        for fila in registros:
            print(fila)
            self.tabla.insert("", 0, text=fila[1], values=fila[2:]) #parametro vacio para decir q no hereda de otra tabla, es un elemento unico, 0 xq queremos introducir datos desde la posicion 0, text es el nombre, x eso es fila 1 y values es el precio, es decir fila de 2 hasta el final de la lista para que rellee el siguiente campo

    def validacion_nombre(self):
        nombre_introducido_por_usuario = self.nombre.get() #llamamos al entry (cajon de texto) y lo devuelve
        return len(nombre_introducido_por_usuario) != 0

    def validacion_precio(self):
        precio_introducido_por_usuario = self.precio.get()
        return len(precio_introducido_por_usuario) != 0

    def validacion_categoria(self):
        categoria_introducida_por_usuario = self.categoria.get()
        return len(categoria_introducida_por_usuario) != 0

    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria():
            query = "INSERT INTO producto VALUES(NULL, ?, ?, ?)" #el id como es autoincremental no hay que dárselo, pero hay q pasar un NULL para q no de error
            parametros = (self.nombre.get(), self.precio.get(), self.categoria.get()) #tienen q ser en una tupla, pues está definido así, y solo puede ser así de hecho
            self.db_consulta(query, parametros) #así quedarían los datos introducidos guardados en la BD, pero no se habrá actualizado en la app
            self.mensaje["text"] = "El producto {} ha sido añadido con éxito".format(self.nombre.get())
            self.nombre.delete(0, END) #con esta instrucción limpiamos los entry
            self.precio.delete(0, END)
            self.categoria.delete(0, END)

            #los print son solo para debug, ya que el usuario no lo verá en la app
            #print(self.nombre.get())
            #print(self.precio.get())
        elif self.validacion_nombre() and self.validacion_categoria() and self.validacion_precio() == False:
            #print("El precio es obligatorio")
            self.mensaje["text"] = "El precio es obligatorio"
        elif self.validacion_nombre() == False and self.validacion_precio() and self.validacion_categoria():
            #print("El nombre es obligatorio")
            self.mensaje["text"] = "El nombre es obligatorio"
        elif self.validacion_categoria() == False and self.validacion_nombre() and self.validacion_precio():
            self.mensaje["text"] = "La categoría es obligatoria"
        else:
            #print("El nombre, el precio y la categoría son obligatorios")
            self.mensaje["text"] = "El nombre, el precio y la categoría son obligatorios"

        self.get_productos()


    def del_producto(self):
        #print(self.tabla.item(self.tabla.selection())) #retorna el item q está seleccionado en la app con el cursor
        if self.tabla.item(self.tabla.selection())["text"]:
            resultado = messagebox.askquestion("Borrar Producto", "¿Está seguro que desea eliminar el producto, esta acción es irreversible?")
            if resultado == "yes":
                nombre = self.tabla.item(self.tabla.selection())["text"]
                query = "DELETE FROM producto WHERE nombre = ?"
                self.db_consulta(query, (nombre,))
                self.mensaje['text'] = "El producto {} ha sido eliminado con éxito".format(nombre)
        else:
            self.mensaje['text'] = "Por favor selecciona un producto a eliminar"

        self.get_productos()

    def ventana_edicion(self):
        if self.tabla.item(self.tabla.selection())["text"]:
            nombre = self.tabla.item(self.tabla.selection())["text"]
            precio_antiguo = self.tabla.item(self.tabla.selection())["values"][0]
            categoria_antigua = self.tabla.item(self.tabla.selection())["values"][1]
            self.ventana_editar = Toplevel()
            self.ventana_editar.title("Edición de Productos")
            self.ventana_editar.resizable(1, 1)

            frame_editar = LabelFrame(self.ventana_editar, text="Editar Producto", font=('Calibri', 16, 'bold'))
            frame_editar.grid(row=1, column=0, columnspan=20, pady=20)

            # label de nombre antiguo
            self.etiqueta_nombre_antiguo = Label(frame_editar, text="Nombre Antiguo: ")
            self.etiqueta_nombre_antiguo.grid(row=2, column=0)
            # Entry de nombre antiguo
            self.input_nombre_antiguo = Entry(frame_editar, textvariable=StringVar(self.ventana_editar, value=nombre), state='readonly')  # cajón de solo lectura
            self.input_nombre_antiguo.grid(row=2, column=1)

            # label nombre nuevo
            self.etiqueta_nombre_nuevo = Label(frame_editar, text="Nombre nuevo: ").grid(row=3, column=0)

            #entry nuevo nombre
            self.input_nombre_nuevo = Entry(frame_editar)
            self.input_nombre_nuevo.grid(row=3, column=1)
            self.input_nombre_nuevo.focus() #situamos la entrada de texto en el primer campo a editar

            # label de precio antiguo
            self.etiqueta_precio_antiguo = Label(frame_editar, text="Precio antiguo: ")
            self.etiqueta_precio_antiguo.grid(row=5, column=0)
            # Entry de precio antiguo
            self.input_precio_antiguo = Entry(frame_editar, textvariable=StringVar(self.ventana_editar, value=precio_antiguo), state='readonly')
            self.input_precio_antiguo.grid(row=5, column=1)

            #label precio nuevo
            self.etiqueta_precio_nuevo = Label(frame_editar, text="Precio nuevo: ").grid(row=6, column=0)
            #Entry precio nuevo
            self.input_precio_nuevo = Entry(frame_editar)
            self.input_precio_nuevo.grid(row=6, column=1)

            # label de categoria antigua
            self.etiqueta_categoria_antigua = Label(frame_editar, text="Categoria antigua: ")
            self.etiqueta_categoria_antigua.grid(row=8, column=0)
            # Entry de categoria antigua
            self.input_categoria_antigua = Entry(frame_editar, textvariable=StringVar(self.ventana_editar, value=categoria_antigua), state='readonly')
            self.input_categoria_antigua.grid(row=8, column=1)

            # label categoria nueva
            self.etiqueta_categoria_nueva = Label(frame_editar, text="Categoría nueva: ").grid(row=9, column=0)
            # Entry categoria nueva
            self.input_categoria_nueva = ttk.Combobox(frame_editar, width=19)
            self.input_categoria_nueva.grid(row=9, column=1)
            opciones = ["Informática", "Electrónica"]
            self.input_categoria_nueva['values'] = opciones


            #boton guardar
            s = ttk.Style()
            s.configure('my.TButton', font=('Calibri', 14, 'bold'))
            self.boton_guardar = ttk.Button(frame_editar, text="Guardar cambios", style='my.TButton', command=lambda: self.editar_producto(self.input_nombre_nuevo.get(), self.input_nombre_antiguo.get(), self.input_precio_nuevo.get(), self.input_precio_antiguo.get(), self.input_categoria_nueva.get(), self.input_categoria_antigua.get()))
            self.boton_guardar.grid(row=10, columnspan=2, sticky=W+E)

        else:
            self.mensaje['text'] = "Por favor selecciona un producto a editar"


    def editar_producto(self, nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio, categoria_nueva, categoria_antigua):
        producto_modificado = False
        query = 'UPDATE producto SET nombre = ?, precio = ?, categoria = ? WHERE nombre = ? AND precio = ? AND categoria = ?'
        if nuevo_nombre != '' and nuevo_precio != '' and categoria_nueva != '':
        # Si el usuario escribe nuevo nombre, nuevo precio y nueva categoría se cambian los tres
            parametros = (nuevo_nombre, nuevo_precio, categoria_nueva, antiguo_nombre, antiguo_precio, categoria_antigua)
            producto_modificado = True
            self.ventana_editar.destroy() #Cuando se ejecuta el update y se guarda, la ventana editar se cierra automáticamente
        elif nuevo_nombre != '' and categoria_nueva != '' and nuevo_precio == '':
        # Si el usuario deja vacio el nuevo precio, se mantiene el pecio anterior
            parametros = (nuevo_nombre, antiguo_precio, categoria_nueva, antiguo_nombre, antiguo_precio, categoria_antigua)
            producto_modificado = True
            self.ventana_editar.destroy()
        elif nuevo_nombre == '' and nuevo_precio != '' and categoria_nueva != '':
        # Si el usuario deja vacio el nuevo nombre, se mantiene el nombre anterior
            parametros = (antiguo_nombre, nuevo_precio, categoria_nueva, antiguo_nombre, antiguo_precio, categoria_antigua)
            producto_modificado = True
            self.ventana_editar.destroy()
        elif categoria_nueva == '' and nuevo_nombre != '' and nuevo_precio != '':
        # Si el usuario deja vacía la nueva categoría, se mantiene la antigua
            parametros = (nuevo_nombre, nuevo_precio, categoria_antigua, antiguo_nombre, antiguo_precio, categoria_antigua)
            producto_modificado = True
            self.ventana_editar.destroy()
        elif categoria_nueva != '' and nuevo_nombre == '' and nuevo_precio == '':
        # Si el usuario introduce el campo categoría pero ninguno de los otros dos se modifica la categoría únicamente
            parametros = (antiguo_nombre, antiguo_precio, categoria_nueva, antiguo_nombre, antiguo_precio, categoria_antigua)
            producto_modificado = True
            self.ventana_editar.destroy()
        elif nuevo_nombre != '' and nuevo_precio == '' and categoria_nueva == '':
            parametros = (nuevo_nombre, antiguo_precio, categoria_antigua, antiguo_nombre, antiguo_precio, categoria_antigua)
            producto_modificado = True
            self.ventana_editar.destroy()
        elif nuevo_precio != '' and nuevo_nombre == '' and categoria_nueva == '':
            parametros = (antiguo_nombre, nuevo_precio, categoria_antigua, antiguo_nombre, antiguo_precio, categoria_antigua)
            producto_modificado = True
            self.ventana_editar.destroy()

        if producto_modificado == True:
            self.db_consulta(query, parametros)  # Ejecutar la consulta
            self.mensaje['text'] = 'El producto {} ha sido actualizado con éxito'.format(antiguo_nombre)
            self.get_productos()  # Actualizar la tabla de productos
        else:
            self.mensaje['text'] = 'El producto {} NO ha sido actualizado '.format(antiguo_nombre)



if __name__ == "__main__":
    root = Tk() #lo primero q hacemos es generar la ventana gráfica. El nombre de la variable sugerida es root, pero puede ser cualquiera. Y genera una instancia de la ventana principal
    app = Producto(root) #para llegar a la clase, creamos un objeto de la misma, de mi modelo de datos, y al objeto le paso mi ventana, q incluirá toda la personalizacion
    root.mainloop()  # con esta instruccion dejamos la ventana abierta hasta q le digamos q se cierre. es como un bucle while