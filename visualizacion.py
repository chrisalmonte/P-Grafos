#En este módulo se crea la visualización de Grafos con pygame

import pgrafos
import pygame

#Propiedades del Grafo
grafo = pgrafos.Grafo.generar_desde_archivo("grafos/malla/malla_100.gv")
metodo_disposicion = pgrafos.Distribucion.spring
ultimo_nodo = 0 #último nodo calculado el fotograma anterior
ipf = 100 #maximo de nodos calculados por fotograma
max_iteraciones_disp = 1000000 #máximo de iteraciones del algoritmo

#Propiedades del programa
ventana_ancho = 1280
ventana_alto = 720
ventana_color = pygame.Color(20,0,25) #RGB
nodo_color = pygame.Color(255,0,118,255) #RGBA
nodo_radio = 6 #px
arista_color = pygame.Color(0,255,200,255)
arista_ancho = 1

#Funciones para el programa
def calcular_posiciones(grafo):
    global max_iteraciones_disp
    global ultimo_nodo
    if  max_iteraciones_disp > 0:
        metodo_disposicion(grafo, ventana_ancho - (nodo_radio * 2), ventana_alto - (nodo_radio * 2), c1=110, c2=15, c3=6, c4=0.01, comienzo=ultimo_nodo, operaciones_por_frame=ipf)
        ultimo_nodo = (ultimo_nodo + ipf) % len(grafo.nodos)
        max_iteraciones_disp -= 1

def dibujar_grafo(surface, grafo):
    for arista in grafo.aristas:
        inicio = (arista.extremos[0].propiedad.get("dis_x", 0) + nodo_radio, arista.extremos[0].propiedad.get("dis_y", 0) + nodo_radio)
        fin = (arista.extremos[1].propiedad.get("dis_x", 0) + nodo_radio, arista.extremos[1].propiedad.get("dis_y", 0) + nodo_radio)
        pygame.draw.line(surface, arista_color, inicio, fin, arista_ancho)

    for nodo in grafo.nodos:
        surface.blit(nodo_sprite, dest=(nodo.propiedad.get("dis_x", 0), nodo.propiedad.get("dis_y", 0)))

#Inicializar pygame
pygame.init()
pantalla = pygame.display.set_mode((ventana_ancho, ventana_alto))
clock = pygame.time.Clock()
ejecutandose = True
delta_time = 0

#Crear representación de nodo a instanciar
nodo_sprite = pygame.Surface((nodo_radio * 2, nodo_radio * 2), pygame.SRCALPHA)
pygame.draw.circle(nodo_sprite, nodo_color, (nodo_sprite.width/2, nodo_sprite.height/2), nodo_radio)

#Ejecución del programa
pgrafos.Distribucion.aleatoria(grafo, ventana_ancho - (nodo_radio * 2), ventana_alto - (nodo_radio * 2))

while ejecutandose:
    #Cerrar programa cuando se presiona "X" en la ventana.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutandose = False
    
    pantalla.fill(ventana_color)
    calcular_posiciones(grafo)
    dibujar_grafo(pantalla, grafo)
    
    #Renderizar el fotograma
    pygame.display.flip()

    #Limitar FPS y calcular Delta Time
    delta_time = clock.tick(60) / 1000
pygame.quit()

