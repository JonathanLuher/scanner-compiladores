class TipoToken:
    def _init_(self, tipo):
        self.tipo = tipo

class Token:
    def _init_(self, tipo, lexema, literal=None):
        self.tipo = tipo
        self.lexema = lexema
        self.literal = literal

    def _str_(self):
        return f"<{self.tipo} {self.lexema} {self.literal}>"
