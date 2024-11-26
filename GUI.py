import tkinter as tk
from tkinter import scrolledtext, filedialog, Toplevel, Canvas, Scrollbar
from PIL import Image, ImageTk
from lexico import errores, lexer, verificar_comentario_inicial
from sintactico import visualizar_arbol, parser
from semantico import AnalizadorSemantico
from generator import CodeGenerator
import os
import PIL
from llvmlite import ir, binding


global archivo
archivo = "1"

# Instancia global de CodeGenerator
global generador
generador = CodeGenerator()

import subprocess


# Ejemplo de uso dentro de run_code
def run_code(arbol, tabla):
    consolePanel.config(state=tk.NORMAL)  # Habilitar la consola para que sea editable
    consolePanel.delete('1.0', tk.END)
    consolePanel.config(state=tk.DISABLED)  # Deshabilitar nuevamente para evitar ediciones manuales
    errores.clear()  # Limpiamos la lista de errores
    code = codePanel.get("1.0", tk.END).strip()
    print("'" + code + "'")
    consolePanel.config(state=tk.NORMAL)
    
    if verificar_comentario_inicial(code):
        lexer.lineno = 1
        lexer.input(code)
        if errores:
            show_errors(errores)
        else:
            lexer.lineno = 1
            arb_sint = parser.parse(code)
            if errores:
                show_errors(errores)
            else:
                if arbol:
                    visualizar_arbol(arb_sint)  # Generar el archivo "arbol_parseo.png"
                    mostrar_imagen_con_scroll("arbol_parseo.png")
                    consolePanel.insert(tk.END, "Árbol de parseo generado con éxito <3 \n", 'exito')
                lexer.lineno = 1
                analizador = AnalizadorSemantico(arb_sint)
                analizador.analizar(arb_sint)

                print(errores)
                if errores:
                   show_errors(errores)
                else:
                    if tabla:
                        analizador.generar_tabla_simbolos(analizador.tabla_simbolos)
                        consolePanel.insert(tk.END, "Tabla de símbolos generada con éxito <3 \n", 'exito')
                        consolePanel.tag_config('exito', foreground="white", font=("Consolas", 13, "bold"))
                        mostrar_imagen_con_scroll("tabla_simbolos.png")
                    consolePanel.insert(tk.END, "Código compilado con éxito <3 \n", 'exito')
                    consolePanel.tag_config('exito', foreground="white", font=("Consolas", 13, "bold"))  # Configuración del estilo para los errores
            arbol_simplificado = analizador.simplificar_arbol(arb_sint)

            ejecutar_asm(arbol_simplificado)
            open_control_window()
    else:
        show_errors(errores)

def show_errors(errors):
    """Muestra los errores en el panel de consola."""
    consolePanel.config(state=tk.NORMAL)  # Habilitar el panel de consola
    for message in errors:
        consolePanel.insert(tk.END, f"{message}\n", 'error')  # Insertar cada error
    consolePanel.tag_config('error', foreground="#c26364", font=("Consolas", 13, "bold"))  # Configuración del estilo para los errores
    consolePanel.config(state=tk.DISABLED)  # Deshabilitar el panel de consola para evitar ediciones

