from TipoToken import TipoToken
from Token import Token

class Scanner:
    palabras_reservadas = {
        "and": TipoToken.AND,
        "else": TipoToken.ELSE,
        "false": TipoToken.FALSE,
        "for": TipoToken.FOR,
        "fun": TipoToken.FUN,
        "if": TipoToken.IF,
        "null": TipoToken.NULL,
        "or": TipoToken.OR,
        "print": TipoToken.PRINT,
        "return": TipoToken.RETURN,
        "true": TipoToken.TRUE,
        "var": TipoToken.VAR,
        "while": TipoToken.WHILE,
    }

    simbolos = {
        "+": TipoToken.PLUS,
        "-": TipoToken.MINUS,
        "*": TipoToken.STAR,
        "{": TipoToken.LEFT_BRACE,
        "}": TipoToken.RIGHT_BRACE,
        "(": TipoToken.LEFT_PAREN,
        ")": TipoToken.RIGHT_PAREN,
        ",": TipoToken.COMMA,
        ".": TipoToken.DOT,
        ";": TipoToken.SEMICOLON,
    }

    def __init__(self, source):
        self.source = source + " "
        self.tokens = []
        self.lexema = ""
        self.estado = 0
        self.linea = 1
        self.caracteres_especiales = set(["+", "-", "*", "{", "}", "(", ")", ",", ".", ";"])

    def __init__(self, source):
        self.source = source + " "
        self.tokens = []
        self.caracteres = ["+", "-", "*", "{", "}", "(", ")", ",", ".", ";"]
        self.error = False

    def scan(self):
        lexema = ""
        estado = 0
        linea = 1

        for i, c in enumerate(self.source):
            if i >= 1 and self.source[i - 1] == '\n':
                linea += 1

            if estado == 0:
                if c.isalpha():
                    estado = 13
                    lexema += c
                elif c.isdigit():
                    estado = 15
                    lexema += c
                elif c == '>':
                    estado = 1
                    lexema += c
                elif c == '<':
                    estado = 4
                    lexema += c
                elif c == '=':
                    estado = 7
                    lexema += c
                elif c == '!':
                    estado = 10
                    lexema += c
                elif c == '/':
                    estado = 26
                    lexema += c
                elif c == '"':
                    estado = 24
                    lexema += c
                elif c in self.caracteres:
                    estado = 33
                    lexema += c

            
            if estado == 1:
                if c == '=':
                    lexema += c
                    t = Token(TipoToken.GREATER_EQUAL, lexema)
                    self.tokens.append(t)
                else:
                    t = Token(TipoToken.GREATER, lexema)
                    self.tokens.append(t)
                    i -= 1
                estado = 0
                lexema = ""

            if estado == 4:
                if c == '=':
                    lexema += c
                    t = Token(TipoToken.LESS_EQUAL, lexema)
                    self.tokens.append(t)
                else:
                    t = Token(TipoToken.LESS, lexema)
                    self.tokens.append(t)
                    i -= 1
                estado = 0
                lexema = ""

            if estado == 7:
                if c == '=':
                    lexema += c
                    t = Token(TipoToken.EQUAL_EQUAL, lexema)
                    self.tokens.append(t)
                else:
                    t = Token(TipoToken.EQUAL, lexema)
                    self.tokens.append(t)
                    i -= 1
                estado = 0
                lexema = ""

            if estado == 10:
                if c == '=':
                    lexema += c
                    t = Token(TipoToken.BANG_EQUAL, lexema)
                    self.tokens.append(t)
                else:
                    t = Token(TipoToken.BANG, lexema)
                    self.tokens.append(t)
                    i -= 1
                estado = 0
                lexema = ""

            if estado == 13:
                if c.isalpha() or c.isdigit():
                    lexema += c
                else:
                    tt = self.palabras_reservadas.get(lexema)
                    if tt is None:
                        t = Token(TipoToken.IDENTIFIER, lexema)
                        self.tokens.append(t)
                    else:
                        t = Token(tt, lexema)
                        self.tokens.append(t)
                    estado = 0
                    lexema = ""
                    i -= 1

            if estado == 15:
                if c.isdigit():
                    lexema += c
                elif c == '.':
                    estado = 16
                    lexema += c
                elif c == 'E':
                    estado = 18
                    lexema += c
                else:
                    t = Token(TipoToken.NUMBER, lexema, int(lexema))
                    self.tokens.append(t)
                    estado = 0
                    lexema = ""
                    i -= 1

            if estado == 16:
                if c.isdigit():
                    estado = 17
                    lexema += c
                else:
                    self.reportar_error(linea, "Se esperaba un número para parte decimal")
                    estado = -1

            if estado == 17:
                if c.isdigit():
                    lexema += c
                elif c == 'E':
                    estado = 18
                    lexema += c
                else:
                    t = Token(TipoToken.NUMBER, lexema, float(lexema))
                    self.tokens.append(t)
                    estado = 0
                    lexema = ""
                    i -= 1



                
               if estado == 18:
                if c in ('+', '-'):
                    estado = 19
                    lexema += c
                elif c.isdigit():
                    estado = 20
                    lexema += c
                else:
                    self.reportar_error(linea, "Se esperaba un '+', un '-' o un número para exponente")
                    estado = -1

            if estado == 19:
                if c.isdigit():
                    estado = 20
                    lexema += c
                else:
                    self.reportar_error(linea, "Se esperaba un número para parte exponente")
                    estado = -1

            if estado == 20:
                if c.isdigit():
                    lexema += c
                else:
                    t = Token(TipoToken.NUMBER, lexema, float(lexema))
                    self.tokens.append(t)
                    estado = 0
                    lexema = ""
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
