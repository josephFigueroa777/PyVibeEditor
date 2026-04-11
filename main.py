import pygame
import sys
from Pantalla import Pantalla
from GestorTexto import GestorTexto

# --- Inicialización ---
pygame.init()
pantalla = Pantalla(800, 600)
gestor = GestorTexto()
pygame.display.set_caption("PyVibe Editor - Joseph")

x_offset, y_offset = 80, 10
scroll_y = 0 
clock = pygame.time.Clock()
line_height = pantalla.line_height
char_width = pantalla.char_width

running = True
while running:
    pantalla.renderizarFondo()
    # print(gestor.cursor_index) test Joseph
    # pantalla.draw_grid(pantalla.char_width, pantalla.line_height)
    needs_autoscroll = False
    
    # Captura de Mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Clic izquierdo
                gestor.seleccionando = True

                # Calculamos el índice basándonos en la cuadrícula btw pantalla.draw_grid
                rel_x = mouse_x - x_offset
                rel_y = (mouse_y - y_offset) + scroll_y

                # Celdas
                col = rel_x // char_width
                fila = rel_y // line_height
                gestor.seleccion_inicio = None

            if event.button == 4: scroll_y = max(0, scroll_y - 30)
            if event.button == 5: scroll_y += 30
        elif event.type == pygame.KEYDOWN:
            needs_autoscroll = gestor.manejar_teclado(event)

    if mouse_click[0]:
        gestor.seleccionando = True
    else:
        gestor.seleccionando = False 

    # --- Posición del cursor para resaltar línea actual ---
    temp_x, temp_y = x_offset, y_offset - scroll_y
    cursor_draw_pos = (temp_x, temp_y)
    for i, char in enumerate(gestor.text_content):
        if i == gestor.cursor_index:
            cursor_draw_pos = (temp_x, temp_y)
            break
        if char == "\n":
            temp_x, temp_y = x_offset, temp_y + line_height
        else:
            temp_x += char_width
            if temp_x > pantalla.width - 40:
                temp_x, temp_y = x_offset, temp_y + line_height
    if gestor.cursor_index == len(gestor.text_content):
        cursor_draw_pos = (temp_x, temp_y)

    # --- PASO 2: RENDERIZADO ÚNICO ---
    pantalla.resaltar_linea_actual(cursor_draw_pos[1], line_height)

    current_x, current_y = x_offset, y_offset - scroll_y
    line_number = 1
    pantalla.dibujar_numero_linea(line_number, 10, current_y)

    for i, char in enumerate(gestor.text_content):
        celda_rect = pygame.Rect(current_x, current_y, char_width, line_height)
        
        if gestor.seleccionando and celda_rect.collidepoint(mouse_x, mouse_y):
            if gestor.seleccion_inicio is None:
                gestor.seleccion_inicio = i
            gestor.seleccion_fin = i
            gestor.cursor_index = i # El cursor sigue al mouse

        # Punto 3: Pintar los caracteres en el medio
        rango = gestor.obtener_seleccion()
        if rango and rango[0] <= i < rango[1]:
            pantalla.dibujar_fondo_seleccion(current_x, current_y, char_width, line_height)

        # C. Manejo de saltos de línea y renderizado de caracteres
        if char == "\n":
            line_number += 1
            current_x, current_y = x_offset, current_y + line_height
            pantalla.dibujar_numero_linea(line_number, 10, current_y)
            continue

        if current_y > -30 and current_y < pantalla.height:
            pantalla.dibujar_texto(char, current_x, current_y)
        
        current_x += char_width
        if current_x > pantalla.width - 40:
            current_x, current_y = x_offset, current_y + line_height

    pantalla.dibujar_cursor(cursor_draw_pos[0], cursor_draw_pos[1], line_height)

    # --- Limpieza de selección si fue solo un clic ---
    if not gestor.seleccionando and gestor.seleccion_inicio == gestor.seleccion_fin:
        gestor.seleccion_inicio = None
        gestor.seleccion_fin = None

    # --- Autoscroll ---
    if needs_autoscroll:
        if cursor_draw_pos[1] > pantalla.height - 60: scroll_y += line_height
        elif cursor_draw_pos[1] < 30: scroll_y = max(0, scroll_y - line_height)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()