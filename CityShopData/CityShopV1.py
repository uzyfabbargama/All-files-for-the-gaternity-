import pygame
import random
import sys

# --- Configuración del Juego ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 5
CELL_SIZE = 100
GRID_START_X = (SCREEN_WIDTH - GRID_SIZE * CELL_SIZE) // 2
GRID_START_Y = (SCREEN_HEIGHT - GRID_SIZE * CELL_SIZE) // 2 + 50 # Un poco más abajo para el botón de menú

# Colores (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (50, 50, 50)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
LIME_GREEN = (50, 205, 50)
GREEN = (0, 128, 0)
TEAL = (0, 128, 128)
BLUE = (0, 0, 255)
INDIGO = (75, 0, 130) # Un poco más oscuro para que se vea bien

# Colores del juego y sus representaciones cortas
GAME_COLORS = {
    'R': RED,
    'N': ORANGE,
    'Y': YELLOW,
    'L': LIME_GREEN,
    'G': GREEN,
    'T': TEAL,
    'B': BLUE,
    'I': INDIGO,
}
COLOR_NAMES = {
    'R': "Rojo", 'N': "Naranja", 'Y': "Amarillo", 'L': "Verde Lima",
    'G': "Verde", 'T': "Verde Azulado", 'B': "Azul", 'I': "Índigo"
}
COLOR_SHORTHANDS = list(GAME_COLORS.keys())
INDEFINIDO_COLOR = DARK_GRAY # Color para la caja indefinida

# Estados del juego
MENU = 0
TUTORIAL = 1
GAME = 2

# --- Inicialización de Pygame ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("City Shop: El Juego de Negocios")
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# --- Clase Material ---
class Material:
    def __init__(self, type, composition=None):
        # type: 'base', 'double', 'composite', 'indefinido'
        self.type = type
        self.composition = composition if composition is not None else [] # Lista de las abreviaturas de colores
        self.visible_color = self._get_visible_color()
        self.text = self._get_text()
        self.is_selected = False

    def _get_visible_color(self):
        if self.type == 'indefinido':
            return INDEFINIDO_COLOR
        elif self.type == 'base':
            return GAME_COLORS[self.composition[0]]
        elif self.type == 'double':
            return GAME_COLORS[self.composition[0]] # El color del material doble es el color base
        elif self.type == 'composite':
            return GAME_COLORS[self.composition[0]] # El color visible del compuesto es el primer color (el "pegamento")
        return BLACK # Fallback

    def _get_text(self):
        if self.type == 'indefinido':
            return "?"
        elif self.type == 'base':
            return self.composition[0]
        elif self.type == 'double':
            return f"{self.composition[0]}{self.composition[0]}"
        elif self.type == 'composite':
            return "".join(self.composition)
        return ""

    def get_base_colors(self):
        # Devuelve una lista de los colores base que componen el material
        if self.type == 'base':
            return [self.composition[0]]
        elif self.type == 'double':
            return [self.composition[0], self.composition[0]]
        elif self.type == 'composite':
            # Para C1C2, la composición es [C1, C2]
            # Sus colores base son C1, C1, C2, C2
            return [self.composition[0], self.composition[0], self.composition[1], self.composition[1]]
        return []

# --- Clase Botón ---
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False

    def draw(self, surface):
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, current_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10) # Borde

        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# --- Clase Juego ---
