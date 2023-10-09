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

            if estado == 24:
                if c == '\n':
                    self.reportar_error(linea, "Se esperaban comillas para el cierre de la cadena")
                    estado = -1
                elif c == '"':
                    lexema += c
                    t = Token(TipoToken.STRING, lexema)
                    self.tokens.append(t)
                    estado = 0
                    lexema = ""
                else:
                    lexema += c

            if estado == 26:
                if c == '*':
                    estado = 27
                elif c == '/':
                    estado = 30
                else:
                    t = Token(TipoToken.SLASH, lexema)
                    self.tokens.append(t)
                    estado = 0
                    lexema = ""
                    i -= 1

            if estado == 27:
                if c == '*':
                    estado = 28
                else:
                    estado = 27

            if estado == 28:
                if c == '*':
                    estado = 28
                elif c == '/':
                    estado = 0
                    lexema = ""
                else:
                    estado = 27

            if estado == 30:
                if c == '\n':
                    estado = 0
                    lexema = ""
                else:
                    estado = 30

            if estado == 33:
                tt = self.simbolos.get(lexema)
                t = Token(tt, lexema)
                self.tokens.append(t)
                estado = 0
                lexema = ""
                i -= 1

            if estado == -1:
                break

        return self.tokens

    def reportar_error(self, linea, mensaje):
        print(f"[linea {linea}] Error: {mensaje}")
        self.error = True