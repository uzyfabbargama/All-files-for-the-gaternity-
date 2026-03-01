import math
import random
import requests
import os
import json
import time
# Nombre del archivo donde se guardará y cargará el estado
print("¿Desea salir? Escriba exit")
Escenario = str(input("Describe el escenario: "))
chat_history = []
Nivel_incomodidad = 0
def get_prompt_history_text():
    # Devuelve el historial como texto formateado
    return "\n".join([f"Usuario: {msg['user']}\nIA: {msg['character']}" for msg in chat_history])
SAVE_FILE = "bhl_session_data.json"
def save_state(Numero, expB, expH, expL, Numero1, expS, expHu, expC, chat_history):
    """Guarda el estado actual del personaje y la conversación en un archivo JSON."""
    data = {
        "bhl_values": Numero,
        "Exp_B": expB,
        "Exp_H": expH,
        "Exp_L": expL,
        "chs_values": Numero1,
        "Exp_S": expS,
        "Exp_Hu": expHu,
        "Exp_C": expC,
        "chat_history": chat_history,
    }
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"\n--- Estado del personaje guardado en '{SAVE_FILE}' ---")

def load_state():
    """Carga el estado del personaje y la conversación desde un archivo JSON."""
    if not os.path.exists(SAVE_FILE):
        return None
    
    with open(SAVE_FILE, 'r') as f:
        data = json.load(f)
    print(f"\n--- Estado del personaje cargado desde '{SAVE_FILE}' ---")
    return data
#Datos de entrada
a = max(1, int(input("Define la bondad: "))) % 100
b = max(1,int(input("Define la hostilidad: "))) % 100
c = max(1,int(input("Define la Lógica: "))) % 100
def Numeraso(a, b, c): #lógica del Numeraso, acarreo, y controladores, sin if 
        Bondad = a #para bondad
        Hostilidad = b #para hostilidad
        Lógica = c #para lógica
        Numero_generado = Bondad*(10**(3*2)) + Hostilidad*(10**3) + Lógica + 9*10**8 + 9*10**5 + 9*10**2 #construcción del numeraso
        return Numero_generado
