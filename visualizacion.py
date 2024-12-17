#En este módulo se crea la visualización de Grafos con pygame

import pgrafos
import pygame

#Propiedades del Grafo
grafo = pgrafos.Grafo.generar_desde_archivo("grafos/malla/malla_30.gv")

#Propiedades del programa
ancho_ventana = 1280
alto_ventana = 720
color_nodos = pygame.Color(255,255,255,255) #RGBA
colo_aristas = pygame.Color(150,230,80,255)

#Inicializar pygame
pygame.init()
pantalla = pygame.display.set_mode((ancho_ventana, alto_ventana))
clock = pygame.time.Clock()
ejecutandose = True
dt = 0

#Funciones para el programa
def dibujar_nodos(grafo):

    return pygame.surface

#Ejecución del programa
while ejecutandose:
    #Cerrar programa cuando se presiona "X" en la ventana.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutandose = False

    pantalla.blit(dibujar_nodos(grafo))
    
    #Renderizar el fotograma
    pygame.display.flip()
pygame.quit()

