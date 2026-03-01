import pygame
import random
import sys

# --- Game Configuration ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 5
CELL_SIZE = 100
GRID_START_X = (SCREEN_WIDTH - GRID_SIZE * CELL_SIZE) // 2
GRID_START_Y = (SCREEN_HEIGHT - GRID_SIZE * CELL_SIZE) // 2 + 50 # Slightly lower for menu button

# Colors (RGB)
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
INDIGO = (75, 0, 130) # Slightly darker for better visibility

# Game colors and their shorthands
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
INDEFINIDO_COLOR = DARK_GRAY # Color for the undefined box

# Game states
MENU = 0
TUTORIAL = 1
GAME = 2

# --- Pygame Initialization ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("City Shop: El Juego de Negocios")
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)
# error_font = pygame.font.Font(None, 28) # Removed as per V2 base

# --- Material Class ---
class Material:
    def __init__(self, type, composition=None):
        # type: 'base', 'double', 'composite', 'indefinido'
        # composition: list of color shorthands, e.g., ['R'], ['R', 'R'], ['R', 'Y'], ['R', 'Y', 'B']
        self.type = type
        self.composition = composition if composition is not None else []
        self.visible_color = self._get_visible_color()
        self.text = self._get_text()
        self.is_selected = False

    def _get_visible_color(self):
        if self.type == 'indefinido':
            return INDEFINIDO_COLOR
        # For base, double, and composite, the visible color is the first color in its composition (the "glue")
        if self.composition:
            return GAME_COLORS.get(self.composition[0], BLACK)
        return BLACK # Fallback

    def _get_text(self):
        if self.type == 'indefinido':
            return "?"
        elif self.type == 'double': # Specific handling for double materials: display C1C1
            return f"{self.composition[0]}{self.composition[0]}"
        # For base and composite, join the composition list
        return "".join(self.composition)

    def get_base_colors(self):
        # Returns a list of base colors that compose the material for money calculation.
        # This is a simplified calculation for the MVP.
        # For a more complex calculation (e.g., RYYBI needing 16 base components),
        # a more detailed composition structure or recursive function would be needed.
        if self.type == 'base':
            return [self.composition[0]]
        elif self.type == 'double':
            return [self.composition[0], self.composition[0]]
        elif self.type == 'composite':
            # Each color in the composite's composition contributes twice (as if it came from a double)
            base_colors = []
            for c in self.composition:
                base_colors.extend([c, c])
            return base_colors
        return []

# --- Button Class ---
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
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10) # Border

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

