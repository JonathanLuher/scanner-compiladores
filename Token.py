from TipoToken import TipoToken 

class Token:
  def __init__(self, tipo, lexema, literal=None): 
    self.tipo = tipo
        self.lexema = lexema
        self.literal = literal

    def __str__(self):
        return f"<{self.tipo} {self.lexema} {self.literal}>"

