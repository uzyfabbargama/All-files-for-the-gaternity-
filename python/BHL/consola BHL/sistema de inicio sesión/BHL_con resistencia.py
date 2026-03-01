import math
import random
import requests
import os
import json
import time
base = 1000
PosC2 = (base**3) #4000000
PosX = (base**2) * 2#400000
PosC1 =(base**2)#200000
PosY = base*2 #2000
PosC = base #1000
PosZ = 1
Archivo = str(input("Elija el nombre de la conversación: "))
password = input("Ingrese su clave gemini")
def inicio():
    api_key = password
    return api_key
def pedir_contraseña():
    password = input("Ingrese su clave gemini")
    api_key = password
    return api_key
inicio()
# Nombre del archivo donde se guardará y cargará el estado
print("¿Desea salir? Escriba exit")

chat_history = []
Nivel_incomodidad = 0
def get_prompt_history_text():
    # Devuelve el historial como texto formateado
    return "\n".join([f"Usuario: {msg['user']}\nIA: {msg['character']}" for msg in chat_history])
SAVE_FILE = Archivo + ".json"
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
        print("No se ha encontrado el archivo seleccionado")
        return None
    
    with open(SAVE_FILE, 'r') as f:
        data = json.load(f)
    print(f"\n--- Estado del personaje cargado desde '{SAVE_FILE}' ---")
    return data

