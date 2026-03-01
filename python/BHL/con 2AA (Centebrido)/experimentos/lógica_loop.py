lógica_loop = """
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
            Numero += eval_data.get('ab', 0) * PosX + expB #a la evaluación le sumamos la experiencia de bondad
            Numero += eval_data.get('ah', 0) * PosY + expH #a la evaluación le sumamos la experiencia de hostilidad
            Numero += eval_data.get('al', 0) * PosZ + expL #a la evaluación le sumamos la experiencia de lógica
            Numero1 += eval_data.get('ac', 0) * PosX - expC #a la experiencia de ir al baño, le restamos la evaluación (esto hace que sea más difícil de satisfacer)
            Numero1 += eval_data.get('ahu', 0) * PosY - expHu #esto hace que la necesidad de hambre sea más difícil de satisfacer con el tiempo
            Numero1 += eval_data.get('As', 0) * PosZ - expS #esto hace que la necesidad de sueño sea más difícil de satisfacer con el tiempo.
            Necesidad_C = (Numero1 // PosX) %100
            Necesidad_H = (Numero1 // PosY) %100
            Necesidad_S = (Numero1 // PosZ ) %100
            Numero -= (Necesidad_C // PosX) %100 + (Necesidad_H // PosX) %100 + (Necesidad_S // PosX)%100 #reduce bondad por las necesidades
            Numero += (Necesidad_C // PosY)%100 + (Necesidad_H // PosY)%100 + (Necesidad_S // PosY)%100 #aumenta la hostilidad ante las necesidades
            Numero -= ((Necesidad_C // PosZ)%100)*2 + ((Necesidad_H // PosZ)%100)*2 + ((Necesidad_S // 10)%100)*2 #disminuye la lógica por 2
            Nivel_incomodidad = eval_data.get('ai',0) #esto da el nivel de incomodidad
            Numeraso_Exp(PosX, PosC, PosY, PosC1, PosZ, PosC2, expH, expB, expL)
            expB,expH,expL = Numeraso_Exp()
    
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
    
    Bondad_actual = max(1, Numero // PosX %100) #obtener el estado de la bondad actual
    Hostilidad_actual = max(1,Numero // PosY) % 100 #obtener el estado de la hostilidad actual
    Lógica_actual = max(1,(Numero // PosZ) % (100)) #obtener el estado de la lógica actual
    Cagar_actual = max(1,Numero1 // PosX) %100 #obtener el estado de la ganas de ir al baño actuales
    Hambre_actual = max(1,Numero1 // PosY) % 100 #obtener el estado de la ganas de comer actuales
    Sueño_actual = max(1,Numero1 // PosZ) % 100 #obtener el estado del sueño actual
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
    Numeraso(Bondad_actual, Hostilidad_actual, Lógica_actual,PosX, PosC, PosY, PosC1, PosZ, PosC2)
    Numeraso_update() #actualizar valores de personalidad
    Numeraso2(Cagar_actual, Hambre_actual, Sueño_actual,PosX, PosC, PosY, PosC1, PosZ, PosC2)
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
"""