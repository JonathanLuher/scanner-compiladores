#this is the archive where we are doing the scanner
import os

def verificar_sintaxis_c(codigo):
    estado0 = 0
    estado11 = 0
    estado10 = 0

# Obtener la ruta absoluta del archivo .c basado en la ruta del programa
ruta_programa = os.path.abspath(__file__)
ruta_c = os.path.join(os.path.dirname(ruta_programa), "codigo.c")

try:
    with open(ruta_c, 'r') as file:
        codigo_c = file.read()
        verificar_sintaxis_c(codigo_c)
except FileNotFoundError:
    print("The file is not found")
except IOError:
    print("Wrong to read the file")