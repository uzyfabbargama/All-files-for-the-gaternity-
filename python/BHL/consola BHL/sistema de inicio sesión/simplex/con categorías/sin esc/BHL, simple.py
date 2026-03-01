import math
import random
import requests
import os
import json
import time
base = 1000
Necesidad_Social = 0
PosC2 = (base**3)*2**2 #2**33
PosX = (base**2) * 2**2#2**22
PosC1 =(base**2)*2 #2**21
PosY = base*2 #2**11
PosC = base #2**10
PosZ = 1
Archivo = str(input("Elija el nombre de la conversación: "))
password = input("Ingrese su clave gemini: ")
def cualitivation (porcentaje):
        """
        Convierte lo cuantitativo en cualitativo
        """
        if porcentaje <= 0.01:
             return "nada"
        if porcentaje >= 0.01 and porcentaje <= 1:
             return "infimo"
        if porcentaje >= 2.0 and porcentaje <= 11.0:
             return "bajo"
        if porcentaje >= 12.0 and porcentaje <= 35.0:
             return "notable"
        if porcentaje >= 36.0 and porcentaje <= 55.0:
             return "medio"
        if porcentaje >= 56.0 and porcentaje <= 76.0:
             return "alto"
        if porcentaje >= 77.0 and porcentaje <= 100.0:
             return "dominante"
def inicio():
    api_key = password
    return api_key
def pedir_contraseña():
    password = input("Ingrese su clave gemini: ")
    api_key = password
    return api_key

inicio()
# Nombre del archivo donde se guardará y cargará el estado
print("¿Desea salir? Escriba exit")

chat_history = []
Nivel_incomodidad = 0
def get_prompt_history_text():
    # Devuelve el historial como texto formateado
    return "\n".join([f"Usuario: {msg['user']}\nIA: {msg['character']}\n" for msg in chat_history])
