import pgrafos

def crear_fs(archivo_base):
    for i in range(3):
        if i == 0:
            ruta = archivo_base + "_30"
        elif i == 1:
            ruta = archivo_base + "_100"
        else:
            ruta = archivo_base + "_500"
        grafo = pgrafos.Grafo.generar_desde_archivo( "grafos/" + ruta + ".gv")
        grafo_fs = grafo.BFS("15")
        grafo_fs.guardar(ruta + "_BFS")
        grafo_fs = grafo.DFS_iterativo("15")
        grafo_fs.guardar(ruta + "_DFSi")
        grafo_fs = grafo.DFS_recursivo("15")
        grafo_fs.guardar(ruta + "_DFSr")

crear_fs("Barbasi-Albert/BarbasiAlbert_variante")
crear_fs("Dorogovstev-Mendes/DorogovtsevMendes")
crear_fs("Erdos-Renyi/ErdosRenyi")
crear_fs("geografico/geografico")
crear_fs("Gilbert/gilbert")
crear_fs("malla/malla")
