class Grafo:
    es_dirigido = False
    nodos = []

    def __init__(self, es_dirigido):
        self.es_dirigido = es_dirigido

    def num_nodos(self):
        return self.nodos.count 

    def conectar_nodos(self, id_de, id_a, **kwargs):
        """
        Conecta 2 nodos dentro del grafo tomando en cuenta si es dirigido o no.
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
        if self.get_nodo(id) is not None:
            nodo = Nodo(id)
            for llave, valor in kwargs.items():
                nodo.definir_propiedad(llave, valor)
            self.nodos.append(nodo)

    def guardar(nombre_archivo):
        #guardar en disco
        pass

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
    identificador = ""
    propiedad = {}
    vecinos = [] ##tuplas (nodo, arista)

    def __init__(self, id):
        self.identificador = id
    
    def conectar_a(self, nodo, arista):
        for vecino in self.vecinos:
            if nodo is vecino[0]:
                self.vecinos.remove(vecino)
        self.vecinos.append((nodo, arista))

    def definir_propiedad(self, llave, valor):
        self.propiedad[llave] = valor

class Arista:
    propiedad = {}

    def __init__(self, **kwargs):
        for llave, valor in kwargs.items():
                self.propiedad[llave] = valor        

    def definir_propiedad(self, llave, valor):
        self.propiedad[llave] = valor

##{Nodo, Nodo, Nodo, Nodo
