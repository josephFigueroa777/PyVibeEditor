import pygame
from emmet import emmetFunction
from edicionArchivo import save_file, abrirArchivo, undo_function, redo_function, paste_function, visualizar_html

class GestorTexto:
    """
    Esta clase es la que maneja los eventos de teclado y del ratón. Es como el controlador en una arquitectura MVC hehehe.

    """
    def __init__(self):
        """
        Inicializa el Gestor con el gran String y su cursor.

        """
        self.text_content = ""
        self.cursor_index = 0

        self.seleccion_inicio = None
        self.seleccion_fin = None
        self.seleccionando = False
        self.texto_seleccionado_test = [];

        # Pilas para el historial
        self.undo_stack = []
        self.redo_stack = []

    def limpiar_seleccion(self):
        self.seleccion_inicio = None
        self.seleccion_fin = None

    def obtener_seleccion(self):
        """ Retorna una tupla (inicio, fin) ordenada o None """
        if self.seleccion_inicio is not None and self.seleccion_fin is not None:
            if self.seleccion_inicio != self.seleccion_fin:
                return sorted((self.seleccion_inicio, self.seleccion_fin))
        return None

    def obtener_texto_seleccionado(self):
        """ Retorna la sublista de caracteres seleccionados """
        rango = self.obtener_seleccion()
        if rango:
            return self.text_content[rango[0]:rango[1]]
        return ""

    def registrar_estado(self):
        """ Guarda el estado actual antes de una modificación """
        if len(self.undo_stack) > 50:
            self.undo_stack.pop(0)
        self.undo_stack.append(self.text_content)
        self.redo_stack = []

    def manejar_teclado(self, event):
        """
        Espera un evento para realizar lo esperado por el usuario.

        Argumentos:
            event (): pygame module for interacting with events and queues
        """
        needs_autoscroll = True

        # --- CTRL + z = undo y  CTRL + y = redo ---
        if event.key in (pygame.K_BACKSPACE, pygame.K_RETURN, pygame.K_TAB) or (event.unicode and event.key not in (pygame.K_ESCAPE, pygame.K_DELETE)):
            if not (pygame.key.get_mods() & pygame.KMOD_CTRL):
                self.registrar_estado()

        # --- Atajos ---
        # --- CTRL + l = Emmet ---
        if event.key == pygame.K_l and (pygame.key.get_mods() & pygame.KMOD_CTRL):
            self.registrar_estado() 
            nuevo_contenido, nuevo_indice = emmetFunction(self.text_content, self.cursor_index)
            self.text_content = nuevo_contenido
            self.cursor_index = nuevo_indice
        
        # --- CTRL + s = guardar archivo ---
        elif event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
            save_file(self.text_content)
        
        # --- CTRL + o = abrir archivo Falta 29 de marzo del 2026 ---
        elif event.key == pygame.K_o and (pygame.key.get_mods() & pygame.KMOD_CTRL):
            self.text_content = abrirArchivo()

        # --- CTRL + z = undo ---
        elif event.key == pygame.K_z and (pygame.key.get_mods() & pygame.KMOD_CTRL):
            self.text_content = undo_function(self.undo_stack, self.redo_stack, self.text_content)
            self.cursor_index = min(self.cursor_index, len(self.text_content))
            return needs_autoscroll
        
        # --- CTRL + y = redo ---
        elif event.key == pygame.K_y and (pygame.key.get_mods() & pygame.KMOD_CTRL):
            self.text_content = redo_function(self.undo_stack, self.redo_stack, self.text_content)
            self.cursor_index = min(self.cursor_index, len(self.text_content))
            return needs_autoscroll
        
        # --- CTRL + c = copy ---
        elif event.key == pygame.K_c and (pygame.key.get_mods() & pygame.KMOD_CTRL):
            self.texto_seleccionado_test = self.obtener_texto_seleccionado()
        
        # --- CTRL + v = pegar ---
        elif event.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_CTRL):
            if self.texto_seleccionado_test: # Solo si hay algo que pegar
                self.registrar_estado() # Guardamos estado para poder hacer Undo del pegado
                
                # Guardamos cuántos caracteres vamos a pegar para mover el cursor después
                largo_pegado = len(self.texto_seleccionado_test)
                
                # Llamamos a la función mejorada
                self.text_content = paste_function(
                    self.text_content, 
                    self.texto_seleccionado_test, 
                    self.cursor_index
                )
                
                # Movemos el cursor al final del bloque pegado
                self.cursor_index += largo_pegado
        
        # --- CTRL + p = visualizar html/css ---
        elif event.key == pygame.K_p and (pygame.key.get_mods() & pygame.KMOD_CTRL):
            visualizar_html(self.text_content)
            
        # --- Movimiento Vertical ---
        elif event.key == pygame.K_UP:
            prev_newline = self.text_content.rfind('\n', 0, self.cursor_index)
            if prev_newline != -1:
                col = self.cursor_index - prev_newline
                line_above_start = self.text_content.rfind('\n', 0, prev_newline)
                self.cursor_index = min(line_above_start + col, prev_newline)
            else:
                self.cursor_index = 0
        
        elif event.key == pygame.K_DOWN:
            next_newline = self.text_content.find('\n', self.cursor_index)
            if next_newline != -1:
                prev_newline = self.text_content.rfind('\n', 0, self.cursor_index)
                col = self.cursor_index - (prev_newline if prev_newline != -1 else -1)
                following_newline = self.text_content.find('\n', next_newline + 1)
                if following_newline == -1: following_newline = len(self.text_content)
                self.cursor_index = min(next_newline + col, following_newline)

        # --- Movimiento Horizontal ---
        elif event.key == pygame.K_LEFT:
            self.cursor_index = max(0, self.cursor_index - 1)
        elif event.key == pygame.K_RIGHT:
            self.cursor_index = min(len(self.text_content), self.cursor_index + 1)
        
        # --- Teclas especiales ---
        elif event.key == pygame.K_BACKSPACE:
            if self.cursor_index > 0:
                self.text_content = self.text_content[:self.cursor_index - 1] + self.text_content[self.cursor_index:]
                self.cursor_index -= 1
        elif event.key == pygame.K_RETURN:
            self.text_content = self.text_content[:self.cursor_index] + "\n" + self.text_content[self.cursor_index:]
            self.cursor_index += 1
        elif event.key == pygame.K_TAB:
            self.text_content = self.text_content[:self.cursor_index] + "    " + self.text_content[self.cursor_index:]
            self.cursor_index += 4
        
        # --- Caracteres ---
        else:
            if event.unicode and event.key not in (pygame.K_ESCAPE, pygame.K_DELETE):
                self.text_content = self.text_content[:self.cursor_index] + event.unicode + self.text_content[self.cursor_index:]
                self.cursor_index += 1
        
        return needs_autoscroll