import pygame
import random
import sys

# --- Configuración del Juego ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 5
CELL_SIZE = 100
GRID_START_X = (SCREEN_WIDTH - GRID_SIZE * CELL_SIZE) // 2
GRID_START_Y = (SCREEN_HEIGHT - GRID_SIZE * CELL_SIZE) // 2 + 50 # Ligeramente más abajo para el botón de menú

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
INDIGO = (75, 0, 130) # Ligeramente más oscuro para mejor visibilidad

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
error_font = pygame.font.Font(None, 28) # Fuente para mensajes de error

# --- Clase Material ---
class Material:
    def __init__(self, type, composition=None):
        # type: 'base', 'double', 'composite', 'indefinido'
        # composition: lista de abreviaturas de colores, ej. ['R'], ['R', 'R'], ['R', 'Y'], ['R', 'Y', 'B']
        self.type = type
        self.composition = composition if composition is not None else []
        self.visible_color = self._get_visible_color()
        self.text = self._get_text()
        self.is_selected = False

    def _get_visible_color(self):
        if self.type == 'indefinido':
            return INDEFINIDO_COLOR
        # Para base, doble y compuesto, el color visible es el primer color en su composición (el "pegamento")
        if self.composition:
            return GAME_COLORS.get(self.composition[0], BLACK)
        return BLACK # Fallback

    def _get_text(self):
        if self.type == 'indefinido':
            return "?"
        elif self.type == 'double': # Manejo específico para materiales dobles: mostrar C1C1
            return f"{self.composition[0]}{self.composition[0]}"
        # Para base y compuesto, unir la lista de composición
        return "".join(self.composition)

    def get_base_colors(self):
        # Devuelve una lista de los colores base que componen el material para el cálculo de dinero.
        # Este es un cálculo simplificado para el MVP.
        if self.type == 'base':
            return [self.composition[0]]
        elif self.type == 'double':
            return [self.composition[0], self.composition[0]]
        elif self.type == 'composite':
            # Cada color en la composición del compuesto contribuye dos veces (como si viniera de un doble)
            base_colors = []
            for c in self.composition:
                base_colors.extend([c, c])
            return base_colors
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
        self.grids = [] # Lista de todas las cuadrículas poseídas por el jugador
        self.current_grid_index = 0 # Índice de la cuadrícula actualmente visible
        self.current_money = 0
        self.grid_purchase_cost = 50 # Costo inicial para la primera cuadrícula adicional
        self.selected_materials = [] # Asegura que selected_materials se inicialice aquí

        self.game_state = MENU
        self.error_message = ""
        self.error_timer = 0

        self.initialize_game_values() # Esto inicializará la primera cuadrícula
        
        # Botones del menú principal
        self.play_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50, "Jugar", GRAY, LIGHT_GRAY)
        self.tutorial_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50, "Tutorial", GRAY, LIGHT_GRAY)
        self.exit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 90, 200, 50, "Salir", GRAY, LIGHT_GRAY)

        # Botón para volver al menú principal (en pantalla de juego/tutorial)
        self.back_to_menu_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 70, 200, 50, "Menú Principal", GRAY, LIGHT_GRAY)

        # Botones de navegación de cuadrícula
        self.left_arrow_button = Button(GRID_START_X + CELL_SIZE * 2 - 70, GRID_START_Y - 40, 50, 30, "<", GRAY, LIGHT_GRAY)
        self.right_arrow_button = Button(GRID_START_X + CELL_SIZE * 3 + 20, GRID_START_Y - 40, 50, 30, ">", GRAY, LIGHT_GRAY)
        
        # Botón para comprar nueva cuadrícula
        self.buy_grid_button = Button(SCREEN_WIDTH - 180, SCREEN_HEIGHT - 70, 160, 50, f"Comprar Cuadrícula (${self.grid_purchase_cost})", GRAY, LIGHT_GRAY)


    def initialize_game_values(self):
        # Reinicia el juego y crea la primera cuadrícula
        self.current_money = 0
        self.grids = []
        self.current_grid_index = 0
        self.grid_purchase_cost = 50 # Reinicia el costo de compra
        self.selected_materials = [] # Asegura que selected_materials se reinicie al inicio de cada partida

        self.add_new_grid() # Añade la primera cuadrícula al inicio del juego

    def add_new_grid(self):
        new_grid_state = {
            'grid_materials': [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)],
            'color_values': {}
        }
        # Asigna un valor aleatorio a cada color base para esta nueva cuadrícula (su "cultura")
        for color_shorthand in COLOR_SHORTHANDS:
            new_grid_state['color_values'][color_shorthand] = random.randint(1, 10)
        
        self.grids.append(new_grid_state)
        self.fill_current_grid() # Rellena la nueva cuadrícula con materiales

    def fill_current_grid(self):
        # Rellena la cuadrícula actualmente activa con materiales base o indefinidos
        current_grid_materials = self.grids[self.current_grid_index]['grid_materials']
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if current_grid_materials[r][c] is None:
                    if random.random() < 0.2: # 20% de probabilidad de ser indefinido
                        current_grid_materials[r][c] = Material('indefinido')
                    else:
                        random_color = random.choice(COLOR_SHORTHANDS)
                        current_grid_materials[r][c] = Material('base', [random_color])

    def draw_grid(self, surface):
        current_grid_materials = self.grids[self.current_grid_index]['grid_materials']
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x = GRID_START_X + c * CELL_SIZE
                y = GRID_START_Y + r * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                
                material = current_grid_materials[r][c]
                if material:
                    pygame.draw.rect(surface, material.visible_color, rect, border_radius=10)
                    pygame.draw.rect(surface, BLACK, rect, 2, border_radius=10) # Borde

                    # Resaltar si está seleccionado
                    if material.is_selected:
                        pygame.draw.rect(surface, (255, 255, 0), rect, 5, border_radius=10) # Borde amarillo

                    # Determinar color del texto basado en el fondo para legibilidad
                    text_color = WHITE
                    if material.visible_color in [YELLOW, LIME_GREEN, GREEN, ORANGE]: # Colores de fondo más claros
                        text_color = BLACK

                    text_surface = font.render(material.text, True, text_color)
                    text_rect = text_surface.get_rect(center=rect.center)
                    surface.blit(text_surface, text_rect)

    def draw_game_ui(self, surface):
        # Mostrar dinero actual
        money_text = font.render(f"Dinero: ${self.current_money}", True, BLACK)
        surface.blit(money_text, (20, 20))

        # Mostrar índice de cuadrícula actual
        grid_info_text = font.render(f"Cuadrícula: {self.current_grid_index + 1}/{len(self.grids)}", True, BLACK)
        grid_info_rect = grid_info_text.get_rect(center=(SCREEN_WIDTH // 2, GRID_START_Y - 25))
        surface.blit(grid_info_text, grid_info_rect)

        # Mostrar valores de los colores de la cuadrícula actual
        values_y = 20
        current_color_values = self.grids[self.current_grid_index]['color_values']
        for color_shorthand, value in current_color_values.items():
            color_name = COLOR_NAMES[color_shorthand]
            color_value_text = small_font.render(f"{color_name}: ${value}", True, BLACK)
            surface.blit(color_value_text, (SCREEN_WIDTH - 150, values_y))
            values_y += 25

        # Mostrar materiales seleccionados
        selected_text_y = SCREEN_HEIGHT - 120
        for i, mat in enumerate(self.selected_materials):
            selected_mat_text = small_font.render(f"Sel {i+1}: {mat.text}", True, BLACK)
            surface.blit(selected_mat_text, (20, selected_text_y + i * 25))
        
        # Mostrar mensaje de error si existe
        if self.error_message and self.error_timer > 0:
            error_surface = error_font.render(self.error_message, True, RED)
            error_rect = error_surface.get_rect(center=(SCREEN_WIDTH // 2, GRID_START_Y - 50))
            surface.blit(error_surface, error_rect)
            self.error_timer -= 1 # Decrementar el temporizador

        # Dibujar botones de navegación de cuadrícula
        self.left_arrow_button.draw(surface)
        self.right_arrow_button.draw(surface)

        # Actualizar y dibujar botón de compra de cuadrícula
        self.buy_grid_button.text = f"Comprar Cuadrícula (${self.grid_purchase_cost})"
        self.buy_grid_button.draw(surface)

    def set_error_message(self, message, duration=120): # Duración en fotogramas (ej. 120 fotogramas = 2 segundos a 60 FPS)
        self.error_message = message
        self.error_timer = duration

    def handle_game_click(self, pos, button_type):
        # Manejar clic en botones de navegación
        if self.left_arrow_button.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': pos, 'button': button_type})):
            self.current_grid_index = (self.current_grid_index - 1) % len(self.grids)
            self.reset_selection()
            return
        if self.right_arrow_button.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': pos, 'button': button_type})):
            self.current_grid_index = (self.current_grid_index + 1) % len(self.grids)
            self.reset_selection()
            return
        
        # Manejar clic en botón de comprar cuadrícula
        if self.buy_grid_button.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': pos, 'button': button_type})):
            if self.current_money >= self.grid_purchase_cost:
                self.current_money -= self.grid_purchase_cost
                self.add_new_grid()
                self.current_grid_index = len(self.grids) - 1 # Cambiar a la nueva cuadrícula
                self.grid_purchase_cost *= 2 # Duplicar el costo para la próxima compra
                self.set_error_message(f"¡Nueva cuadrícula comprada por ${self.grid_purchase_cost // 2}!", 180)
                self.reset_selection()
            else:
                self.set_error_message(f"¡No tienes suficiente dinero! Necesitas ${self.grid_purchase_cost}", 120)
            return

        # Lógica de clic en la cuadrícula
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
            current_grid_materials = self.grids[self.current_grid_index]['grid_materials']
            material = current_grid_materials[clicked_row][clicked_col]

            if material is None:
                return # No hacer nada si la celda está vacía

            if button_type == 3: # Clic derecho para crujir/vender cualquier material
                self.crunch_material(material, clicked_row, clicked_col)
                self.reset_selection() # Deseleccionar todo después de crujir
                return

            if button_type == 1: # Clic izquierdo para selección/combinación
                if material.type == 'indefinido':
                    # Revelar caja indefinida
                    random_color = random.choice(COLOR_SHORTHANDS)
                    current_grid_materials[clicked_row][clicked_col] = Material('base', [random_color])
                    self.reset_selection() # Deseleccionar todo al revelar
                    return

                # Si el material ya está seleccionado, deseleccionarlo
                if material.is_selected:
                    material.is_selected = False
                    self.selected_materials.remove(material)
                else:
                    # Si hay menos de 2 materiales seleccionados, seleccionar este
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

        # Obtener las posiciones de los materiales seleccionados en la cuadrícula actual
        pos1 = self.find_material_position(mat1)
        pos2 = self.find_material_position(mat2)

        if not pos1 or not pos2: # Si por alguna razón no se encuentran, resetear
            self.reset_selection()
            return

        new_material = None

        # Regla 1: C1 + C1 = C1C1 (dos materiales base del mismo color)
        if mat1.type == 'base' and mat2.type == 'base' and mat1.composition[0] == mat2.composition[0]:
            new_material = Material('double', [mat1.composition[0]])
            print(f"Combinación exitosa: {mat1.text} + {mat2.text} = {new_material.text}")

        # Regla 2: C1C1 + C2C2 = C1C2 (dos materiales dobles)
        elif mat1.type == 'double' and mat2.type == 'double':
            # El primer color de la composición será el "pegamento" (el de mat1)
            new_material = Material('composite', [mat1.composition[0], mat2.composition[0]])
            print(f"Combinación exitosa: {mat1.text} + {mat2.text} = {new_material.text}")

        # Regla 3: C1CN... + C1CM... = C1CN...M... (dos materiales compuestos con la misma raíz)
        elif mat1.type == 'composite' and mat2.type == 'composite':
            # Verificar si tienen la misma raíz
            if mat1.composition[0] == mat2.composition[0]:
                # Nueva composición: raíz + partes no raíz de mat1 + partes no raíz de mat2
                new_composition = [mat1.composition[0]] + mat1.composition[1:] + mat2.composition[1:]
                new_material = Material('composite', new_composition)
                print(f"Combinación exitosa: {mat1.text} + {mat2.text} = {new_material.text}")
            else:
                print("¡Error! Los materiales compuestos deben tener la misma raíz (primer color) para combinarse.")
                self.set_error_message("¡Error! Compuestos sin misma raíz.", 90)
        else:
            print("Combinación no válida. Intenta con C1+C1, C1C1+C2C2, o compuestos con la misma raíz.")
            self.set_error_message("Combinación no válida.", 90)
        
        if new_material:
            # Reemplazar mat1 con el nuevo material, eliminar mat2
            current_grid_materials = self.grids[self.current_grid_index]['grid_materials']
            current_grid_materials[pos1[0]][pos1[1]] = new_material
            current_grid_materials[pos2[0]][pos2[1]] = None # Eliminar el segundo material
            self.refill_grid_after_crunch(pos2[0], pos2[1]) # Rellenar el espacio vacío

        self.reset_selection()

    def find_material_position(self, material_to_find):
        current_grid_materials = self.grids[self.current_grid_index]['grid_materials']
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if current_grid_materials[r][c] is material_to_find:
                    return (r, c)
        return None

    def crunch_material(self, material, row, col):
        # Calcula el dinero ganado
        money_gained = 0
        base_colors_in_material = material.get_base_colors()
        current_color_values = self.grids[self.current_grid_index]['color_values']
        for color_shorthand in base_colors_in_material:
            money_gained += current_color_values.get(color_shorthand, 0) # Suma el valor de cada color base

        self.current_money += money_gained
        print(f"Material {material.text} 'crujido'. Ganado ${money_gained}. Dinero total: ${self.current_money}")

        # Elimina el material y rellena la cuadrícula
        current_grid_materials = self.grids[self.current_grid_index]['grid_materials']
        current_grid_materials[row][col] = None
        self.refill_grid_after_crunch(row, col)

    def refill_grid_after_crunch(self, row, col):
        # Desplaza los materiales hacia abajo y genera nuevos en la parte superior
        current_grid_materials = self.grids[self.current_grid_index]['grid_materials']
        for r in range(row, 0, -1): # Desde la fila del material crujido hacia arriba
            current_grid_materials[r][col] = current_grid_materials[r-1][col]
        
        # Generar un nuevo material en la fila superior
        if random.random() < 0.2:
            current_grid_materials[0][col] = Material('indefinido')
        else:
            random_color = random.choice(COLOR_SHORTHANDS)
            current_grid_materials[0][col] = Material('base', [random_color])

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
                        self.initialize_game_values() # Reiniciar valores y crear la primera cuadrícula
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
                    elif event.type == pygame.MOUSEBUTTONDOWN: # Verificar cualquier clic de ratón
                        self.handle_game_click(event.pos, event.button) # Pasar el tipo de botón
                
                # Manejar eventos de hover para todos los botones
                self.play_button.handle_event(event)
                self.tutorial_button.handle_event(event)
                self.exit_button.handle_event(event)
                self.back_to_menu_button.handle_event(event)
                self.left_arrow_button.handle_event(event)
                self.right_arrow_button.handle_event(event)
                self.buy_grid_button.handle_event(event)


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
                    "7. Múltiples Cuadrículas: Usa las flechas para navegar entre tus cuadrículas.",
                    "8. Comprar Cuadrículas: Gasta dinero para expandir tu imperio con nuevas cuadrículas."
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
