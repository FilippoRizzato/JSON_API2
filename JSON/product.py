class Product:
    def __init__(self, id, nome, marca, prezzo):
        self.id = id
        self.nome= nome
        self.marca = marca
        self.prezzo = prezzo
        
    def getId(self):
        return self.id
    
    def setNome(self, nome):
        self.nome = nome
        
    def getNome(self):
        return self.nome
    
    def getMarca(self):
        return self.marca
    
    def setMarca(self, marca):
        self.marca = marca
        
    def getPrezzo(self):
        return self.prezzo
    
    def setPrezzo(self, prezzo):
        self.prezzo = prezzo