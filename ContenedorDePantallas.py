import pygame

class ContenedorDePantallas:
    def __init__(self, ancho_total, alto_total):
        # 1. LA MESA (Ventana principal)
        self.ventana_principal = pygame.display.set_mode((ancho_total, alto_total))
        pygame.display.set_caption("PyVibe Editor - Workspace")

        # 2. LAS HOJAS DE PAPEL (Superficies)
        self.ancho_explorador = 200
        self.ancho_editor = ancho_total - self.ancho_explorador
        
        self.superficie_explorador = pygame.Surface((self.ancho_explorador, alto_total))
        self.superficie_editor = pygame.Surface((self.ancho_editor, alto_total))

    def actualizar_pantallas(self):
        # 3. PEGAR LAS HOJAS EN LA MESA (Blit)
        # Pegamos el explorador en la coordenada X=0
        self.ventana_principal.blit(self.superficie_explorador, (0, 0))
        # Pegamos el editor justo donde termina el explorador (X=200)
        self.ventana_principal.blit(self.superficie_editor, (self.ancho_explorador, 0))

        pygame.display.flip()