def mostrar_imagen_con_scroll(ruta_imagen):
    try:
        # Cargar la imagen
        img = Image.open(ruta_imagen)
        img_tk = ImageTk.PhotoImage(img)

        # Crear una ventana emergente
        nueva_ventana = Toplevel(root)
        nueva_ventana.title("Árbol de Parseo")

        # Crear un Canvas dentro de la nueva ventana
        canvas = Canvas(nueva_ventana, width=800, height=600)  # Tamaño inicial de la ventana
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Añadir barras de desplazamiento
        scrollbar_x = Scrollbar(nueva_ventana, orient=tk.HORIZONTAL, command=canvas.xview)
        scrollbar_y = Scrollbar(nueva_ventana, orient=tk.VERTICAL, command=canvas.yview)

        canvas.config(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

        # Posicionar las barras de desplazamiento
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurar el tamaño del canvas para que coincida con la imagen
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        canvas.config(scrollregion=canvas.bbox(tk.ALL))

        # Guardar una referencia a la imagen para evitar que sea recolectada por el garbage collector
        canvas.image = img_tk

    except Exception as e:
        print(f"Error cargando la imagen: {e}")

def update_line_numbers(event=None):
    numbersText.config(state=tk.NORMAL)
    numbersText.delete('1.0', tk.END)

    current_line = codePanel.index('@0,0').split('.')[0]
    last_line = codePanel.index(tk.END).split('.')[0]

    line_number_str = "\n".join(str(i) for i in range(int(current_line), int(last_line)))
    numbersText.insert('1.0', line_number_str + '\n')
    numbersText.config(state=tk.DISABLED)

def load_file_content(file_path):
    """Carga el contenido de un archivo y lo muestra en codePanel"""
    with open(file_path, 'r') as file:
        file_content = file.read()
        codePanel.delete("1.0", tk.END)  # Limpiar el panel de código actual
        codePanel.insert(tk.END, file_content)
        update_line_numbers()


def new_file():
    """Crea un nuevo archivo y solicita guardarlo de inmediato"""
    global archivo
    # Abrir el cuadro de diálogo para guardar archivo
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

    if file_path:
        # Crear el archivo vacío en la ruta especificada
        with open(file_path, 'w') as file:
            file.write("")  # Escribir contenido vacío

        # Obtener el nombre del archivo
        file_name = os.path.basename(file_path)

        # Limpiar el área de edición
        codePanel.delete("1.0", tk.END)
        update_line_numbers()
        name = file_name.replace('.txt', '')
        # Crear y añadir el botón del archivo al panel de archivos
        fileButton = tk.Button(filesPanel, text=name, font=("Consolas", 11, "bold"), bg="#4b6eaf", fg="#3b3d3f",
                               width=30,
                               height=2, relief=tk.FLAT, activebackground="#aaacad",
                               command=lambda: load_file_content(file_path))
        fileButton.pack(pady=2)

        # Actualizar el contador de archivos
        archivo = str(int(archivo) + 1)


def upload_file():
    global archivo
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    fileButton = archivo
    if file_path:
        file_name = os.path.basename(file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
        except UnicodeDecodeError:
            # Si falla con UTF-8, intentamos con 'latin-1'
            with open(file_path, 'r', encoding='latin-1') as file:
                file_content = file.read()

        codePanel.delete("1.0", tk.END)  # Limpiar el panel de código actual
        codePanel.insert(tk.END, file_content)
        update_line_numbers()
        name = file_name.replace('.txt', '')
        fileButton = tk.Button(filesPanel, text=name, font=("Consolas", 11, "bold"), bg="#4b6eaf", fg="#3b3d3f",
                               width=30,
                               height=2, relief=tk.FLAT, activebackground="#aaacad",
                               command=lambda: load_file_content(file_path))
        fileButton.pack(pady=2)
        archivo = (int(archivo) + 1)


def save_file():
    global archivo
    # Abrir el cuadro de diálogo para guardar archivo
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

    if file_path:
        # Guardar el contenido del codePanel en el archivo
        with open(file_path, 'w') as file:
            file_content = codePanel.get("1.0", tk.END).strip()
            file.write(file_content)

        # Obtener el nombre del archivo
        file_name = os.path.basename(file_path)
        name = file_name.replace('.txt', '')

        # Crear y añadir el botón del archivo al panel de archivos
        fileButton = tk.Button(filesPanel, text=name, font=("Consolas", 11, "bold"), bg="#4b6eaf", fg="#3b3d3f",
                               width=30,
                               height=2, relief=tk.FLAT, activebackground="#aaacad",
                               command=lambda: load_file_content(file_path))
        fileButton.pack(pady=2)

        # Actualizar el contador de archivos
        archivo = str(int(archivo) + 1)


# Crear la ventana principal
root = tk.Tk()
root.title("GUI")
root.configure(background='#343536')
widthWindow = 1600
heightWindow = 800
root.geometry(f"{widthWindow}x{heightWindow}")
root.resizable(False, False)

"""
Barra del menú
"""
# Crear el marco para la barra de menús
menuFrame = tk.Frame(root, bg="#3b3d3f", bd=0, height=50)
menuFrame.pack(side=tk.TOP, fill=tk.X)

"""
Botones del menú
"""
# Botón play
runImage = Image.open("Images/run.png")
runImage = runImage.resize((28, 28), PIL.Image.Resampling.LANCZOS)
runImageTk = ImageTk.PhotoImage(runImage)   

runButton = tk.Button(menuFrame, image=runImageTk, command=lambda: run_code(False, False), bg="#3b3d3f", relief=tk.FLAT, activebackground="#4c5052")
runButton.place(x=widthWindow-200, y=7)

# Botón del árbol de parseo
treeImage = Image.open("Images/tree.png")
treeImage = treeImage.resize((28, 28), PIL.Image.Resampling.LANCZOS)
treeImageTk = ImageTk.PhotoImage(treeImage)

treeButton = tk.Button(menuFrame, image=treeImageTk, command=lambda: run_code(True, False), bg="#3b3d3f", relief=tk.FLAT, activebackground="#4c5052")
treeButton.place(x=widthWindow-150, y=7)

# Botón de tabla de símbolos
tableImage = Image.open("Images/table.png")
tableImage = tableImage.resize((28, 28), PIL.Image.Resampling.LANCZOS)
tableImageTk = ImageTk.PhotoImage(tableImage)

tableButton = tk.Button(menuFrame, image=tableImageTk, command=lambda: run_code(False,True), bg="#3b3d3f", relief=tk.FLAT, activebackground="#4c5052")
tableButton.place(x=widthWindow-100, y=7)

# Botones de  archivos

newFileButton = tk.Button(menuFrame, text="Nuevo Archivo", font=("Consolas", 13, "bold"),
                          command=new_file, bg="#b4b4af", fg="#3b3d3f", relief=tk.FLAT, activebackground="#4b6eaf", activeforeground="#b4b4af")
newFileButton.place(x=15, y=7)  # Colocar entre "Subir Archivo" y "Guardar Archivo"

uploadButton = tk.Button(menuFrame, text="Subir Archivo", font=("Consolas", 13, "bold"),
                         command=upload_file, bg="#b4b4af", fg="#3b3d3f", relief=tk.FLAT, activebackground="#4b6eaf", activeforeground="#b4b4af")
uploadButton.place(x=170, y=7)

saveButton = tk.Button(menuFrame, text="Guardar Archivo", font=("Consolas", 13, "bold"),
                       command=save_file, bg="#b4b4af", fg="#3b3d3f", relief=tk.FLAT, activebackground="#4b6eaf", activeforeground="#b4b4af")
saveButton.place(x=325, y=7)

"""
Panel de consola, aquí se va a printear
"""
consolePanel = scrolledtext.ScrolledText(root, bg="#2b2b2b", fg="white", insertbackground="white",
                                         font=("Consolas", 11), height=10, bd=0, relief=tk.FLAT)
consolePanel.pack(side=tk.BOTTOM, fill=tk.X, padx=2, pady=2)

consoleLabel = tk.Label(root, text="Consola", bg="#3c3f41", fg="#828485", font=("Consolas", 13, "bold"), padx=10, pady=5, anchor=tk.W)
consoleLabel.pack(side=tk.BOTTOM, fill=tk.X, padx=2)

# Separador para estética
separator = tk.Frame(root, bg="#313335", height=25)
separator.pack(side=tk.BOTTOM, fill=tk.X)

"""
Ventana del dibujo generado
"""
# Función para abrir la nueva ventana con la matriz y los botones
def open_control_window():

    control_window = Toplevel(root)
    control_window.title("Control de Ejecución")
    control_window.geometry("800x700")
    control_window.configure(background="#2b2b2b")

    # Crear un contenedor para los botones
    button_frame = tk.Frame(control_window, bg="#2b2b2b")
    button_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

    # Botones en la parte superior
    step_button = tk.Button(button_frame, text="Step by Step", font=("Consolas", 12, "bold"),
                             bg="#4b6eaf", fg="white", relief=tk.FLAT, activebackground="#6b8ecf", activeforeground="white",
                             command=step_by_step_action)
    step_button.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

    final_button = tk.Button(button_frame, text="Final", font=("Consolas", 12, "bold"),
                              bg="#4b6eaf", fg="white", relief=tk.FLAT, activebackground="#6b8ecf", activeforeground="white",
                              command=final_action)
    final_button.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

    back_button = tk.Button(button_frame, text="Atrás", font=("Consolas", 12, "bold"),
                             bg="#4b6eaf", fg="white", relief=tk.FLAT, activebackground="#6b8ecf", activeforeground="white",
                             command=control_window.destroy)
    back_button.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

    # Crear un contenedor para la matriz
    matrix_frame = tk.Frame(control_window, bg="#2b2b2b")
    matrix_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # Crear la matriz en el Canvas
    create_canvas_matrix(matrix_frame, 64, 64, cell_size=10)

# Crear matriz de puntos usando Canvas
def create_canvas_matrix(parent, rows, cols, cell_size):
    canvas = Canvas(parent, bg="#2b2b2b", width=cols * cell_size, height=rows * cell_size, highlightthickness=0)
    canvas.pack(expand=True)

    # Dibujar la matriz de celdas
    for i in range(rows):
        for j in range(cols):
            x0, y0 = j * cell_size, i * cell_size
            x1, y1 = x0 + cell_size, y0 + cell_size
            rect_id = canvas.create_rectangle(x0, y0, x1, y1, fill="#48494a", outline="#2b2b2b")
            # Asociar eventos a las celdas
            canvas.tag_bind(rect_id, "<Button-1>", lambda e, id=rect_id: toggle_canvas_cell(canvas, id))

# Alternar el color de una celda en el Canvas
def toggle_canvas_cell(canvas, rect_id):
    current_color = canvas.itemcget(rect_id, "fill")
    new_color = "white" if current_color == "#48494a" else "#48494a"
    canvas.itemconfig(rect_id, fill=new_color)

# Acciones de los botones
def step_by_step_action():
    consolePanel.config(state=tk.NORMAL)
    consolePanel.insert(tk.END, "Ejecución paso a paso iniciada...\n", 'info')
    consolePanel.config(state=tk.DISABLED)
    consolePanel.tag_config('info', foreground="#6bcf8f", font=("Consolas", 13, "bold"))

def final_action():
    consolePanel.config(state=tk.NORMAL)
    consolePanel.insert(tk.END, "Ejecución final completada.\n", 'info')
    consolePanel.config(state=tk.DISABLED)
    consolePanel.tag_config('info', foreground="#6bcf8f", font=("Consolas", 13, "bold"))

import sys

class ConsoleRedirector:
    def __init__(self, console_panel):
        self.console_panel = console_panel

    def write(self, message):
        self.console_panel.config(state=tk.NORMAL)  # Habilitar el panel
        self.console_panel.insert(tk.END, message)  # Agregar el mensaje al final
        self.console_panel.see(tk.END)  # Hacer scroll hasta el final
        self.console_panel.config(state=tk.DISABLED)  # Deshabilitar el panel

    def flush(self):
        pass  # Método requerido para compatibilidad con `sys.stdout`





def ejecutar_asm(ast):
    global generador

    # Limpiar la consola antes de empezar
    consolePanel.config(state=tk.NORMAL)
    consolePanel.delete('1.0', tk.END)
    consolePanel.config(state=tk.DISABLED)

    # Ejemplo de AST de entrada con un for loop

    consolePanel.config(state=tk.NORMAL)
    consolePanel.insert(tk.END, "Generando código...\n", 'info')
    consolePanel.update()  # Forzar actualización de la interfaz
    consolePanel.config(state=tk.DISABLED)

    print(ast)

    generador.generar_codigo(ast)

    consolePanel.config(state=tk.NORMAL)
    consolePanel.insert(tk.END, "Código generado:\n", 'info')
    consolePanel.insert(tk.END, str(generador.module) + "\n")
    consolePanel.update()  # Forzar actualización
    consolePanel.config(state=tk.DISABLED)

    # Generar el archivo ensamblador .asm
    generador.generar_archivo_asm("output.asm")

    consolePanel.config(state=tk.NORMAL)
    consolePanel.insert(tk.END, "Archivo ensamblador generado: output.asm\n", 'info')
    consolePanel.update()  # Forzar actualización
    consolePanel.config(state=tk.DISABLED)

    # Opcionalmente: ejecutar el código LLVM usando el motor JIT
    modulo_llvm = binding.parse_assembly(str(generador.module))
    modulo_llvm.verify()

    target_machine = binding.Target.from_default_triple().create_target_machine()

    with binding.create_mcjit_compiler(modulo_llvm, target_machine) as ee:
        ee.finalize_object()

        # Llamar a la función main
        if "main" in generador.funciones:
            func_ptr = ee.get_function_address("main")
            import ctypes
            main_fn = ctypes.CFUNCTYPE(None)(func_ptr)

            consolePanel.config(state=tk.NORMAL)
            consolePanel.insert(tk.END, "Ejecutando función main...\n", 'info')
            consolePanel.update()  # Forzar actualización
            consolePanel.config(state=tk.DISABLED)

            main_fn()

    consolePanel.config(state=tk.NORMAL)
    consolePanel.insert(tk.END, "Ejecución completada.\n", 'info')
    consolePanel.update()  # Forzar actualización
    consolePanel.config(state=tk.DISABLED)


"""
Panel de izquierda
"""
leftPanel = tk.Frame(root, bg="#48494a", width=300)
leftPanel.pack(side=tk.LEFT, fill=tk.Y, padx=2, pady=2)

"""
Panel de archivos
"""
filesPanel = tk.Frame(leftPanel, bg="#48494a")
filesPanel.pack()

filesLabel = tk.Label(filesPanel, text="Archivos", bg="#3c3f41", fg="#828485", font=("Consolas", 13, "bold"), width=52)
filesLabel.pack(fill=tk.X)


"""
Panel de números de línea
"""
numbersPanel = tk.Frame(root, bg="#313335", width=100)
numbersPanel.pack(side=tk.LEFT, fill=tk.Y)

# Mover el área de números de línea al nuevo panel
numbersText = tk.Text(numbersPanel, bg="#313335", fg="#9d9d9e", width=5, state=tk.DISABLED,
                      font=("Consolas", 12), bd=0, relief=tk.FLAT)
numbersText.pack(side=tk.LEFT, fill=tk.Y)

"""
Panel de código
"""
# Crear un marco para contener el área de código y las barras de desplazamiento
codePanelFrame = tk.Frame(root, bg="#2b2b2b")
codePanelFrame.pack(expand=True, fill=tk.BOTH, padx=2, pady=2)

# Crear la barra de desplazamiento horizontal
h_scroll = Scrollbar(codePanelFrame, orient=tk.HORIZONTAL)
h_scroll.pack(side=tk.BOTTOM, fill=tk.X)  # Colocar la barra de desplazamiento en la parte inferior del marco

# Crear el área de texto con desplazamiento horizontal
codePanel = scrolledtext.ScrolledText(
    codePanelFrame,
    bg="#2b2b2b",
    fg="white",
    insertbackground="white",
    font=("Consolas", 12),
    bd=0,
    relief=tk.FLAT,
    wrap="none",  # Deshabilitar el ajuste automático de línea
    xscrollcommand=h_scroll.set  # Asociar la barra de desplazamiento horizontal
)
codePanel.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

# Configurar la barra de desplazamiento horizontal
h_scroll.config(command=codePanel.xview)

# Actualizar los números de línea al cambiar el contenido o desplazarse
codePanel.bind('<KeyRelease>', update_line_numbers)
codePanel.bind('<MouseWheel>', update_line_numbers)

root.mainloop()