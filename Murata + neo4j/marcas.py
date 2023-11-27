class Marca:

   def __init__(self, nombre, padre):
      self.nombre = nombre
      self.hijos = []
      self.padre = padre
      # print(f"marca creada {nombre}")

   def agregarHijo(self, hijo):
      self.hijos = hijo
      # print(f" Marca {self.nombre} Hijos {self.hijos}")
      print()


   def padre(self):
      return self.padre()