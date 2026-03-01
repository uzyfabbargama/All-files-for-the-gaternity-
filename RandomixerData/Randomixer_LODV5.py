import pygame
import sys
import math
import colorsys # <--- Nuevo import para la manipulación de colores

# --- Game Configuration ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
BLOCK_SIZE = 32
FPS = 60

# CHUNK_SIZE define el tamaño de un trozo de mundo (e.g., 16x16 bloques)
# Un chunk de 16x16 bloques tiene 512x512 píxeles (16 * 32)
CHUNK_SIZE = 16

# Distancia de renderizado en chunks alrededor del jugador (e.g., 3 chunks en cada dirección)
RENDER_DISTANCE_CHUNKS = 3

# Base Colors (these are the "pure colors" that will be assigned)
PURE_RED = (255, 0, 0)
PURE_YELLOW = (255, 255, 0)
PURE_GREEN = (0, 255, 0)
PURE_BLUE = (0, 0, 255)

# Colors for in-game visualization (tones and UI)
PLAYER_COLOR = (255, 0, 0) # Bright red for player
INVENTORY_SLOT_COLOR = (70, 70, 70)
INVENTORY_SELECTED_COLOR = (0, 150, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
LIGHT_GRAY = (100, 100, 100)
GREEN = (0, 200, 0) # For button

# Lighting and Draw Distance
DRAW_DISTANCE_CHUNKS = 15 # How many blocks away the light effect is noticeable

# --- Game Classes ---

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, base_strength, jump_force, gravity):
        super().__init__()
        # Posición del jugador en coordenadas de MUNDO (no de pantalla)
        self.world_x = x
        self.world_y = y

        self.image = pygame.Surface([BLOCK_SIZE, BLOCK_SIZE * 2])
        self.image.fill(PLAYER_COLOR)
        # El rect ahora se inicializa en 0,0 porque su posición real será manejada por la cámara
        self.rect = self.image.get_rect(topleft=(0, 0))

        self.vel_y = 0
        self.vel_x = 0
        self.on_ground = False
        self.base_strength = base_strength
        # jump_force_factor ahora representa la ALTURA de salto deseada en "metros" conceptuales (bloques)
        self.jump_force_factor = jump_force
        self.player_strength = base_strength
        # Asegurarse de que la gravedad tenga un valor mínimo para evitar división por cero o problemas de física
        self.gravity_force = max(0.1, gravity)
        self.move_speed = BLOCK_SIZE * 0.1
        self.auto_jump_cooldown = 0
        self.auto_jump_cooldown_max = 10

    def update(self, world_blocks, world_generator):
        # Copiar posición actual para detección de colisiones
        prev_world_x = self.world_x
        prev_world_y = self.world_y

        if abs(self.vel_x) < 0.1:
            self.vel_x = 0

        # --- Auto-Jump Logic ---
        if self.on_ground and self.vel_x != 0 and self.auto_jump_cooldown == 0:
            check_direction = 1 if self.vel_x > 0 else -1

            # Usar coordenadas de bloque del mundo
            target_block_x = (self.world_x + BLOCK_SIZE * check_direction + BLOCK_SIZE / 2 * check_direction) // BLOCK_SIZE
            player_bottom_y_block = (self.world_y + BLOCK_SIZE * 2 - 1) // BLOCK_SIZE

            wall_height = 0
            for y_offset in range(int(self.jump_force_factor * 2) + 1):
                check_y_block = player_bottom_y_block - y_offset

                if check_y_block < 0:
                    break

                # Obtener bloque del mundo a través del world_generator
                block_in_front = world_generator.get_block_at_world_coords(target_block_x, check_y_block)

                if block_in_front and not block_in_front.is_fluid():
                    wall_height += 1
                else:
                    break

            if wall_height > 0 and wall_height <= self.jump_force_factor:
                block_at_feet_level_in_front = world_generator.get_block_at_world_coords(target_block_x, player_bottom_y_block)
                if block_at_feet_level_in_front and not block_at_feet_level_in_front.is_fluid():
                    self.jump(world_generator.numerium_core.gravity) # Pasa la gravedad actual al salto
                    self.auto_jump_cooldown = self.auto_jump_cooldown_max

        if self.auto_jump_cooldown > 0:
            self.auto_jump_cooldown -= 1

        # --- Horizontal Movement (en coordenadas de mundo) ---
        self.world_x += self.vel_x

        # Crear un rect de colisión temporal en coordenadas de mundo
        temp_rect = pygame.Rect(self.world_x, self.world_y, BLOCK_SIZE, BLOCK_SIZE * 2)

        self.on_ground = False # Reset on ground state

        for block in world_blocks: # world_blocks are the blocks currently active in the render
            if temp_rect.colliderect(block.rect) and not block.is_fluid():
                if self.vel_x > 0:
                    self.world_x = block.rect.left - BLOCK_SIZE
                elif self.vel_x < 0:
                    self.world_x = block.rect.right
                temp_rect.x = self.world_x # Update temporary rect

        # --- Gravity and Vertical Movement (en coordenadas de mundo) ---
        # Gravity is applied as an acceleration per frame
        self.vel_y += self.gravity_force / FPS / 10 # /10 is kept for finer control
        self.world_y += self.vel_y

        temp_rect.y = self.world_y # Update temporary rect for Y

        for block in world_blocks:
            if temp_rect.colliderect(block.rect) and not block.is_fluid():
                if self.vel_y > 0: # Falling, collided with a block's top
                    self.world_y = block.rect.top - BLOCK_SIZE * 2
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0: # Jumping, collided with a block's bottom
                    self.world_y = block.rect.bottom
                    self.vel_y = 0
                temp_rect.y = self.world_y # Update temporary rect

        # There is no lower screen limit, the world continues downwards (you would fall into the void)
        # You can add a limit if you want the player to "die" if they fall too far
        # if self.world_y > world_generator.max_world_y_limit:
        #    # Implement death or respawn logic

    def start_move_x(self, direction):
        self.vel_x = direction * self.move_speed

    def stop_move_x(self):
        self.vel_x = 0

    def jump(self, current_gravity):
        """
        Calculates the initial velocity needed to jump the desired height (self.jump_force_factor).
        self.jump_force_factor is now the HEIGHT in conceptual "meters" (blocks).
        """
        if self.on_ground:
            # Desired height in pixels
            desired_height_pixels = self.jump_force_factor * BLOCK_SIZE

            # Ensure gravity has a minimum value to prevent division by zero
            # or infinite jumps with zero gravity.
            effective_gravity = max(0.1, current_gravity) # Use the current universe's gravity

            # Gravity acceleration per frame in pixels/frame^2
            gravity_acceleration_per_frame = effective_gravity / FPS / 10

            # Formula for initial velocity (v0 = sqrt(2 * a * h))
            # We adjust to avoid sqrt of negative numbers if desired_height_pixels is 0 or very small
            if desired_height_pixels <= 0 or gravity_acceleration_per_frame <= 0:
                self.vel_y = 0
            else:
                self.vel_y = -math.sqrt(2 * gravity_acceleration_per_frame * desired_height_pixels)

            self.on_ground = False # No longer on the ground once it jumps

    def update_strength_from_inventory(self, inventory):
        tool_bonus = inventory.get_current_tool_strength()
        self.player_strength = self.base_strength + tool_bonus


class Block(pygame.sprite.Sprite):
    def __init__(self, world_x, world_y, material_data):
        super().__init__()
        # Store world position of the block
        self.world_x = world_x
        self.world_y = world_y

        self.image = pygame.Surface([BLOCK_SIZE, BLOCK_SIZE])
        self.image.fill(material_data['color'])
        # The rect is initialized with the world position for collisions,
        # but for drawing, the camera offset will be used
        self.rect = pygame.Rect(world_x, world_y, BLOCK_SIZE, BLOCK_SIZE)
        self.material_data = material_data
        self.world_pos = (world_x, world_y)


    def get_resistance(self):
        return self.material_data['resistance']

    def get_structural_resistance(self):
        return self.material_data['structural_resistance']

    def get_name(self):
        return self.material_data['name']

    def is_fluid(self):
        return self.material_data['is_fluid']

    def get_color(self):
        return self.material_data['color']

