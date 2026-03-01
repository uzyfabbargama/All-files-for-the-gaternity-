import pygame
import sys
import random
import time
import math
import json
import os 

# --- PYGAME CONFIGURATION ---
ANCHO_PANTALLA = 1000
ALTO_PANTALLA = 700
FPS = 30
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0) # Red + Green
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)
CIAN = (0, 255, 255) # Blue + Green
BLANCO_APAGADO = (240, 240, 240) # For input background
global neuronas, neuronas_visuales
pygame.init()
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Bynarium Prototipo Extendido y Creador")
reloj = pygame.time.Clock()
fuente = pygame.font.Font(None, 30)
fuente_pequena = pygame.font.Font(None, 20)
fuente_tooltip = pygame.font.Font(None, 22)
fuente_grande = pygame.font.Font(None, 40)

# --- SCREEN STATES ---
SCREEN_NETWORK = 0
SCREEN_CREATOR = 1
current_screen = SCREEN_NETWORK

# --- ZOOM AND PANNING VARIABLES ---
zoom_level = 1.0
offset_x = 0
offset_y = 0
panning_active = False
pan_start_mouse_x, pan_start_mouse_y = 0, 0
pan_start_offset_x, pan_start_offset_y = 0, 0

# --- NEURON DESCRIPTIONS FOR TOOLTIP ---
NEURON_DESCRIPTIONS = {
    "NS": "Sensor",
    "NA": "Analysis",
    "NP": "Depth and Context",
    "NM": "Memory",
    "NO": "NOT Gate", # Added description for NOT gate
    "GO": "Government" # Added description for Government neuron
}

# --- SUMMATION FUNCTIONS ---
def calcular_capacidad_almacenamiento(bits):
    """
    Calculates the storage capacity (max_almacenamiento) of a neuron
    based on its number of bits (role), using Bynarium's formulas.

    For even roles (bits % 2 == 0): (bits/2)^2
    For odd roles (bits % 2 != 0): (bits-1) * (((bits-1)/2) + 1)/2

    This function uses 'bits' directly and applies the logic for even/odd roles.
    """
    if bits <= 0:
        return 0

    if bits % 2 == 0:  # Even Role
        return int((bits / 2) ** 2)
    else:  # Odd Role
        N = bits - 1
        # For N=0 (bits=1), this would result in 0 * (...)/2 = 0, which is correct for Rol 1 (NOT gate).
        return int(N * ((N / 2) + 1) / 2)

def generar_sumatoria_str(bits):
    """
    Generates the string representation of the formula/calculation
    for the tooltip, based on the number of bits (role).
    """
    if bits <= 0:
        return "0"

    if bits % 2 == 0: # Even Role: (bits/2)^2
        return f"({bits}/2)² = {int((bits/2)**2)}"
    else: # Odd Role: (bits-1) * (((bits-1)/2) + 1)/2
        N = bits - 1
        return f"({N} * (({N}/2) + 1)/2) = {int(N * ((N/2) + 1)/2)}"


# --- BYNARIUM SIMULATION ---
class NeuronaBynarium:
    def __init__(self, id, bits, valor_decimal=0, activacion=0, hi_score_activaciones=0, vida_util_restante=20):
        self.id = id
        self.tipo = id[:2] 
        self.bits = bits
        self.valor_decimal = valor_decimal
        
        # Calculate max_almacenamiento using the unified function
        self.max_almacenamiento = calcular_capacidad_almacenamiento(self.bits)
        
        self.activacion = activacion
        self.conectada_a = [] 
        self.conectada_desde = [] 
        
        self.hi_score_activaciones = hi_score_activaciones 
        
        # Life Utility: Now always 20 at start
        self.vida_util_restante = vida_util_restante # Initialized directly to 20

    def recibir_activacion(self, input_val=1):
        """
        Allows the neuron to receive activation.
        Handles special logic for Rol 1 (NOT gate).
        """
        # Special logic for Rol 1 (NOT Gate)
        if self.bits == 1:
            if input_val > 0:
                # If Rol 1 receives input, it gets 'blocked' or 'deactivated' from generating (activacion > 0)
                # For Bynarium, a Rol 1 with activacion > 0 means "do not generate 1"
                return True 
            #else:
                # If Rol 1 receives no input (input_val=0), it 'activates' to generate 1 (activacion = 0)
                #self.activacion = 0
            # Rol 1 does not accumulate HiScore in the same way as others, nor does it wear out from receiving input.
            # Its wear is only from its "infinite generation" when in the 0 state.
            #return True # Always successful in changing its state

        # Logic for other neurons
        if self.activacion < self.max_almacenamiento:
            self.activacion += input_val
            self.hi_score_activaciones += input_val
            # The life_util_restante wear is handled in the main loop when HS reaches MAX
            return True
        return False # Could not receive more activation

    def set_valor(self, valor):
        if 0 <= valor <= self.max_almacenamiento:
            self.valor_decimal = valor
            return True
        return False

    def conectar(self, otra_neurona):
        if otra_neurona not in self.conectada_a:
            self.conectada_a.append(otra_neurona)
            otra_neurona.conectada_desde.append(self) 
            return True
        return False 
    
    def desconectar(self, otra_neurona):
        if otra_neurona in self.conectada_a:
            self.conectada_a.remove(otra_neurona)
            otra_neurona.conectada_desde.remove(self)
            return True
        return False

    def __repr__(self):
        return f"Neurona(ID={self.id}, Tipo={self.tipo}, Bits={self.bits}, Valor={self.valor_decimal}, Act={self.activacion}, HiScore={self.hi_score_activaciones}, Vida={self.vida_util_restante})"