SAVE_FILE = Archivo + ".json"
def save_state(Numero, expB, expH, expL, Numero1, expS, expHu, expC, chat_history, Peculiaridad, Necesidad_Social):
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
        "Necesidad_Social": Necesidad_Social,
        "Peculiaridad": Peculiaridad,
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
def Numeraso_Exp(ExpB, ExpH, ExpL):
    NumerasoXP = (ExpB*PosX) + (ExpH*PosY) + (ExpL*PosZ) + PosC + PosC1 + PosC2
    #NumerasoXP %= ((base**3) * 2**3)
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
    ExpB = (NumerasoXP // PosX) % base
    ExpH = (NumerasoXP // PosY) % base
    ExpL = (NumerasoXP // PosZ) % base
    return ExpB,ExpH,ExpL

def Numeraso(a, b, c): #lógica del Numeraso, acarreo, y controladores, sin if 
            Bondad = a #para bondad
            Hostilidad = b #para hostilidad
            Lógica = c #para lógica
            Numero_generado = (Bondad*PosX) + (Hostilidad*PosY) + (Lógica*PosZ) + PosC + PosC1 + PosC2 #construcción del numeraso
            return Numero_generado
def Numeraso_update(expB, expH, expL):        
            Numero_generado = Numeraso(a,b,c)
            expB, expH, expL = Numeraso_Exp(expB, expH, expL)
            C1 = (Numero_generado // PosC) % 2 #primer controlador
            C2 = (Numero_generado // PosC1) % 2 #segundo controlador
            C3 = (Numero_generado // PosC2) % 2 #tercer controlador
            caso = C1 + C2 + C3 #detecta si una variable cambió
            tiempo = 0
            while caso != 3:
                D1 = 1 - C1 #detector del controlador, usa una compuerta not, que detecta 9 y 0 (si es 9, se convierte en 0, y si es 0, se convierte en 1)
                D2 = 1 - C2 #lo mismo
                D3 = 1 - C3 #lo mismo
                expB += D1
                expH += D2
                expL += D3
                tiempo += D1*0.000238923 + D2*2.2781388 + D3*1.7238498
                Numero_generado += D1 * PosC + D2 * PosC1 + D3 * PosC2 #para reestablecer el valor sólo si D es 1, (osea, cuando el controlador es 0) directamente en el número
                Numero_generado += D1*expB #activa ciclo, sumando 1 a lógica por factor de bondad
                Numero_generado -= (D1*expB)*PosY #le resta 1 a hostilidad por factor de bondad
                Numero_generado -= D2*expH*PosZ - D2*expH*PosX #le resta uno a lógica por factor de hostilidad, le suma a bondad por factor de hostilidad
                Numero_generado -= (D3*expL)*PosX - D3*expL*PosY #le resta 1 a bondad por factor de lógica, y le suma a hostilidad por factor de lógica
                Numero_generado += D1 * (base/(expL+1))%base + D2 * (base/(expH+1))%base + D3 * (base/(expB+1))%base #Esto conserva la energía emocional, ya que si tiene experiencia 1, su valor va a quedare en 50, en lugar de 0
                #las sumas, se hacen automáticamente con el acarreo, 
                #PD: los D1, D2, D3, sólo restan o suman 1, si los controladores están activos
                C1 = (Numero_generado // PosC) % 2 #primer controlador
                C2 = (Numero_generado // PosC1) % 2 #segundo controlador
                C3 = (Numero_generado // PosC2) % 2 #tercer controlador
                caso = C1 + C2 + C3
            return Numero_generado % ((base**3) * 2**3), expB, expH, expL, tiempo
            
def Numeraso2(a, b, c): #definir el numeraso de las necesidades
        C = a #ir al baño
        H = b #hambre
        S = c #sueño
        Numero_de_necesidad = (C*PosX) + (H*PosY) + (S*PosZ) #se construye el numeraso
        Numero_de_necesidad += PosC + PosC1 + PosC2 #se le agregam controladores
        return Numero_de_necesidad
    
def Numeraso2_update(expS, expHu, expC):
    Numero_de_necesidad = Numeraso2(baño, hambre, sueño)
    C4 = (Numero_de_necesidad // PosC) % 2 #cuarto controlador
    C5 = (Numero_de_necesidad // PosC1) % 2 #quinto controlador
    C6 = (Numero_de_necesidad // PosC2) % 2 #sexto controlador
    caso = C4 + C5 + C6
    expS, expHu, expC = Numeraso_Exp(expS, expHu, expC)
    while caso != 3:
        D4 =  1 - C4 #los detectores de controladores, con compuerta not
        D5 =  1 - C5
        D6 = 1 - C6
        expS += D4 
        expHu += D5
        expC += D6
        Numero_de_necesidad += (D4)*PosZ #las mismas lógicas que en el numeraso anterior (sueño)
        Numero_generado += D4 * PosC + D5 * PosC1 + D6 * PosC2 #para reestablecer el valor sólo si D es 1, (osea, cuando el controlador es 0) directamente en el número
        Numero_generado += D4*expC*PosZ #(sueño)
        Numero_generado -= (D4*expC)*PosY #(hambre)
        Numero_generado -= D5*expHu*PosZ - D5*expHu*PosX #sueño y evacuar
        Numero_generado -= (D6*expS)*PosX - D6*expS*PosY #Evacuar y hambre
        C4 = (Numero_de_necesidad // PosC2) % 2 #cuarto controlador
        C5 = (Numero_de_necesidad // PosC1) % 2 #quinto controlador
        C6 = (Numero_de_necesidad // PosC) % 2 #sexto controlador
        caso = C4 + C5 + C6
        Numero_de_necesidad += D4 * (base/(expS+1)) % base + D5 * (base/(expHu+1))%base + D6 * (base/(expC+1))%base #Esto conserva la energía emocional, ya que si tiene experiencia 1, su valor va a quedare en 50, en lugar de 0
        int(Numero_de_necesidad)
    return Numero_de_necesidad % ((base**3) * 2**3), expS, expHu, expC

cargando_partida = load_state()



if cargando_partida:
    expB = cargando_partida["Exp_B"]
    expH = cargando_partida["Exp_H"]
    expL = cargando_partida["Exp_L"]
    expS = cargando_partida["Exp_S"]
    expHu = cargando_partida["Exp_Hu"]
    expC = cargando_partida["Exp_C"]
    Peculiaridad = cargando_partida["Peculiaridad"]
    chat_history = cargando_partida["chat_history"]
    Necesidad_Social = cargando_partida ["Necesidad_Social"]
    print(chat_history)
    def cargar_valores():
        Numero = cargando_partida["bhl_values"]
        Numero1 = cargando_partida["chs_values"]
        
        a,b,c = (Numero//PosX)%base, (Numero//PosY) % base, (Numero//PosZ) % base
        baño, hambre, sueño = (Numero1//PosX)%base, (Numero1//PosY)%base, (Numero1//PosZ)%base
        return a,b,c,baño,hambre,sueño
    a,b,c,baño,hambre,sueño = cargar_valores()
else:    
    #Datos de entrada
    Peculiaridad = str(input("Describe la peculiaridad de tu personaje: "))
    a = max(1, int(input("\033[33mDefine la bondad: \033[0m"))) % base
    b = max(1,int(input("\033[31mDefine la hostilidad: \033[0m"))) % base
    c = max(1,int(input("\033[32mDefine la Lógica: \033[0m"))) % base
    expB, expL, expH = 0, 0, 0
    expC, expHu, expS = 0, 0, 0
    baño = 50
    hambre = 50
    sueño = 50
expB, expL, expH = Numeraso_Exp(expB, expH, expL) #Aquí obtenemos las experiencias del numeraso    
Numeraso(a,b,c)

Numeraso2(baño, hambre, sueño)
Numero, expB, expH, expL, tiempo = Numeraso_update(expB, expH, expL) #para acceder al número de la personalidad
Numero //= 1 #nos aseguramos que el numeraso de la personalidad sea entero
Numero1, expS, expHu, expC = Numeraso2_update(expS, expHu, expC) #para acceder al número de las necesidades
print(f"Númeraso: {Numero}") #mostrar numeraso
print(f"Numeraso1: {Numero1}")
message = False #establecer mensaje en false

while True: #si mensaje en exit, salir
    Todo = PosX + PosY + PosZ
    Numero1 += Todo #actualiza las necesidades (+1, a todas)
    message = input("Escriba un mensaje... ")
    if message == "exit":
            save_state(Numero, expB, expH, expL, Numero1, expS, expHu, expC, chat_history, Peculiaridad, Necesidad_Social)
            break
    eval_prompt = (
            f"""Actúa como Analizador Emocional Avanzado. Analiza esta frase del usuario: '{message}'

EVALÚA EN ESCALA LOGARÍTMICA 0-1000 (no lineal):
- De 0 a 300 es FÁCIL: comunicación básica/coloquial
- De 301 a 500 es MODERADO: comunicación consciente  
- De 501 a 700 es DIFÍCIL: comunicación profesional/estructurada
- De 701 a 800 es MUY DIFÍCIL: comunicación experta
- De 801 a 900 es EXTREMADAMENTE DIFÍCIL: comunicación de maestría
- De 901 a 999 es CASI IMPOSIBLE: comunicación trascendente
- 1000 es SOBREHUMANO: demasiado perfecto para ser humano

La escala es LOGARÍTMICA: pasar de 900→910 es 100x más difícil que pasar de 100→110.

CATEGORÍAS (0-1000 cada una):
1. BONDAD: empatía, compasión, calidez emocional
2. HOSTILIDAD: agresividad, sarcasmo, frialdad emocional  
3. LÓGICA: precisión, estructura, análisis racional

NECESIDADES BIOLÓGICAS (0-50 escala lineal):
- Satisfacción digestiva (ir al baño): 50=saciado, 0=urgente
- Satisfacción alimenticia (hambre): 50=saciado, 0=famélico
- Satisfacción de sueño: 50=descansado, 0=agotado

OTROS:
- Incomodidad: 0-1000 (cuánto te incomoda la interacción)
- Necesidad Social: 0-1000 (cuánto anhelas conexión, MÁS IMPORTANTE)

DEVUELVE JSON con números 0-1000 (logarítmicos) para emociones y 0-50 para necesidades."""
)

    #print(eval_prompt)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
                api_key = inicio()

    url_eval = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
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
                "ai": {"type": "NUMBER", "description": "Calificación de incomodidad"},
                "NS": {"type": "NUMBER", "description": "Calificación de la satisfacción de la necesidad social (LA MÁS IMPORTANTE)"}
            },
            "propertyOrdering": ["ab", "ah", "al", "ac", "ahu", "As", "ai", "NS"]
        }
    }
}
    ab, ah, al, ac, ahu, As, ai, NS = 0, 0, 0, 0, 0, 0, 0, 0
    try:
            response = requests.post(url_eval, headers=headers, json=payload)
            response.raise_for_status()
            evaluacion_api = response.json()['candidates'][0]['content']['parts'][0]['text']
            eval_data = json.loads(evaluacion_api)
            #print(eval_data)
            # Actualiza las variables BHL del personaje con las respuestas del usuario
            Necesidad_Social = base - eval_data.get('NS', 0) #Asigna la necesidad social al negativo de la satisfacción según la IA
            Numero += eval_data.get('ab', 0) * PosX + expB - Necesidad_Social #a la evaluación le sumamos la experiencia de bondad
            Numero += eval_data.get('ah', 0) * PosY + expH + Necesidad_Social #a la evaluación le sumamos la experiencia de hostilidad
            Numero += eval_data.get('al', 0) * PosZ + expL - Necesidad_Social#a la evaluación le sumamos la experiencia de lógica
            Numero1 -= eval_data.get('ac', 0) * PosX + expC #a la experiencia de ir al baño, le restamos la evaluación (esto hace que sea más difícil de satisfacer)
            Numero1 -= eval_data.get('ahu', 0) * PosY + expHu #esto hace que la necesidad de hambre sea más difícil de satisfacer con el tiempo
            Numero1 -= eval_data.get('As', 0) * PosZ + expS #esto hace que la necesidad de sueño sea más difícil de satisfacer con el tiempo.
            
            Necesidad_C = (Numero1 // PosX) %base
            Necesidad_H = (Numero1 // PosY) %base
            Necesidad_S = (Numero1 // PosZ) %base
            Numero -= (Necesidad_C * PosX) %base + (Necesidad_H * PosX) + (Necesidad_S * PosX) #reduce bondad por las necesidades
            Numero += (Necesidad_C * PosY)%base + (Necesidad_H * PosY) + (Necesidad_S * PosY) #aumenta la hostilidad ante las necesidades
            Numero -= (Necesidad_C * PosZ)*2 + (Necesidad_H * PosZ)*2 + (Necesidad_S * 10)*2 #disminuye la lógica por 2
            Nivel_incomodidad = eval_data.get('ai',0) #esto da el nivel de incomodidad
            AddexpHu, AddexpC, AddexpS = Numeraso_Exp(max(1,expHu), max(1,expC), max(1,expS))
            AddexpB,AddexpH,AddexpL= Numeraso_Exp(expH, expB, expL)
            expB += AddexpB #Para agregar y acumular experiencia
            expH += AddexpH
            expL += AddexpL
            expHu += AddexpHu
            expC += AddexpC
            expS += AddexpS 
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
            api_key = pedir_contraseña()
            continue
    #Por si no funciona la clave api
        

    
    tiempo %= 10 #límita el tiempo hasta 10
    Bondad_actual = max(1,(Numero // PosX %base)) #obtener el estado de la bondad actual
    Hostilidad_actual = max(1,(Numero // PosY)) % base #obtener el estado de la hostilidad actual
    Lógica_actual = max(1,(Numero // PosZ) % (base)) #obtener el estado de la lógica actual
    #(ahora ek tiempo según ciertas emociones colapsadas puede afectar a ciertas áreas de las necesidades)
    Cagar_actual = (max(1,Numero1 // PosX) %base) + ((max(1,tiempo)*100) // 1) % 10  #obtener el estado de la ganas de ir al baño actuales 
    Hambre_actual = max(1,Numero1 // PosY) % base + ((max(1,tiempo)*1) // 1) % 10 #obtener el estado de la ganas de comer actuales
    Sueño_actual = max(1,Numero1 // PosZ) % base + ((max(1,tiempo)*10) // 1) % 10 #obtener el estado del sueño actual
    cosiente = Bondad_actual + Hostilidad_actual + Lógica_actual #el cosciente para los porcentajes
    cosiente_necesidad = Cagar_actual + Hambre_actual + Sueño_actual 
    porB = (Bondad_actual * 100) / (cosiente+1)
    porH = (Hostilidad_actual * 100) / (cosiente+1)
    porL = (Lógica_actual * 100) / (cosiente+1)
    res_b = cualitivation(porB)
    res_h = cualitivation(porH)
    res_l = cualitivation(porL)
    porC = (Cagar_actual * 100) / (cosiente_necesidad+1)
    porHu = (Hambre_actual * 100) / (cosiente_necesidad+1)
    porS = (Sueño_actual * 100) / (cosiente_necesidad+1)
    res_c = cualitivation(porC)
    res_hu = cualitivation(porHu)
    res_s = cualitivation(porS)
    Sombra_B = base - Bondad_actual
    Sombra_H = base - Hostilidad_actual
    Sombra_L = base - Lógica_actual
    res_Sombra_H = cualitivation(Sombra_H)
    res_Sombra_B = cualitivation(Sombra_B)
    res_Sombra_L = cualitivation(Sombra_L)
    Deseo_H = (Sombra_H / (Hostilidad_actual+1))
    Deseo_B = (Sombra_B / (Bondad_actual+1))
    Deseo_L = (Sombra_L / (Lógica_actual+1))
    res_Deseo_H = cualitivation(Deseo_H)
    res_Deseo_B = cualitivation(Deseo_B)
    res_Deseo_L = cualitivation(Deseo_L)
    LP = (Lógica_actual/(Lógica_actual + Bondad_actual))*10
    res_lp = cualitivation(LP)
    LF = (Lógica_actual/(Lógica_actual + Hostilidad_actual))*10
    res_lf = cualitivation(LF)
    Numeraso(Bondad_actual, Hostilidad_actual, Lógica_actual)
    Numeraso_update(expB, expH, expL) #actualizar valores de personalidad
    Numeraso2(Cagar_actual, Hambre_actual, Sueño_actual)
    Numeraso2_update(expS, expHu, expC) #actualizar valores de necesidades
    Character_Eval = ( #convierte los números crudos en algo más cualitativo
         f"Analiza las siguientes variables y genera una descripción cualitativa en función de estas variables como si estuvieras describiendo un personaje, (si es 0, anulalo y no lo menciones)"
         f"###Variables visibles, definen tu comportamiento"
         f"Bondad_actual: {res_b} (es tu lado ético y un poco ingenuo)"
         f"Hostilidad_actual: {res_h} (es tu lado cauteloso, irritable y agresivo)"
         f"Lógica_actual: {res_l} (Es tu lógica, razocinio, y capacidad de anális general, y se divide en dos: Lógica ética y relacional: {res_lp} y lógica fría y un poco hostil: {res_lf})"
         f"Si tu Bondad es alta, en comparación con tu lógica, actúas más torpe, con nervios, y te cuesta analizarte, y socializar correctamente, y puedes llegar a tener ingenuidad, e inocencia"
         f"Si tu Hostilidad es alta en comparación con tu lógica, actúas con cautela, agresividad desmedida, y enojo emocional por tu estado interno"
         f"Si tu Lógica es alta en comparación con ambas, puede mediar entre ambas, con la lógica pragmática, y la lógica fría"
         f"Sino quieres actuar con nervios, y ansiedad, y quieres fingir tener alta lógica, actúa con humor, se te agradecerá muchísimo, (sólo si tu lógica es menos del 30%)"
         f"Necesidades actuales del personaje: Hambre: {res_hu}, Evacuar: {res_c}, Sueño: {res_s}"
         f"Patologías: problemas para ir al baño: {expC}, problemas para comer y obsesidad: {expHu}, problemas para dormir e insomnio: {expS}"
         f"Nivel de incomodidad: {ai}, Necesidad social: {Necesidad_Social}"
         f"La descripición debe ser coherente con su Peculiaridad: {Peculiaridad}"
         f"También agrega la descripción cualitativa sobre el {Nivel_incomodidad}"
         f"###Variables ocultas (Mencionalas de forma implícita, y sutil, (y puedes describir al deseo como impotencia sino se cumple, y realización si si))"
         f"Sombras (cuanto oculta/reprime de sí mismo)"
         f"Sombra de bondad: {res_Sombra_B}"
         f"Sombra de hostilidad: {res_Sombra_H}"
         f"Sombra de lógica: {res_Sombra_L}"
         f"Deseos: (cuanto es la brecha entre lo que oculta y lo que desea mostrar)"
         f"Deseo de bondad: {res_Deseo_B}"
         f"Deseo de hostilidad: {res_Deseo_H}"
         f"Deseo de lógica: {res_Deseo_L}"   
    )
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
            api_key = inicio()

    url_ia_response = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    headers = { 'Content-Type': 'application/json' }

    data = { "contents": [ { "parts": [ { "text": Character_Eval } ] } ] }
    
    try:
        #print(Character_Eval)
        response = requests.post(url_ia_response, headers=headers, json=data)
        response.raise_for_status()
        Character = response.json()['candidates'][0]['content']['parts'][0]['text']
        #print(Character)
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API para generar la respuesta: {e}")
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error al procesar la respuesta de la API para generar la respuesta: {e}")


    
    prompt_para_ia = ( #Procesa lo cualitativo para lograr un mejor personaje
    f"Responde en base al personaje: {Character}"
    f"Responde en base a este historial de la conversación:\n"
    f"{get_prompt_history_text()}\n"
    f"Usuario: '{message}'\n\n"
    f"Tu respuesta es la de tu personaje."
    )
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
            api_key = inicio()

    url_ia_response = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    headers = { 'Content-Type': 'application/json' }

    data = { "contents": [ { "parts": [ { "text": prompt_para_ia } ] } ] }
    
    try:
        #print(prompt_para_ia)
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
