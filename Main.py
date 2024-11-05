import pgrafos

grafo = pgrafos.Grafo.generar_malla(5, 5, True)
grafo.guardar("hola")
grafo = pgrafos.Grafo.generar_desde_archivo("grafos/hola.gv")
grafo.guardar("adios")