Numeraso(a,b,c)
def Numeraso_update():        
        Numero_generado = Numeraso(a,b,c)
        C1 = (Numero_generado // 10**8) % 10 #primer controlador
        C2 = (Numero_generado // 10**5) % 10 #segundo controlador
        C3 = (Numero_generado // 10**2) % 10 #tercer controlador
        caso = C1 + C2 + C3 #detecta si una variable cambió
        expL = 0
        expB = 0
        expH = 0
        while caso != 27:
            D1 = 9 - C1 #detector del controlador, usa una compuerta not, que detecta 9 y 0 (si es 9, se convierte en 0, y si es 0, se convierte en 1)
            D2 = 9 - C2 #lo mismo
            D3 = 9 - C3 #lo mismo
            expB += D1%2
            expH += D2%2
            expL += D3%2
            Numero_generado += D1 * 10**8 + D2 * 10**5 + D3 * 10**2 #para reestablecer el valor sólo si D es 1, (osea, cuando el controlador es 0) directamente en el número
            Numero_generado += D1%2 #activa ciclo, sumando 1 a lógica
            Numero_generado -= (D1%2)*(10**3) #le resta 1 a hostilidad
            Numero_generado -= D2%2 #le resta uno a lógica
            Numero_generado -= (D3%2)*(10**(3*2)) #le resta 1 a bondad
            #las sumas, se hacen automáticamente con el acarreo, 
            #PD: los D1, D2, D3, sólo restan o suman 1, si los controladores están activos
            C1 = (Numero_generado // 10**8) % 10 #primer controlador
            C2 = (Numero_generado // 10**5) % 10 #segundo controlador
            C3 = (Numero_generado // 10**2) % 10 #tercer controlador
            caso = C1 + C2 + C3
        return Numero_generado % 10**9, expB, expH, expL
baño = 50
hambre = 50
sueño = 50
def Numeraso2(a, b, c): #definir el numeraso de las necesidades
    C = a #ir al baño
    H = b #hambre
    S = c #sueño
    Numero_de_necesidad = C*10**(3*2) + H*10**(3) + S #se construye el numeraso
    Numero_de_necesidad += 9*10**8 + 9*10**5 + 9*10**2 #se le agregam controladores
    return Numero_de_necesidad
Numeraso2(baño, hambre, sueño)
def Numeraso2_update():
    Numero_de_necesidad = Numeraso2(baño, hambre, sueño)
    C4 = (Numero_de_necesidad // 10**8) % 10 #cuarto controlador
    C5 = (Numero_de_necesidad // 10**5) % 10 #quinto controlador
    C6 = (Numero_de_necesidad // 10**2) % 10 #sexto controlador
    caso = C4 + C5 + C6
    expS = 0
    expHu = 0
    expC = 0
    while caso != 27:
        D4 =  9 - C4 #los detectores de controladores, con compuerta not
        D5 =  9 - C5
        D6 = 9 - C6
        expS += D4%2 
        expHu += D5%2
        expC += D6%2
        Numero_de_necesidad += (D4%2) #las mismas lógicas que en el numeraso anterior (sueño)
        Numero_de_necesidad -= (D4%2)*(10**3) #(hambre)
        Numero_de_necesidad -= (D5%2) #(sueño)
        Numero_de_necesidad -= (D6%2)*(10**(3*2)) #hambre
        C4 = (Numero_de_necesidad // 10**8) % 10 #cuarto controlador
        C5 = (Numero_de_necesidad // 10**5) % 10 #quinto controlador
        C6 = (Numero_de_necesidad // 10**2) % 10 #sexto controlador
        caso = C4 + C5 + C6
        Numero_de_necesidad += 1*10**3
    return Numero_de_necesidad, expS, expHu, expC
Numero, expB, expH, expL = Numeraso_update() #para acceder al número de la personalidad
Numero1, expS, expHu, expC = Numeraso2_update() #para acceder al número de las necesidades
print(f"Númeraso: {Numero}") #mostrar numeraso
print(f"Numeraso1: {Numero1}")
message = False #establecer mensaje en false
while True: #si mensaje en exit, salir
    Numero1 += 1*10**(3*2) + 1*10**3 + 1 #actualiza las necesidades
    message = input("Escriba un mensaje... ")
    if message == "exit":
            save_state(Numero, expB, expH, expL, Numero1, expS, expHu, expC, chat_history)
            break
    eval_prompt = (
            f"Analiza la siguiente frase del usuario en una escala del 0 al 20 "
            f"para cada una de las siguientes categorías: Bondad, Hostilidad y Lógica. "
            f"La escala es de 0 (nada) a 20 (máximo). "
            f"También debes analizar el nivel de satisfacción biológica en las categorías: Hambre, Ir al baño, y dormir"
            f"Esas necesidades, se analizan a diferencia de las emociones, del 0 al 100"
            f"Frase del usuario: '{message}'"
            f"También debes analizar la incomodidad que te puede generar la interacción con el usuario y aumentar la calificación de la incomodidad"
        )

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
                api_key = "AIzaSyBa6T3dKbfNA_SxI_dj5Ymk7fB6gk8i3zM"

    url_eval = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
    headers = { 'Content-Type': 'application/json' }
    payload = {
    "contents": [ { "parts": [ { "text": eval_prompt } ] } ],
    "generationConfig": {
        "responseMimeType": "application/json",
        "responseSchema": {
            "type": "OBJECT",
            "properties": {
                "ab": {"type": "NUMBER", "description": "Calificación de bondad"},
                "ah": {"type": "NUMBER", "description": "Calificación de hostilidad"},
                "al": {"type": "NUMBER", "description": "Calificación de lógica"},
                "ac": {"type": "NUMBER", "description": "Calificación de satisfacción con la eliminación de residuos"},
                "ahu": {"type": "NUMBER", "description": "Calificación de satisfacción con la alimentación"},
                "As": {"type": "NUMBER", "description": "Calificación de satisfacción con la calidad del sueño"},
                "ai": {"type": "NUMBER", "description": "Calificación de incomodidad"}
            },
            "propertyOrdering": ["ab", "ah", "al", "ac", "ahu", "As", "ai"]
        }
    }
}
    ab, ah, al, ac, ahu, As, ai = 0, 0, 0, 0, 0, 0, 0
    try:
            response = requests.post(url_eval, headers=headers, json=payload)
            response.raise_for_status()
            evaluacion_api = response.json()['candidates'][0]['content']['parts'][0]['text']
            eval_data = json.loads(evaluacion_api)

            # Actualiza las variables BHL del personaje con las respuestas del usuario
            Numero += eval_data.get('ab', 0) * (10**(3*2)) + expB #a la evaluación le sumamos la experiencia de bondad
            Numero += eval_data.get('ah', 0) * (10**3) + expH #a la evaluación le sumamos la experiencia de hostilidad
            Numero += eval_data.get('al', 0) + expL #a la evaluación le sumamos la experiencia de lógica
            Numero1 += eval_data.get('ac', 0) * (10**(3*2)) - expC #a la experiencia de ir al baño, le restamos la evaluación (esto hace que sea más difícil de satisfacer)
            Numero1 += eval_data.get('ahu', 0) * (10**3) - expHu #esto hace que la necesidad de hambre sea más difícil de satisfacer con el tiempo
            Numero1 += eval_data.get('As', 0) - expS #esto hace que la necesidad de sueño sea más difícil de satisfacer con el tiempo.
            Necesidad_C = (Numero1 // 10**(3*2)%100)
            Necesidad_H = (Numero1 // 10**3) % 100 
            Necesidad_S = Numero1 % 100
            Numero -= (Necesidad_C // 10)*10**(3*2)%100 + (Necesidad_H // 10)*10**(3*2)%100 + (Necesidad_S // 10)*10**(3*2)%100 #reduce bondad por las necesidades
            Numero += (Necesidad_C // 10)*10**(3)%100 + (Necesidad_H // 10)*10**(3)%100 + (Necesidad_S // 10)*10**(3)%100 #aumenta la hostilidad ante las necesidades
            Numero -= ((Necesidad_C // 10)%100)*2 + ((Necesidad_H // 10)%100)*2 + ((Necesidad_S // 10)%100)*2 #disminuye la lógica por 2
            Nivel_incomodidad = eval_data.get('ai',0) #esto da el nivel de incomodidad
    except (requests.exceptions.RequestException, json.JSONDecodeError) as err:
            print(f"Error al conectar o decodificar la API: {err}")
            continue
    prompt_para_escenario = (
        f"Eres un narrador. Basado en el siguiente mensaje del usuario y el escenario actual, "
        f"describe el nuevo escenario en una sola frase concisa. "
        f"No añadas diálogos ni descripciones del personaje. Simplemente actualiza el escenario. "
        f"Si el mensaje del usuario no cambia el escenario, repite el escenario actual. "
        f"Escenario actual: '{Escenario}'\n"
        f"Mensaje del usuario: '{message}'\n"
        f"Nuevo escenario:"
    )
    url_escenario = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
    headers = { 'Content-Type': 'application/json' }
    data_escenario = { "contents": [ { "parts": [ { "text": prompt_para_escenario } ] } ] }
    
    try:
        response_escenario = requests.post(url_escenario, headers=headers, json=data_escenario)
        response_escenario.raise_for_status()
        Escenario_nuevo = response_escenario.json()['candidates'][0]['content']['parts'][0]['text']
        # Limpiamos el texto para evitar espacios o saltos de línea extra
        Escenario = Escenario_nuevo.strip() 
        print(f"\n--- El escenario ha cambiado a: {Escenario} ---")
    except requests.exceptions.RequestException as e:
        print(f"Error al actualizar el escenario: {e}")
        # En caso de error, el escenario no cambia
        
    # --- Fin del nuevo bloque de código ---
    
    Bondad_actual = max(1, Numero // (10**(3*2)) %100) #obtener el estado de la bondad actual
    Hostilidad_actual = max(1,Numero // (10**3) % 100) #obtener el estado de la hostilidad actual
    Lógica_actual = max(1,Numero % (100)) #obtener el estado de la lógica actual
    Cagar_actual = max(1,Numero1 // 10**(3*2)) %100 #obtener el estado de la ganas de ir al baño actuales
    Hambre_actual = max(1,Numero1 // 10**3 % 100) #obtener el estado de la ganas de comer actuales
    Sueño_actual = max(1,Numero1 % 10) #obtener el estado del sueño actual
    cosiente = Bondad_actual + Hostilidad_actual + Lógica_actual #el cosciente para los porcentajes
    porB = (Bondad_actual * 100) / cosiente
    porH = (Hostilidad_actual * 100) / cosiente
    porL = (Lógica_actual * 100) / cosiente
    Sombra_B = 100 - Bondad_actual
    Sombra_H = 100 - Hostilidad_actual
    Sombra_L = 100 - Lógica_actual
    Deseo_H = Sombra_H / Hostilidad_actual
    Deseo_B = Sombra_B / Bondad_actual
    Deseo_L = Sombra_L / Lógica_actual
    Numeraso(Bondad_actual, Hostilidad_actual, Lógica_actual)
    Numeraso_update() #actualizar valores de personalidad
    Numeraso2(Cagar_actual, Hambre_actual, Sueño_actual)
    Numeraso2_update() #actualizar valores de necesidades
    prompt_para_ia = (
    f"Eres un personaje con la siguiente personalidad y necesidades:\n"
    f"Personalidad: Bondad={porB:.2f}%, Hostilidad={porH:.2f}%, Lógica={porL:.2f}%\n"
    f"Motivaciones secretas (no las menciones): "
    f"Reprimiendo Bondad (Deseo={Deseo_B}%), Reprimiendo Hostilidad (Deseo={Deseo_H}%), Reprimiendo Lógica (Deseo={Deseo_L}%).\n"
    f"Necesidades físicas: Hambre={Hambre_actual}, Sueño={Sueño_actual}, Evacuación={Cagar_actual}\n"
    f"Sientes una incomodidad general de {Nivel_incomodidad} y estás procesando las experiencias de Bondad={expB}, Hostilidad={expH} y Lógica={expL}.\n"
    f"Tono y comportamiento: Tu tono es fluido con tus porcentajes y necesidades. Actúa con incomodidad si es alta. Responde de forma detallada y reflexiva.\n\n"
    f"Historial de la conversación:\n"
    f"{get_prompt_history_text()}\n"
    f"Usuario: '{message}'\n\n"
    f"Tu respuesta es la de tu personaje."
    f"Para empezar, toma de punto de partida la descripción de este escenario {Escenario}"
    f"Si tienes un valor de experiencia de evacuación: {expC}, experiencia de sueño {expS}, y Experiencia de hambre {expHu} altas (mayor o cercano a 100) tendrás patologías crónicas"
    f"Experiencia de sueño: problemas para dormir"
    f"Experiencia de evacuación: problemas gastrointestinales, problemas para ir al baño"
    f"Experiencia de hambre: Problemas de obesidad, relacionados con el apetito, como que la comida no te satisface"
)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
            api_key = "AIzaSyBa6T3dKbfNA_SxI_dj5Ymk7fB6gk8i3zM"

    url_ia_response = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
    headers = { 'Content-Type': 'application/json' }

    data = { "contents": [ { "parts": [ { "text": prompt_para_ia } ] } ] }
    
    try:
        response = requests.post(url_ia_response, headers=headers, json=data)
        response.raise_for_status()
        respuesta_ia = response.json()['candidates'][0]['content']['parts'][0]['text']
        print("\nRespuesta de tu personaje:")
        print(respuesta_ia)
        print("-" * 50)
        
        chat_history.append({"user": message, "character": respuesta_ia})
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API para generar la respuesta: {e}")
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error al procesar la respuesta de la API para generar la respuesta: {e}")
    