# --- FUNCTION TO CALCULATE NEURON COLOR BASED ON RULES ---
def get_neuron_color(bits):
    r, g, b = 0, 0, 0 

    # Base colors: even is red, odd is blue
    if bits % 2 == 0: # Even
        r = 255
        r = max(0, 255 - ((bits // 2) - 1) * 5)
    else: # Odd
        b = 255
        b = max(0, 255 - (((bits - 1) // 2) - 1) * 5)

    # Multiple of 3 is green (combines with base color)
    if bits % 3 == 0:
        g = 255 

    r = min(255, max(0, r))
    g = min(255, max(0, g))
    b = min(255, max(0, b))

    return (r, g, b)


# --- VISUAL REPRESENTATION IN PYGAME ---
class NeuronaVisual:
    def __init__(self, neurona, x, y, color_inactivo):
        self.neurona = neurona
        self.x = x
        self.y = y
        self.radio = neurona.bits * 7  
        self.color_inactivo = color_inactivo
        self.color_activo = VERDE # Color when active (>0 activation) and not at max
        self.color_valor = AZUL
        self.color_max_almacenamiento = PURPURA
        self.color_seleccion = AMARILLO 

        self.flash_start_time = 0
        self.flash_duration = 0.2
        self.flash_color = AMARILLO
        
    def trigger_flash(self): 
        self.flash_start_time = time.time()

    def dibujar(self, superficie, zoom, offset_x, offset_y, is_selected=False, is_dragging=False, is_delete_mode=False, is_rename_mode=False, is_disconnect_mode=False):
        current_time = time.time()
        is_flashing = (current_time - self.flash_start_time) < self.flash_duration

        color_base = self.color_inactivo
        
        # Color if neuron is about to wear out (High HiScore) - only for normal neurons
        if self.neurona.bits > 1 and self.neurona.hi_score_activaciones >= (self.neurona.max_almacenamiento * 0.7):
             color_base = NARANJA 
        
        # Color if life utility is very low - only for normal neurons
        if self.neurona.bits > 1 and self.neurona.vida_util_restante <= 5 and self.neurona.vida_util_restante > 0:
            color_base = ROJO 
        elif self.neurona.bits > 1 and self.neurona.vida_util_restante <= 0:
            color_base = NEGRO # Dead (if allowed to persist)

        # Color if active (has charge) - for roles > 1
        if self.neurona.bits > 1 and self.neurona.activacion > 0: 
            color_base = self.color_activo
        
        # Special color for Rol 1 (NOT gate)
        if self.neurona.bits == 1:
            if self.neurona.activacion == 0: # When Rol 1 has not received input, it's "active" (generating 1)
                color_base = VERDE # Distinct color for active NOT
            else: # When Rol 1 received input, it's "inactive" (not generating 1)
                color_base = GRIS # Distinct color for inactive NOT

        display_color = self.flash_color if is_flashing else color_base
        
        if is_delete_mode:
            display_color = ROJO 
        elif is_rename_mode: 
            display_color = PURPURA
        elif is_disconnect_mode: 
            display_color = CIAN


        # Apply zoom and offset for drawing
        draw_x = int((self.x + offset_x) * zoom)
        draw_y = int((self.y + offset_y) * zoom)
        scaled_radio = int(self.radio * zoom)


        pygame.draw.circle(superficie, display_color, (draw_x, draw_y), scaled_radio)
        pygame.draw.circle(superficie, NEGRO, (draw_x, draw_y), scaled_radio, 2) 

        if is_selected: 
            pygame.draw.circle(superficie, self.color_seleccion, (draw_x, draw_y), scaled_radio + int(5 * zoom), int(3 * zoom))
        if is_dragging: 
            pygame.draw.circle(superficie, CIAN, (draw_x, draw_y), scaled_radio + int(5 * zoom), int(3 * zoom))


        # Adjust font size with zoom, but within reasonable limits
        scaled_font_size = max(10, int(30 * zoom))
        scaled_font_pequena_size = max(8, int(20 * zoom))
        
        # Reload fonts for dynamic sizing
        dynamic_fuente = pygame.font.Font(None, scaled_font_size)
        dynamic_fuente_pequena = pygame.font.Font(None, scaled_font_pequena_size)


        texto_id = dynamic_fuente.render(self.neurona.id, True, NEGRO)
        texto_rect_id = texto_id.get_rect(center=(draw_x, draw_y - scaled_radio - int(20 * zoom)))
        superficie.blit(texto_id, texto_rect_id)

        texto_valor = dynamic_fuente_pequena.render(f"V:{self.neurona.valor_decimal}", True, self.color_valor)
        texto_rect_valor = texto_valor.get_rect(center=(draw_x, draw_y + scaled_radio + int(10 * zoom)))
        superficie.blit(texto_valor, texto_rect_valor)

        texto_activacion = dynamic_fuente_pequena.render(f"A:{self.neurona.activacion}", True, ROJO)
        texto_rect_activacion = texto_activacion.get_rect(center=(draw_x, draw_y + scaled_radio + int(25 * zoom)))
        superficie.blit(texto_activacion, texto_rect_activacion)

        texto_max = dynamic_fuente_pequena.render(f"M:{self.neurona.max_almacenamiento}", True, self.color_max_almacenamiento)
        texto_rect_max = texto_max.get_rect(center=(draw_x, draw_y + scaled_radio + int(40 * zoom)))
        superficie.blit(texto_max, texto_rect_max)

        texto_hi_score = dynamic_fuente_pequena.render(f"HS:{self.neurona.hi_score_activaciones}", True, NARANJA)
        texto_rect_hi_score = texto_hi_score.get_rect(center=(draw_x, draw_y + scaled_radio + int(55 * zoom)))
        superficie.blit(texto_hi_score, texto_rect_hi_score)

        texto_vida_util = dynamic_fuente_pequena.render(f"VU:{self.neurona.vida_util_restante}", True, CIAN) 
        texto_rect_vida_util = texto_vida_util.get_rect(center=(draw_x, draw_y + scaled_radio + int(70 * zoom))) 
        pantalla.blit(texto_vida_util, texto_rect_vida_util)


# --- INITIAL NEURON CREATION AND CONNECTION ---
neuronas = {}
neuronas_visuales = {}

def inicializar_red_predeterminada():
    global neuronas, neuronas_visuales
    neuronas.clear()
    neuronas_visuales.clear()

    # Adjusted to include a Rol 1 (NOT) for testing
    ns1 = NeuronaBynarium("NS1", 2) # Sensor
    ns2 = NeuronaBynarium("NS2", 2) # Sensor
    ns3 = NeuronaBynarium("NS3", 2) # Sensor
    
    # New Rol 1 for NOT gate
    not1 = NeuronaBynarium("NOT1", 1) 

    na1 = NeuronaBynarium("NA1", 3) # AND of 2 inputs
    na2 = NeuronaBynarium("NA2", 3) # AND of 2 inputs
    
    np1 = NeuronaBynarium("NP1", 4) # Integrator

    nm1 = NeuronaBynarium("NM1", 5) # Higher capacity
    nm2 = NeuronaBynarium("NM2", 6) # Higher capacity

    # High-role neuron to act as a "government"
    gov1 = NeuronaBynarium("GOV1", 10) 


    neuronas = {
        "NS1": ns1, "NS2": ns2, "NS3": ns3,
        "NOT1": not1,
        "NA1": na1, "NA2": na2,
        "NP1": np1,
        "NM1": nm1, "NM2": nm2,
        "GOV1": gov1
    }

    # Initial connections
    ns1.conectar(na1)
    ns2.conectar(na1)
    
    # Example XOR using NOT1 and NA1 (conceptual, not full setup here)
    # NS1 activates NOT1. If NS1 is ON, NOT1 is OFF (activacion=1). If NS1 is OFF, NOT1 is ON (activacion=0).
    ns1.conectar(not1) 
    not1.conectar(na2) # Output of NOT1 goes to NA2
    ns3.conectar(na2) # NS3 also goes to NA2 (for testing AND/XOR)

    na1.conectar(np1)
    na2.conectar(np1)

    na1.conectar(nm1)
    np1.conectar(nm1)

    ns1.conectar(nm2)
    ns2.conectar(nm2)
    ns3.conectar(nm2)
    
    # Connect governments to sensors or low-VU nodes
    gov1.conectar(ns1)
    gov1.conectar(na1)


    posiciones = {
        "NS1": (100, 100), "NS2": (100, 250), "NS3": (100, 400),
        "NOT1": (250, 100), # Position for the NOT gate
        "NA1": (400, 200), "NA2": (400, 350),
        "NP1": (600, 275),
        "NM1": (800, 200), "NM2": (800, 400),
        "GOV1": (800, 550) # Position of the government neuron
    }

    for id, pos in posiciones.items():
        neurona_obj = neuronas.get(id)
        initial_color = get_neuron_color(neurona_obj.bits)
        neuronas_visuales.update({id: NeuronaVisual(neurona_obj, pos[0], pos[1], initial_color)})

inicializar_red_predeterminada() 

# --- HELPER FUNCTIONS ---
def dibujar_tooltip(superficie, mouse_pos, neurona_visual_obj):
    tooltip_text = f"{neurona_visual_obj.neurona.id}: {NEURON_DESCRIPTIONS.get(neurona_visual_obj.neurona.tipo, 'Unknown')}"
    # The formula is generated using the new function for consistency
    if neurona_visual_obj.neurona.bits >= 1:
        tooltip_text += f"\nBits: {neurona_visual_obj.neurona.bits}"
        tooltip_text += f"\nMax Storage: {neurona_visual_obj.neurona.max_almacenamiento}"
        tooltip_text += f"\nFormula: {generar_sumatoria_str(neurona_visual_obj.neurona.bits)}"
        tooltip_text += f"\nFatigue (HS): {neurona_visual_obj.neurona.hi_score_activaciones}"
        tooltip_text += f"\nLife Utility (VU): {neurona_visual_obj.neurona.vida_util_restante}"


    lines = tooltip_text.split('\n')
    max_width = max(fuente_tooltip.render(line, True, BLANCO).get_width() for line in lines)
    
    padding = 10
    tooltip_width = max_width + 2 * padding
    tooltip_height = len(lines) * fuente_tooltip.get_height() + 2 * padding
    
    tooltip_x = mouse_pos[0] + 15
    tooltip_y = mouse_pos[1] - tooltip_height - 5
    
    if tooltip_x + tooltip_width > ANCHO_PANTALLA:
        tooltip_x = ANCHO_PANTALLA - tooltip_width - 5
    if tooltip_y < 0:
        tooltip_y = mouse_pos[1] + 15

    tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)
    
    pygame.draw.rect(superficie, NEGRO, tooltip_rect, 0, 5)
    pygame.draw.rect(superficie, GRIS, tooltip_rect, 2, 5)
    
    for i, line in enumerate(lines):
        text_surface = fuente_tooltip.render(line, True, BLANCO)
        superficie.blit(text_surface, (tooltip_x + padding, tooltip_y + padding + i * fuente_tooltip.get_height()))

# --- SAVE AND LOAD FUNCTIONS ---
# Absolute path for save directory
SAVE_DIR = r"C:\BynariumData\bynarium_saves" # Use r"" for raw string to avoid backslash issues
SAVE_FILENAME = "red_bynarium.json"
FULL_SAVE_PATH = os.path.join(SAVE_DIR, SAVE_FILENAME)

# --- START DEBUGGING ---
print(f"DEBUG: SCRIPT_DIR: {os.path.dirname(os.path.abspath(__file__))}") 
print(f"DEBUG: CURRENT_WORKING_DIR: {os.getcwd()}")
print(f"DEBUG: SAVE_DIR: {SAVE_DIR}")
print(f"DEBUG: FULL_SAVE_PATH: {FULL_SAVE_PATH}")
# --- END DEBUGGING ---

def guardar_red():
    # Step 1: Ensure save folder exists
    try:
        print(f"DEBUG: Checking/Creating directory: '{SAVE_DIR}'")
        os.makedirs(SAVE_DIR, exist_ok=True)
        print(f"DEBUG: Directory '{SAVE_DIR}' exists or was created successfully.")
        
        # Add a small delay to ensure file system is ready
        time.sleep(0.1) 
        
        # Verify again if directory exists and is a directory
        if not os.path.isdir(SAVE_DIR):
            error_msg = f"CRITICAL ERROR: Directory '{SAVE_DIR}' not found or is not a valid directory after creation."
            print(error_msg)
            return False, f"Error verifying save folder."

    except Exception as e:
        error_msg = f"CRITICAL ERROR: Failed to ensure/create directory '{SAVE_DIR}': {e}"
        print(error_msg)
        return False, f"Error preparing save: {e}"
    
    # Step 2: Prepare data to save
    data_to_save = []
    for id, neurona_obj in neuronas.items():
        visual_obj = neuronas_visuales.get(id)
        if visual_obj:
            connected_to_ids = [n.id for n in neurona_obj.conectada_a]
            
            data_to_save.append({
                "id": neurona_obj.id,
                "bits": neurona_obj.bits,
                "valor_decimal": neurona_obj.valor_decimal,
                "activacion": neurona_obj.activacion,
                "hi_score_activaciones": neurona_obj.hi_score_activaciones,
                "vida_util_restante": neurona_obj.vida_util_restante,
                "pos_x": visual_obj.x,
                "pos_y": visual_obj.y,
                "conectada_a_ids": connected_to_ids 
            })
    
    # Step 3: Attempt to save the file
    try:
        print(f"Attempting to save file to '{FULL_SAVE_PATH}'...")
        with open(FULL_SAVE_PATH, 'w') as f:
            json.dump(data_to_save, f, indent=4)
        print(f"Success: Network saved to '{FULL_SAVE_PATH}'.")
        return True, f"Network saved to '{os.path.basename(SAVE_FILENAME)}'." 
    except Exception as e:
        error_msg = f"ERROR: Failed to save file to '{FULL_SAVE_PATH}': {e}"
        print(error_msg)
        return False, f"Error saving: {e}"

def cargar_red():
    global neuronas, neuronas_visuales, zoom_level, offset_x, offset_y # Reset zoom/pan on load
    
    print(f"DEBUG: Attempting to load from '{FULL_SAVE_PATH}'. Checking existence...")
    if not os.path.exists(FULL_SAVE_PATH):
        print(f"ERROR: Save file not found at '{FULL_SAVE_PATH}'.")
        return False, f"Error: '{os.path.basename(SAVE_FILENAME)}' not found."

    try:
        print(f"DEBUG: File '{FULL_SAVE_PATH}' found. Reading...")
        with open(FULL_SAVE_PATH, 'r') as f:
            loaded_data = json.load(f)
        
        neuronas.clear()
        neuronas_visuales.clear()

        temp_neuronas_by_id = {}
        temp_visuals_by_id = {}

        for item in loaded_data:
            neurona_obj = NeuronaBynarium(
                item["id"], 
                item["bits"], 
                item["valor_decimal"], 
                item["activacion"], 
                item["hi_score_activaciones"],
                item["vida_util_restante"] 
            )
            temp_neuronas_by_id[neurona_obj.id] = neurona_obj
            neuronas[neurona_obj.id] = neurona_obj 

            initial_color = get_neuron_color(neurona_obj.bits)
            visual_obj = NeuronaVisual(neurona_obj, item["pos_x"], item["pos_y"], initial_color)
            temp_visuals_by_id[neurona_obj.id] = visual_obj
            neuronas_visuales[neurona_obj.id] = visual_obj 

        for item in loaded_data:
            origen_id = item["id"]
            neurona_origen = temp_neuronas_by_id[origen_id]
            
            for destino_id in item["conectada_a_ids"]:
                if destino_id in temp_neuronas_by_id:
                    neurona_destino = temp_neuronas_by_id[destino_id]
                    neurona_origen.conectar(neurona_destino)
                else:
                    print(f"Warning: Destination neuron '{destino_id}' for '{origen_id}' not found while loading.")
        
        # Reset zoom and pan when loading a new network
        zoom_level = 1.0
        offset_x = 0
        offset_y = 0

        print(f"Success: Network loaded from '{FULL_SAVE_PATH}'.")
        return True, f"Network loaded from '{os.path.basename(SAVE_FILENAME)}'."
    except json.JSONDecodeError:
        print(f"ERROR: Invalid JSON file: '{FULL_SAVE_PATH}'.")
        return False, f"Error: File '{os.path.basename(SAVE_FILENAME)}' is not valid JSON."
    except Exception as e:
        print(f"ERROR: Failed to load network: {e}") 
        return False, f"Error loading: {e}"

# --- CONNECTION INTERACTION ---
first_clicked_neuron_visual = None
modo_conexion_activo = False
modo_conexion_tipo = "bidireccional"  
modo_eliminar_activo = False
modo_desconectar_activo = False 
activation_mode_active = False 
connection_message_display_time = 0
CONNECTION_MESSAGE_DURATION = 2 

# --- RENAME NEURON FUNCTIONALITY ---
modo_renombrar_activo = False
selected_neuron_for_rename_visual = None
rename_input_active = False
rename_input_text = ""
rename_input_rect = None # Will be set dynamically

# Temporary screen messages
message_display_time = 0
current_message = ""
MESSAGE_DEFAULT_DURATION = 3 
MESSAGE_CRITICAL_DURATION = 5 

def set_message(message, duration=MESSAGE_DEFAULT_DURATION):
    global current_message, message_display_time
    current_message = message
    message_display_time = time.time() + duration

# --- DRAG NEURON FUNCTIONALITY ---
dragging_neuron_visual = None
drag_offset_x, drag_offset_y = 0, 0 

# --- NEURON CREATOR ---
input_name_rect = pygame.Rect(ANCHO_PANTALLA // 2 - 100, ALTO_PANTALLA // 2 - 100, 200, 40)
input_name_text = "" 
active_input_name_box = False

input_bits_rect = pygame.Rect(ANCHO_PANTALLA // 2 - 100, ALTO_PANTALLA // 2 - 50, 200, 40) 
input_bits_text = '2' 
active_input_bits_box = False 

create_button_rect = pygame.Rect(ANCHO_PANTALLA // 2 - 75, ALTO_PANTALLA // 2 + 10, 150, 50) 
back_button_rect = pygame.Rect(50, 50, 100, 40) 

neuronas_a_eliminar = []

# --- MAIN PYGAME LOOP ---
running = True
while running:
    neuronas_a_eliminar = [] 

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_screen == SCREEN_NETWORK:
            # --- MOUSE EVENT HANDLING IN NETWORK SCREEN ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    # Priority 1: UI control buttons (not affected by zoom/pan)
                    eliminar_button_rect = pygame.Rect(ANCHO_PANTALLA - 200, ALTO_PANTALLA - 70, 50, 50)
                    conexion_button_rect = pygame.Rect(ANCHO_PANTALLA - 140, ALTO_PANTALLA - 70, 50, 50)
                    rename_button_rect = pygame.Rect(ANCHO_PANTALLA - 260, ALTO_PANTALLA - 70, 50, 50)
                    disconnect_button_rect = pygame.Rect(ANCHO_PANTALLA - 320, ALTO_PANTALLA - 70, 50, 50) 
                    activate_nodes_button_rect = pygame.Rect(ANCHO_PANTALLA - 420, ALTO_PANTALLA - 70, 100, 50) 
                    save_button_rect = pygame.Rect(ANCHO_PANTALLA - 480, ALTO_PANTALLA - 70, 50, 50) 
                    load_button_rect = pygame.Rect(ANCHO_PANTALLA - 540, ALTO_PANTALLA - 70, 50, 50) 
                    plus_button_rect = pygame.Rect(ANCHO_PANTALLA - 70, ALTO_PANTALLA - 70, 50, 50)

                    # Check click on control buttons
                    if eliminar_button_rect.collidepoint(event.pos):
                        modo_eliminar_activo = not modo_eliminar_activo 
                        # Deactivate all other modes when activating a new one
                        activation_mode_active = False ; modo_conexion_activo = False ; modo_renombrar_activo = False; modo_desconectar_activo = False
                        rename_input_active = False; selected_neuron_for_rename_visual = None; first_clicked_neuron_visual = None
                        connection_message_display_time = 0
                        set_message(f"Delete mode {'activated' if modo_eliminar_activo else 'deactivated'}.")
                        continue
                    elif conexion_button_rect.collidepoint(event.pos):
                        modo_conexion_activo = not modo_conexion_activo
                        activation_mode_active = False ; modo_eliminar_activo = False ; modo_renombrar_activo = False; modo_desconectar_activo = False
                        rename_input_active = False; selected_neuron_for_rename_visual = None; first_clicked_neuron_visual = None
                        connection_message_display_time = 0
                        set_message(f"Connection mode {'activated' if modo_conexion_activo else 'deactivated'}.")
                        continue
                    elif rename_button_rect.collidepoint(event.pos):
                        modo_renombrar_activo = not modo_renombrar_activo
                        activation_mode_active = False; modo_conexion_activo = False; modo_eliminar_activo = False; modo_desconectar_activo = False
                        if not modo_renombrar_activo: 
                            rename_input_active = False; selected_neuron_for_rename_visual = None; rename_input_text = ""
                        set_message(f"Rename mode {'activated' if modo_renombrar_activo else 'deactivated'}.")
                        continue
                    elif disconnect_button_rect.collidepoint(event.pos):
                        modo_desconectar_activo = not modo_desconectar_activo
                        activation_mode_active = False; modo_conexion_activo = False; modo_eliminar_activo = False; modo_renombrar_activo = False
                        first_clicked_neuron_visual = None 
                        set_message(f"Disconnect mode {'activated' if modo_desconectar_activo else 'deactivated'}.")
                        continue
                    elif activate_nodes_button_rect.collidepoint(event.pos):
                        activation_mode_active = not activation_mode_active
                        modo_conexion_activo = False ; modo_eliminar_activo = False ; modo_renombrar_activo = False; modo_desconectar_activo = False
                        rename_input_active = False; selected_neuron_for_rename_visual = None; first_clicked_neuron_visual = None
                        connection_message_display_time = 0
                        set_message(f"Node activation mode {'activated' if activation_mode_active else 'deactivated'}.")
                        continue
                    elif save_button_rect.collidepoint(event.pos):
                        success, msg = guardar_red()
                        set_message(msg, duration=MESSAGE_CRITICAL_DURATION) 
                        continue
                    elif load_button_rect.collidepoint(event.pos):
                        success, msg = cargar_red()
                        set_message(msg, duration=MESSAGE_CRITICAL_DURATION) 
                        if success: 
                            modo_conexion_activo = False; modo_eliminar_activo = False; activation_mode_active = False
                            modo_renombrar_activo = False; modo_desconectar_activo = False
                            rename_input_active = False; selected_neuron_for_rename_visual = None
                            first_clicked_neuron_visual = None; dragging_neuron_visual = None
                        continue
                    elif plus_button_rect.collidepoint(event.pos):
                        current_screen = SCREEN_CREATOR
                        input_name_text = ""; active_input_name_box = False
                        input_bits_text = '2'; active_input_bits_box = False
                        first_clicked_neuron_visual = None ; connection_message_display_time = 0
                        dragging_neuron_visual = None 
                        modo_conexion_activo = False ; modo_eliminar_activo = False
                        activation_mode_active = False; modo_renombrar_activo = False ; modo_desconectar_activo = False
                        rename_input_active = False; selected_neuron_for_rename_visual = None
                        set_message("Creator mode activated.")
                        continue

                    # Priority 2: Neuron Interaction or Panning with left click
                    # Convert mouse coordinates to "world" coordinates (affected by zoom and pan)
                    transformed_mouse_x = (mouse_x / zoom_level) - offset_x
                    transformed_mouse_y = (mouse_y / zoom_level) - offset_y

                    clicked_on_neuron = False
                    for visual_neurona in list(neuronas_visuales.values()): 
                        dist_a_neurona = math.hypot(transformed_mouse_x - visual_neurona.x, transformed_mouse_y - visual_neurona.y)
                        if dist_a_neurona <= visual_neurona.radio: 
                            clicked_on_neuron = True
                            if modo_renombrar_activo:
                                selected_neuron_for_rename_visual = visual_neurona
                                rename_input_active = True
                                rename_input_text = visual_neurona.neurona.id
                                rename_input_rect = pygame.Rect(visual_neurona.x * zoom_level + offset_x * zoom_level - 75, 
                                                                visual_neurona.y * zoom_level + offset_y * zoom_level - visual_neurona.radio * zoom_level - 50, 
                                                                150, 30)
                                set_message(f"Selected '{visual_neurona.neurona.id}' for renaming.")
                                break 
                            elif modo_eliminar_activo:
                                id_a_borrar = visual_neurona.neurona.id
                                if id_a_borrar in neuronas:
                                    neuronas_a_eliminar.append(id_a_borrar) 
                                    set_message(f"Neuron '{id_a_borrar}' marked for deletion.", duration=1.5)
                                    break
                            elif modo_desconectar_activo: 
                                if first_clicked_neuron_visual is None:
                                    first_clicked_neuron_visual = visual_neurona
                                    set_message(f"Neuron '{visual_neurona.neurona.id}' selected for disconnection.")
                                elif first_clicked_neuron_visual.neurona.id == visual_neurona.neurona.id:
                                    first_clicked_neuron_visual = None
                                    set_message("Disconnection selection cancelled.")
                                else:
                                    origen_desc = first_clicked_neuron_visual.neurona
                                    destino_desc = visual_neurona.neurona
                                    # Try disconnecting in both directions
                                    disconnected = False
                                    if destino_desc in origen_desc.conectada_a:
                                        origen_desc.desconectar(destino_desc)
                                        disconnected = True
                                    if origen_desc in destino_desc.conectada_a: 
                                        destino_desc.desconectar(origen_desc)
                                        disconnected = True
                                    
                                    if disconnected:
                                        set_message(f"Disconnected: {origen_desc.id} ⟷ {destino_desc.id}")
                                    else:
                                        set_message(f"No connection between {origen_desc.id} and {destino_desc.id}", duration=2)
                                    first_clicked_neuron_visual = None
                                    modo_desconectar_activo = False 
                                break
                            elif activation_mode_active:
                                if visual_neurona.neurona.bits == 1: # Special logic for Rol 1 (NOT)
                                    if visual_neurona.neurona.activacion == 0: # If it's currently generating '1' (no input)
                                        visual_neurona.neurona.recibir_activacion(1) # Simulate receiving an input to stop it
                                        set_message(f"'{visual_neurona.neurona.id}' (NOT) received input. Act: {visual_neurona.neurona.activacion}", duration=1.5)
                                    else: # If it's currently blocked (received input)
                                        visual_neurona.neurona.recibir_activacion(0) # Simulate removing input
                                        set_message(f"'{visual_neurona.neurona.id}' (NOT) without input. Act: {visual_neurona.neurona.activacion}", duration=1.5)
                                else: # Normal neuron activation
                                    if visual_neurona.neurona.recibir_activacion():
                                        visual_neurona.trigger_flash()
                                        set_message(f"'{visual_neurona.neurona.id}' activated. Act: {visual_neurona.neurona.activacion}", duration=1.5)
                                    else:
                                        set_message(f"'{visual_neurona.neurona.id}' already at max activation.", duration=1.5)
                                break 
                            elif modo_conexion_activo:
                                if first_clicked_neuron_visual is None:
                                    first_clicked_neuron_visual = visual_neurona
                                    connection_message_display_time = time.time()
                                    set_message(f"Neuron '{visual_neurona.neurona.id}' selected for connection.")
                                elif first_clicked_neuron_visual.neurona.id == visual_neurona.neurona.id:
                                    first_clicked_neuron_visual = None
                                    connection_message_display_time = 0
                                    set_message("Connection selection cancelled.")
                                else:
                                    origen = first_clicked_neuron_visual.neurona
                                    destino = visual_neurona.neurona
                                    if modo_conexion_tipo == "bidireccional":
                                        origen.conectar(destino)
                                        destino.conectar(origen)
                                        set_message(f"Bidirectional connection: {origen.id} ⇆ {destino.id}")
                                    elif modo_conexion_tipo == "salida":
                                        origen.conectar(destino)
                                        set_message(f"Output connection: {origen.id} → {destino.id}")
                                    elif modo_conexion_tipo == "entrada":
                                        destino.conectar(origen)
                                        set_message(f"Input connection: {destino.id} ← {origen.id}")
                                    first_clicked_neuron_visual = None
                                    connection_message_display_time = 0
                            else:
                                # Normal mode: drag neuron
                                dragging_neuron_visual = visual_neurona
                                drag_offset_x = transformed_mouse_x - visual_neurona.x
                                drag_offset_y = transformed_mouse_y - visual_neurona.y
                                first_clicked_neuron_visual = None  
                                connection_message_display_time = 0
                                panning_active = False # Ensure panning is not active if dragging a neuron
                            break 

                    # If click was not on a neuron NOR on a UI button, start panning with left click
                    if not clicked_on_neuron:
                        if first_clicked_neuron_visual is not None and dragging_neuron_visual is None:
                            first_clicked_neuron_visual = None
                            set_message("Connection/disconnection selection cancelled (clicked outside).")
                        if modo_renombrar_activo and rename_input_active:
                            if rename_input_rect and not rename_input_rect.collidepoint(event.pos):
                                rename_input_active = False
                                selected_neuron_for_rename_visual = None
                                rename_input_text = ""
                                set_message("Rename cancelled (clicked outside).", duration=1.5)
                        
                        # Start panning with left click if nothing else was interacted with
                        if not modo_eliminar_activo and not modo_desconectar_activo and \
                           not activation_mode_active and not modo_conexion_activo and \
                           not modo_renombrar_activo and not dragging_neuron_visual:
                            panning_active = True
                            pan_start_mouse_x, pan_start_mouse_y = event.pos
                            pan_start_offset_x, pan_start_offset_y = offset_x, offset_y

                elif event.button == 2: # Middle mouse click for panning (existing)
                    panning_active = True
                    pan_start_mouse_x, pan_start_mouse_y = event.pos
                    pan_start_offset_x, pan_start_offset_y = offset_x, offset_y

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 or event.button == 2: # Any button up stops dragging or panning
                    dragging_neuron_visual = None
                    panning_active = False

            elif event.type == pygame.MOUSEMOTION:
                if dragging_neuron_visual:
                    transformed_mouse_x = (mouse_x / zoom_level) - offset_x
                    transformed_mouse_y = (mouse_y / zoom_level) - offset_y
                    dragging_neuron_visual.x = transformed_mouse_x - drag_offset_x
                    dragging_neuron_visual.y = transformed_mouse_y - drag_offset_y
                elif panning_active:
                    dx = (mouse_x - pan_start_mouse_x) / zoom_level
                    dy = (mouse_y - pan_start_mouse_y) / zoom_level
                    offset_x = pan_start_offset_x + dx
                    offset_y = pan_start_offset_y + dy
            
            elif event.type == pygame.MOUSEWHEEL:
                zoom_factor = 1.1 if event.y > 0 else 1 / 1.1 
                
                world_x_before_zoom = (mouse_x / zoom_level) - offset_x
                world_y_before_zoom = (mouse_y / zoom_level) - offset_y

                zoom_level = max(0.2, min(5.0, zoom_level * zoom_factor)) 

                offset_x = (mouse_x / zoom_level) - world_x_before_zoom
                offset_y = (mouse_y / zoom_level) - world_y_before_zoom
                
                set_message(f"Zoom: {zoom_level:.2f}x", duration=1)

            # Keyboard handling for renaming
            if event.type == pygame.KEYDOWN:
                if rename_input_active:
                    if event.key == pygame.K_RETURN:
                        old_id = selected_neuron_for_rename_visual.neurona.id
                        new_id = rename_input_text.strip() 

                        if not new_id:
                            set_message("Error: Name cannot be empty.", duration=2)
                        elif new_id == old_id:
                            set_message("No name changes were made.", duration=1.5)
                        else:
                            is_unique = True
                            for neuron_key, _ in neuronas.items():
                                if neuron_key.lower() == new_id.lower() and neuron_key != old_id: 
                                    is_unique = False
                                    break
                            
                            if not is_unique:
                                set_message(f"Error: Name '{new_id}' is already in use.", duration=2)
                            else:
                                try:
                                    selected_neuron_for_rename_visual.neurona.id = new_id
                                  
                                    
                                    new_neuronas = {}
                                    for neuron_key, neuron_obj in neuronas.items():
                                        if neuron_key == old_id:
                                            new_neuronas[new_id] = neuron_obj
                                        else:
                                            new_neuronas[neuron_key] = neuron_obj
                                    neuronas = new_neuronas

                                    new_neuronas_visuales = {}
                                    for visual_key, visual_obj in neuronas_visuales.items():
                                        if visual_key == old_id:
                                            new_neuronas_visuales[new_id] = visual_obj
                                        else:
                                            new_neuronas_visuales[visual_key] = visual_obj
                                    neuronas_visuales = new_neuronas_visuales

                                    # Update connections to use new ID references
                                    for neuron_obj in neuronas.values():
                                        neuron_obj.conectada_a = [
                                            (neuronas[new_id] if n.id == old_id else n) 
                                            for n in neuron_obj.conectada_a
                                        ]
                                        neuron_obj.conectada_desde = [
                                            (neuronas[new_id] if n.id == old_id else n) 
                                            for n in neuron_obj.conectada_desde
                                        ]

                                    set_message(f"Neuron '{old_id}' renamed to '{new_id}'.", duration=2)
                                except Exception as e:
                                    set_message(f"Error renaming: {e}", duration=3)
                        
                        rename_input_active = False
                        selected_neuron_for_rename_visual = None
                        rename_input_text = ""
                        modo_renombrar_activo = False 
                    
                    elif event.key == pygame.K_BACKSPACE:
                        rename_input_text = rename_input_text[:-1]
                    else:
                        if len(rename_input_text) < 20: 
                            rename_input_text += event.unicode
                
                # Other keyboard shortcuts (outside rename mode or active input)
                if not rename_input_active:
                    if event.key == pygame.K_TAB:
                        if modo_conexion_activo: 
                            if modo_conexion_tipo == "bidireccional":
                                modo_conexion_tipo = "salida"
                            elif modo_conexion_tipo == "salida":
                                modo_conexion_tipo = "entrada"
                            elif modo_conexion_tipo == "entrada":
                                modo_conexion_tipo = "bidireccional"
                            set_message(f"Connection type changed to: {modo_conexion_tipo}")
                    
                    if event.key == pygame.K_SPACE:
                        # Activate Rol 2 neurons (Sensors)
                        set_message("Activating Rol 2 neurons...", duration=1) 
                        for id, neurona_obj in list(neuronas.items()): 
                            if neurona_obj.bits == 2: # Rol 2 are sensors
                                if neurona_obj.recibir_activacion(): # Just receive 1 activation
                                    neuronas_visuales[id].trigger_flash()
                                else:
                                    set_message(f"'{id}' already at max.", duration=1.5)

                    if event.key == pygame.K_a: 
                        if neuronas: 
                            random_ns = random.choice(list(neuronas.values()))
                            # Rol 1 special activation based on user input for 'a' (toggle)
                            if random_ns.bits == 1:
                                if random_ns.activacion == 0: # If currently 'active' (no input)
                                    random_ns.recibir_activacion(1) # Simulate input
                                    set_message(f"'{random_ns.id}' (NOT) received input by 'A'.", duration=1.5)
                                else: # If currently 'inactive' (received input)
                                    random_ns.recibir_activacion(0) # Simulate removing input
                                    set_message(f"'{random_ns.id}' (NOT) without input by 'A'.", duration=1.5)
                            else: # Normal neuron activation
                                if random_ns.recibir_activacion():
                                    neuronas_visuales[random_ns.id].trigger_flash()
                                    set_message(f"'{random_ns.id}' activated by 'A'.", duration=1.5)
                                else:
                                    set_message(f"'{random_ns.id}' already at max.", duration=1.5)
                        else:
                            set_message("No neurons to activate.", duration=1.5)

                    if event.key == pygame.K_v:
                        for neurona_obj in neuronas.values():
                            if neurona_obj.bits == 1: # Rol 1 doesn't store decimal value
                                neurona_obj.valor_decimal = 0
                            else:
                                random_val = random.randint(0, neurona_obj.max_almacenamiento) 
                                if neurona_obj.set_valor(random_val):
                                    neuronas_visuales[neurona_obj.id].trigger_flash()
                        set_message("Neuron values set randomly.", duration=1.5)

                    if event.key == pygame.K_c:
                        set_message("Propagation and traffic management...", duration=1)
                        neurons_to_propagate_this_cycle = []
                        
                        # Collect neurons ready to propagate
                        for n in neuronas.values():
                            if n.bits == 1: # Rol 1 (NOT)
                                n.inputs_recibidos_este_ciclo = 0
                                if n.activacion == 0: # If Rol 1 is in its 'active' (generating 1) state
                                    neurons_to_propagate_this_cycle.append(n)
                            elif n.activacion == n.max_almacenamiento and n.max_almacenamiento > 0: # Normal full neuron
                                neurons_to_propagate_this_cycle.append(n)

                        propagated_any = False
                        
                        # --- GOVERNMENT HEALING LOGIC (before general propagation) ---
                        # High-bit neurons (governors) try to heal
                        GOVERNOR_THRESHOLD_BITS = 10 # Example threshold for a "governor" neuron
                        VULNERABLE_VU_THRESHOLD = 5 # VU below this is vulnerable
                        VULNERABLE_HS_THRESHOLD_FACTOR = 0.5 # HS > this factor of max_almacenamiento is considered high

                        governors_ready_to_heal = []
                        for n in neuronas.values():
                            # Governor must be a high-bit neuron AND be at max activation to perform healing
                            if n.bits >= GOVERNOR_THRESHOLD_BITS and n.activacion >= n.max_almacenamiento and n.max_almacenamiento > 0:
                                governors_ready_to_heal.append(n)
                        
                        for governor in governors_ready_to_heal:
                            vulnerable_neurons = []
                            for target_n in neuronas.values():
                                if target_n.id == governor.id: continue # A neuron cannot heal itself
                                # A neuron is vulnerable if low VU AND high HS AND it's not a Rol 1 (Rol 1 has different VU/HS rules)
                                if target_n.vida_util_restante <= VULNERABLE_VU_THRESHOLD and \
                                   target_n.hi_score_activaciones > (target_n.max_almacenamiento * VULNERABLE_HS_THRESHOLD_FACTOR) and \
                                   target_n.bits > 1: # Rol 1s are handled differently for VU/HS
                                   vulnerable_neurons.append(target_n)
                            
                            if vulnerable_neurons:
                                # Prioritize connection based on some criteria (e.g., lowest VU, then highest HS)
                                vulnerable_neurons.sort(key=lambda x: (x.vida_util_restante, -x.hi_score_activaciones)) 
                                selected_vulnerable = vulnerable_neurons[0]

                                # Perform healing (connection + reset VU/HS)
                                # Ensure bidirectional connection for healing effect, if not already connected
                                if not governor.conectar(selected_vulnerable):
                                    pass # Already connected, no need to establish new link
                                selected_vulnerable.conectar(governor) # Ensure bidirectional
                                
                                governor.vida_util_restante = 20
                                governor.hi_score_activaciones = 0
                                selected_vulnerable.vida_util_restante = 20
                                selected_vulnerable.hi_score_activaciones = 0
                                governor.activacion = governor.activacion / 2 # Governor resets its activation after performing healing

                                neuronas_visuales[governor.id].trigger_flash()
                                neuronas_visuales[selected_vulnerable.id].trigger_flash()
                                set_message(f"'{governor.id}' (GOV) healed '{selected_vulnerable.id}' (VU/HS reset).", duration=2)
                                propagated_any = True # Indicate some action happened
                                break # Governor only heals one neuron per cycle, then its activacion is reset

                        # --- GENERAL PROPAGATION LOGIC ---
                        for neurona_origen in neurons_to_propagate_this_cycle:
                            if neurona_origen.id not in neuronas: continue # Skip if deleted by healing above
                            
                            neuronas_visuales[neurona_origen.id].trigger_flash() 
                            
                            # Destinations need to be able to receive activation and not be source itself
                            potential_destinations = [
                                n for n in neurona_origen.conectada_a
                                if n.activacion < n.max_almacenamiento and n.id in neuronas and n.id != neurona_origen.id
                            ]
                            
                            # Prioritize destinations with low VU and high HS for traffic management
                            potential_destinations.sort(key=lambda n: (n.vida_util_restante, -n.hi_score_activaciones))

                            # Handle Rol 1 (NOT) propagation
                            if neurona_origen.bits == 1:
                                if neurona_origen.activacion == 0: # Rol 1 is in active state (no input), generates '1'
                                    for destino_neurona in potential_destinations:
                                        if destino_neurona.recibir_activacion(1): # Propagate '1'
                                            neuronas_visuales[destino_neurona.id].trigger_flash()
                                            set_message(f"NOT Propagation: {neurona_origen.id} -> {destino_neurona.id}", duration=0.5)
                                            propagated_any = True
                                else: # Rol 1 is in inactive state (received input), generates '0'
                                    # User wants it to consume input and effectively generate 0, so no propagation.
                                    # We reset its activacion here so it goes back to default 'generating 1' if input is removed.
                                    neurona_origen.activacion = 0
                            else: # Normal neuron propagation
                                # Propagate to ALL connected destinations if source has enough activation
                                initial_activation = neurona_origen.activacion
                                for destino_neurona in potential_destinations:
                                    if neurona_origen.activacion > 0: # Check if source still has activation
                                        if destino_neurona.recibir_activacion(1):
                                            neuronas_visuales[destino_neurona.id].trigger_flash()
                                            set_message(f"Propagation: {neurona_origen.id} -> {destino_neurona.id}", duration=0.5)
                                            neurona_origen.activacion -= 1 # Decrement for each successful propagation
                                            propagated_any = True
                                    else:
                                        break # Source exhausted its activation

                                # Reset any remaining activation if not fully depleted
                                #if neurona_origen.activacion > 0:
                                    #neurona_origen.activacion = 0
                            
                        if not propagated_any and not governors_ready_to_heal: 
                            set_message("No full neurons to propagate, nor governors to heal.", duration=2)
                    
                    if event.key == pygame.K_r:
                        for neurona_obj in neuronas.values():
                            neurona_obj.activacion = 0
                            neurona_obj.valor_decimal = 0
                            neurona_obj.hi_score_activaciones = 0
                            neurona_obj.vida_util_restante = 20 # Reset to 20
                            neuronas_visuales[neurona_obj.id].trigger_flash()
                        set_message("Network reset.", duration=1.5)

        elif current_screen == SCREEN_CREATOR:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if back_button_rect.collidepoint(event.pos):
                        current_screen = SCREEN_NETWORK
                        set_message("Returning to network.", duration=1.5)
                        continue
                    
                    if input_name_rect.collidepoint(event.pos):
                        active_input_name_box = True
                        active_input_bits_box = False 
                    elif input_bits_rect.collidepoint(event.pos):
                        active_input_bits_box = True
                        active_input_name_box = False 
                    else:
                        active_input_name_box = False
                        active_input_bits_box = False
                    
                    if create_button_rect.collidepoint(event.pos):
                        new_id = input_name_text.strip()
                        try:
                            new_bits = int(input_bits_text)
                            
                            if not new_id:
                                set_message("Error: Neuron name cannot be empty.", duration=2)
                            elif new_bits < 1:
                                set_message("Error: NB must be >= 1.", duration=2)
                            else:
                                is_unique = True
                                for neuron_key in neuronas.keys():
                                    if neuron_key.lower() == new_id.lower():
                                        is_unique = False
                                        break
                                
                                if not is_unique:
                                    set_message(f"Error: Neuron '{new_id}' already exists.", duration=2)
                                else:
                                    new_neuron_bynarium = NeuronaBynarium(new_id, new_bits)
                                    neuronas[new_id] = new_neuron_bynarium

                                    new_neuron_color = get_neuron_color(new_bits)

                                    new_x = ANCHO_PANTALLA // 2
                                    new_y = ALTO_PANTALLA // 2

                                    new_neuron_visual = NeuronaVisual(new_neuron_bynarium, new_x, new_y, new_neuron_color)
                                    neuronas_visuales[new_id] = new_neuron_visual
                                    
                                    set_message(f"Neuron '{new_id}' created (NB: {new_bits}).", duration=2)
                                    input_name_text = "" 
                                    input_bits_text = '2' 
                                    current_screen = SCREEN_NETWORK 

                        except ValueError:
                            set_message("Error: Enter a valid number for Bits.", duration=2)

            if event.type == pygame.KEYDOWN:
                if active_input_name_box:
                    if event.key == pygame.K_RETURN:
                        active_input_name_box = False
                        active_input_bits_box = True 
                    elif event.key == pygame.K_BACKSPACE:
                        input_name_text = input_name_text[:-1]
                    else:
                        if len(input_name_text) < 20: 
                            input_name_text += event.unicode
                elif active_input_bits_box: 
                    if event.key == pygame.K_RETURN:
                        active_input_bits_box = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_bits_text = input_bits_text[:-1]
                    else:
                        if event.unicode.isdigit() and len(input_bits_text) < 3: 
                            input_bits_text += event.unicode


    # --- AUTO-AGING AND AUTOMATIC CONNECTION LOGIC (Fatigue) ---
    for id_origen, neurona_origen in list(neuronas.items()): 
        if id_origen in neuronas_a_eliminar:
            continue
        
        # Only normal neurons (not Rol 1) undergo this specific HS based aging
        if neurona_origen.bits > 1:
            if neurona_origen.hi_score_activaciones >= neurona_origen.max_almacenamiento:
                neurona_origen.vida_util_restante -= 1
                neurona_origen.hi_score_activaciones = 0 # Reset HS after a cycle of aging
                
                set_message(f"'{id_origen}' reached fatigue. VU: {neurona_origen.vida_util_restante}", duration=1.5)

                if neurona_origen.vida_util_restante <= 0:
                    # Explicitly mark for deletion when VU runs out
                    if id_origen not in neuronas_a_eliminar: 
                        neuronas_a_eliminar.append(id_origen)
                        set_message(f"'{id_origen}' ran out of life utility and will disappear.", duration=1.5)
                else:
                    neuronas_visuales[id_origen].trigger_flash()


        # Automatic connection for overloaded neurons (HS high, not necessarily VU low)
        # This is for "traffic management" - forming more connections to resist traffic
        if neurona_origen.bits > 1 and neurona_origen.hi_score_activaciones >= (neurona_origen.max_almacenamiento * 0.9): 
            # Find a neuron that is NOT connected to and is not about to be deleted
            neuronas_sueltas_para_conexion = [
                n for n in neuronas.values() 
                if n.id != neurona_origen.id 
                and n not in neurona_origen.conectada_a
                and n.id not in neuronas_a_eliminar 
                and n.bits > 1 # Don't auto-connect to Rol 1 (unless explicitly designed)
            ]
            if neuronas_sueltas_para_conexion:
                # Prioritize connecting to less used or more 'available' neurons
                neuronas_sueltas_para_conexion.sort(key=lambda x: x.hi_score_activaciones) # Connect to less 'busy' neurons first
                
                # Try to connect to a few, not just one, if source is very overloaded
                for neurona_destino_aleatoria in neuronas_sueltas_para_conexion[:min(3, len(neuronas_sueltas_para_conexion))]: # Try up to 3 new connections
                    if neurona_origen.conectar(neurona_destino_aleatoria):
                        # The HS reset for 'repair' happens in the government logic or manual reset.
                        # Here, it just forms connections to distribute traffic.
                        neuronas_visuales[neurona_origen.id].trigger_flash()
                        neuronas_visuales[neurona_destino_aleatoria.id].trigger_flash()
                        set_message(f"'{neurona_origen.id}' formed new connection with '{neurona_destino_aleatoria.id}' (traffic management).", duration=1.5)
                        # No break here, allow multiple connections if enough 'activacion' or 'pressure'

    # Remove marked neurons
    for id_eliminar in neuronas_a_eliminar:
        for n_obj in list(neuronas.values()): 
            n_obj.conectada_a = [target for target in n_obj.conectada_a if target.id != id_eliminar]
            n_obj.conectada_desde = [source for source in n_obj.conectada_desde if source.id != id_eliminar]

        if id_eliminar in neuronas:
            del neuronas[id_eliminar]
        if id_eliminar in neuronas_visuales:
            del neuronas_visuales[id_eliminar]


    # --- DRAWING LOGIC ---
    pantalla.fill(BLANCO)

    if current_screen == SCREEN_NETWORK:
        # Draw connections (apply zoom and offset)
        for id_origen, neurona_o in list(neuronas.items()): 
            if id_origen in neuronas_visuales:
                inicio_x = int((neuronas_visuales[id_origen].x + offset_x) * zoom_level)
                inicio_y = int((neuronas_visuales[id_origen].y + offset_y) * zoom_level)
                inicio = (inicio_x, inicio_y)
                for neurona_destino_obj in list(neurona_o.conectada_a):
                    id_destino = neurona_destino_obj.id
                    if id_destino in neuronas_visuales:
                        fin_x = int((neuronas_visuales[id_destino].x + offset_x) * zoom_level)
                        fin_y = int((neuronas_visuales[id_destino].y + offset_y) * zoom_level)
                        fin = (fin_x, fin_y)
                        pygame.draw.line(pantalla, GRIS, inicio, fin, max(1, int(3 * zoom_level))) 

        # Draw bottom control buttons (no zoom/pan)
        button_y = ALTO_PANTALLA - 70
        button_height = 50
        button_width = 50 
        
        plus_button_rect = pygame.Rect(ANCHO_PANTALLA - 70, button_y, button_width, button_height)
        conexion_button_rect = pygame.Rect(ANCHO_PANTALLA - 140, button_y, button_width, button_height)
        eliminar_button_rect = pygame.Rect(ANCHO_PANTALLA - 200, button_y, button_width, button_height)
        rename_button_rect = pygame.Rect(ANCHO_PANTALLA - 260, button_y, button_width, button_height) 
        disconnect_button_rect = pygame.Rect(ANCHO_PANTALLA - 320, button_y, button_width, button_height) 
        activate_nodes_button_rect = pygame.Rect(ANCHO_PANTALLA - 420, button_y, 100, button_height) 
        save_button_rect = pygame.Rect(ANCHO_PANTALLA - 480, button_y, button_width, button_height) 
        load_button_rect = pygame.Rect(ANCHO_PANTALLA - 540, button_y, button_width, button_height) 


        # Draw "🗑️" button
        color_boton_eliminar = ROJO if modo_eliminar_activo else GRIS
        pygame.draw.rect(pantalla, color_boton_eliminar, eliminar_button_rect, 0, 5)
        pygame.draw.rect(pantalla, NEGRO, eliminar_button_rect, 2, 5)
        texto_eliminar = fuente.render("🗑️", True, NEGRO)
        pantalla.blit(texto_eliminar, (eliminar_button_rect.x + 10, eliminar_button_rect.y + 8))
                   
        # Draw "⇆" button (Connection Mode)
        color_boton = VERDE if modo_conexion_activo else GRIS
        pygame.draw.rect(pantalla, color_boton, conexion_button_rect, 0, 5)
        pygame.draw.rect(pantalla, NEGRO, conexion_button_rect, 2, 5)
        simbolo = {"bidireccional": "⇆", "salida": "→", "entrada": "←"}[modo_conexion_tipo]
        texto_conectar = fuente.render(simbolo, True, NEGRO)
        pantalla.blit(texto_conectar, (conexion_button_rect.x + 15, conexion_button_rect.y + 10))

        # Draw "✍️" button (Rename)
        color_rename_button = PURPURA if modo_renombrar_activo else GRIS
        pygame.draw.rect(pantalla, color_rename_button, rename_button_rect, 0, 5)
        pygame.draw.rect(pantalla, NEGRO, rename_button_rect, 2, 5)
        texto_renombrar = fuente.render("✍️", True, NEGRO)
        pantalla.blit(texto_renombrar, (rename_button_rect.x + 10, rename_button_rect.y + 8))

        # Draw "🔗" button (Disconnect)
        color_disconnect_button = CIAN if modo_desconectar_activo else GRIS
        pygame.draw.rect(pantalla, color_disconnect_button, disconnect_button_rect, 0, 5)
        pygame.draw.rect(pantalla, NEGRO, disconnect_button_rect, 2, 5)
        texto_desconectar = fuente.render("🔗", True, NEGRO)
        pantalla.blit(texto_desconectar, (disconnect_button_rect.x + 10, disconnect_button_rect.y + 8))


        # Draw "Activate Nodes" button
        color_activate_button = VERDE if activation_mode_active else GRIS
        pygame.draw.rect(pantalla, color_activate_button, activate_nodes_button_rect, 0, 5)
        pygame.draw.rect(pantalla, NEGRO, activate_nodes_button_rect, 2, 5)
        texto_activate = fuente_pequena.render("Activate", True, NEGRO)
        texto_activate_rect = texto_activate.get_rect(center=activate_nodes_button_rect.center)
        pantalla.blit(texto_activate, texto_activate_rect)

        # Draw "Save" button
        pygame.draw.rect(pantalla, AMARILLO, save_button_rect, 0, 5)
        pygame.draw.rect(pantalla, NEGRO, save_button_rect, 2, 5)
        texto_guardar = fuente.render("💾", True, NEGRO)
        pantalla.blit(texto_guardar, (save_button_rect.x + 10, save_button_rect.y + 8))

        # Draw "Load" button
        pygame.draw.rect(pantalla, CIAN, load_button_rect, 0, 5)
        pygame.draw.rect(pantalla, NEGRO, load_button_rect, 2, 5)
        texto_cargar = fuente.render("📂", True, NEGRO)
        pantalla.blit(texto_cargar, (load_button_rect.x + 10, texto_cargar.get_height() // 2 + load_button_rect.y))


        # Draw neurons (apply zoom and offset)
        hovered_neuron_visual = None
        for visual_neurona in list(neuronas_visuales.values()): 
            if visual_neurona != dragging_neuron_visual:
                is_selected = (first_clicked_neuron_visual == visual_neurona)
                is_renaming_this = (selected_neuron_for_rename_visual == visual_neurona and rename_input_active)
                is_disconnecting_this = (first_clicked_neuron_visual == visual_neurona and modo_desconectar_activo)
                visual_neurona.dibujar(pantalla, zoom_level, offset_x, offset_y, is_selected, False, modo_eliminar_activo, is_renaming_this, is_disconnecting_this) 
                
                # Collision for tooltip, using inverse transformed coordinates
                transformed_mouse_x = (mouse_x / zoom_level) - offset_x
                transformed_mouse_y = (mouse_y / zoom_level) - offset_y
                dist_a_neurona = math.hypot(transformed_mouse_x - visual_neurona.x, transformed_mouse_y - visual_neurona.y)
                if dist_a_neurona <= visual_neurona.radio and dragging_neuron_visual is None:
                    hovered_neuron_visual = visual_neurona
        
        if dragging_neuron_visual:
            dragging_neuron_visual.dibujar(pantalla, zoom_level, offset_x, offset_y, False, True, modo_eliminar_activo) 
            hovered_neuron_visual = dragging_neuron_visual 

        if hovered_neuron_visual:
            # Tooltip is drawn in screen coordinates, so no zoom/offset applied
            dibujar_tooltip(pantalla, (mouse_x, mouse_y), hovered_neuron_visual)

        # Draw Rename Input Box if active
        if rename_input_active and selected_neuron_for_rename_visual:
            # Recalculate input box position in screen coordinates
            rename_input_rect = pygame.Rect(
                (selected_neuron_for_rename_visual.x + offset_x) * zoom_level - 75, 
                (selected_neuron_for_rename_visual.y + offset_y) * zoom_level - (selected_neuron_for_rename_visual.radio * zoom_level) - 50, 
                150, 30)

            pygame.draw.rect(pantalla, BLANCO_APAGADO, rename_input_rect, 0, 5)
            pygame.draw.rect(pantalla, AZUL, rename_input_rect, 2, 5) 
            text_surface = fuente_pequena.render(rename_input_text, True, NEGRO)
            pantalla.blit(text_surface, (rename_input_rect.x + 5, rename_input_rect.y + 5))


        # Indicate which keys to use (on screen, no zoom/pan)
        texto_ayuda_y_offset = 20
        texto_ayuda_teclas = [
            "SPACE: Activate Rol 2 NS", 
            "A: Activate random neuron (Rol 1 for NOT)", 
            "V: Set random values (except Rol 1)", 
            "C: Propagate 1 step (Full, with governments and traffic)", 
            "R: Reset Network"
        ]
        for i, linea in enumerate(texto_ayuda_teclas):
            texto_render = fuente_pequena.render(linea, True, NEGRO)
            pantalla.blit(texto_render, (20, texto_ayuda_y_offset + i * 15))

        texto_ayuda_drag = fuente_pequena.render("Click and drag to move neurons.", True, NEGRO)
        pantalla.blit(texto_ayuda_drag, (20, texto_ayuda_y_offset + len(texto_ayuda_teclas) * 15 + 5))
        texto_ayuda_connect = fuente_pequena.render("Click 2 times on neurons to connect (origin → destination). TAB: Change type.", True, NEGRO)
        pantalla.blit(texto_ayuda_connect, (20, texto_ayuda_y_offset + len(texto_ayuda_teclas) * 15 + 20))
        texto_ayuda_rename = fuente_pequena.render("Rename mode: Click on neuron to edit ID. ENTER to confirm.", True, NEGRO)
        pantalla.blit(texto_ayuda_rename, (20, texto_ayuda_y_offset + len(texto_ayuda_teclas) * 15 + 35))
        texto_ayuda_zoom_pan = fuente_pequena.render("Mouse wheel: Zoom. Left click (outside neuron): Pan. Middle click: Pan.", True, NEGRO)
        pantalla.blit(texto_ayuda_zoom_pan, (20, texto_ayuda_y_offset + len(texto_ayuda_teclas) * 15 + 50))
        texto_ayuda_disconnect = fuente_pequena.render("Disconnect mode: Click on 2 connected neurons to disconnect them.", True, NEGRO)
        pantalla.blit(texto_ayuda_disconnect, (20, texto_ayuda_y_offset + len(texto_ayuda_teclas) * 15 + 65))


        # Connection/disconnection message
        if first_clicked_neuron_visual is not None and (time.time() - connection_message_display_time) < CONNECTION_MESSAGE_DURATION:
            msg_text = fuente.render(f"Click another neuron to connect/disconnect '{first_clicked_neuron_visual.neurona.id}'", True, AZUL)
            msg_rect = msg_text.get_rect(center=(ANCHO_PANTALLA // 2, 50))
            pantalla.blit(msg_text, msg_rect)
        
        # Draw '+' button to go to creator
        pygame.draw.circle(pantalla, GRIS, plus_button_rect.center, 25)
        pygame.draw.line(pantalla, NEGRO, (plus_button_rect.centerx - 10, plus_button_rect.centery), (plus_button_rect.centerx + 10, plus_button_rect.centery), 3)
        pygame.draw.line(pantalla, NEGRO, (plus_button_rect.centerx, plus_button_rect.centery - 10), (plus_button_rect.centerx, plus_button_rect.centery + 10), 3)

        # Display temporary messages
        if current_message and time.time() < message_display_time:
            msg_surface = fuente_grande.render(current_message, True, NEGRO)
            msg_rect = msg_surface.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2))
            bg_rect = msg_rect.inflate(40, 20)
            s = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            s.fill((200, 200, 200, 180))
            pantalla.blit(s, (bg_rect.x, bg_rect.y))
            pygame.draw.rect(pantalla, NEGRO, bg_rect, 2, 5)
            pantalla.blit(msg_surface, msg_rect)

    elif current_screen == SCREEN_CREATOR:
        titulo = fuente_grande.render("Create New Bynarium Neuron", True, NEGRO)
        titulo_rect = titulo.get_rect(center=(ANCHO_PANTALLA // 2, 100))
        pantalla.blit(titulo, titulo_rect)

        pygame.draw.rect(pantalla, GRIS, back_button_rect, 0, 5)
        pygame.draw.rect(pantalla, NEGRO, back_button_rect, 2, 5)
        texto_back = fuente.render("Back", True, NEGRO)
        texto_back_rect = texto_back.get_rect(center=back_button_rect.center)
        pantalla.blit(texto_back, texto_back_rect)

        # Input for neuron name
        texto_name_label = fuente.render("Neuron Name (ID):", True, NEGRO)
        pantalla.blit(texto_name_label, (input_name_rect.x - texto_name_label.get_width() - 10, input_name_rect.y + 5))
        color_input_name = BLANCO_APAGADO if active_input_name_box else BLANCO
        pygame.draw.rect(pantalla, color_input_name, input_name_rect, 0, 5)
        pygame.draw.rect(pantalla, NEGRO, input_name_rect, 2, 5)
        texto_input_name = fuente.render(input_name_text, True, NEGRO)
        pantalla.blit(texto_input_name, (input_name_rect.x + 5, input_name_rect.y + 5))

        # Input for number of bits
        texto_bits_label = fuente.render("Number of Bits (NB):", True, NEGRO)
        pantalla.blit(texto_bits_label, (input_bits_rect.x - texto_bits_label.get_width() - 10, input_bits_rect.y + 5))
        color_input_bits = BLANCO_APAGADO if active_input_bits_box else BLANCO
        pygame.draw.rect(pantalla, color_input_bits, input_bits_rect, 0, 5)
        pygame.draw.rect(pantalla, NEGRO, input_bits_rect, 2, 5)
        texto_input_bits = fuente.render(input_bits_text, True, NEGRO)
        pantalla.blit(texto_input_bits, (input_bits_rect.x + 5, input_bits_rect.y + 5))

        try:
            preview_bits = int(input_bits_text)
            if preview_bits >= 1:
                preview_color = get_neuron_color(preview_bits)
                preview_center_y = ALTO_PANTALLA // 2 + 180
                preview_radius = preview_bits * 7
                
                max_almacenamiento_preview = calcular_capacidad_almacenamiento(preview_bits)

                preview_vida_util = 20 # Always 20 now

                pygame.draw.circle(pantalla, preview_color, (ANCHO_PANTALLA // 2, preview_center_y), preview_radius)
                pygame.draw.circle(pantalla, NEGRO, (ANCHO_PANTALLA // 2, preview_center_y), preview_radius, 2)
                
                texto_preview_bits = fuente_pequena.render(f"NB: {preview_bits}", True, NEGRO)
                texto_preview_max = fuente_pequena.render(f"Max Storage: {max_almacenamiento_preview}", True, PURPURA)
                texto_preview_vida_util = fuente_pequena.render(f"Life Utility: {preview_vida_util}", True, CIAN)

                pantalla.blit(texto_preview_bits, (ANCHO_PANTALLA // 2 - texto_preview_bits.get_width() // 2, preview_center_y - preview_radius - 30))
                pantalla.blit(texto_preview_max, (ANCHO_PANTALLA // 2 - texto_preview_max.get_width() // 2, preview_center_y + preview_radius + 10))
                pantalla.blit(texto_preview_vida_util, (ANCHO_PANTALLA // 2 - texto_preview_vida_util.get_width() // 2, preview_center_y + preview_radius + 25))

            else:
                texto_error = fuente_pequena.render("NB must be >= 1", True, ROJO)
                pantalla.blit(texto_error, (ANCHO_PANTALLA // 2 - texto_error.get_width() // 2, ALTO_PANTALLA // 2 + 150))

        except ValueError:
            texto_error = fuente_pequena.render("Enter a valid number", True, ROJO)
            pantalla.blit(texto_error, (ANCHO_PANTALLA // 2 - texto_error.get_width() // 2, ALTO_PANTALLA // 2 + 150))


        pygame.draw.rect(pantalla, VERDE, create_button_rect, 0, 5)
        pygame.draw.rect(pantalla, NEGRO, create_button_rect, 2, 5)
        texto_crear = fuente.render("Create Neuron", True, BLANCO)
        texto_crear_rect = texto_crear.get_rect(center=create_button_rect.center)
        pantalla.blit(texto_crear, texto_crear_rect)


    pygame.display.flip()
    reloj.tick(FPS)

pygame.quit()
sys.exit()
