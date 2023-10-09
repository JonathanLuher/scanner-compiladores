from Scanner import Scanner
import sys

def ejecutar_archivo(path):
    try:
        with open(path, "r") as archivo:
            source = archivo.read()
            scanner = Scanner(source)
            tokens = scanner.scan()

            for token in tokens:
                print(token)
    except FileNotFoundError:
        print(f"No se pudo encontrar el archivo '{path}'")

def main():
    existen_errores = False

    if len(sys.argv) != 1:
        print("Uso correcto: Interprete")
        sys.exit(64)

    ejecutar_archivo("Pruebas.txt")

if __name__ == "__main__":
    main()

