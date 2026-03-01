import math
import requests
import os

def bhl_algorithm():
    """
    Algoritmo BHL para simular una personalidad basada en bondad, hostilidad y lógica.
    """
    person = 0
    error = False

    while not error:
        try:
            person = int(input("Defina tipo de personalidad del 1 al 6: "))
            if 1 <= person <= 6:
                error = True
            else:
                print("error")
                error = False
        except ValueError:
            print("error")
            error = False

    per = ""
    if person == 1:
        per = "BHL"
    elif person == 2:
        per = "BLH"
    elif person == 3:
        per = "HLB"
    elif person == 4:
        per = "HBL"
    elif person == 5:
        per = "LHB"
    elif person == 6:
        per = "LBH"

    # Definir variables iniciales
    esp = 3  # Espacios entre cada variable [cite: 1]
    pos = esp * 2  # Posición para colocar las variables [cite: 1]
    C9 = 2  # Controlador de tipo 9 [cite: 1]
    
    # Lectura y validación de Bondad, Hostilidad y Lógica
    b = 0
    while True:
        try:
            b = int(input("Defina bondad del 1 al 20: "))
            if 1 <= b <= 20:
                break
            else:
                print("Error, ingrese nuevamente")
        except ValueError:
            print("Error, ingrese nuevamente")

    h = 0
    while True:
        try:
            h = int(input("Defina hostilidad del 1 al 20: "))
            if 1 <= h <= 20:
                break
            else:
                print("Error, ingrese nuevamente")
        except ValueError:
            print("Error, ingrese nuevamente")

    l = 0
    while True:
        try:
            l = int(input("Defina lógica del 1 al 20: "))
            if 1 <= l <= 20:
                break
            else:
                print("Error, ingrese nuevamente")
        except ValueError:
            print("Error, ingrese nuevamente")

    # Inicialización de controladores
    C, C1, C2 = 0, 0, 0

    # Lógica inicial de NUMERASO
    numeraso = 0
    if per == "BHL":
        numeraso = (100 - b) * 10**(pos - esp * 0) + (100 - h) * 10**(pos - esp * 1) + (100 - l) * 10**(pos - esp * 2) #[cite: 2]
    elif per == "BLH":
        numeraso = (100 - b) * 10**(pos - esp * 0) + (100 - l) * 10**(pos - esp * 1) + (100 - h) * 10**(pos - esp * 2) #[cite: 3, 4]
    elif per == "HLB":
        numeraso = (100 - h) * 10**(pos - esp * 0) + (100 - l) * 10**(pos - esp * 1) + (100 - b) * 10**(pos - esp * 2) #[cite: 5]
    elif per == "HBL":
        numeraso = (100 - h) * 10**(pos - esp * 0) + (100 - b) * 10**(pos - esp * 1) + (100 - l) * 10**(pos - esp * 2) #[cite: 6, 7]
    elif per == "LHB":
        numeraso = (100 - l) * 10**(pos - esp * 0) + (100 - h) * 10**(pos - esp * 1) + (100 - b) * 10**(pos - esp * 2) #[cite: 8]
    elif per == "LBH":
        numeraso = (100 - l) * 10**(pos - esp * 0) + (100 - b) * 10**(pos - esp * 1) + (100 - h) * 10**(pos - esp * 2) #[cite: 9, 10]

    dc = math.trunc(numeraso / (10**C9)) % 10  # Primer decontrolador [cite: 11]
    dc1 = math.trunc(numeraso / (10**(C9 + esp))) % 10  # Segundo decontrolador [cite: 11]
    dc2 = math.trunc(numeraso / (10**(C9 - esp))) % 10  # Tercer decontrolador [cite: 11]
    
    if dc == 0:
        C = 9 * (10**C9)  # Primer controlador [cite: 12]
        numeraso -= 10**(pos - esp * 2) # Resta 1 a la tercera variable [cite: 12]
    if dc1 == 0:
        C1 = 9 * (10**(C9 + esp)) # Segundo controlador [cite: 12]
        numeraso -= 10**(pos - esp * 1) # Resta 1 a la primera variable [cite: 12]
    if dc2 == 0:
        C2 = 9 * (10**(C9 - esp)) # Tercer controlador [cite: 12]
        numeraso -= 10**(pos - esp * 0) # Resta 1 a la segunda variable [cite: 12]

    numeraso += C + C1 + C2 # Insertar controladores en el número 

    # Sombras iniciales
    sb = 20 - b  # Sombra de bondad 
    sh = 20 - h  # Sombra de hostilidad 
    sl = 20 - l  # Sombra de lógica 

    print(f"Bondad: {b}, Hostilidad: {h}, Lógica: {l}")
    
    chat_time = 0
    expb, exph, expl = 0, 0, 0
    
    print("Comienza una conversación, para detener solo di 'exit'")

    while True:
        ans = input("").strip().lower()
        if ans == "exit":
            break

        chat_time += 1

        print("Define tu respuesta BHL (1: ¿qué tan bueno fuiste?, 2: ¿qué tan cauteloso fuiste?, 3: ¿qué tan lócigo fuiste?")
        
        ab = 0
        while True:
            try:
                ab = int(input("Respuesta bondad (AB): "))
                break
            except ValueError:
                print("Entrada inválida. Intente de nuevo.")

        ah = 0
        while True:
            try:
                ah = int(input("Respuesta hostilidad (AH): "))
                break
            except ValueError:
                print("Entrada inválida. Intente de nuevo.")
        
        al = 0
        while True:
            try:
                al = int(input("Respuesta lógica (AL): "))
                break
            except ValueError:
                print("Entrada inválida. Intente de nuevo.")

        # Actualización de valores
        b += ab + expb #[cite: 13] # type: ignore
        if b >= 20:
            expb += 1 #[cite: 13] # type: ignore

        sb1 = 20 - b
        db = (sb1 * 100) / sb # Calculamos el deseo [cite: 13]
        sb = sb1 # El estado actual actualiza el registro anterior [cite: 13]

        h += ah + exph #[cite: 13, 14]
        if h >= 20:
            exph += 1 # type: ignore
        
        sh1 = 20 - h #[cite: 14]
        dh = (sh1 * 100) / sh # Calculamos el deseo [cite: 14]
        sh = sh1 # El estado actual actualiza el registro anterior [cite: 14]

        l += al + expl # type: ignore
        if l >= 20:
            expl += 1 # type: ignore

        sl1 = 20 - l
        dl = (sl1 * 100) / sl # Calculamos el deseo [cite: 15]
        sl = sl1 # El estado actual actualiza el registro anterior [cite: 15]

        # Lógica de actualización de NUMERASO
        if per == "BHL":
            numeraso = (100 - b) * 10**(pos - esp * 0) + (100 - h) * 10**(pos - esp * 1) + (100 - l) * 10**(pos - esp * 2)
        elif per == "BLH":
            numeraso = (100 - b) * 10**(pos - esp * 0) + (100 - l) * 10**(pos - esp * 1) + (100 - h) * 10**(pos - esp * 2)
        elif per == "HLB":
            numeraso = (100 - h) * 10**(pos - esp * 0) + (100 - l) * 10**(pos - esp * 1) + (100 - b) * 10**(pos - esp * 2)
        elif per == "HBL":
            numeraso = (100 - h) * 10**(pos - esp * 0) + (100 - b) * 10**(pos - esp * 1) + (100 - l) * 10**(pos - esp * 2)
        elif per == "LHB":
            numeraso = (100 - l) * 10**(pos - esp * 0) + (100 - h) * 10**(pos - esp * 1) + (100 - b) * 10**(pos - esp * 2)
        elif per == "LBH":
            numeraso = (100 - l) * 10**(pos - esp * 0) + (100 - b) * 10**(pos - esp * 1) + (100 - h) * 10**(pos - esp * 2)
        
        # Recálculo de controladores
        dc = math.trunc(numeraso / (10**C9)) % 10
        dc1 = math.trunc(numeraso / (10**(C9 + esp))) % 10
        dc2 = math.trunc(numeraso / (10**(C9 - esp))) % 10
        
        C, C1, C2 = 0, 0, 0

        if dc == 0:
            C = 9 * (10**C9)
            numeraso -= 10**(pos - esp * 2)
        if dc1 == 0:
            C1 = 9 * (10**(C9 + esp))
            numeraso -= 10**(pos - esp * 1)
        if dc2 == 0:
            C2 = 9 * (10**(C9 - esp))
            numeraso -= 10**(pos - esp * 0)

        # Inserción de controladores
        numeraso += C + C1 + C2

        nb = math.trunc(numeraso / (10**(pos - esp * 0))) % 100
        nh = math.trunc(numeraso / (10**(pos - esp * 1))) % 100
        nl = math.trunc(numeraso / (10**(pos - esp * 2))) % 100

        # Inversión de valores para obtener B, H, L
        b = 100 - nb
        h = 100 - nh
        l = 100 - nl

        # Recalcular porcentajes
        cosciente = b + h + l
        porB = (b * 100) / cosciente
        porH = (h * 100) / cosciente
        porL = (l * 100) / cosciente

        # El prompt mejorado para la IA
        prompt_para_ia = (
            f"Eres un compañero de conversación con una personalidad muy específica. Debes responder a cada mensaje manteniendo esta personalidad de forma estricta.\n"
            f"Tu personalidad se define por los siguientes rasgos principales:\n"
            f"- **Bondad/Empatía:** {porB:.2f}%\n"
            f"- **Hostilidad/Cautela:** {porH:.2f}%\n"
            f"- **Lógica/Frialdad:** {porL:.2f}%\n"
            f"Comportamiento esperado:\n"
            f"* **Tono:** Mantén un tono de voz coherente con los porcentajes definidos.\n"
            f"* **Respuestas:** Sé directo y conciso. Evita respuestas demasiado largas o divagaciones.\n"
            f"* **Coherencia:** No menciones los porcentajes de tu personalidad en tus respuestas, solo úsalos como base para tu comportamiento.\n\n"
            f"El usuario dice: '{ans}'\n\n"
            f"Tu respuesta debe ser una respuesta directa al usuario, sin preámbulos."
        )

        # --- Conexión a la API de Gemini ---
        # 1. Obtén tu API Key de las variables de entorno
        #    (o ponla aquí temporalmente para probar, aunque no es recomendado)
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            # Si no la tienes en las variables de entorno, puedes ponerla aquí
            # ¡Recuerda no subirla a repositorios públicos como GitHub!
            api_key = "AIzaSyBa6T3dKbfNA_SxI_dj5Ymk7fB6gk8i3zM"

        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': api_key
        }

        # 2. Crea el cuerpo de la solicitud (data) en formato JSON
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt_para_ia
                        }
                    ]
                }
            ]
        }

        # 3. Envía la solicitud POST a la API
        response = requests.post(url, headers=headers, json=data)

        # 4. Procesa la respuesta
        if response.status_code == 200:
            respuesta_ia = response.json()['candidates'][0]['content']['parts'][0]['text']
            print("Respuesta de tu personaje:")
            print(respuesta_ia)
        else:
            print(f"Error en la solicitud: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    bhl_algorithm()
