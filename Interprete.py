import sys
import os

from scanner import Scanner

existen_errores = False

def main():
    if len(sys.argv) > 1:
        print("Uso correcto: Interprete [archivo.txt]")
        sys.exit(64)
    elif len(sys.argv) == 1:
        ejecutar_archivo(sys.argv[1])
    else:
        ejecutar_prompt() 
        #nos ayuda a ver como va a empezar a ejecutar el programa

def ejecutar_archivo(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            codigo = file.read()
            ejecutar(codigo)

        # Se indica que existe un error
        if existen_errores:
            sys.exit(65)
    except FileNotFoundError:
        print(f"Archivo '{path}' no encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Error al ejecutar el archivo: {e}")
        sys.exit(1)
        
def ejecutarPrompt():
    try:
        while True:
            linea = input(">>> ")
            if not linea:
                break  # Presionar Ctrl + D o dejar la línea en blanco para salir
            ejecutar(linea)
            existenErrores = False
    except KeyboardInterrupt:
        pass  # Manejar la interrupción de Ctrl + C

def ejecutar(codigo_fuente):
    try:
        scanner = Scanner(codigo_fuente)
        tokens = scanner.scan()

        for token in tokens:
            print(token)
    except Exception as ex:
        print(ex)

# El método error se puede usar desde las distintas clases para
# reportar los errores: Main.error(...);

def error(linea, mensaje):
    reportar(linea, "", mensaje)

def reportar(linea, posicion, mensaje):
    print(f"[linea {linea}] Error {posicion}: {mensaje}")
    existen_errores = True


if __name__ == "__main__":
    main()