# --- Numerium and Randomixer Logic ---

class NumeriumCore:
    def __init__(self, randomixer_seed):
        self.randomixer_seed = randomixer_seed
        self.seed_digits = self._extract_seed_digits(self.randomixer_seed)

        # 1. Get duplas from the seed in their original order and by product
        self.duplas_from_seed_in_order = self._get_dupla_data_ordered_by_original_position() # Original (C1,C2), (C3,C4)...
        self.duplas_by_product = self._get_dupla_data_ordered_by_product() # Sorted by product

        # Fallback values for gravity and player strength duplas if not enough data
        self.gravity_dupla_data = self.duplas_by_product[0] if self.duplas_by_product else {'product': 32, 'c1': 4, 'c2': 8, 'dupla_raw': (4,8)}
        self.player_strength_dupla_data = self.duplas_by_product[1] if len(self.duplas_by_product) > 1 else {'product': 12, 'c1': 3, 'c2': 4, 'dupla_raw': (3,4)}

        self.gravity = self.gravity_dupla_data['product']
        # Ensure gravity is never zero to prevent division by zero errors in structural resistance calculation
        if self.gravity == 0:
            self.gravity = 1 # Minimum value to avoid division errors

        # 2. Assign material names ("Piedra", "Roca", "Madera", "Agua") to the (min,max) duplas of the seed,
        #    according to their hierarchical order
        self.material_archetypes_by_min_max_key = self._assign_names_to_sorted_seed_duplas() # Returns { (min,max)_dupla : name }

        # 3. Assign initial pure colors to material names,
        #    based on the original dupla of the seed to which that material was mapped.
        self.material_name_to_initial_pure_color = self._assign_initial_pure_colors_to_material_names()

        # Map for final material colors (after mixes)
        self.material_name_to_color = {}

        # --- Calculate mixed colors for Wood and Leaves ---
        # Rule for Leaves color: its base color is the initial pure color of "Madera"
        self.material_name_to_color['Hojas'] = self.material_name_to_initial_pure_color.get("Madera", BLACK)

        # Rule for Wood color: Subtractive mix of the initial pure color of "Piedra"
        # and the final (already derived) color of "Hojas".
        color_piedra_base = self.material_name_to_initial_pure_color.get("Piedra", BLACK)
        color_hojas_final = self.material_name_to_color.get("Hojas", BLACK) # Use the color already assigned to Leaves
        self.material_name_to_color['Madera'] = self._subtractive_mix_rgb(color_piedra_base, color_hojas_final)

        # Other materials retain their initial pure colors
        for name, color in self.material_name_to_initial_pure_color.items():
            if name not in self.material_name_to_color: # Do not overwrite Madera or Hojas
                self.material_name_to_color[name] = color

        # 4. Create the final map of material properties (with names and colors already assigned)
        self.material_properties_map = self._create_material_properties_map()

        # 5. Calculate player strength and jump force (now that wood properties are defined)
        self.player_strength_base = self._calculate_player_strength_base()
        # MODIFICACIÓN: Escalar jump_force para que el valor sea una altura en bloques/metros conceptuales
        # Se multiplica por 60 para que el valor por defecto (2.17) se convierta en ~130 bloques.
        self.jump_force = self._calculate_jump_force() * 1 # Multiplicador para altura en bloques/metros

    def _extract_seed_digits(self, seed_val):
        """
        Extracts 8 digits from the seed, padding with zeros if necessary.
        """
        s = str(seed_val).zfill(8)
        return [int(d) for d in s]

    def _get_adjacent_non_overlapping_products_data(self):
        """
        Calculates the products and original duplas for duplas S0S1, S2S3, S4S5, S6S7.
        Returns a list of dictionaries with 'product', 'c1', 'c2' and 'dupla_raw'.
        """
        products_data = []
        for i in range(0, 8, 2):
            if i + 1 < 8: # Ensure there is a second digit in the dupla
                c1 = self.seed_digits[i]
                c2 = self.seed_digits[i+1]
                products_data.append({'product': c1 * c2, 'c1': c1, 'c2': c2, 'dupla_raw': (c1, c2)})

        return products_data

    def _get_dupla_data_ordered_by_product(self):
        """
        Separates the seed into duplas, calculates their products, and returns them sorted
        by product in descending order.
        """
        products_data = self._get_adjacent_non_overlapping_products_data()

        # Sort by product in descending order
        return sorted(products_data, key=lambda x: x['product'], reverse=True)

    def _get_dupla_data_ordered_by_original_position(self):
        """
        Separates the seed into duplas and returns them in their original positional order.
        """
        positional_data = []
        for i in range(0, 8, 2):
            c1 = self.seed_digits[i]
            c2 = self.seed_digits[i+1]
            positional_data.append({'c1': c1, 'c2': c2, 'dupla_raw': (c1, c2)})
        return positional_data


    def _assign_names_to_sorted_seed_duplas(self):
        """
        Assigns fixed names ("Piedra", "Roca", "Madera", "Agua")
        to the unique (min, max) duplas extracted from the seed,
        sorted from smallest to largest (first by min value, then by max value).
        Returns a dictionary { (min,max)_dupla : material_name }.
        """
        unique_min_max_duplas = set()
        for dupla_data in self.duplas_from_seed_in_order:
            raw_dupla = dupla_data['dupla_raw']
            # Ensure the dupla is in (min, max) format for the key
            unique_min_max_duplas.add(tuple(sorted(raw_dupla)))

        sorted_unique_min_max_duplas = sorted(list(unique_min_max_duplas))

        material_name_map = {}
        # Fixed names in the desired hierarchical order
        fixed_names = ["Piedra", "Roca", "Madera", "Agua"]

        # Assign names to the sorted duplas hierarchically
        for i, min_max_key in enumerate(sorted_unique_min_max_duplas):
            if i < len(fixed_names):
                material_name_map[min_max_key] = fixed_names[i]
            else:
                # Fallback for extra duplas if the seed had more than 4 unique duplas
                material_name_map[min_max_key] = f"MaterialExtra{i}"
        return material_name_map

    def _subtractive_mix_rgb(self, rgb1, rgb2):
        """
        Mixes two RGB colors in a way that simulates subtractive mixing (darker).
        Uses HSV for more intuitive control of brightness and saturation.
        """
        # Average RGB components for an initial mix
        r_avg = (rgb1[0] + rgb2[0]) // 2
        g_avg = (rgb1[1] + rgb2[1]) // 2
        b_avg = (rgb1[2] + rgb2[2]) // 2

        # Convert to HSV to manipulate brightness and saturation
        # Normalise to 0.0-1.0 for colorsys
        h, s, v = colorsys.rgb_to_hsv(r_avg/255.0, g_avg/255.0, b_avg/255.0)

        # Reduce Value (brightness) and Saturation to simulate the subtractive mixing effect
        # and to get more "earthy" or "natural" tones from mixes.
        v_final = v * 0.7 # Reduce brightness to 70%
        s_final = s * 0.8 # Reduce saturation slightly to 80%

        # Convert back to RGB and scale to 0-255
        r_new, g_new, b_new = colorsys.hsv_to_rgb(h, s_final, v_final)

        final_r = int(max(0, min(255, r_new * 255)))
        final_g = int(max(0, min(255, g_new * 255)))
        final_b = int(max(0, min(255, b_new * 255)))

        return (final_r, final_g, final_b)

    def _assign_initial_pure_colors_to_material_names(self):
        """
        Assigns pure colors (R,Y,G,B) to material NAMES
        based on the original color of the raw dupla to which that name was mapped.
        Returns a dictionary { material_name : pure_color }.
        """
        material_name_to_pure_color_map = {}
        pure_colors_in_order = [PURE_RED, PURE_YELLOW, PURE_GREEN, PURE_BLUE]

        # Create an inverse mapping from (min,max)_dupla to the original raw dupla AND its original index
        min_max_to_original_dupla_and_index = {}
        for i, dupla_data in enumerate(self.duplas_from_seed_in_order):
            min_max_dupla = tuple(sorted(dupla_data['dupla_raw']))
            # Store only the first occurrence if there are duplicate (min,max) duplas
            if min_max_dupla not in min_max_to_original_dupla_and_index:
                min_max_to_original_dupla_and_index[min_max_dupla] = {'raw_dupla': dupla_data['dupla_raw'], 'index': i}

        # Assign pure colors to fixed material names
        for fixed_material_name in ["Piedra", "Roca", "Madera", "Agua"]:
            # Find the (min,max)_dupla that mapped to this name
            found_min_max_key = None
            for min_max_key, assigned_name in self.material_archetypes_by_min_max_key.items():
                if assigned_name == fixed_material_name:
                    found_min_max_key = min_max_key
                    break

            if found_min_max_key and found_min_max_key in min_max_to_original_dupla_and_index:
                original_index = min_max_to_original_dupla_and_index[found_min_max_key]['index']
                if original_index < len(pure_colors_in_order):
                    material_name_to_pure_color_map[fixed_material_name] = pure_colors_in_order[original_index]
                else:
                    material_name_to_pure_color_map[fixed_material_name] = BLACK # Fallback
            else:
                material_name_to_pure_color_map[fixed_material_name] = BLACK # Fallback if mapping not found

        return material_name_to_pure_color_map


    def _create_material_properties_map(self):
        """
        Creates a complete map of material properties for this universe.
        The map key will be the (min_val, max_val) dupla that identifies the material,
        or a string key for derived materials like "Hojas".
        """
        material_data_map = {}

        # Iterate over the duplas that define the material archetypes in this universe
        for min_max_key, material_name_archetype in self.material_archetypes_by_min_max_key.items():

            # Get the color from the final color map (which includes mixes)
            color = self.material_name_to_color.get(material_name_archetype, BLACK)

            current_dupla_product = min_max_key[0] * min_max_key[1]

            # Hardness = (Gravity_Product - Current_Dupla_Product) + Current_Dupla_Min
            base_resistance = (self.gravity_dupla_data['product'] - current_dupla_product) + min_max_key[0]

            if base_resistance < 1: # Ensure a minimum resistance to avoid negative or zero values
                base_resistance = 1

            is_fluid = (material_name_archetype == "Agua") # Only water is fluid by default

            material_data_map[min_max_key] = {
                'name': material_name_archetype,
                'color': color,
                'base_resistance': base_resistance, # Base resistance before role adjustment
                'is_fluid': is_fluid,
                'product': current_dupla_product
            }

        # --- Add "Hojas" as an explicitly derived material ---
        leaves_color = self.material_name_to_color.get("Hojas", BLACK)
        leaves_base_resistance = 0.5 # Leaves are very easy to break
        leaves_is_fluid = False

        # We will use a string as a key for "Hojas" in the properties map,
        # to distinguish it from the (min,max) duplas that identify other materials.
        material_data_map['Hojas_Derived_Material_Key'] = {
            'name': "Hojas",
            'color': leaves_color,
            'base_resistance': leaves_base_resistance,
            'is_fluid': leaves_is_fluid,
            'product': 0 # Dummy product, as it is not based on a direct dupla
        }

        return material_data_map

    def _calculate_player_strength_base(self):
        """
        Calculates the player's base strength.
        Logic: Wood hardness + first digit (C1) of the second largest dupla by product.
        """
        # Find the (min, max) dupla that corresponds to the name "Madera" in THIS universe
        wood_dupla_key = None
        for key, name in self.material_archetypes_by_min_max_key.items():
            if name == "Madera":
                wood_dupla_key = key
                break

        dureza_madera = 23 # Default value if wood is not found
        if wood_dupla_key and wood_dupla_key in self.material_properties_map:
            dureza_madera = self.material_properties_map[wood_dupla_key]['base_resistance']
        else:
            # Fallback if wood could not be found by its (min,max) dupla
            # This can happen if the material_archetypes_by_min_max_key mapping is incomplete
            print("Warning: Wood hardness could not be found by its dupla, using default value.")

        # The second largest dupla by product is already in self.player_strength_dupla_data
        min_second_dupla = self.player_strength_dupla_data['c1'] # It's C1 of the dupla

        return dureza_madera + min_second_dupla

    def _calculate_jump_force(self):
        """
        Calculates the player's jump force.
        Jump Force = Player_Strength / (sum of digits of the gravity dupla).
        """
        if self.gravity_dupla_data and self.player_strength_base > 0:
            sum_of_gravity_digits = self.gravity_dupla_data['c1'] + self.gravity_dupla_data['c2']
            if sum_of_gravity_digits > 0:
                return self.player_strength_base / sum_of_gravity_digits
        return 2.67 # Default value

    def get_material_properties(self, material_key, y_coord_for_role):
        """
        Returns the complete material properties for a given key (min_max_dupla_key or string),
        adjusted by role/depth.
        """
        material_base_data = self.material_properties_map.get(material_key)

        if not material_base_data:
            # Fallback for unknown keys
            return {
                'name': "Desconocido",
                'color': BLACK,
                'resistance': 1,
                'structural_resistance': 1,
                'is_fluid': False,
                'element_dupla_key': material_key, # Store original key for debugging
                'role': 0
            }


        base_name = material_base_data['name']
        base_color = material_base_data['color']
        base_resistance_unadjusted = material_base_data['base_resistance']
        is_fluid = material_base_data['is_fluid']

        # --- Role logic by height (CORRECTED to use world coordinates) ---
        SURFACE_WORLD_Y_THRESHOLD = 200
        MID_DEPTH_WORLD_Y_THRESHOLD = 220

        role_num = 0
        if y_coord_for_role < SURFACE_WORLD_Y_THRESHOLD:
            role_num = 2
        elif y_coord_for_role < MID_DEPTH_WORLD_Y_THRESHOLD:
            role_num = 3
        else:
            role_num = 4

        # Water always has the fluidity role
        if base_name == "Agua":
            role_num = 1
            is_fluid = True
        # Leaves always have a resistance role of 0.1, and are not affected by depth
        elif base_name == "Hojas":
            role_num = 1 # To use role_capacity = 0.1
            is_fluid = False # Not fluid

        role_capacity = 0
        if role_num == 1: role_capacity = 0.1 # Very low resistance for fluids and leaves
        elif role_num == 2: role_capacity = 1
        elif role_num == 3: role_capacity = 2
        elif role_num == 4: role_capacity = 4
        elif role_num == 5: role_capacity = 6

        final_resistance = base_resistance_unadjusted * role_capacity

        # Reaffirm that fluids and leaves have fixed low resistance (0.1)
        if base_name == "Agua" or base_name == "Hojas":
            final_resistance = 0.1 # Very low resistance

        # Ensure self.gravity is not zero before division
        structural_resistance = (final_resistance ** 2) / self.gravity if self.gravity > 0 else 0

        return {
            'name': f"{base_name} ({role_capacity}R)",
            'color': base_color,
            'resistance': final_resistance,
            'structural_resistance': structural_resistance,
            'is_fluid': is_fluid,
            'element_dupla_key': material_key, # Use the original key
            'role': role_num
        }

