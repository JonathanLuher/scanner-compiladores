import sys
from Scanner import Scanner

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "Pruebas.txt":
        try:
            with open("Pruebas.txt", "r") as file:
                source = file.read()
                ejecutar(source)
        except FileNotFoundError:
            print("El archivo 'pruebas.txt' no existe.")
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
