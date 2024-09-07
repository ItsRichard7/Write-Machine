import tkinter as tk
from tkinter import scrolledtext, filedialog
from PIL import Image, ImageTk  # Importa Pillow
import os


global archivo
archivo = "1"

def run_code():
    code = codePanel.get("1.0", tk.END).strip()
    consolePanel.config(state=tk.NORMAL)
    #consolePanel.delete('1.0', tk.END)
    consolePanel.insert(tk.END, "Código ingresado:\n")
    consolePanel.insert(tk.END, code + '\n')
    consolePanel.config(state=tk.DISABLED)

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

def upload_file():
    global archivo
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    fileButton = archivo
    if file_path:
        file_name = os.path.basename(file_path)
        with open(file_path, 'r') as file:
            file_content = file.read()
            codePanel.delete("1.0", tk.END)  # Limpiar el panel de código actual
            codePanel.insert(tk.END, file_content)
            update_line_numbers()
            fileButton = tk.Button(filesPanel, text=file_name, font=("Consolas", 11, "bold"), bg="#4b6eaf", fg="#3b3d3f", width=30,
                                height=2, relief=tk.FLAT, activebackground="#aaacad", command=lambda: load_file_content(file_path))
            fileButton.pack(pady=2)
            archivo = (int(archivo) + 1)


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
runImage = runImage.resize((28, 28), Image.ANTIALIAS)
runImageTk = ImageTk.PhotoImage(runImage)

runButton = tk.Button(menuFrame, image=runImageTk, command=run_code, bg="#3b3d3f", relief=tk.FLAT, activebackground="#4c5052")
runButton.place(x=widthWindow-200, y=7)

# Botón del árbol de parseo
treeImage = Image.open("Images/tree.png")
treeImage = treeImage.resize((28, 28), Image.ANTIALIAS)
treeImageTk = ImageTk.PhotoImage(treeImage)

treeButton = tk.Button(menuFrame, image=treeImageTk, command=run_code, bg="#3b3d3f", relief=tk.FLAT, activebackground="#4c5052")
treeButton.place(x=widthWindow-150, y=7)

# Botón de tabla de símbolos
tableImage = Image.open("Images/table.png")
tableImage = tableImage.resize((28, 28), Image.ANTIALIAS)
tableImageTk = ImageTk.PhotoImage(tableImage)

tableButton = tk.Button(menuFrame, image=tableImageTk, command=run_code, bg="#3b3d3f", relief=tk.FLAT, activebackground="#4c5052")
tableButton.place(x=widthWindow-100, y=7)

# Botón de subir archivo
uploadButton = tk.Button(menuFrame, text="Subir Archivo", font=("Consolas", 13, "bold"),
                         command=upload_file, bg="#b4b4af", fg="#3b3d3f", relief=tk.FLAT, activebackground="#4b6eaf", activeforeground="#b4b4af")
uploadButton.place(x=15, y=7)

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

editableFile = tk.Button(filesPanel, text="Archivo editable", font=("Consolas", 11, "bold"), bg="#4b6eaf", fg="#3b3d3f", width=30,
                         height=2, relief=tk.FLAT, activebackground="#aaacad", command=lambda: [codePanel.delete("1.0", tk.END),update_line_numbers()])
editableFile.pack()


"""
Panel de errores
"""
warningsPanel = tk.Frame(leftPanel, bg="#3c3f41", height=400)
warningsPanel.pack()

warningsLabel = tk.Label(warningsPanel, text="Errores y precauciones", bg="#3c3f41", fg="#828485", font=("Consolas", 13, "bold"), width=50)
warningsLabel.pack(fill=tk.X, padx=10, pady=5)

error1 = tk.Label(warningsPanel, text="Error 1: En la línea 3", font=("Consolas", 11), bg="#48494a", fg="#c26364", padx=100, pady=5)
error1.pack(fill=tk.X)

error2 = tk.Label(warningsPanel, text="Error 2: En la línea 13", font=("Consolas", 11), bg="#48494a", fg="#c26364", padx=100, pady=5)
error2.pack(fill=tk.X)


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
codePanel = scrolledtext.ScrolledText(root, bg="#2b2b2b", fg="white", insertbackground="white",
                                      font=("Consolas", 12), bd=0, relief=tk.FLAT)
codePanel.pack(expand=True, fill=tk.BOTH, padx=2, pady=2)

# Actualizar los números de línea al cambiar el contenido o desplazarse
codePanel.bind('<KeyRelease>', update_line_numbers)
codePanel.bind('<MouseWheel>', update_line_numbers)

root.mainloop()
