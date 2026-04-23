import pygame
import os

class Pantalla:
    """
    La clase que representa la pantalla. Esta clase es responsable de renderizar todo lo que ve el usuario.

    Atributos:
        width (int): El ancho de la ventana.
        height (int): El alto de la ventana.
    """
    def __init__(self, width, height, superficie):
        """
        Inicializa la pantalla con las dimensiones, colores y tipografías

        Argumentos:
            width (int): El ancho de la ventana.
            height (int): El alto de la ventana.
        """
        self.width = width
        self.height = height
        self.pantallaPygame = superficie
        
        # --- Colores ---
        self.BG_COLOR = (24, 24, 24)
        self.TEXT_COLOR = (150, 255, 150)
        self.LINE_NUM_COLOR = (70, 70, 70)
        self.CURSOR_COLOR = (0, 255, 255)
        self.HIGHLIGHT_COLOR = (40, 40, 40)
        self.SEL_COLOR = (0, 80, 150)
        
        # --- Fuentes ---
        self.font_size = 16
        path_fuente = "FiraCodeNerdFont-Regular.ttf" 
        if os.path.exists(path_fuente):
            self.font = pygame.font.Font(path_fuente, self.font_size)
        else:
            print("Archivo TTF no encontrado, usando fallback...")
            self.font = pygame.font.SysFont("monospace", self.font_size)

        # --- Medir un caracter ---
        self.char_width = self.font.size("M")[0]
        self.line_height = self.font.get_linesize()
    
    def draw_grid(self, cell_width, cell_height, color=(200, 200, 200), offset=(80, 10), line_thickness=1):
        """
        Dibuja una cuadrícula rectangular en la surface dada con celdas que pueden
        tener ancho y alto distintos.

        Parámetros:
        - cell_width (int): ancho de cada celda en píxeles.
        - cell_height (int): alto de cada celda en píxeles.
        - color :(tupla RGB) color de las líneas de la cuadrícula .
        - offset (tupla RGB): Desde donde va a comenzar la rejilla .
        - line_thickness (int): grosor de las líneas.
        """
        # Líneas verticales
        x_off, y_off = offset
        x = x_off
        while x <= x_off + self.width:
            pygame.draw.line(self.pantallaPygame, color, (x, y_off), (x, y_off + self.height), line_thickness)
            x += cell_width

        # Líneas horizontales
        y = y_off
        while y <= y_off + self.height:
            pygame.draw.line(self.pantallaPygame, color, (x_off, y), (x_off + self.width, y), line_thickness)
            y += cell_height
    
    def renderizarFondo(self, color):
        """
        Dibuja el fondo de un color.

        """
        self.pantallaPygame.fill(color)
    
    def resaltar_linea_actual(self, y, line_height):
        """
        Dibuja una franja en la línea que se encuentra el cursor

        Argumentos:
            y (int): Posición Y del cursor
            line_height (int): El alto de cada línea del editor
        """
        rect = pygame.Rect(0, y, self.width, line_height)
        pygame.draw.rect(self.pantallaPygame, self.HIGHLIGHT_COLOR, rect)

    def dibujar_texto(self, char, x, y):
        """
        Dibuja un carácter en una posición X, Y

        Argumentos:
            char (char): El carácter que se va a dibujar
            x (int): Posición X del cursor
            y (int): Posición Y del cursor
        """
        char_surface = self.font.render(char, True, self.TEXT_COLOR)
        self.pantallaPygame.blit(char_surface, (x, y))

    def dibujar_numero_linea(self, num, x, y):
        """
        Dibuja la fila verticalmente del conteo de líneas

        Argumentos:
            num (int): El número correspondiente a la línea del archivo abierto
            x (int): Posición X del cursor
            y (int): Posición Y del cursor
        """
        # rjust(3) alineación
        num_surface = self.font.render(str(num).rjust(3), True, self.LINE_NUM_COLOR)
        self.pantallaPygame.blit(num_surface, (10, y))

    def dibujar_cursor(self, x, y, line_height):
        """
        Dibuja el cursor que parpadea en X y Y

        Argumentos:
            x (int): Posición X del cursor
            y (int): Posición Y del cursor
            line_height (int): El alto de cada línea del editor
        """
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            pygame.draw.rect(self.pantallaPygame, self.CURSOR_COLOR, (x, y, 2, line_height))

    def dibujar_fondo_seleccion(self, x, y, char_width, line_height):
        """
        Dibuja el rectangulo detrás del texto seleccionado

        Argumentos:
            x (int): Posición X del cursor
            y (int): Posición Y del cursor
            char_width (int): El ancho del caracter
            line_height (int): El alto de cada línea del editor
        """
        rect = pygame.Rect(x, y, char_width, line_height)
        pygame.draw.rect(self.pantallaPygame, self.SEL_COLOR, rect)
            