# --- Game Class ---
class Game:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.current_money = 0
        self.color_values = {} # Random values for each base color per game
        self.selected_materials = [] # List to store 0, 1, or 2 selected materials
        self.game_state = MENU
        # self.error_message = "" # Removed as per V2 base
        # self.error_timer = 0 # Removed as per V2 base

        self.initialize_game_values()
        self.fill_grid()

        # Main menu buttons
        self.play_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50, "Jugar", GRAY, LIGHT_GRAY)
        self.tutorial_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50, "Tutorial", GRAY, LIGHT_GRAY)
        self.exit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 90, 200, 50, "Salir", GRAY, LIGHT_GRAY)

        # Button to return to main menu (on game/tutorial screen)
        self.back_to_menu_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 70, 200, 50, "Menú Principal", GRAY, LIGHT_GRAY)

    def initialize_game_values(self):
        # Assigns a random value to each base color at the start of a new game
        self.current_money = 0
        for color_shorthand in COLOR_SHORTHANDS:
            self.color_values[color_shorthand] = random.randint(1, 10) # Value between 1 and 10

    def fill_grid(self):
        # Fills the grid with base or undefined materials
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c] is None:
                    if random.random() < 0.2: # 20% probability of being undefined
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
                    pygame.draw.rect(surface, BLACK, rect, 2, border_radius=10) # Border

                    # Highlight if selected
                    if material.is_selected:
                        pygame.draw.rect(surface, (255, 255, 0), rect, 5, border_radius=10) # Yellow border

                    # Determine text color based on background for readability
                    text_color = WHITE
                    if material.visible_color in [YELLOW, LIME_GREEN, GREEN, ORANGE]: # Lighter background colors
                        text_color = BLACK

                    text_surface = font.render(material.text, True, text_color)
                    text_rect = text_surface.get_rect(center=rect.center)
                    surface.blit(text_surface, text_rect)

    def draw_game_ui(self, surface):
        # Display current money
        money_text = font.render(f"Dinero: ${self.current_money}", True, BLACK)
        surface.blit(money_text, (20, 20))

        # Display color values
        values_y = 20
        for color_shorthand, value in self.color_values.items():
            color_name = COLOR_NAMES[color_shorthand]
            color_value_text = small_font.render(f"{color_name}: ${value}", True, BLACK)
            surface.blit(color_value_text, (SCREEN_WIDTH - 150, values_y))
            values_y += 25

        # Display selected materials
        selected_text_y = SCREEN_HEIGHT - 120
        for i, mat in enumerate(self.selected_materials):
            selected_mat_text = small_font.render(f"Sel {i+1}: {mat.text}", True, BLACK)
            surface.blit(selected_mat_text, (20, selected_text_y + i * 25))
        
        # Display error message if any (removed as per V2 base)
        # if self.error_message and self.error_timer > 0:
        #     error_surface = error_font.render(self.error_message, True, RED)
        #     error_rect = error_surface.get_rect(center=(SCREEN_WIDTH // 2, GRID_START_Y - 20))
        #     surface.blit(error_surface, error_rect)
        #     self.error_timer -= 1 # Decrement timer

    # def set_error_message(self, message, duration=120): # Removed as per V2 base
    #     self.error_message = message
    #     self.error_timer = duration

    def handle_game_click(self, pos, button_type):
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
                return # Do nothing if cell is empty

            if button_type == 3: # Right-click to crunch/sell any material
                self.crunch_material(material, clicked_row, clicked_col)
                self.reset_selection() # Deselect all after crunching
                return

            if button_type == 1: # Left-click for selection/combination
                if material.type == 'indefinido':
                    # Reveal undefined box
                    random_color = random.choice(COLOR_SHORTHANDS)
                    self.grid[clicked_row][clicked_col] = Material('base', [random_color])
                    self.reset_selection() # Deselect all when revealing
                    return

                # If material is already selected, deselect it
                if material.is_selected:
                    material.is_selected = False
                    self.selected_materials.remove(material)
                else:
                    # If less than 2 materials selected, select this one
                    if len(self.selected_materials) < 2:
                        material.is_selected = True
                        self.selected_materials.append(material)
                    else:
                        # If 2 are already selected, deselect the first and select the new one
                        self.selected_materials[0].is_selected = False
                        self.selected_materials.pop(0)
                        material.is_selected = True
                        self.selected_materials.append(material)
                
                # Attempt to combine if two materials are selected
                if len(self.selected_materials) == 2:
                    self.try_combine_materials()


    def try_combine_materials(self):
        mat1 = self.selected_materials[0]
        mat2 = self.selected_materials[1]

        # Get positions of selected materials
        pos1 = self.find_material_position(mat1)
        pos2 = self.find_material_position(mat2)

        if not pos1 or not pos2: # If for some reason they are not found, reset
            self.reset_selection()
            return

        new_material = None
        # error_msg = "" # Removed as per V2 base

        # Rule 1: C1 + C1 = C1C1 (two base materials of the same color)
        if mat1.type == 'base' and mat2.type == 'base' and mat1.composition[0] == mat2.composition[0]:
            new_material = Material('double', [mat1.composition[0]])
            print(f"Combinación exitosa: {mat1.text} + {mat2.text} = {new_material.text}")

        # Rule 2: C1C1 + C2C2 = C1C2 (two double materials)
        elif mat1.type == 'double' and mat2.type == 'double':
            # The first color of the composition will be the "glue" (from mat1)
            new_material = Material('composite', [mat1.composition[0], mat2.composition[0]])
            print(f"Combinación exitosa: {mat1.text} + {mat2.text} = {new_material.text}")

        # Rule 3: C1CN... + C1CM... = C1CN...M... (two composite materials with the same root)
        elif mat1.type == 'composite' and mat2.type == 'composite':
            # Check for common root
            if mat1.composition[0] == mat2.composition[0]:
                # New composition: root + non-root parts of mat1 + non-root parts of mat2
                new_composition = [mat1.composition[0]] + mat1.composition[1:] + mat2.composition[1:]
                new_material = Material('composite', new_composition)
                print(f"Combinación exitosa: {mat1.text} + {mat2.text} = {new_material.text}")
            else:
                # error_msg = "¡Error! Los materiales compuestos deben tener la misma raíz (primer color) para combinarse." # Removed as per V2 base
                print("¡Error! Los materiales compuestos deben tener la misma raíz (primer color) para combinarse.")
        else:
            # error_msg = "Combinación no válida. Intenta con C1+C1, C1C1+C2C2, o compuestos con la misma raíz." # Removed as per V2 base
            print("Combinación no válida. Intenta con C1+C1, C1C1+C2C2, o compuestos con la misma raíz.")
        
        if new_material:
            # Replace mat1 with the new material, remove mat2
            self.grid[pos1[0]][pos1[1]] = new_material
            self.grid[pos2[0]][pos2[1]] = None # Remove the second material
            self.refill_grid_after_crunch(pos2[0], pos2[1]) # Refill the empty space
        # elif error_msg: # Removed as per V2 base
        #     self.set_error_message(error_msg)

        self.reset_selection()

    def find_material_position(self, material_to_find):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c] is material_to_find:
                    return (r, c)
        return None

    def crunch_material(self, material, row, col):
        # Calculate money earned
        money_gained = 0
        base_colors_in_material = material.get_base_colors()
        for color_shorthand in base_colors_in_material:
            money_gained += self.color_values.get(color_shorthand, 0) # Sum the value of each base color

        self.current_money += money_gained
        print(f"Material {material.text} 'crujido'. Ganado ${money_gained}. Dinero total: ${self.current_money}")

        # Remove the material and refill the grid
        self.grid[row][col] = None
        self.refill_grid_after_crunch(row, col)

    def refill_grid_after_crunch(self, row, col):
        # Shift materials down and generate new ones at the top
        for r in range(row, 0, -1): # From the crunched material's row upwards
            self.grid[r][col] = self.grid[r-1][col]
        
        # Generar un nuevo material en la fila superior
        if random.random() < 0.2:
            self.grid[0][col] = Material('indefinido')
        else:
            random_color = random.choice(COLOR_SHORTHANDS)
            self.grid[0][col] = Material('base', [random_color])

    def reset_selection(self):
        for mat in self.selected_materials:
            if mat: # Ensure the material hasn't been removed
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
                        self.initialize_game_values() # Reset values for new game
                        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)] # Clear grid
                        self.fill_grid() # Fill new grid
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
                    elif event.type == pygame.MOUSEBUTTONDOWN: # Check for any mouse button down
                        self.handle_game_click(event.pos, event.button) # Pass button type
                
                # Handle hover events for all buttons
                self.play_button.handle_event(event)
                self.tutorial_button.handle_event(event)
                self.exit_button.handle_event(event)
                self.back_to_menu_button.handle_event(event)

            # --- Draw ---
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
                    "2. Cajas '?' (Indefinidas): Haz clic IZQUIERDO para revelar un color base.",
                    "3. Materiales Base (R, Y, B, etc.): Son los colores puros.",
                    "4. Combinaciones (Clic IZQUIERDO):",
                    "   - C1 + C1 = C1C1 (ej. Rojo + Rojo = RR)",
                    "   - C1C1 + C2C2 = C1C2 (ej. RR + YY = RY)",
                    "   - C1C... + C1C... = C1CC... (ej. RY + RB = RYB)",
                    "   - Selecciona 2 materiales. ¡Los materiales compuestos deben tener la misma raíz!",
                    "5. Vender Materiales (Clic DERECHO): Haz clic DERECHO en CUALQUIER material para 'crujirlo' y ganar dinero.",
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

# --- Run the Game ---
if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        pygame.quit()
        sys.exit()
