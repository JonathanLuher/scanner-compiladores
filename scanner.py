#this is the archive where we are doing the scanner
class TipoToken:
    def __init__(self, tipo):
        self.tipo = tipo

class Token:
    def __init__(self, tipo, lexema, valor=None):
        self.tipo = tipo
        self.lexema = lexema
        self.valor = valor

class Scanner:
    palabras_reservadas = {
        "and": TipoToken("AND"),
        "else": TipoToken("ELSE"),
        "false": TipoToken("FALSE"),
        "for": TipoToken("FOR"),
        "fun": TipoToken("FUN"),
        "if": TipoToken("IF"),
        "null": TipoToken("NULL"),
        "or": TipoToken("OR"),
        "print": TipoToken("PRINT"),
        "return": TipoToken("RETURN"),
        "true": TipoToken("TRUE"),
        "var": TipoToken("VAR"),
        "while": TipoToken("WHILE")
    }

    simbolos = {
        "+": TipoToken("PLUS"),
        "-": TipoToken("MINUS"),
        "*": TipoToken("STAR"),
        "{": TipoToken("LEFT_BRACE"),
        "}": TipoToken("RIGHT_BRACE"),
        "(": TipoToken("LEFT_PAREN"),
        ")": TipoToken("RIGHT_PAREN"),
        ",": TipoToken("COMMA"),
        ".": TipoToken("DOT"),
        ";": TipoToken("SEMICOLON"),
    }

    def __init__(self, source):
        self.source = source + " "
        self.tokens = []
        self.lexema = ""
        self.estado = 0
        self.linea = 1
        self.caracteres_especiales = set(["+", "-", "*", "{", "}", "(", ")", ",", ".", ";"])

    def scan(self):
        for i in range(len(self.source)):
            c = self.source[i]
            if i >= 1 and self.source[i - 1] == '\n':
                self.linea += 1

            if self.estado == 0:
                if c.isalpha():
                    self.estado = 13
                    self.lexema += c
                elif c.isdigit():
                    self.estado = 15
                    self.lexema += c
                elif c == '>':
                    self.estado = 1
                    self.lexema += c
                elif c == '<':
                    self.estado = 4
                    self.lexema += c
                elif c == '=':
                    self.estado = 7
                    self.lexema += c
                elif c == '!':
                    self.estado = 10
                    self.lexema += c
                elif c == '/':
                    self.estado = 26
                    self.lexema += c
                elif c == '"':
                    self.estado = 24
                    self.lexema += c
                elif c in self.caracteres_especiales:
                    self.estado = 33
                    self.lexema += c
            elif self.estado == 1:
                if c == '=':
                    self.lexema += c
                    self.add_token(self.get_tipo_token(TipoToken, "GREATER_EQUAL"), self.lexema)
                else:
                    self.add_token(self.get_tipo_token(TipoToken, "GREATER"), self.lexema)
                    i -= 1
                self.estado = 0
                self.lexema = ""
            elif self.estado == 4:
                if c == '=':
                    self.lexema += c
                    self.add_token(self.get_tipo_token(TipoToken, "LESS_EQUAL"), self.lexema)
                else:
                    self.add_token(self.get_tipo_token(TipoToken, "LESS"), self.lexema)
                    i -= 1
                self.estado = 0
                self.lexema = ""
            elif self.estado == 7:
                if c == '=':
                    self.lexema += c
                    self.add_token(self.get_tipo_token(TipoToken, "EQUAL_EQUAL"), self.lexema)
                else:
                    self.add_token(self.get_tipo_token(TipoToken, "EQUAL"), self.lexema)
                    i -= 1
                self.estado = 0
                self.lexema = ""
            elif self.estado == 10:
                if c == '=':
                    self.lexema += c
                    self.add_token(self.get_tipo_token(TipoToken, "BANG_EQUAL"), self.lexema)
                else:
                    self.add_token(self.get_tipo_token(TipoToken, "BANG"), self.lexema)
                    i -= 1
                self.estado = 0
                self.lexema = ""
            elif self.estado == 13:
                if c.isalnum():
                    self.lexema += c
                else:
                    self.add_identifier_or_reserved_word_token(self.lexema)
                    self.estado = 0
                    self.lexema = ""
                    i -= 1
            elif self.estado == 15:
                if c.isdigit():
                    self.lexema += c
                elif c == '.':
                    self.estado = 16
                    self.lexema += c
                elif c == 'E':
                    self.estado = 18
                    self.lexema += c
                else:
                    self.add_token(self.get_tipo_token(TipoToken, "NUMBER"), self.lexema, int(self.lexema))
                    self.estado = 0
                    self.lexema = ""
                    i -= 1
            elif self.estado == 16:
                if c.isdigit():
                    self.estado = 17
                    self.lexema += c
                else:
                    Main.error(self.linea, "Se esperaba un número para parte decimal")
                    self.estado = -1
            elif self.estado == 17:
                if c.isdigit():
                    self.lexema += c
                elif c == 'E':
                    self.estado = 18
                    self.lexema += c
                else:
                    self.add_token(self.get_tipo_token(TipoToken, "NUMBER"), self.lexema, float(self.lexema))
                    self.estado = 0
                    self.lexema = ""
                    i -= 1
            elif self.estado == 18:
                if c in ('+', '-'):
                    self.estado = 19
                    self.lexema += c
                elif c.isdigit():
                    self.estado = 20
                    self.lexema += c
                else:
                    Main.error(self.linea, "Se esperaba un '+', un '-' o un número para exponente")
                    self.estado = -1
            elif self.estado == 19:
                if c.isdigit():
                    self.estado = 20
                    self.lexema += c
                else:
                    Main.error(self.linea, "Se esperaba un número para parte exponente")
                    self.estado = -1
            elif self.estado == 20:
                if c.isdigit():
                    self.lexema += c
                else:
                    self.add_token(self.get_tipo_token(TipoToken, "NUMBER"), self.lexema, float(self.lexema))
                    self.estado = 0
                    self.lexema = ""
                    i -= 1
            elif self.estado == 24:
                if c == '\n':
                    Main.error(self.linea, "Se esperaban comillas para el cierre de la cadena")
                    self.estado = -1
                elif c == '"':
                    self.lexema += c
                    self.add_token(self.get_tipo_token(TipoToken, "STRING"), self.lexema)
                    self.estado = 0
                    self.lexema = ""
                else:
                    self.lexema += c
            elif self.estado == 26:
                if c == '*':
                    self.estado = 27
                elif c == '/':
                    self.estado = 30
                else:
                    self.add_token(self.get_tipo_token(TipoToken, "SLASH"), self.lexema)
                    self.estado = 0
                    self.lexema = ""
                    i -= 1
            elif self.estado == 27:
                if c == '*':
                    self.estado = 28
                else:
                    self.estado = 27
            elif self.estado == 28:
                if c == '*':
                    self.estado = 28
                elif c == '/':
                    self.estado = 0
                    self.lexema = ""
                else:
                    self.estado = 27
            elif self.estado == 30:
                if c == '\n':
                    self.estado = 0
                    self.lexema = ""
                else:
                    self.estado = 30
            elif self.estado == 33:
                self.add_token(self.get_tipo_token(TipoToken, self.lexema), self.lexema)
                self.estado = 0
                self.lexema = ""
                i -= 1
            else:
                Main.error(self.linea, "Error desconocido")
                self.lexema = ""

            if self.estado == -1:
                break

        return self.tokens

    def add_token(self, tipo, lexema, valor=None):
        self.tokens.append(Token(tipo, lexema, valor))

    def add_identifier_or_reserved_word_token(self, lexema):
        tt = Scanner.palabras_reservadas.get(lexema)
        if tt is None:
            self.add_token(TipoToken("IDENTIFIER"), lexema)
        else:
            self.add_token(tt, lexema)
    
    @staticmethod
    def get_tipo_token(clase_tipo_token, tipo):
        return getattr(clase_tipo_token, tipo)

class Main:
    @staticmethod
    def error(linea, mensaje):
        print(f"Error en línea {linea}: {mensaje}")

# Uso del escáner
codigo_fuente = """
if x > 5:
    print("Mayor que 5")
else:
    print("Menor o igual que 5")
"""

scanner = Scanner(codigo_fuente)
tokens = scanner.scan()

for token in tokens:
    print(f"Tipo: {token.tipo.tipo}, Lexema: {token.lexema}, Valor: {token.valor}")