# --- World Generator ---
class WorldGenerator:
    def __init__(self, numerium_core, numerium_seed_val, detail_level):
        self.numerium_core = numerium_core
        self.numerium_seed = numerium_seed_val
        self.numerium_seed_digits = self._extract_seed_digits(self.numerium_seed)
        self.detail_level = detail_level # New: Detail level

        # Dictionary to store chunks. The key is (chunk_x, chunk_y)
        # The value is a pygame.sprite.Group containing the blocks of that chunk
        self.chunks = {}

        # List of chunks that are currently loaded and active for rendering/collisions
        self.active_chunks = []

        # Terrain generation parameters based on the Numerium seed
        self.c1_num_terrain = 0
        self.c2_num_terrain = 0
        self.c3_num_terrain = 0
        self._process_numerium_seed_for_terrain()

        # Store the (min, max) dupla that represents water for faster access
        # (It is assumed that 'Agua' is always a valid material type)
        self.water_dupla_key = None
        for key, name in self.numerium_core.material_archetypes_by_min_max_key.items():
            if name == "Agua":
                self.water_dupla_key = key
                break

        # Key for the Leaves material
        self.leaves_material_key = 'Hojas_Derived_Material_Key'


    def _extract_seed_digits(self, seed_val):
        """Extracts 3 digits from the seed, padding with zeros if necessary."""
        s = str(seed_val).zfill(3)
        return [int(d) for d in s]

    def _process_numerium_seed_for_terrain(self):
        """
        Processes the Numerium seed to determine terrain parameters,
        magnifying the digits with the detail level as a coefficient,
        but limiting the exponent for c3_num_terrain to optimize performance.
        """
        s0 = self.numerium_seed_digits[0]
        s1 = self.numerium_seed_digits[1]
        s2 = self.numerium_seed_digits[2]

        # Magnification factor based on the Detail Level.
        # We multiply by (self.detail_level / 10.0) so that LOD=10 maintains the original magnitude of the digits.
        magnification_factor = self.detail_level / 10.0

        # c1 and c2 control the slope and displacement of the height variation.
        # These can be large numbers without directly affecting the module's performance.
        # We add 1 to each digit before magnifying to ensure that even a '0' digit has an impact.
        self.c1_num_terrain = max(1, int(round((s0 + 1) * magnification_factor)))
        self.c2_num_terrain = max(1, int(round((s1 + 1) * magnification_factor)))

        # For c3_num_terrain (the period), the exponent base is magnified,
        # BUT the final exponent is CLIPPED to a manageable value to optimize module performance.
        # An exponent of 30 (2^30) already gives a period of ~10^9, which is massive and will seem infinite in the game.
        MAX_EXPONENT_FOR_C3 = 30

        # Calculate the potential value of the magnified base exponent
        raw_base_exponent_val = int(round((s2 + 1) * magnification_factor))

        # Limit the effective exponent used for C3 so that it does not exceed MAX_EXPONENT_FOR_C3.
        # The actual exponent in 2**X is (raw_base_exponent_val + 1), so we clip this value.
        effective_exponent = min(MAX_EXPONENT_FOR_C3, raw_base_exponent_val + 1)

        # Calculate c3_num_terrain using the limited exponent.
        self.c3_num_terrain = 2**(effective_exponent)

        # Ensure c3_num_terrain is at least 1 (although 2**X always will be >= 2 for positive exponents)
        if self.c3_num_terrain < 1:
            self.c3_num_terrain = 1

    def get_chunk_coords_from_world_coords(self, world_x, world_y):
        """Converts world coordinates to chunk coordinates."""
        return (world_x // (CHUNK_SIZE * BLOCK_SIZE), world_y // (CHUNK_SIZE * BLOCK_SIZE))

    def get_world_coords_from_chunk_coords(self, chunk_x, chunk_y):
        """Converts chunk coordinates to world coordinates of the chunk origin."""
        return (chunk_x * CHUNK_SIZE * BLOCK_SIZE, chunk_y * CHUNK_SIZE * BLOCK_SIZE)

    def generate_chunk_at(self, chunk_x, chunk_y):
        """
        Generates a chunk of blocks at the given chunk coordinates.
        If the chunk already exists, it does nothing.
        """
        if (chunk_x, chunk_y) in self.chunks:
            return

        new_chunk_blocks = pygame.sprite.Group()

        # Get the (min, max) material duplas defined in NumeriumCore for generation
        # Ensures that the order of materials in the world reflects the seed definition
        material_min_max_duplas_for_generation_order = sorted(list(self.numerium_core.material_archetypes_by_min_max_key.keys()))

        if not material_min_max_duplas_for_generation_order:
            # Fallback if for some reason no materials are defined
            material_min_max_duplas_for_generation_order = [
                (2, 6), (2, 7), (3, 4), (4, 8)
            ]

        # Calculate initial world coordinates of this chunk
        start_world_x, start_world_y = self.get_world_coords_from_chunk_coords(chunk_x, chunk_y)

        for x_local in range(CHUNK_SIZE):
            world_block_x = (start_world_x // BLOCK_SIZE) + x_local # X coordinate of the block in the world

            # Surface height generation (adapted to world coordinates)
            # Surface height is relative to the bottom of the chunk
            height_variation_factor = (self.c1_num_terrain * world_block_x + self.c2_num_terrain) % self.c3_num_terrain

            # The terrain surface is generated higher in the world
            # We adjust this height to a more global base.
            # We take 200 blocks as "maximum height" for the simulated sea level
            base_surface_y_block = 200
            surface_y_block_coord = base_surface_y_block - (height_variation_factor * 2)

            # Ensure surface is not too low or too high
            if surface_y_block_coord < base_surface_y_block - 100: surface_y_block_coord = base_surface_y_block - 100
            if surface_y_block_coord > base_surface_y_block + 10: surface_y_block_coord = base_surface_y_block + 10


            # Use the appropriate material dupla for the surface column
            idx = int(world_block_x % len(material_min_max_duplas_for_generation_order))
            min_max_dupla_for_column = material_min_max_duplas_for_generation_order[idx]

            # --- Tree/Vegetation Generation Logic (Moved and Enhanced) ---
            # Generate a tree if the column is on the surface and follows a pattern (e.g., every 10 blocks X).
            # Also, ensure it's not water at the surface, which would conflict with tree placement.
            surface_material_name_for_tree_check = self.numerium_core.material_archetypes_by_min_max_key.get(min_max_dupla_for_column, "Desconocido")

            if (world_block_x % 10 == 0) and (surface_material_name_for_tree_check != "Agua"):
                # Variable tree height based on a digit from the Randomixer seed (e.g., 4th digit, index 3)
                # Map digit (0-9) to a height range (e.g., 2 to 5 blocks for the trunk)
                # tree_trunk_height = 2 + (digit_from_seed % 4) -> 2,3,4,5
                # We use seed_digits[3] for the trunk height
                # Make sure the index seed_digits[3] exists
                if len(self.numerium_core.seed_digits) > 3:
                    tree_trunk_height = 2 + (self.numerium_core.seed_digits[3] % 4)
                else:
                    tree_trunk_height = 3 # Default height if not enough digits in the seed

                # Properties of wood (its color is already mixed in NumeriumCore)
                # For wood resistance, we use the dupla that mapped to "Madera"
                wood_material_key_for_properties = None
                for key, name in self.numerium_core.material_archetypes_by_min_max_key.items():
                    if name == "Madera":
                        wood_material_key_for_properties = key
                        break

                # Properties of leaves (its color is already mixed in NumeriumCore, and has a special key)
                # The height of the leaves is based on the trunk height
                leaves_material_data = self.numerium_core.get_material_properties(self.leaves_material_key, surface_y_block_coord - tree_trunk_height - 1)

                if wood_material_key_for_properties: # Ensure we found the key for wood
                    wood_material_data = self.numerium_core.get_material_properties(wood_material_key_for_properties, surface_y_block_coord - tree_trunk_height)

                    # Place trunk blocks
                    for h_offset in range(tree_trunk_height):
                        trunk_y = surface_y_block_coord - 1 - h_offset # Trunk grows upwards from surface
                        if not self.get_block_at_world_coords(world_block_x, trunk_y):
                            wood_block = Block(world_block_x * BLOCK_SIZE, trunk_y * BLOCK_SIZE, wood_material_data)
                            new_chunk_blocks.add(wood_block)

                    # Place leaves (small canopy) - three blocks on top and sides of the trunk, plus one more on top
                    # Y coordinate for the base of the leaves (just above the top trunk block)
                    leaves_base_y = surface_y_block_coord - tree_trunk_height

                    # Place central top leaf block
                    if leaves_material_data and not self.get_block_at_world_coords(world_block_x, leaves_base_y):
                        leaves_block_center_top = Block(world_block_x * BLOCK_SIZE, leaves_base_y * BLOCK_SIZE, leaves_material_data)
                        new_chunk_blocks.add(leaves_block_center_top)

                    # Place side leaf blocks (left and right of central leaf block)
                    leaves_block_side_left_x = world_block_x - 1
                    leaves_block_side_right_x = world_block_x + 1
                    if leaves_material_data and not self.get_block_at_world_coords(leaves_block_side_left_x, leaves_base_y):
                        leaves_block_side_left = Block(leaves_block_side_left_x * BLOCK_SIZE, leaves_base_y * BLOCK_SIZE, leaves_material_data)
                        new_chunk_blocks.add(leaves_block_side_left)
                    if leaves_material_data and not self.get_block_at_world_coords(leaves_block_side_right_x, leaves_base_y):
                        leaves_block_side_right = Block(leaves_block_side_right_x * BLOCK_SIZE, leaves_base_y * BLOCK_SIZE, leaves_material_data)
                        new_chunk_blocks.add(leaves_block_side_right)

                    # Place one more block above the center (for a rounder shape)
                    leaves_block_top_y = leaves_base_y - 1
                    if leaves_material_data and not self.get_block_at_world_coords(world_block_x, leaves_block_top_y):
                        leaves_block_top = Block(world_block_x * BLOCK_SIZE, leaves_block_top_y * BLOCK_SIZE, leaves_material_data)
                        new_chunk_blocks.add(leaves_block_top)


            # Generate blocks for the terrain column
            for y_local in range(CHUNK_SIZE):
                world_block_y = (start_world_y // BLOCK_SIZE) + y_local # Y coordinate of the block in the world

                if world_block_y == surface_y_block_coord:
                    material_props = self.numerium_core.get_material_properties(min_max_dupla_for_column, world_block_y)
                    block = Block(world_block_x * BLOCK_SIZE, world_block_y * BLOCK_SIZE, material_props)
                    new_chunk_blocks.add(block)
                elif world_block_y > surface_y_block_coord:
                    # For underground blocks, cycle through available materials.
                    underground_material_idx = int((world_block_y - surface_y_block_coord - 1 + world_block_x) % len(material_min_max_duplas_for_generation_order))
                    underground_min_max_dupla = material_min_max_duplas_for_generation_order[underground_material_idx]

                    material_props = self.numerium_core.get_material_properties(underground_min_max_dupla, world_block_y)
                    block = Block(world_block_x * BLOCK_SIZE, world_block_y * BLOCK_SIZE, material_props)
                    new_chunk_blocks.add(block)

                # If the surface material of the column is "Water", fill below with water
                surface_material_name = self.numerium_core.material_archetypes_by_min_max_key.get(min_max_dupla_for_column, "Desconocido")
                if surface_material_name == "Agua" and world_block_y > surface_y_block_coord:
                    if self.water_dupla_key: # Only if water has a defined dupla
                        water_material_props = self.numerium_core.get_material_properties(self.water_dupla_key, world_block_y)
                        block = Block(world_block_x * BLOCK_SIZE, world_block_y * BLOCK_SIZE, water_material_props)
                        new_chunk_blocks.add(block)


        self.chunks[(chunk_x, chunk_y)] = new_chunk_blocks

    def update_active_chunks(self, player_world_x, player_world_y):
        """
        Determines which chunks should be active (loaded and ready for rendering/collisions)
        based on the player's position. Generates new chunks if necessary.
        """
        player_chunk_x, player_chunk_y = self.get_chunk_coords_from_world_coords(player_world_x, player_world_y)

        new_active_chunks = set()
        all_blocks_in_active_chunks = pygame.sprite.Group()

        for dx in range(-RENDER_DISTANCE_CHUNKS, RENDER_DISTANCE_CHUNKS + 1):
            for dy in range(-RENDER_DISTANCE_CHUNKS, RENDER_DISTANCE_CHUNKS + 1):
                chunk_x = player_chunk_x + dx
                chunk_y = player_chunk_y + dy

                # Generate the chunk if it does not exist
                if (chunk_x, chunk_y) not in self.chunks:
                    self.generate_chunk_at(chunk_x, chunk_y)

                # Add the blocks of the chunk to the list of active blocks
                if (chunk_x, chunk_y) in self.chunks:
                    all_blocks_in_active_chunks.add(self.chunks[(chunk_x, chunk_y)])

                new_active_chunks.add((chunk_x, chunk_y))

        # Remove chunks that are no longer in rendering distance (future optimization: unloading)
        # For now, we simply update the list of active chunks for the drawing cycle.
        self.active_chunks = list(new_active_chunks)
        return all_blocks_in_active_chunks # Returns a group of all blocks in active chunks


    def get_blocks_in_active_chunks(self):
        """Returns all blocks from currently active chunks."""
        all_blocks = pygame.sprite.Group()
        for chunk_coords in self.active_chunks:
            if chunk_coords in self.chunks:
                all_blocks.add(self.chunks[chunk_coords])
        return all_blocks

    def get_block_at_world_coords(self, world_block_x, world_block_y):
        """Returns a specific block at world coordinates."""
        chunk_x = world_block_x // CHUNK_SIZE
        chunk_y = world_block_y // CHUNK_SIZE

        if (chunk_x, chunk_y) in self.chunks:
            # Get the block by its world coordinates
            for block in self.chunks[(chunk_x, chunk_y)]:
                if block.world_x // BLOCK_SIZE == world_block_x and \
                   block.world_y // BLOCK_SIZE == world_block_y:
                    return block
        return None

    def remove_block_at_world_coords(self, world_block_x, world_block_y):
        """Removes a block at world coordinates."""
        chunk_x = world_block_x // CHUNK_SIZE
        chunk_y = world_block_y // CHUNK_SIZE

        if (chunk_x, chunk_y) in self.chunks:
            block_to_remove = None
            for block in self.chunks[(chunk_x, chunk_y)]:
                if block.world_x // BLOCK_SIZE == world_block_x and \
                   block.world_y // BLOCK_SIZE == world_block_y:
                    block_to_remove = block
                    break

            if block_to_remove:
                self.chunks[(chunk_x, chunk_y)].remove(block_to_remove)
                return block_to_remove
        return None

    def place_block_at_world_coords(self, world_block_x, world_block_y, material_data):
        """Places a block at world coordinates."""
        chunk_x = world_block_x // CHUNK_SIZE
        chunk_y = world_block_y // CHUNK_SIZE

        # Ensure the chunk exists to place the block
        # This is important for building in new/unloaded areas
        if (chunk_x, chunk_y) not in self.chunks:
            self.generate_chunk_at(chunk_x, chunk_y)

        # Ensure there is no other block in the position
        if not self.get_block_at_world_coords(world_block_x, world_block_y):
            new_block = Block(world_block_x * BLOCK_SIZE, world_block_y * BLOCK_SIZE, material_data)
            self.chunks[(chunk_x, chunk_y)].add(new_block)
            return new_block
        return None


# --- Drawing and Slicing Functions ---
# --- Optimized Surface Cache ---
print (FPS)
surface_cache = {}

def get_cached_surface(color, alpha):
    # Ensure color is a valid RGB tuple
    if color is None or not isinstance(color, tuple) or len(color) != 3:
        print("Invalid color detected, using emergency magenta.")
        color = (255, 0, 255)  # Magenta as error marker

    # Ensure alpha is an integer between 0 and 255
    try:
        alpha = int(alpha)
        if alpha < 0 or alpha > 255:
            alpha = 255
    except:
        alpha = 255

    key = (color, alpha)

    if key not in surface_cache:
        try:
            surf = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
            surf.fill((*color, alpha))
            surface_cache[key] = surf
        except Exception as e:
            print(f"ERROR creating surface for color={color}, alpha={alpha} → {e}")
            # Return error surface to prevent game from breaking
            fallback_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
            fallback_surface.fill((255, 0, 255, 255))  # Full magenta
            return fallback_surface

    return surface_cache[key]

def draw_2d_block(screen, block, camera_offset_x, camera_offset_y, draw_alpha=255):
    """
    Draws a simple 2D block with camera offset and alpha.
    """
    if draw_alpha <= 0:
        return

    # Calculate screen position of the block
    screen_x = block.rect.x + camera_offset_x
    screen_y = block.rect.y + camera_offset_y
    #print("Color:", block.get_color(), "Alpha:", draw_alpha)
    # Only draw if within view
    if -BLOCK_SIZE < screen_x < SCREEN_WIDTH and -BLOCK_SIZE < screen_y < SCREEN_HEIGHT:
        block_rect = pygame.Rect(screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE)
        surface = get_cached_surface(block.get_color(), draw_alpha) # Surface with alpha
        screen.blit(surface, block_rect)
        #print(f"CACHE SIZE:{len(surface_cache)}")

def apply_light_effect_2d(screen, block, player_world_block_coords, numerium_core, camera_offset_x, camera_offset_y, draw_distance_chunks):
    """
    Applies a simplified light effect to a single block in 2D.
    """
    # Use world block coordinates
    block_x_world = block.world_x // BLOCK_SIZE
    block_y_world = block.world_y // BLOCK_SIZE

    dist_x = abs(block_x_world - player_world_block_coords[0])
    dist_y = abs(block_y_world - player_world_block_coords[1])
    distance_blocks = math.sqrt(dist_x**2 + dist_y**2)

    light_intensity = max(0, 1.0 - (distance_blocks / draw_distance_chunks))

    # Highlight "Piedra" blocks if they are close enough
    if "Piedra" in block.get_name() and light_intensity > 0.3:
        screen_x = block.rect.x + camera_offset_x
        screen_y = block.rect.y + camera_offset_y
        if -BLOCK_SIZE < screen_x < SCREEN_WIDTH and -BLOCK_SIZE < screen_y < SCREEN_HEIGHT:
            block_rect = pygame.Rect(screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, WHITE, block_rect, 1)

    alpha = int(255 * light_intensity)
    if block.is_fluid():
        alpha = int(255 * 0.4 * light_intensity)
    return alpha


# --- Inventory System ---
class Inventory:
    def __init__(self, num_slots_hotbar, num_rows_full_inventory, num_cols_full_inventory, block_size):
        self.hotbar_slots = [None] * num_slots_hotbar
        self.full_inventory_slots = [[None for _ in range(num_cols_full_inventory)] for _ in range(num_rows_full_inventory)]
        self.selected_slot = 0 # For the hotbar
        self.block_size = block_size
        self.font = pygame.font.Font(None, 20)
        self.num_rows_full = num_rows_full_inventory
        self.num_cols_full = num_cols_full_inventory

    def add_item(self, material_data, count=1):
        """Adds a material to the inventory, stacking it if it already exists."""
        # Try to add to hotbar first
        for i, slot in enumerate(self.hotbar_slots):
            if slot and slot['material_data']['name'] == material_data['name']:
                slot['count'] += count
                return True
        for i, slot in enumerate(self.hotbar_slots):
            if slot is None:
                self.hotbar_slots[i] = {'material_data': material_data, 'count': count}
                return True

        # Then try to add to full inventory
        for r in range(self.num_rows_full):
            for c in range(self.num_cols_full):
                slot = self.full_inventory_slots[r][c]
                if slot and slot['material_data']['name'] == material_data['name']:
                    slot['count'] += count
                    return True
        for r in range(self.num_rows_full):
            for c in range(self.num_cols_full):
                if self.full_inventory_slots[r][c] is None:
                    self.full_inventory_slots[r][c] = {'material_data': material_data, 'count': count}
                    return True
        return False # Inventory is full

    def remove_item(self, material_data_name, count=1):
        """Removes a material from the inventory."""
        # Try to remove from hotbar first
        for i, slot in enumerate(self.hotbar_slots):
            if slot and slot['material_data']['name'] == material_data_name:
                slot['count'] -= count
                if slot['count'] <= 0:
                    self.hotbar_slots[i] = None
                return True
        # Then try to remove from full inventory
        for r in range(self.num_rows_full):
            for c in range(self.num_cols_full):
                slot = self.full_inventory_slots[r][c]
                if slot and slot['material_data']['name'] == material_data_name:
                    slot['count'] -= count
                    if slot['count'] <= 0:
                        self.full_inventory_slots[r][c] = None
                    return True
        return False

    def get_selected_item(self):
        """Returns the currently selected material in the hotbar."""
        if self.hotbar_slots[self.selected_slot]:
            return self.hotbar_slots[self.selected_slot]['material_data']
        return None

    def get_item_properties_by_name(self, name_to_find):
        """Searches for and returns the properties of a material by its name in the inventory."""
        for slot in self.hotbar_slots:
            if slot and name_to_find in slot['material_data']['name']:
                return slot['material_data']
        for row in self.full_inventory_slots:
            for slot in row:
                if slot and name_to_find in slot['material_data']['name']:
                    return slot['material_data']
        return None

    def has_item_by_name(self, name_to_find):
        """Checks if the inventory contains a material by its name."""
        return self.get_item_properties_by_name(name_to_find) is not None

    def get_current_tool_strength(self):
        """
        Calculates the strength of the strongest tool the player possesses
        based on material types.
        """
        max_tool_strength = 0

        # Material types that can act as tools
        tool_material_types = [
            "Piedra", "Roca", "Madera"
        ]

        for tool_type in tool_material_types:
            for slot in self.hotbar_slots:
                if slot and tool_type in slot['material_data']['name']:
                    # Tool strength is material resistance
                    if slot['material_data']['resistance'] > max_tool_strength:
                        max_tool_strength = slot['material_data']['resistance']
            for row in self.full_inventory_slots:
                for slot in row:
                    if slot and tool_type in slot['material_data']['name']:
                        if slot['material_data']['resistance'] > max_tool_strength:
                            max_tool_strength = slot['material_data']['resistance']

        return max_tool_strength

    def draw_hotbar(self, screen):
        """Draws the hotbar on the screen."""
        inventory_x = SCREEN_WIDTH // 2 - (len(self.hotbar_slots) * (self.block_size + 5)) // 2
        inventory_y = SCREEN_HEIGHT - (self.block_size + 10)

        for i, slot in enumerate(self.hotbar_slots):
            slot_rect = pygame.Rect(inventory_x + i * (self.block_size + 5), inventory_y, self.block_size, self.block_size)

            pygame.draw.rect(screen, INVENTORY_SLOT_COLOR, slot_rect, 0, 5)
            pygame.draw.rect(screen, BLACK, slot_rect, 2, 5)

            if i == self.selected_slot:
                pygame.draw.rect(screen, INVENTORY_SELECTED_COLOR, slot_rect, 3, 5)

            if slot:
                block_image = pygame.Surface([self.block_size - 4, self.block_size - 4])
                block_image.fill(slot['material_data']['color'])
                screen.blit(block_image, (slot_rect.x + 2, slot_rect.y + 2))

                count_text = self.font.render(str(slot['count']), True, WHITE)
                screen.blit(count_text, (slot_rect.right - count_text.get_width() - 2, slot_rect.bottom - count_text.get_height() - 2))

    def draw_inventory_grid(self, screen):
        """Draws the full 5x5 inventory grid on the screen."""
        # Draw a semi-transparent background over the game
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150)) # Black with 150 alpha (out of 255)
        screen.blit(overlay, (0, 0))

        grid_width = self.num_cols_full * (self.block_size + 10) - 10 # 10 for padding
        grid_height = self.num_rows_full * (self.block_size + 10) - 10

        start_x = (SCREEN_WIDTH - grid_width) // 2
        start_y = (SCREEN_HEIGHT - grid_height) // 2

        # Draw the main inventory background
        inventory_bg_rect = pygame.Rect(start_x - 20, start_y - 20, grid_width + 40, grid_height + 40)
        pygame.draw.rect(screen, GRAY, inventory_bg_rect, 0, 10)
        pygame.draw.rect(screen, BLACK, inventory_bg_rect, 3, 10)

        # Draw "Inventory" title
        title_font = pygame.font.Font(None, 36)
        title_text = title_font.render("Inventario", True, WHITE)
        screen.blit(title_text, (inventory_bg_rect.centerx - title_text.get_width() // 2, inventory_bg_rect.y + 15))


        # Draw hotbar slots at the top of the inventory grid
        hotbar_display_y = start_y + 50 # Below the title
        for i, slot in enumerate(self.hotbar_slots):
            slot_x = start_x + i * (self.block_size + 10)
            slot_rect = pygame.Rect(slot_x, hotbar_display_y, self.block_size, self.block_size)

            pygame.draw.rect(screen, INVENTORY_SLOT_COLOR, slot_rect, 0, 5)
            pygame.draw.rect(screen, BLACK, slot_rect, 2, 5)

            if i == self.selected_slot:
                pygame.draw.rect(screen, INVENTORY_SELECTED_COLOR, slot_rect, 3, 5)

            if slot:
                block_image = pygame.Surface([self.block_size - 4, self.block_size - 4])
                block_image.fill(slot['material_data']['color'])
                screen.blit(block_image, (slot_rect.x + 2, slot_rect.y + 2))

                count_text = self.font.render(str(slot['count']), True, WHITE)
                screen.blit(count_text, (slot_rect.right - count_text.get_width() - 2, slot_rect.bottom - count_text.get_height() - 2))

        # Draw the main 5x5 inventory slots below the hotbar
        main_inventory_start_y = hotbar_display_y + self.block_size + 20 # 20 for spacing

        for r in range(self.num_rows_full):
            for c in range(self.num_cols_full):
                slot_x = start_x + c * (self.block_size + 10)
                slot_y = main_inventory_start_y + r * (self.block_size + 10)
                slot_rect = pygame.Rect(slot_x, slot_y, self.block_size, self.block_size)

                pygame.draw.rect(screen, INVENTORY_SLOT_COLOR, slot_rect, 0, 5)
                pygame.draw.rect(screen, BLACK, slot_rect, 2, 5)

                slot_data = self.full_inventory_slots[r][c]
                if slot_data:
                    block_image = pygame.Surface([self.block_size - 4, self.block_size - 4])
                    block_image.fill(slot_data['material_data']['color'])
                    screen.blit(block_image, (slot_rect.x + 2, slot_rect.y + 2))

                    count_text = self.font.render(str(slot_data['count']), True, WHITE)
                    screen.blit(count_text, (slot_rect.right - count_text.get_width() - 2, slot_rect.bottom - count_text.get_height() - 2))


# --- Input Box Class (Seeds) ---
class InputBox:
    """Class for a text input field for seeds."""
    def __init__(self, x, y, w, h, text='', label='', min_val=None, max_val=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = LIGHT_GRAY
        self.text = text
        self.label = label
        self.font = pygame.font.Font(None, 32)
        self.active = False
        self.txt_surface = self.font.render(self.text, True, BLACK)
        self.min_val = min_val
        self.max_val = max_val

    def handle_event(self, event):
        """Handles keyboard and mouse events for the input box."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = INVENTORY_SELECTED_COLOR if self.active else LIGHT_GRAY
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.color = LIGHT_GRAY
                    self._validate_input()
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.unicode.isdigit():
                        self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, BLACK)

    def _validate_input(self):
        """Validates the input text against min_val and max_val."""
        if self.text.isdigit():
            val = int(self.text)
            if self.min_val is not None and val < self.min_val:
                self.text = str(self.min_val)
            elif self.max_val is not None and val > self.max_val:
                self.text = str(self.max_val)
        else: # If it's not a number, reset to minimum if it exists
            if self.min_val is not None:
                self.text = str(self.min_val)
            else:
                self.text = '' # Or leave empty if there's no minimum
        self.txt_surface = self.font.render(self.text, True, BLACK)


    def draw(self, screen):
        """Draws the input box and its label on the screen."""
        label_surface = self.font.render(self.label, True, WHITE)
        screen.blit(label_surface, (self.rect.x, self.rect.y - 30))
        pygame.draw.rect(screen, self.color, self.rect, 0, 5)
        pygame.draw.rect(screen, BLACK, self.rect, 2, 5)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + (self.rect.h - self.txt_surface.get_height()) // 2))

    def get_text(self):
        """Returns the current text of the input box."""
        return self.text

# --- Game State ---
GAME_STATE = "MENU"

# --- Pygame Initialization ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Randomixer 2D Demo")
clock = pygame.time.Clock()

# --- Game Instances (initialized upon entering the game) ---
numerium = None
world_generator = None
active_blocks_group = pygame.sprite.Group() # Group for currently visible/interactable blocks
player = None
all_sprites = pygame.sprite.Group()
inventory = None

# Camera variables (world position at top-left of viewport)
camera_offset_x = 0
camera_offset_y = 0

# --- Menu Elements ---
randomixer_seed_input = InputBox(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100, 300, 40, text='27482634', label='Reglas (Randomixer - 8 cifras)')
numerium_seed_input = InputBox(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 30, 300, 40, text='123', label='Terreno (Numerium - 3 cifras)')
# New InputBox for Detail Level
detail_level_input = InputBox(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 40, 300, 40, text='10', label='Nivel de Detalle (10-32)', min_val=10, max_val=32)

start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120, 200, 50)
start_button_text_surface = pygame.font.Font(None, 36).render("Iniciar Juego", True, BLACK)

def initialize_game(randomixer_seed_str, numerium_seed_str, detail_level_str):
    """
    Initializes all game components with the given seeds and detail level.
    """
    global numerium, world_generator, active_blocks_group, player, all_sprites, inventory, camera_offset_x, camera_offset_y

    try:
        randomixer_seed = int(randomixer_seed_str)
        numerium_seed = int(numerium_seed_str)
        detail_level = int(detail_level_str)
        # Ensure that the detail level is within the allowed range
        if not (10 <= detail_level <= 32):
            print("Error: The Detail Level must be between 10 and 32.")
            return False

    except ValueError:
        print("Error: Seeds and detail level must be valid integers.")
        return False

    numerium = NumeriumCore(randomixer_seed)
    # Pass the detail level to the WorldGenerator
    world_generator = WorldGenerator(numerium, numerium_seed, detail_level)

    # Start the player at a known base position (e.g., center of the initial world)
    # and ensure the starting chunk is generated
    initial_spawn_world_x = 0 * BLOCK_SIZE # Start at block (0, Y) of the world
    # Adjust initial_spawn_world_y to be in a "surface" area (e.g., Y=160, which will be role_num=2)
    initial_spawn_world_y = 160 * BLOCK_SIZE

    # Force loading chunks around the player's starting position
    active_blocks_group = world_generator.update_active_chunks(initial_spawn_world_x, initial_spawn_world_y)

    player = Player(initial_spawn_world_x, initial_spawn_world_y,
                    numerium.player_strength_base,
                    numerium.jump_force, # numerium.jump_force is now the desired height in blocks
                    numerium.gravity)
    all_sprites = pygame.sprite.Group(player)

    # Initialize inventory with 5 hotbar slots and a 5x5 full inventory
    inventory = Inventory(num_slots_hotbar=5, num_rows_full_inventory=5, num_cols_full_inventory=5, block_size=BLOCK_SIZE)

    # Initialize camera to center the player
    camera_offset_x = SCREEN_WIDTH // 2 - player.world_x
    camera_offset_y = SCREEN_HEIGHT // 2 - player.world_y

    return True

# --- Main Game Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if GAME_STATE == "MENU":
            randomixer_seed_input.handle_event(event)
            numerium_seed_input.handle_event(event)
            detail_level_input.handle_event(event) # Handle events for the new input
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    # Pass the detail level to the game initializer
                    if initialize_game(randomixer_seed_input.get_text(), numerium_seed_input.get_text(), detail_level_input.get_text()):
                        GAME_STATE = "GAME"

        elif GAME_STATE == "GAME":
            player.update_strength_from_inventory(inventory)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump(numerium.gravity) # Pasa la gravedad actual al salto
                if event.key == pygame.K_a:
                    player.start_move_x(-1)
                if event.key == pygame.K_d:
                    player.start_move_x(1)
                if event.key == pygame.K_e: # Toggle inventory
                    GAME_STATE = "INVENTORY"

                # Handle hotbar slot selection with number keys
                if pygame.K_1 <= event.key <= pygame.K_5:
                    inventory.selected_slot = event.key - pygame.K_1
                    print(f"Slot {inventory.selected_slot + 1} seleccionado.")

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player.stop_move_x()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Translate screen coordinates to world coordinates
                world_click_x = mouse_x - camera_offset_x
                world_click_y = mouse_y - camera_offset_y

                # Convert to world block coordinates
                block_x_coord_clicked = world_click_x // BLOCK_SIZE
                block_y_coord_clicked = world_click_y // BLOCK_SIZE

                if event.button == 1: # Left Click (Mine)
                    block_to_mine = world_generator.get_block_at_world_coords(block_x_coord_clicked, block_y_coord_clicked)
                    if block_to_mine:
                        print(f"Intentando minar: {block_to_mine.get_name()} (Resistencia: {block_to_mine.get_resistance():.2f})")
                        print(f"Fuerza actual del jugador: {player.player_strength:.2f}")

                        # --- STRENGTH VERIFICATION FOR MINING ---
                        # Player can only break blocks if their strength is equal to or greater than the block's resistance
                        if player.player_strength >= block_to_mine.get_resistance():
                            # Get player's block coordinates
                            player_current_block_x = player.world_x // BLOCK_SIZE
                            player_current_block_y = player.world_y // BLOCK_SIZE

                            is_in_range = False
                            if abs(player_current_block_x - block_x_coord_clicked) <= 2 and \
                               abs(player_current_block_y - block_y_coord_clicked) <= 2:
                                is_in_range = True

                            if is_in_range:
                                mined_block_data = world_generator.remove_block_at_world_coords(block_x_coord_clicked, block_y_coord_clicked)
                                if mined_block_data:
                                    # Ensure it's also removed from active blocks if it's there
                                    active_blocks_group.remove(mined_block_data)
                                    if inventory.add_item(mined_block_data.material_data):
                                        print(f"¡{mined_block_data.get_name()} minado y añadido al inventario!")
                                    else:
                                        print("Inventario lleno. Bloque minado pero no añadido.")
                                else:
                                    print("No hay bloque para minar (ya fue removido).")
                            else:
                                print("Demasiado lejos para minar este bloque.")
                        else:
                            print(f"Fuerza insuficiente. Necesitas {block_to_mine.get_resistance():.2f} de fuerza para minar {block_to_mine.get_name()}. Tienes {player.player_strength:.2f}.")
                    else:
                        print("No hay bloque para minar aquí.")

                elif event.button == 3: # Right Click (Place)
                    selected_item = inventory.get_selected_item()
                    if selected_item:
                        # Check if placement position is valid (not occupied and with support if not fluid)
                        if not world_generator.get_block_at_world_coords(block_x_coord_clicked, block_y_coord_clicked):
                            block_below_for_support = world_generator.get_block_at_world_coords(block_x_coord_clicked, block_y_coord_clicked + 1)
                            # Allow placement if there is a block below OR if the material is fluid
                            if block_below_for_support or selected_item['is_fluid']:
                                placed_block = world_generator.place_block_at_world_coords(block_x_coord_clicked, block_y_coord_clicked, selected_item)
                                if placed_block:
                                    active_blocks_group.add(placed_block) # Ensure the new block is added to the active group
                                    inventory.remove_item(selected_item['name'])
                                    print(f"Bloque {selected_item['name']} colocado en ({block_x_coord_clicked},{block_y_coord_clicked})!")
                                else:
                                    print("No se pudo colocar el bloque.")
                            else:
                                print("No se puede colocar el bloque en el aire sin soporte (a menos que sea fluido).")
                        else:
                            print("Ya hay un bloque en esta posición.")
                    else:
                        print("No hay bloque seleccionado en el inventario.")

        elif GAME_STATE == "INVENTORY":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e: # Toggle inventory off
                    GAME_STATE = "GAME"


    # --- Update and Draw ---
    screen.fill(BLACK)

    if GAME_STATE == "MENU":
        screen.fill(GRAY)
        randomixer_seed_input.draw(screen)
        numerium_seed_input.draw(screen)
        detail_level_input.draw(screen) # Draw the new input
        pygame.draw.rect(screen, GREEN, start_button_rect, 0, 5)
        screen.blit(start_button_text_surface, start_button_text_surface.get_rect(center=start_button_rect.center))

    elif GAME_STATE == "GAME" or GAME_STATE == "INVENTORY":
        # Update player's world position only if in GAME state
        if GAME_STATE == "GAME":
            player.update(active_blocks_group, world_generator)

        # Calculate camera offset to center the player
        camera_offset_x = SCREEN_WIDTH // 2 - player.world_x - BLOCK_SIZE // 2
        camera_offset_y = SCREEN_HEIGHT // 2 - player.world_y - BLOCK_SIZE # Adjustment so player's feet are slightly below center

        # Update which chunks are active and visible
        active_blocks_group = world_generator.update_active_chunks(player.world_x, player.world_y)

        # Get the world block coordinates where the player is
        player_world_block_x = player.world_x // BLOCK_SIZE
        player_world_block_y = player.world_y // BLOCK_SIZE

        # Draw active blocks with camera offset
        for block in active_blocks_group:
            alpha_value = apply_light_effect_2d(screen, block, (player_world_block_x, player_world_block_y), numerium, camera_offset_x, camera_offset_y, DRAW_DISTANCE_CHUNKS)
            draw_2d_block(screen, block, camera_offset_x, camera_offset_y, draw_alpha=alpha_value)

        # Draw the player centered on the screen
        player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        screen.blit(player.image, player.rect)


        # Display seed and player information
        font = pygame.font.Font(None, 24)
        text_surface_seed = font.render(
            f"R_Seed: {numerium.randomixer_seed} | N_Seed: {world_generator.numerium_seed} | Grav: {numerium.gravity:.2f} | Detail: {world_generator.detail_level}",
            True, WHITE
        )
        screen.blit(text_surface_seed, (10, 10))

        text_surface_player = font.render(
            # jump_force now is the desired height in conceptual "meters" (blocks)
            f"Strength: {player.player_strength:.2f} | Jump: {numerium.jump_force:.2f}m | Base: {numerium.player_strength_base:.2f}",
            True, WHITE

        )
        screen.blit(text_surface_player, (10, 40))

        # Optional: Display player's world coordinates
        text_surface_coords = font.render(
            f"World X: {player.world_x // BLOCK_SIZE} | World Y: {player.world_y // BLOCK_SIZE}",
            True, WHITE
        )
        screen.blit(text_surface_coords, (10, 70))

        if GAME_STATE == "GAME":
            inventory.draw_hotbar(screen) # Only draw hotbar in game state
        elif GAME_STATE == "INVENTORY":
            inventory.draw_inventory_grid(screen) # Draw full inventory grid

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