class Game:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.current_money = 0
        self.color_values = {} # Valores aleatorios para cada color base por partida
        self.selected_materials = [] # Lista para almacenar 0, 1 o 2 materiales seleccionados
        self.game_state = MENU
        self.initialize_game_values()
        self.fill_grid()

        # Botones del menú principal
        self.play_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50, "Jugar", GRAY, LIGHT_GRAY)
        self.tutorial_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50, "Tutorial", GRAY, LIGHT_GRAY)
        self.exit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 90, 200, 50, "Salir", GRAY, LIGHT_GRAY)

        # Botón para volver al menú principal (en pantalla de juego/tutorial)
        self.back_to_menu_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 70, 200, 50, "Menú Principal", GRAY, LIGHT_GRAY)

    def initialize_game_values(self):
        # Asigna un valor aleatorio a cada color base al inicio de una nueva partida
        self.current_money = 0
        for color_shorthand in COLOR_SHORTHANDS:
            self.color_values[color_shorthand] = random.randint(1, 10) # Valor entre 1 y 10

    def fill_grid(self):
        # Rellena la cuadrícula con materiales base o indefinidos
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c] is None:
                    if random.random() < 0.2: # 20% de probabilidad de ser indefinido
                        self.grid[r][c] = Material('indefinido')
                    else:
                        random_color = random.choice(COLOR_SHORTHANDS)
                        self.grid[r][c] = Material('base', [random_color])

    def draw_grid(self, surface):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x = GRID_START_X + c * CELL_SIZE
                y = GRID_START_Y + r * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                
                material = self.grid[r][c]
                if material:
                    pygame.draw.rect(surface, material.visible_color, rect, border_radius=10)
                    pygame.draw.rect(surface, BLACK, rect, 2, border_radius=10) # Borde

                    # Resaltar si está seleccionado
                    if material.is_selected:
                        pygame.draw.rect(surface, (255, 255, 0), rect, 5, border_radius=10) # Borde amarillo

                    text_surface = font.render(material.text, True, WHITE if material.visible_color == INDEFINIDO_COLOR or material.visible_color == BLUE or material.visible_color == INDIGO else BLACK)
                    text_rect = text_surface.get_rect(center=rect.center)
                    surface.blit(text_surface, text_rect)

    def draw_game_ui(self, surface):
        # Mostrar dinero actual
        money_text = font.render(f"Dinero: ${self.current_money}", True, BLACK)
        surface.blit(money_text, (20, 20))

        # Mostrar valores de los colores
        values_y = 20
        for color_shorthand, value in self.color_values.items():
            color_name = COLOR_NAMES[color_shorthand]
            color_value_text = small_font.render(f"{color_name}: ${value}", True, BLACK)
            surface.blit(color_value_text, (SCREEN_WIDTH - 150, values_y))
            values_y += 25

        # Mostrar materiales seleccionados
        selected_text_y = SCREEN_HEIGHT - 120
        for i, mat in enumerate(self.selected_materials):
            selected_mat_text = small_font.render(f"Sel {i+1}: {mat.text}", True, BLACK)
            surface.blit(selected_mat_text, (20, selected_text_y + i * 25))

    def handle_game_click(self, pos):
        clicked_row, clicked_col = -1, -1
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x = GRID_START_X + c * CELL_SIZE
                y = GRID_START_Y + r * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                if rect.collidepoint(pos):
                    clicked_row, clicked_col = r, c
                    break
            if clicked_row != -1:
                break

        if clicked_row != -1:
            material = self.grid[clicked_row][clicked_col]

            if material is None:
                return # No hacer nada si la celda está vacía

            if material.type == 'indefinido':
                # Revelar caja indefinida
                random_color = random.choice(COLOR_SHORTHANDS)
                self.grid[clicked_row][clicked_col] = Material('base', [random_color])
                self.selected_materials = [] # Deseleccionar todo al revelar
                for r_grid in range(GRID_SIZE): # Asegurarse de que no haya nada seleccionado
                    for c_grid in range(GRID_SIZE):
                        if self.grid[r_grid][c_grid] and self.grid[r_grid][c_grid].is_selected:
                            self.grid[r_grid][c_grid].is_selected = False
                return

            # Si el material es un producto final (doble o compuesto), lo "cruje" por dinero
            if material.type == 'double' or material.type == 'composite':
                self.crunch_material(material, clicked_row, clicked_col)
                self.selected_materials = [] # Deseleccionar todo al crujir
                for r_grid in range(GRID_SIZE):
                    for c_grid in range(GRID_SIZE):
                        if self.grid[r_grid][c_grid] and self.grid[r_grid][c_grid].is_selected:
                            self.grid[r_grid][c_grid].is_selected = False
                return

            # Si no es indefinido ni un producto final, es un material seleccionable para combinar
            if material.is_selected:
                material.is_selected = False
                self.selected_materials.remove(material)
            else:
                if len(self.selected_materials) < 2:
                    material.is_selected = True
                    self.selected_materials.append(material)
                else:
                    # Si ya hay 2 seleccionados, deseleccionar el primero y seleccionar el nuevo
                    self.selected_materials[0].is_selected = False
                    self.selected_materials.pop(0)
                    material.is_selected = True
                    self.selected_materials.append(material)
            
            # Intentar combinar si hay dos materiales seleccionados
            if len(self.selected_materials) == 2:
                self.try_combine_materials()


    def try_combine_materials(self):
        mat1 = self.selected_materials[0]
        mat2 = self.selected_materials[1]

        # Obtener las posiciones de los materiales seleccionados
        pos1 = self.find_material_position(mat1)
        pos2 = self.find_material_position(mat2)

        if not pos1 or not pos2: # Si por alguna razón no se encuentran, resetear
            self.reset_selection()
            return

        new_material = None

        # Regla: C1 + C1 = C1C1 (dos materiales base del mismo color)
        if mat1.type == 'base' and mat2.type == 'base' and mat1.composition[0] == mat2.composition[0]:
            new_material = Material('double', [mat1.composition[0]])
            print(f"Combinación exitosa: {mat1.text} + {mat2.text} = {new_material.text}")

        # Regla: C1C1 + C2C2 = C1C2 (dos materiales dobles)
        elif mat1.type == 'double' and mat2.type == 'double':
            # El primer color de la composición será el "pegamento" (el de mat1)
            new_material = Material('composite', [mat1.composition[0], mat2.composition[0]])
            print(f"Combinación exitosa: {mat1.text} + {mat2.text} = {new_material.text}")
        
        if new_material:
            # Reemplazar mat1 con el nuevo material, eliminar mat2
            self.grid[pos1[0]][pos1[1]] = new_material
            self.grid[pos2[0]][pos2[1]] = None # Eliminar el segundo material
            self.refill_grid_after_crunch(pos2[0], pos2[1]) # Rellenar el espacio vacío

        self.reset_selection()

    def find_material_position(self, material_to_find):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c] is material_to_find:
                    return (r, c)
        return None

    def crunch_material(self, material, row, col):
        # Calcula el dinero ganado
        money_gained = 0
        base_colors_in_material = material.get_base_colors()
        for color_shorthand in base_colors_in_material:
            money_gained += self.color_values.get(color_shorthand, 0) # Suma el valor de cada color base

        self.current_money += money_gained
        print(f"Material {material.text} 'crujido'. Ganado ${money_gained}. Dinero total: ${self.current_money}")

        # Elimina el material y rellena la cuadrícula
        self.grid[row][col] = None
        self.refill_grid_after_crunch(row, col)

    def refill_grid_after_crunch(self, row, col):
        # Desplaza los materiales hacia abajo y genera nuevos en la parte superior
        for r in range(row, 0, -1): # Desde la fila del material crujido hacia arriba
            self.grid[r][col] = self.grid[r-1][col]
        
        # Generar un nuevo material en la fila superior
        if random.random() < 0.2:
            self.grid[0][col] = Material('indefinido')
        else:
            random_color = random.choice(COLOR_SHORTHANDS)
            self.grid[0][col] = Material('base', [random_color])

    def reset_selection(self):
        for mat in self.selected_materials:
            if mat: # Asegurarse de que el material no haya sido eliminado
                mat.is_selected = False
        self.selected_materials = []

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if self.game_state == MENU:
                    if self.play_button.handle_event(event):
                        self.game_state = GAME
                        self.initialize_game_values() # Reiniciar valores para nueva partida
                        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)] # Limpiar cuadrícula
                        self.fill_grid() # Rellenar nueva cuadrícula
                        self.reset_selection()
                    elif self.tutorial_button.handle_event(event):
                        self.game_state = TUTORIAL
                    elif self.exit_button.handle_event(event):
                        running = False
                
                elif self.game_state == TUTORIAL:
                    if self.back_to_menu_button.handle_event(event):
                        self.game_state = MENU
                
                elif self.game_state == GAME:
                    if self.back_to_menu_button.handle_event(event):
                        self.game_state = MENU
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.handle_game_click(event.pos)
                
                # Manejar eventos de hover para todos los botones
                self.play_button.handle_event(event)
                self.tutorial_button.handle_event(event)
                self.exit_button.handle_event(event)
                self.back_to_menu_button.handle_event(event)

            # --- Dibujar ---
            screen.fill(WHITE)

            if self.game_state == MENU:
                title_surface = font.render("CITY SHOP", True, BLACK)
                title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
                screen.blit(title_surface, title_rect)
                self.play_button.draw(screen)
                self.tutorial_button.draw(screen)
                self.exit_button.draw(screen)
            
            elif self.game_state == TUTORIAL:
                tutorial_title = font.render("Tutorial de City Shop", True, BLACK)
                tutorial_title_rect = tutorial_title.get_rect(center=(SCREEN_WIDTH // 2, 50))
                screen.blit(tutorial_title, tutorial_title_rect)

                tutorial_text = [
                    "Objetivo: ¡Crea materiales y véndelos para ganar dinero!",
                    "",
                    "1. Cuadrícula 5x5: Aquí aparecen los materiales.",
                    "2. Cajas '?' (Indefinidas): Haz clic para revelar un color base.",
                    "3. Materiales Base (R, Y, B, etc.): Son los colores puros.",
                    "4. Combinaciones:",
                    "   - C1 + C1 = C1C1 (ej. Rojo + Rojo = RR)",
                    "   - C1C1 + C2C2 = C1C2 (ej. RR + YY = RY)",
                    "   - Selecciona 2 materiales para combinarlos.",
                    "5. Vender Materiales: Haz clic en un material C1C1 o C1C2 para 'crujirlo' y ganar dinero.",
                    "   - El dinero que ganas depende del valor aleatorio de cada color en esta partida.",
                    "6. Relleno: Cuando 'crujes' un material, nuevos caen desde arriba.",
                    "¡Usa tu dinero para expandirte en futuras versiones!"
                ]
                text_y = 100
                for line in tutorial_text:
                    line_surface = small_font.render(line, True, BLACK)
                    line_rect = line_surface.get_rect(center=(SCREEN_WIDTH // 2, text_y))
                    screen.blit(line_surface, line_rect)
                    text_y += 30
                
                self.back_to_menu_button.draw(screen)

            elif self.game_state == GAME:
                self.draw_grid(screen)
                self.draw_game_ui(screen)
                self.back_to_menu_button.draw(screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

# --- Ejecutar el Juego ---
if __name__ == "__main__":
    game = Game()
    game.run()
