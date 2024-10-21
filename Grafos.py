class Grafo:    

    def __init__(self, es_dirigido):
        self.es_dirigido = es_dirigido
        self.nodos = []

    def num_nodos(self):
        return self.nodos.count 

    def conectar_nodos(self, id_de, id_a, **kwargs):
        """
        Crea una arista y conecta 2 nodos dentro del grafo tomando en cuenta si es dirigido o no.
        """
        nodo_de = self.get_nodo(id_de)
        nodo_a = self.get_nodo(id_a)
        if nodo_de is None or nodo_a is None:
            return
        
        arista = Arista(**kwargs)
        nodo_de.conectar_a(nodo_a, arista)
        if not self.es_dirigido:
            nodo_a.conectar_a(nodo_de, arista)

    def get_nodo(self, id):
        """
        Devuelve el nodo con el ID especificado o None si no existe.
        """
        for nodo in self.nodos:
            if nodo.identificador == id:
                return nodo
        return None
    
    def crear_nodo(self, id, **kwargs):
        """
        Crea un nuevo nodo con ID único.
        """
        if self.get_nodo(id) is None:
            nodo = Nodo(id, **kwargs)
            self.nodos.append(nodo)

    def guardar(self, nombre_archivo, identificador = ""):
        with open(nombre_archivo + ".gv", 'w') as archivo:
            archivo.write(("digraph " if self.es_dirigido else "graph ") + ((identificador + " {") if identificador else "{") + '\n')
            for nodo in self.nodos:
                for vecino in nodo.vecinos:
                    archivo.write(str(nodo.identificador) + (" -> " if self.es_dirigido else " -- ") + str(vecino[0].identificador) + '\n')
            archivo.write("}")

    @classmethod
    def generar_malla(cls, n, m, es_dirigido = False):
        grafo = cls(es_dirigido)
        return grafo
    
    @classmethod
    def generar_ErdosRenyi(cls, n, m, es_dirigido = False):
        grafo = cls(es_dirigido)
        return grafo
    
    @classmethod
    def generar_Gilbert(cls, n, p, es_dirigido = False):
        grafo = cls(es_dirigido)
        return grafo
    
    @classmethod
    def generar_geo_simple(cls, n, r, es_dirigido = False):
        grafo = cls(es_dirigido)
        return grafo
    
    @classmethod
    def generar_BarbasiAlbert_variante(cls, n, d, es_dirigido = False):
        grafo = cls(es_dirigido)
        return grafo
    
    @classmethod
    def generar_DorogovtsevMendes(cls, n, es_dirigido = False):
        grafo = cls(es_dirigido)
        return grafo

class Nodo:
    def __init__(self, id, **kwargs):
        self.identificador = id
        self.propiedad = {}
        self.vecinos = [] ##tuplas (nodo, arista)
        for llave, valor in kwargs.items():
                self.propiedad[llave] = valor
    
    def __str__(self):
        return str(self.identificador)
    
    def conectar_a(self, nodo, arista):
        for vecino in self.vecinos:
            if nodo is vecino[0]:
                self.vecinos.remove(vecino)    
        self.vecinos.append((nodo, arista))

    def definir_propiedad(self, llave, valor):
        self.propiedad[llave] = valor

class Arista:    

    def __init__(self, **kwargs):
        self.propiedad = {}
        for llave, valor in kwargs.items():
                self.propiedad[llave] = valor        

    def definir_propiedad(self, llave, valor):
        self.propiedad[llave] = valor