def Numeraso_Exp(ExpB, ExpH, ExpL, PosX, PosC, PosY, PosC1, PosZ, PosC2):
    NumerasoXP = ExpB*PosX + ExpH*PosY + ExpL*PosZ + PosC + PosC1 + PosC2
    C1 = (NumerasoXP // PosC) % 2 #primer controlador
    C2 = (NumerasoXP // PosC1) % 2 #segundo controlador
    C3 = (NumerasoXP // PosC2) % 2 #tercer controlador
    caso = C1 + C2 + C3 #detecta si una variable cambió
    while caso != 3:
        D1 = 1 - C1
        D2 = 1 - C2
        D3 = 1 - C3
        NumerasoXP += D1 * PosC + D2 * PosC1 + D3 * PosC2 #para reestablecer el valor sólo si D es 1, (osea, cuando el controlador es 0) directamente en el número
        NumerasoXP += D1 #activa ciclo, sumando 1 a lógica
        NumerasoXP -= (D1)*PosY #le resta 1 a hostilidad
        NumerasoXP -= D2*PosZ #le resta uno a lógica
        NumerasoXP -= (D3)*PosX #le resta 1 a bondad
            #las sumas, se hacen automáticamente con el acarreo, 
            #PD: los D1, D2, D3, sólo restan o suman 1, si los controladores están activos
        C1 = (NumerasoXP // PosC) % 2 #primer controlador
        C2 = (NumerasoXP // PosC1) % 2 #segundo controlador
        C3 = (NumerasoXP // PosC2) % 2 #tercer controlador
        caso = C1 + C2 + C3
    
    return expB,expH,expL
def Numeraso(a, b, c, PosX, PosC, PosY, PosC1, PosZ, PosC2): #lógica del Numeraso, acarreo, y controladores, sin if 
            Bondad = a #para bondad
            Hostilidad = b #para hostilidad
            Lógica = c #para lógica
            Numero_generado = Bondad*PosX + Hostilidad*PosY + Lógica*PosZ + PosC + PosC1 + PosC2 #construcción del numeraso
            return expB,expH,expL,Numero_generado
def Numeraso_update():        
            Numero_generado,expB,expH,expL = Numeraso(a,b,c,PosX, PosC, PosY, PosC1, PosZ, PosC2)
            C1 = (Numero_generado // PosC) % 2 #primer controlador
            C2 = (Numero_generado // PosC1) % 2 #segundo controlador
            C3 = (Numero_generado // PosC2) % 2 #tercer controlador
            caso = C1 + C2 + C3 #detecta si una variable cambió
            expL = 0
            expB = 0
            expH = 0
            tiempo = 0
            while caso != 3:
                D1 = 1 - C1 #detector del controlador, usa una compuerta not, que detecta 9 y 0 (si es 9, se convierte en 0, y si es 0, se convierte en 1)
                D2 = 1 - C2 #lo mismo
                D3 = 1 - C3 #lo mismo
                expB += D1
                expH += D2
                expL += D3
                tiempo += D1*1.100238923 + D2*2.2781388 + D3*3.7238498
                Numero_generado += D1 * PosC + D2 * PosC1 + D3 * PosC2 #para reestablecer el valor sólo si D es 1, (osea, cuando el controlador es 0) directamente en el número
                Numero_generado += D1 #activa ciclo, sumando 1 a lógica
                Numero_generado -= (D1)*PosY #le resta 1 a hostilidad
                Numero_generado -= D2*PosZ #le resta uno a lógica
                Numero_generado -= (D3)*PosX #le resta 1 a bondad
                Numero_generado += D1 * (base/(expL+1))%base + D2 * (base/(expH+1))%base + D3 * (base/(expB+1))%base #Esto conserva la energía emocional, ya que si tiene experiencia 1, su valor va a quedare en 50, en lugar de 0
                #las sumas, se hacen automáticamente con el acarreo, 
                #PD: los D1, D2, D3, sólo restan o suman 1, si los controladores están activos
                C1 = (Numero_generado // PosC) % 2 #primer controlador
                C2 = (Numero_generado // PosC1) % 2 #segundo controlador
                C3 = (Numero_generado // PosC2) % 2 #tercer controlador
                caso = C1 + C2 + C3
                int(Numero_generado)
            return Numero_generado % 800000000, expB, expH, expL, tiempo
            
def Numeraso2(a, b, c,PosX, PosC, PosY, PosC1, PosZ, PosC2): #definir el numeraso de las necesidades
        C = a #ir al baño
        H = b #hambre
        S = c #sueño
        Numero_de_necesidad = C*PosX + H*PosY + S*PosZ #se construye el numeraso
        Numero_de_necesidad += PosC + PosC1 + PosC2 #se le agregam controladores
        return Numero_de_necesidad
    
def Numeraso2_update():
    Numero_de_necesidad = Numeraso2(baño, hambre, sueño, PosX, PosC, PosY, PosC1, PosZ, PosC2)
    C4 = (Numero_de_necesidad // PosC) % 2 #cuarto controlador
    C5 = (Numero_de_necesidad // PosC1) % 2 #quinto controlador
    C6 = (Numero_de_necesidad // PosC2) % 2 #sexto controlador
    caso = C4 + C5 + C6
    expS = 0
    expHu = 0
    expC = 0
    while caso != 3:
        D4 =  1 - C4 #los detectores de controladores, con compuerta not
        D5 =  1 - C5
        D6 = 1 - C6
        expS += D4 
        expHu += D5
        expC += D6
        Numero_de_necesidad += (D4)*PosZ #las mismas lógicas que en el numeraso anterior (sueño)
        Numero_de_necesidad -= (D4)*PosY #(hambre)
        Numero_de_necesidad -= D5 * PosZ #(sueño)
        Numero_de_necesidad -= (D6)*PosY #hambre
        Numero_de_necesidad -= (D4)*PosX #Evacuar
        C4 = (Numero_de_necesidad // PosC2) % 2 #cuarto controlador
        C5 = (Numero_de_necesidad // PosC1) % 2 #quinto controlador
        C6 = (Numero_de_necesidad // PosC) % 2 #sexto controlador
        caso = C4 + C5 + C6
        Numero_de_necesidad += D4 * (base/(expS+1)) % base + D5 * (base/(expHu+1))%base + D6 * (base/(expC+1))%base #Esto conserva la energía emocional, ya que si tiene experiencia 1, su valor va a quedare en 50, en lugar de 0
        int(Numero_de_necesidad)
    return Numero_de_necesidad, expS, expHu, expC

cargando_partida = load_state()

cargando_partida = load_state()

if cargando_partida:
    expB = cargando_partida["Exp_B"]
    expH = cargando_partida["Exp_H"]
    expL = cargando_partida["Exp_L"]
    expS = cargando_partida["Exp_S"]
    expHu = cargando_partida["Exp_Hu"]
    expC = cargando_partida["Exp_C"]
    chat_history = cargando_partida["chat_history"]
    def cargar_valores():
        Numero = cargando_partida["bhl_values"]
        Numero1 = cargando_partida["chs_values"]
        
        a,b,c = (Numero//PosX)%base, (Numero//PosY) % base, (Numero//PosZ) % base
        baño, hambre, sueño = (Numero1//PosX)%base, (Numero1//PosY)%base, (Numero1//PosZ)%base
        return a,b,c,baño,hambre,sueño
    a,b,c,baño,hambre,sueño = cargar_valores()
else:    
    #Datos de entrada
    Escenario = str(input("Describe el escenario: "))
    a = max(1, int(input("Define la bondad: "))) % base
    b = max(1,int(input("Define la hostilidad: "))) % base
    c = max(1,int(input("Define la Lógica: "))) % base
    expB, expL, expH = 0, 0, 0
    baño = 500
    hambre = 500
    sueño = 500
expB, expL, expH = Numeraso_Exp(expB, expH, expL, PosX, PosC, PosY, PosC1, PosZ, PosC2) #Aquí obtenemos las experiencias del numeraso    
Numeraso(a,b,c,PosX, PosC, PosY, PosC1, PosZ, PosC2)

Numeraso2(baño, hambre, sueño,PosX, PosC, PosY, PosC1, PosZ, PosC2)
Numero, expB, expH, expL, tiempo = Numeraso_update() #para acceder al número de la personalidad
Numero //= 1 #nos aseguramos que el numeraso de la personalidad sea entero
Numero1, expS, expHu, expC = Numeraso2_update() #para acceder al número de las necesidades
print(f"Númeraso: {Numero}") #mostrar numeraso
print(f"Numeraso1: {Numero1}")
message = False #establecer mensaje en false
Escenario = str(input("Describe el escenario: "))    
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
            f"Esas necesidades, se analizan a diferencia de las emociones, del 0 al 50"
            f"Frase del usuario: '{message}'"
            f"También debes analizar la incomodidad que te puede generar la interacción con el usuario y aumentar la calificación de la incomodidad"
        )

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
                api_key = inicio()

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
            Numero += eval_data.get('ab', 0) * PosX + expB #a la evaluación le sumamos la experiencia de bondad
            Numero += eval_data.get('ah', 0) * PosY + expH #a la evaluación le sumamos la experiencia de hostilidad
            Numero += eval_data.get('al', 0) * PosZ + expL #a la evaluación le sumamos la experiencia de lógica
            Numero1 -= eval_data.get('ac', 0) * PosX - expC #a la experiencia de ir al baño, le restamos la evaluación (esto hace que sea más difícil de satisfacer)
            Numero1 -= eval_data.get('ahu', 0) * PosY - expHu #esto hace que la necesidad de hambre sea más difícil de satisfacer con el tiempo
            Numero1 -= eval_data.get('As', 0) * PosZ - expS #esto hace que la necesidad de sueño sea más difícil de satisfacer con el tiempo.
            Necesidad_C = (Numero1 // PosX) %base
            Necesidad_H = (Numero1 // PosY) %base
            Necesidad_S = (Numero1 // PosZ ) %base
            Numero -= (Necesidad_C // PosX) %base + (Necesidad_H // PosX) %base + (Necesidad_S // PosX)%base #reduce bondad por las necesidades
            Numero += (Necesidad_C // PosY)%base + (Necesidad_H // PosY)%base + (Necesidad_S // PosY)%base #aumenta la hostilidad ante las necesidades
            Numero -= ((Necesidad_C // PosZ)%base)*2 + ((Necesidad_H // PosZ)%base)*2 + ((Necesidad_S // 10)%base)*2 #disminuye la lógica por 2
            Nivel_incomodidad = eval_data.get('ai',0) #esto da el nivel de incomodidad
            
            expB,expH,expL= Numeraso_Exp(PosX, PosC, PosY, PosC1, PosZ, PosC2, expH, expB, expL)
    
    except (requests.exceptions.RequestException, json.JSONDecodeError) as err:
            print(f"Error al conectar o decodificar la API: {err}")
            print("Si no tiene una clave vaya a https://aistudio.google.com/app/apikey")
            print("SECCIÓN 1:")
            print("")
            print("Paso 1: Abre el enlace proporcionado")
            print("") #
            print("Paso 2: Utiliza tu cuenta de google para acceder. La clave está ligada a esta cuenta")
            print("")
            print("Paso 3: Si es tu primero, lee y acepta los términos del servicio de Google AI Studio")
            print("")
            print("")
            print("SECCIÓN 2:")
            print("")
            print("Paso 1: En el panel de control (Dashboard) o en la sección de 'API keys', busca el botón que dice 'Create API key' (Crear clave API) o 'Get API Key' ")
            print("Paso 2: Haz clic en el botón. Google Studio generará una cadena de texto única y larga")
            print("Paso 3: Copia la clave de inmediato. Esta es una credencial secreta y, por segurdad, no se volverá a mostrar completa. si la pierdes, tendrás que generar una nueva.")
            print("Listo ¡Disfruta este sistema!")
            pedir_contraseña()
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
    
    tiempo %= 10 #límita el tiempo hasta 10
    Bondad_actual = max(1, Numero // PosX %base) #obtener el estado de la bondad actual
    Hostilidad_actual = max(1,Numero // PosY) % base #obtener el estado de la hostilidad actual
    Lógica_actual = max(1,(Numero // PosZ) % (base)) #obtener el estado de la lógica actual
    #(ahora ek tiempo según ciertas emociones colapsadas puede afectar a ciertas áreas de las necesidades)
    Cagar_actual = (max(1,Numero1 // PosX) %base) + ((max(1,tiempo)*100) // 1) % 10  #obtener el estado de la ganas de ir al baño actuales 
    Hambre_actual = max(1,Numero1 // PosY) % base + ((max(1,tiempo)*1) // 1) % 10 #obtener el estado de la ganas de comer actuales
    Sueño_actual = max(1,Numero1 // PosZ) % base + ((max(1,tiempo)*10) // 1) % 10 #obtener el estado del sueño actual
    cosiente = Bondad_actual + Hostilidad_actual + Lógica_actual #el cosciente para los porcentajes
    cosiente_necesidad = Cagar_actual + Hambre_actual + Sueño_actual 
    porB = ((Bondad_actual*100) / cosiente) 
    porH = ((Hostilidad_actual*100) / cosiente)
    porL = ((Lógica_actual*100) / cosiente)

    porC = ((Cagar_actual*100) / base)
    porHu = ((Hambre_actual*100) / base)
    porS = ((Sueño_actual*100) / base)
    Sombra_B = base - Bondad_actual
    Sombra_H = base - Hostilidad_actual
    Sombra_L = base - Lógica_actual
    Deseo_H = Sombra_H / (Hostilidad_actual+1)
    Deseo_B = Sombra_B / (Bondad_actual+1)
    Deseo_L = Sombra_L / (Lógica_actual+1)
    
    Numeraso(Bondad_actual, Hostilidad_actual, Lógica_actual,PosX, PosC, PosY, PosC1, PosZ, PosC2)
    Numeraso_update() #actualizar valores de personalidad
    Numeraso2(Cagar_actual, Hambre_actual, Sueño_actual,PosX, PosC, PosY, PosC1, PosZ, PosC2)
    Numeraso2_update() #actualizar valores de necesidades
    prompt_para_ia = (
    f"Eres un personaje con la siguiente personalidad y necesidades:\n"
    f"Personalidad: Bondad={porB:.2f}%, Hostilidad={porH:.2f}%, Lógica={porL:.2f}%\n"
    f"Motivaciones secretas (no las menciones): "
    f"Reprimiendo Bondad (Deseo={Deseo_B}%), Reprimiendo Hostilidad (Deseo={Deseo_H}%), Reprimiendo Lógica (Deseo={Deseo_L}%).\n"
    f"Necesidades físicas: Hambre={porHu:.2f}%, Sueño={porS:.2f}%, Evacuación={porC:.2f}%\n"
    f"Sientes una incomodidad general de {Nivel_incomodidad} y estás procesando las experiencias de Bondad={expB}, Hostilidad={expH} y Lógica={expL}.\n"
    f"Tono y comportamiento: Tu tono es fluido con tus porcentajes y necesidades. Actúa con incomodidad si es alta. Responde de forma detallada y reflexiva.\n\n"
    f"Historial de la conversación:\n"
    f"{get_prompt_history_text()}\n"
    f"Usuario: '{message}'\n\n"
    f"Tu respuesta es la de tu personaje."
    f"Para empezar, toma de punto de partida la descripción de este escenario {Escenario}"
    f"Si tienes un valor de experiencia de evacuación: {expC}, experiencia de sueño {expS}, y Experiencia de hambre {expHu} altas (mayor o cercano a 500) tendrás patologías crónicas"
    f"Experiencia de sueño: problemas para dormir"
    f"Experiencia de evacuación: problemas gastrointestinales, problemas para ir al baño"
    f"Experiencia de hambre: Problemas de obesidad, relacionados con el apetito, como que la comida no te satisface"
)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
            api_key = inicio()

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
    
