import sys
from Scanner import Scanner

def main():
    if len(sys.argv) > 1:
        archivo = sys.argv[1]
        try:
            with open(archivo, "r") as file:
                source = file.read()
                ejecutar(source)
        except FileNotFoundError:
            print(f"El archivo '{archivo}' no existe.")
    else:
        ejecutar_terminal()

def ejecutar(source):
    scanner = Scanner(source)
    tokens = scanner.scan()

    for token in tokens:
        print(token)

def ejecutar_terminal():
    while True:
        source = input(">>> ")
        if not source:
            break
        ejecutar(source)

if __name__ == "__main__":
    main()
