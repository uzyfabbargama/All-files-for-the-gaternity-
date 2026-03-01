# social_parser.py
# Este módulo se encarga de analizar el texto del usuario para identificar
# sustantivos propios y comunes, y asignarles valores BHL y CHS iniciales
# utilizando una API de IA para un análisis más preciso.

import spacy
import time
import uuid
import json
import asyncio
import aiohttp # Se recomienda usar aiohttp para llamadas asíncronas

# Carga el modelo de spaCy para el español.
try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    print("Descargando modelo de spaCy para español. Esto puede tardar unos segundos...")
    from spacy.cli import download
    download("es_core_news_sm")
    nlp = spacy.load("es_core_news_sm")

async def get_bhl_chs_from_api(character_description):
    """
    Usa la API de Gemini para analizar la descripción de un personaje y
    devolver sus valores BHL y CHS en formato JSON.
    """
    # La API key se proporciona automáticamente en el entorno de Canvas si se deja vacía.
    api_key = "AIzaSyBa6T3dKbfNA_SxI_dj5Ymk7fB6gk8i3zM"
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"

    # Define el esquema JSON que esperamos de la respuesta.
    response_schema = {
        "type": "OBJECT",
        "properties": {
            "Bondad": {"type": "INTEGER", "minimum": 0, "maximum": 100},
            "Hostilidad": {"type": "INTEGER", "minimum": 0, "maximum": 100},
            "Logica": {"type": "INTEGER", "minimum": 0, "maximum": 100},
            "Ego": {"type": "INTEGER", "minimum": 0, "maximum": 100},
            "C": {"type": "INTEGER", "minimum": 0, "maximum": 100},
            "H": {"type": "INTEGER", "minimum": 0, "maximum": 100},
            "S": {"type": "INTEGER", "minimum": 0, "maximum": 100}
        },
        "required": ["Bondad", "Hostilidad", "Logica", "Ego", "C", "H", "S"]
    }

    prompt = (
        f"Analiza la siguiente descripción del personaje y asigna valores numéricos de 0 a 100 para sus variables BHL (Bondad, Hostilidad, Lógica, Ego) "
        f"y CHS (Comer, Hambre, Dormir). "
        f"Sé estricto con los valores de CHS; solo asigna un valor alto si el texto menciona comida, sueño o ir al baño. "
        f"La descripción es: '{character_description}'. "
        f"Tu respuesta debe ser un objeto JSON que siga el siguiente esquema, sin ninguna otra explicación, texto o formato."
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": response_schema
        }
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=payload) as response:
                response.raise_for_status()
                result = await response.json()
                
                if result.get('candidates') and result['candidates'][0].get('content') and result['candidates'][0]['content'].get('parts'):
                    json_text = result['candidates'][0]['content']['parts'][0]['text']
                    data = json.loads(json_text)
                    
                    # Separar los valores BHL y CHS en diccionarios separados
                    bhl_values = {k: data[k] for k in ["Bondad", "Hostilidad", "Logica", "Ego"]}
                    chs_values = {k: data[k] for k in ["C", "H", "S"]}
                    
                    return bhl_values, chs_values
                else:
                    return {"Bondad": 50, "Hostilidad": 50, "Logica": 50, "Ego": 5}, {"C": 50, "H": 50, "S": 50}

    except Exception as e:
        print(f"Error al llamar a la API de Gemini: {e}")
        return {"Bondad": 50, "Hostilidad": 50, "Logica": 50, "Ego": 5}, {"C": 50, "H": 50, "S": 50}

async def analyze_social_text(text):
    """
    Analiza un texto para identificar sustantivos propios (personas) y
    sus posibles atributos BHL y CHS usando una API de IA.
    Devuelve un diccionario de perfiles sociales.
    """
    doc = nlp(text)
    new_profiles = {}

    for ent in doc.ents:
        if ent.label_ == "PER":
            name = ent.text.strip()
            # Captura una pequeña ventana de texto alrededor de la entidad para dar contexto a la API.
            start_char = max(0, ent.start_char - 100)
            end_char = min(len(text), ent.end_char + 100)
            context = text[start_char:end_char]
            
            # Obtiene los valores BHL/CHS de la API
            bhl_values, chs_values = await get_bhl_chs_from_api(context)
            
            profile = {
                "id": str(uuid.uuid4()),
                "variables_BHL": bhl_values,
                "variables_tiempo": {
                    "primera_interaccion": time.time(),
                    "ultima_interaccion": time.time(),
                    "tiempo_relacion": 0
                }
            }
            new_profiles[name] = profile
    
    return new_profiles


async def update_social_memory(social_memory, text):
    """
    Función de utilidad para integrar el parser con la memoria social.
    social_memory: una instancia de la clase MemoriaSocial.
    text: el texto del usuario para analizar.
    """
    new_profiles = await analyze_social_text(text)
    
    if not new_profiles:
        return "No se encontraron nuevos perfiles en el texto."

    for name, profile in new_profiles.items():
        if name not in social_memory.db:
            social_memory.db[name] = profile
            social_memory.guardar_estado()
            print(f"--- Nuevo perfil creado para '{name}' y añadido a la memoria social. ---")
        else:
            print(f"--- El perfil para '{name}' ya existe. No se hicieron cambios. ---")
    
    return "Memoria social actualizada con nuevos perfiles."

if __name__ == '__main__':
    # Ejemplo de cómo usar el parser
    print("--- Ejemplo de análisis de texto social usando la API ---")
    
    test_text_1 = "Juana, es muy altiva y a veces un poco soberbia, pero en el fondo ella siente envidia de Carlota, por su comportamiento amable. Juan gusta de Juana sin saber que Carlota también ha desarrollado gusto por él, por su siempre disposición a ayudar al grupo de amigos con el tema del almuerzo."
    
    profiles_found = asyncio.run(analyze_social_text(test_text_1))
    
    for name, profile in profiles_found.items():
        print(f"\nPerfil de '{name}' detectado:")
        print(f"  ID: {profile['id']}")
        print(f"  BHL inicial: {profile['variables_BHL']}")
        print(f"  Tiempo: {profile['variables_tiempo']}")
        
    # Un segundo ejemplo
    test_text_2 = "Ayer vi a Donato, estaba cansado y no quería hablar con nadie, solo quería dormir."
    
    profiles_found_2 = asyncio.run(analyze_social_text(test_text_2))
    
    for name, profile in profiles_found_2.items():
        print(f"\nPerfil de '{name}' detectado:")
        print(f"  ID: {profile['id']}")
        print(f"  BHL inicial: {profile['variables_BHL']}")
        print(f"  Tiempo: {profile['variables_tiempo']}")

