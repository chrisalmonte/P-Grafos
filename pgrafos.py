import random
import math
import os
from copy import deepcopy

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
        Crea un nuevo nodo con ID único y las propiedades especificadas.
        """
        if self.get_nodo(id) is None:
            nodo = Nodo(id, **kwargs)
            self.nodos.append(nodo)
    
    def copiar_nodo(self, nodo, nuevo_id = None):
        """
        Agrega una copia sin vecinos de un objeto de clase Nodo al grafo, siempre y cuando no exista un nodo con el mismo identificador en el grafo. 
        :param nodo: Nodo a agregar.
        """
        if self.get_nodo(nodo.identificador) is None:
            copia = Nodo(nodo.identificador if (nuevo_id is None) else nuevo_id)
            copia.propiedad = nodo.propiedad.copy()
            self.nodos.append(copia)

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
                if len(nodo.vecinos) == 0 or nodo.propiedad:
                    archivo.write(str(nodo) + ";")
                    archivo.write(" [" if nodo.propiedad else "")
                    for propiedad in nodo.propiedad:
                        archivo.write(" " + str(propiedad) + "=" + str(nodo.propiedad[propiedad]) + " ")
                    archivo.write("]\n" if nodo.propiedad else "\n")
                for vecino in nodo.vecinos:
                        archivo.write(str(nodo) + (" -> " if self.es_dirigido else " -- ") + str(vecino[0]))
                        archivo.write(" [" if nodo.propiedad else "")
                        for propiedad in vecino[1].propiedad:
                            archivo.write(" " + str(propiedad) + "=" + str(vecino[1].propiedad[propiedad]) + " ")
                        archivo.write("]\n" if nodo.propiedad else "\n")
            archivo.write("}\n")
    
    def BFS(self, s):
        """
        Genera un grafo con el árbol inducido por el algorítmo de búsqueda "Breadth First Search".
        :param s: ID del nodo de inicio. 
        :return: Grafo
        """
        if(self.get_nodo(s) is None):
            return None
        capas = [[s]]
        descubiertos = [s]
        arbol = Grafo(self.es_dirigido)
        arbol.copiar_nodo(self.get_nodo(s))
        capas.append([])
        for capa in capas:
            capas.append([])
            for nodoActual in capa:
                for vecino in self.get_nodo(nodoActual).vecinos:
                    id = vecino[0].identificador
                    if id not in descubiertos:
                        descubiertos.append(id)
                        capas[-1].append(id)
                        arbol.copiar_nodo(vecino[0])
                        arbol.conectar_nodos(self.get_nodo(nodoActual).identificador, id)
            if not capas[-1]:
                capas.pop()
        return arbol

    def DFS_iterativo(self, s):
        """
        Genera un grafo con el árbol inducido por el algorítmo de búsqueda "Depth First Search" de manera iterativa.
        :param s: ID del nodo de inicio. 
        :return: Grafo
        """
        if(self.get_nodo(s) is None):
            return None
        descubiertos = [self.get_nodo(s)]
        index_nodo_raiz = 0
        nodo_siguiente = None
        arbol = Grafo(self.es_dirigido)
        arbol.copiar_nodo(descubiertos[0])
        while index_nodo_raiz > -1:
            nodo_siguiente = None
            for vecino in descubiertos[index_nodo_raiz].vecinos:
                if (vecino[0] not in descubiertos):
                    arbol.copiar_nodo(vecino[0])
                    arbol.conectar_nodos(descubiertos[index_nodo_raiz].identificador, vecino[0].identificador)
                    descubiertos.insert(index_nodo_raiz + 1, vecino[0])
                    index_nodo_raiz += 1
                    nodo_siguiente = vecino[0]
                    break
            if (nodo_siguiente is None):
                index_nodo_raiz = (index_nodo_raiz - 1)
        return arbol

    def DFS_recursivo(self, s):
        """
        Genera un grafo con el árbol inducido por el algorítmo de búsqueda "Depth First Search" de manera recursiva y
        limpia el árbol de las propiedades "visitado".
        :param s: ID del nodo de inicio. 
        :return: Grafo
        """
        arbol = self.DFS_llamada_recursiva(s)
        for nodo in self.nodos:
            nodo.propiedad.pop("dfs_visitado", "")
        return arbol

    
    def DFS_llamada_recursiva(self, s):
        """
        No invocar directamente. Para generar el DFS de manera recursiva utilice el método "DFS_recursivo".
        """
        if(self.get_nodo(s) is None):
            return None
        nodo_origen = self.get_nodo(s)
        nodo_origen.definir_propiedad("dfs_visitado", True)
        arbol = Grafo(self.es_dirigido)
        arbol.copiar_nodo(nodo_origen)        
        for vecino in nodo_origen.vecinos:
            if not vecino[0].propiedad.get("dfs_visitado", False):
                arbol.nodos.extend(self.DFS_llamada_recursiva(vecino[0].identificador).nodos)
                arbol.conectar_nodos(s, vecino[0].identificador)
        return arbol
    
    def dijkstra(self, s):
        """
        Genera un grafo generado con el algorítmo de Dijkstra, en el que se etiqueta cada nodo con las distancias a partir de el nodo s.
        Requiere de la propiedad en las aristas llamadas "distancia", de otra forma se tomará como 0.
        
        Parameters:
            s (Any): ID del nodo de inicio.
        Returns:
          grafos (tuple): Tupla donde el elemento [0] es una copia del grafo etiquetado con las distancias y [1] el árbol inducido.
        """
        if(self.get_nodo(s) is None):
            return None
        dijkstra = deepcopy(self)
        arbol = Grafo(self.es_dirigido)
        for nodo in dijkstra.nodos:
            nodo.definir_propiedad("dja_distancia_min", math.inf)
            nodo.definir_propiedad("dja_calculado", False)
            nodo.definir_propiedad("dja_descubierto", False)
        nodo_s = dijkstra.get_nodo(s)
        nodo_s.definir_propiedad("color", "red")
        nodo_s.definir_propiedad("dja_distancia_min", 0)

        capas = [[nodo_s]]
        for capa in capas:
            capas.append([])
            for nodo_a_calcular in capa:
                if not nodo_a_calcular.propiedad["dja_calculado"]:
                    for vecino in nodo_a_calcular.vecinos:
                        if not vecino[0].propiedad["dja_calculado"]:
                            vecino[0].definir_propiedad("dja_distancia_min", min(vecino[0].propiedad["dja_distancia_min"], (nodo_a_calcular.propiedad["dja_distancia_min"] + vecino[1].propiedad.get("distancia", 0))))
                            if not vecino[0].propiedad["dja_descubierto"]:
                                capas[-1].append(vecino[0])
                                vecino[0].definir_propiedad("dja_descubierto", True)
                nodo_a_calcular.definir_propiedad("dja_calculado", True)
            if not capas[-1]:
                capas.pop()
        for nodo in dijkstra.nodos:
            nodo.propiedad.pop("dja_calculado", "")
            nodo.propiedad.pop("dja_descubierto", "")
        return (dijkstra, arbol)
        
        

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
    
    @classmethod
    def generar_desde_archivo(cls, ruta):
        """
        Genera el grafo a partir de un archivo .gv creado por pgrafos.
        :param ruta: Ruta del archivo.
        """
        grafo = None
        conector = "--"

        if not os.path.exists(ruta):
            print("No se encuentra el archivo de grafo especificado. (" + str(ruta) + ")")
            return grafo
        
        with open(ruta) as archivo:
            for linea in archivo:
                if grafo is None:
                    if linea.find('{') != -1:
                        grafo = cls(linea.find("digraph") != -1)
                        conector = ("->" if grafo.es_dirigido else "--")
                else:
                    if linea.find('}') != -1:
                        return grafo
                    conexion = linea.partition(conector)
                    if not conexion[1] or not conexion[2]:
                        conexion = linea.partition(';')
                        if conexion[0]:
                            nodo = conexion[0].replace(" ", "").strip()
                            grafo.crear_nodo(nodo)
                    else:
                        nodo_de = conexion[0].replace(" ","").strip()
                        nodo_a = conexion[2].replace(" ","").strip()
                        grafo.crear_nodo(nodo_de)
                        grafo.crear_nodo(nodo_a)
                        grafo.conectar_nodos(nodo_de, nodo_a)
            print("ADVERTENCIA: No se encontró marcador final del grafo. Verifique la integridad del archivo.")
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
