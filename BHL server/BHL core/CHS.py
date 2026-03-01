import time
import requests
import os
import json

def integrated_bhl_chs_system():
    """
    Sistema integrado BHL y CHS que simula una personalidad
    y necesidades biológicas en un solo agente digital.
    """
    # -------------------------------------------------------------------
    # Variables de estado BHL (Alma/Personalidad)
    # -------------------------------------------------------------------
    variables_bhl = {
        "B": 50,  # Bondad
        "H": 50,  # Hostilidad
        "L": 50,  # Lógica
    }

    # Definición de las 6 permutaciones de personalidad (BHL)
    permutations_bhl = ["BHL", "BLH", "HLB", "HBL", "LHB", "LBH"]
    
    while True:
        print("Elige el tipo de personalidad psicológica (BHL, BLH, HLB, HBL, LHB, LBH):")
        chosen_type_bhl = input("> ").upper()
        if chosen_type_bhl in permutations_bhl:
            break
        print("Opción inválida. Intenta de nuevo.")

    # -------------------------------------------------------------------
    # Variables de estado CHS (Cuerpo/Necesidades)
    # -------------------------------------------------------------------
    variables_chs = {
        "C": 50,  # Cagar (alto valor = necesidad)
        "H": 80,  # Hambre (alto valor = satisfecho)
        "S": 70,  # Sueño (alto valor = despierto)
    }

    # Definición de las 6 permutaciones de necesidades (CHS)
    permutations_chs = ["CHS", "CSH", "HCS", "HSC", "SCH", "SHC"]

    while True:
        print("Elige el tipo de personalidad biológica (CHS, CSH, HCS, HSC, SCH, SHC):")
        chosen_type_chs = input("> ").upper()
        if chosen_type_chs in permutations_chs:
            break
        print("Opción inválida. Intenta de nuevo.")
    
    print(f"\n--- Sistema BHL ({chosen_type_bhl}) y CHS ({chosen_type_chs}) activado ---")

    # -------------------------------------------------------------------
    # Lógica de los sistemas
    # -------------------------------------------------------------------

    def update_numeraso_variables(variables, user_input, sign, chosen_type, magnitude=10):
        """
        Actualiza las variables de un sistema (BHL o CHS) en función del input del usuario.
        """
        priorities = list(chosen_type)
        
        # Afecta a las variables en función de su prioridad
        for i, char in enumerate(priorities):
            # El efecto es más fuerte en la variable con mayor prioridad
            effect = magnitude / (i + 1)
            
            # Aplica el signo (+/-)
            variables[char] += effect * sign
            
        # Asegura que los valores se mantengan entre 0 y 99
        for key in variables:
            variables[key] = max(0, min(99, int(variables[key])))

    def update_chs_state(variables_chs, chosen_type_chs):
        """
        Actualiza el estado biológico del CHS basado en el paso del tiempo.
        """
        # El hambre baja con el tiempo. Es el motor del sistema.
        variables_chs["H"] -= 2
        
        # La necesidad de cagar aumenta lentamente con el tiempo
        variables_chs["C"] += 1

        # Lógica de "controladores" del sistema CHS
        priorities = list(chosen_type_chs)
        main_priority = priorities[0]

        if main_priority == 'H': # Si el hambre es la prioridad, afecta al sueño y las ganas de cagar
            if variables_chs["H"] < 20: # Poca hambre = ganas de cagar aumentan para preservar energía
                variables_chs["C"] += 2
            elif variables_chs["H"] > 80: # Mucha hambre = ganas de cagar disminuyen
                variables_chs["C"] -= 1

        elif main_priority == 'S': # Si el sueño es la prioridad, afecta al hambre y las ganas de cagar
            if variables_chs["H"] < 20: # Poca hambre = el sueño aumenta para conservar energía
                variables_chs["S"] += 3
            elif variables_chs["H"] > 80: # Mucha hambre = el sueño disminuye porque el cuerpo está ocupado
                variables_chs["S"] -= 2

        # Se asegura que todos los valores se mantengan en el rango [0, 99]
        for key in variables_chs:
            variables_chs[key] = max(0, min(99, int(variables_chs[key])))

    def get_combined_numeraso(vars_bhl, chosen_type_bhl, vars_chs, chosen_type_chs):
        """Genera un único numeraso para el alma (BHL) y el cuerpo (CHS)."""
        bhl_numeraso_str = "".join([f"{vars_bhl[char]:02}" for char in chosen_type_bhl])
        chs_numeraso_str = "".join([f"{vars_chs[char]:02}" for char in chosen_type_chs])
        return f"{bhl_numeraso_str}-{chs_numeraso_str}"

    def get_api_prompt(vars_bhl, chosen_type_bhl, vars_chs, chosen_type_chs, user_input):
        """
        Construye el prompt para la IA combinando el estado de ambos sistemas.
        """
        # Descripción de la personalidad (BHL)
        personality_prompt = f"Actúa como un personaje con la siguiente personalidad: {chosen_type_bhl} (Bondad:{vars_bhl['B']}, Hostilidad:{vars_bhl['H']}, Lógica:{vars_bhl['L']}). "
        
        # Descripción de las necesidades biológicas (CHS)
        needs_prompt = f"Tus necesidades biológicas son: {chosen_type_chs} (Cagar:{vars_chs['C']}, Hambre:{vars_chs['H']}, Sueño:{vars_chs['S']}). "
        
        # Agrega el input del usuario
        full_prompt = personality_prompt + needs_prompt + "Responde al usuario de forma coherente con tu personalidad y necesidades. Aquí está el mensaje del usuario: '" + user_input + "'"
        return full_prompt

    def call_gemini_api(prompt):
        """
        Función simulada para llamar a la API de Gemini.
        En una aplicación real, se usaría la clave de API y la URL.
        """
        print("\n--- [Simulación de llamada a la IA] ---")
        print(f"Prompt enviado: {prompt[:100]}...") # Muestra solo una parte del prompt
        
        # Lógica de respuesta simulada basada en el prompt
        if "Hambre:99" in prompt:
            return "Lo siento, tengo demasiada hambre para concentrarme."
        elif "Cagar:99" in prompt:
            return "Necesito un momento, mi sistema biológico está en un estado crítico."
        elif "Sueño:0" in prompt:
            return "Estoy tan cansado que mi lógica está fallando."
        elif "Hostilidad:99" in prompt:
            return "Tu pregunta es irrelevante y no vale mi tiempo."
        else:
            return "Tu pregunta es muy interesante, por favor, continúa..."

    # -------------------------------------------------------------------
    # Bucle principal del sistema integrado
    # -------------------------------------------------------------------
    
    while True:
        print("\n" + "="*70)
        # 1. Muestra el estado actual y el numeraso combinado
        print(f"Estado BHL: B:{variables_bhl['B']}, H:{variables_bhl['H']}, L:{variables_bhl['L']} (Tipo: {chosen_type_bhl})")
        print(f"Estado CHS: C:{variables_chs['C']}, H:{variables_chs['H']}, S:{variables_chs['S']} (Tipo: {chosen_type_chs})")
        print(f"Numeraso Total: {get_combined_numeraso(variables_bhl, chosen_type_bhl, variables_chs, chosen_type_chs)}")
        
        # 2. Obtiene la entrada del usuario
        user_input = input("Tú: ")
        
        # 3. Procesa el input para ambos sistemas
        # Asume que palabras como "enojado" o "amable" afectan a BHL,
        # mientras que palabras como "comer" o "descansar" afectan a CHS.
        user_input_lower = user_input.lower()
        if "amable" in user_input_lower or "agradezco" in user_input_lower:
            update_numeraso_variables(variables_bhl, user_input, 1, chosen_type_bhl)
        elif "enojado" in user_input_lower or "estúpida" in user_input_lower:
            update_numeraso_variables(variables_bhl, user_input, -1, chosen_type_bhl, magnitude=20)
        
        if "comer" in user_input_lower:
            variables_chs["H"] += 50
        elif "descansar" in user_input_lower:
            variables_chs["S"] += 50
        elif "baño" in user_input_lower:
            variables_chs["C"] -= 50
        
        # 4. Actualiza el estado biológico (paso del tiempo)
        update_chs_state(variables_chs, chosen_type_chs)
        
        # 5. Genera el prompt y llama a la IA
        full_prompt = get_api_prompt(variables_bhl, chosen_type_bhl, variables_chs, chosen_type_chs, user_input)
        response = call_gemini_api(full_prompt)
        
        print("\nAgente BHL-CHS dice:")
        print(response)

        time.sleep(1) # Espera 1 segundo para simular el paso del tiempo


# Inicia el sistema integrado
if __name__ == "__main__":
    integrated_bhl_chs_system()
