import random
import math
import os

class Grafo:
    def __init__(self, es_dirigido):
        self.es_dirigido = es_dirigido
        self.nodos = []
        self.aristas = []

    def num_nodos(self):
        """
        Cantidad de nodos en el grafo.
        """
        return len(self.nodos) 

    def conectar_nodos(self, id_de, id_a, **kwargs):
        """
        Crea una arista y conecta 2 nodos dentro del grafo tomando en cuenta si es dirigido o no.
        """
        nodo_de = self.get_nodo(id_de)
        nodo_a = self.get_nodo(id_a)
        if nodo_de is None or nodo_a is None:
            return
        
        arista = Arista(**kwargs)
        self.aristas.append(arista)
        nodo_de.conectar_a(nodo_a, arista)

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
        Crea un nuevo nodo con ID único y las propiedades especificadas.
        """
        if self.get_nodo(id) is None:
            nodo = Nodo(id, **kwargs)
            self.nodos.append(nodo)

    def guardar(self, nombre_archivo, identificador = ""):
        """
        Guarda el grafo en un archivo GV con el nombre especificado.
        """
        try:
            os.mkdir("grafos")
            nombre_archivo = "grafos/" + nombre_archivo
        except FileExistsError:
            nombre_archivo = "grafos/" + nombre_archivo
            pass
        except:
            pass

        with open(nombre_archivo + ".gv", 'w') as archivo:
            archivo.write(("digraph " if self.es_dirigido else "graph ") + ((identificador + " {") if identificador else "{") + '\n')
            for nodo in self.nodos:
                if len(nodo.vecinos) == 0:
                    archivo.write(str(nodo) + ";\n")
                else:
                    for vecino in nodo.vecinos:
                        archivo.write(str(nodo) + (" -> " if self.es_dirigido else " -- ") + str(vecino[0]) + '\n')
            archivo.write("}\n")

    @classmethod
    def generar_malla(cls, n, m, es_dirigido = False):
        """
        Genera una malla de n filas por m columnas.
        :param n: Filas
        :param m: Columnas
        :return: Grafo
        """
        grafo = cls(es_dirigido)
        for i in range(0, n):
            for j in range(0, m):
                id_actual = j + (i * m)
                grafo.crear_nodo(id_actual)
                if (id_actual % m) != 0:
                    grafo.conectar_nodos(id_actual, id_actual - 1)
                if id_actual >= m:
                    grafo.conectar_nodos(id_actual, id_actual - m)
        return grafo
    
    @classmethod
    def generar_ErdosRenyi(cls, n, m, es_dirigido = False):
        """
        Crea un gráfo con el modelo Erdös-Renyi. Define n nodos y elige m parejas al azar.
        :param n: Cantidad de nodos
        :param m: Cantidad de aristas (>= n-1)
        :return: Grafo
        """
        grafo = cls(es_dirigido)
        for i in range(0, n):
            grafo.crear_nodo(i)
        for i in range(0, m):
            n_de = random.randrange(0, n)
            n_a = random.randrange(0, n)
            if n_de == n_a:
                n_a = (n_a + 1) % n
            grafo.conectar_nodos(n_de, n_a)
        return grafo
    
    @classmethod
    def generar_Gilbert(cls, n, p, es_dirigido = False):
        """
        Crea un gráfo con el modelo de Gilbert. Define n nodos con p probabilidad de cada uno conectarse con el resto.
        :param n: Cantidad de nodos
        :param p: [0 - 1] Probabilidad de conectar un nodo con el resto.
        :return: Grafo
        """
        p = min(p, 1) * 100
        grafo = cls(es_dirigido)
        for i in range(0, n):
            grafo.crear_nodo(i)
        for i in range(0, n):
            for j in range(0, n):
                if i == j:
                    break
                if(random.randint(0, 100) <= p):
                    grafo.conectar_nodos(i, j)
        return grafo
    
    @classmethod
    def generar_geo_simple(cls, n, r, es_dirigido = False):
        """
        Crea un gráfo con el método geográfico simple. Define n nodos con coordenadas aleatorias normales. 
        Se conectan aquellos entre distancia menor o igual a r. 
        :param n: Cantidad de nodos
        :param r: Distancia mínima para conectarse.
        :return: Grafo
        """
        r = min(r, 1)
        grafo = cls(es_dirigido)
        for i in range(0, n):
            grafo.crear_nodo(i, x = random.random(), y = random.random())
        for i in range(0, n):
            for j in range(0, n):
                if i == j:
                    break
                if (r >= math.dist([grafo.get_nodo(i).propiedad["x"], grafo.get_nodo(i).propiedad["y"]],
                                                 [grafo.get_nodo(j).propiedad["x"], grafo.get_nodo(i).propiedad["y"]])):
                    grafo.conectar_nodos(i, j)
        return grafo
    
    @classmethod
    def generar_BarbasiAlbert_variante(cls, n, d, es_dirigido = False):
        """
        Crea un gráfo con una variante del Método Barbasi-Albert. 
        :param n: Cantidad de nodos
        :param d: Grado máximo esperado por cada nodo.
        :return: Grafo
        """
        grafo = cls(es_dirigido)
        grafo.crear_nodo(0)
        nodos_revueltos = [0]

        for i in range(1, n):
            grafo.crear_nodo(i)
            if d <= 0:
                break
            random.shuffle(nodos_revueltos)
            for j in nodos_revueltos:
                probabilidad = 1 - (len(grafo.get_nodo(j).vecinos) / d)
                if random.random() <= probabilidad:
                    grafo.conectar_nodos(i,j)
                if len(grafo.get_nodo(i).vecinos) == d:
                    break
            nodos_revueltos.append(i)
        return grafo
    
    @classmethod
    def generar_DorogovtsevMendes(cls, n, es_dirigido = False):
        """
        Se crean 3 nodos y 3 aristas formando un triángulo.
        Para cada nodo adicional, se selecciona una arista al azar y se crean aristas entre sus extremos y el nodo nuevo.
        :param n: Cantidad de nodos (>= 3)
        :return: Grafo
        """
        n = max(n, 3)
        grafo = cls(es_dirigido)
        grafo.crear_nodo(0)
        grafo.crear_nodo(1)
        grafo.crear_nodo(2)
        grafo.conectar_nodos(0, 1)
        grafo.conectar_nodos(1, 2)
        grafo.conectar_nodos(2, 0)
        for i in range(3, n):
            grafo.crear_nodo(i)
            arista_de = random.randrange(0, i)
            arista_a = grafo.get_nodo(arista_de).vecinos[random.randrange(0, len(grafo.get_nodo(arista_de).vecinos))][0].identificador
            grafo.conectar_nodos(i, arista_de)
            grafo.conectar_nodos(i, arista_a)
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
        """
        Conecta el nodo al nodo especificado usando la arista dada.
        """
        for vecino in self.vecinos:
            if nodo is vecino[0]:
                self.vecinos.remove(vecino)
        arista.definir_extremos(self.identificador, nodo.identificador)
        self.vecinos.append((nodo, arista))

    def definir_propiedad(self, llave, valor):
        """
        Define la llave y valor de una propiedad en el nodo.
        """
        self.propiedad[llave] = valor


class Arista:
    def __init__(self, **kwargs):
        self.propiedad = {}
        self.extremos = ("", "")
        for llave, valor in kwargs.items():
                self.propiedad[llave] = valor
    
    def __str__(self):
        return str(self.extremos[0]) + " --> " + str(self.extremos[1])

    def definir_extremos(self, id_nodo_de, id_nodo_a):
        self.extremos = (id_nodo_de, id_nodo_a)

    def definir_propiedad(self, llave, valor):
        """
        Define la llave y valor de una propiedad en la arista.
        """
        self.propiedad[llave] = valor
