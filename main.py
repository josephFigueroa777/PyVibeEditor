import pygame
import sys
from Pantalla import Pantalla
from GestorTexto import GestorTexto
from ContenedorDePantallas import ContenedorDePantallas

# --- Inicialización ---
pygame.init()

# 1. Instanciamos el contenedor maestro (Ventana de 1000x600)
contenedor = ContenedorDePantallas(1000, 600)

# 2. Instanciamos el Editor, pasándole su "hoja de papel" (superficie_editor)
# El tamaño de esta pantalla será 800x600 (los 1000 totales menos los 200 del explorador)
pantalla_editor = Pantalla(contenedor.ancho_editor, 600, contenedor.superficie_editor)
pantalla_explorador_test = Pantalla(contenedor.ancho_explorador, 600, contenedor.superficie_explorador)

gestor = GestorTexto('Nuevo documento')

x_offset, y_offset = 80, 10
scroll_y = 0 
clock = pygame.time.Clock()
line_height = pantalla_editor.line_height
char_width = pantalla_editor.char_width

running = True
while running:
    # --- RENDERIZADO DE FONDOS ---
    pantalla_editor.renderizarFondo((24, 24, 24)) # Limpia la hoja del editor
    pantalla_explorador_test.renderizarFondo((30, 30, 30))
    
    needs_autoscroll = False
    
    # Captura de Mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    
    # --- AJUSTE CRÍTICO DE COORDENADAS ---
    # Traducimos la posición real de la pantalla a la posición relativa de la superficie del editor
    mouse_x_editor = mouse_x - contenedor.ancho_explorador
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                # Solo interactuamos con el texto si el clic fue dentro del área del editor
                if mouse_x_editor >= 0:
                    gestor.seleccionando = True
                    rel_x = mouse_x_editor - x_offset
                    rel_y = (mouse_y - y_offset) + scroll_y
                    col = rel_x // char_width
                    fila = rel_y // line_height
                    gestor.seleccion_inicio = None
                else:
                    print("Clic en el explorador de archivos!") # Aquí pondrás tu lógica de archivos luego

            if event.button == 4: scroll_y = max(0, scroll_y - 30)
            if event.button == 5: scroll_y += 30
        elif event.type == pygame.KEYDOWN:
            needs_autoscroll = gestor.manejar_teclado(event)

    if mouse_click[0] and mouse_x_editor >= 0:
        gestor.seleccionando = True
    else:
        gestor.seleccionando = False 

    # --- PASO 1: Calcular posición visual ---
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
            if temp_x > pantalla_editor.width - 40:
                temp_x, temp_y = x_offset, temp_y + line_height
    if gestor.cursor_index == len(gestor.text_content):
        cursor_draw_pos = (temp_x, temp_y)

    # --- PASO 2: RENDERIZADO ÚNICO EN LA SUPERFICIE DEL EDITOR ---
    pantalla_editor.resaltar_linea_actual(cursor_draw_pos[1], line_height)

    current_x, current_y = x_offset, y_offset - scroll_y
    line_number = 1
    pantalla_editor.dibujar_numero_linea(line_number, 10, current_y)

    for i, char in enumerate(gestor.text_content):
        celda_rect = pygame.Rect(current_x, current_y, char_width, line_height)
        
        # OJO: Usamos mouse_x_editor para la colisión
        if gestor.seleccionando and celda_rect.collidepoint(mouse_x_editor, mouse_y):
            if gestor.seleccion_inicio is None:
                gestor.seleccion_inicio = i
            gestor.seleccion_fin = i
            gestor.cursor_index = i 

        rango = gestor.obtener_seleccion()
        if rango and rango[0] <= i < rango[1]:
            pantalla_editor.dibujar_fondo_seleccion(current_x, current_y, char_width, line_height)

        if char == "\n":
            line_number += 1
            current_x, current_y = x_offset, current_y + line_height
            pantalla_editor.dibujar_numero_linea(line_number, 10, current_y)
            continue

        if current_y > -30 and current_y < pantalla_editor.height:
            pantalla_editor.dibujar_texto(char, current_x, current_y)
        
        current_x += char_width
        if current_x > pantalla_editor.width - 40:
            current_x, current_y = x_offset, current_y + line_height

    pantalla_editor.dibujar_cursor(cursor_draw_pos[0], cursor_draw_pos[1], line_height)

    if not gestor.seleccionando and gestor.seleccion_inicio == gestor.seleccion_fin:
        gestor.seleccion_inicio = None
        gestor.seleccion_fin = None

    if needs_autoscroll:
        if cursor_draw_pos[1] > pantalla_editor.height - 60: scroll_y += line_height
        elif cursor_draw_pos[1] < 30: scroll_y = max(0, scroll_y - line_height)

    # --- PASO 3: ENSAMBLAR TODO Y MOSTRAR ---
    contenedor.actualizar_pantallas() # Reemplaza el display.flip() solitario
    clock.tick(60)

pygame.quit()
sys.exit()