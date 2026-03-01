inicio = 1
os = 1
requests = 1
json = 1
Escenario_prompt = ("Crea un escenario aleatorio")
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
        api_key = inicio()

url_ia_response = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
headers = { 'Content-Type': 'application/json' }

data = { "contents": [ { "parts": [ { "text": Escenario_prompt } ] } ] }

try:
    #print(prompt_para_ia)
    response = requests.post(url_ia_response, headers=headers, json=data)
    response.raise_for_status()
    respuesta_ia = response.json()['candidates'][0]['content']['parts'][0]['text']
    print("\nRespuesta de tu personaje:")
    print(respuesta_ia)
    print("-" * 50)
    
    
except requests.exceptions.RequestException as e:
    print(f"Error al conectar con la API para generar la respuesta: {e}")
except (json.JSONDecodeError, KeyError) as e:
    print(f"Error al procesar la respuesta de la API para generar la respuesta: {e}")

Escenario_prompt = ("Crea un escenario aleatorio")
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
        api_key = inicio()

url_ia_response = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
headers = { 'Content-Type': 'application/json' }

data = { "contents": [ { "parts": [ { "text": Escenario_prompt } ] } ] }

try:
    #print(prompt_para_ia)
    response = requests.post(url_ia_response, headers=headers, json=data)
    response.raise_for_status()
    respuesta_ia = response.json()['candidates'][0]['content']['parts'][0]['text']
    print("\nRespuesta de tu personaje:")
    print(respuesta_ia)
    print("-" * 50)
    
    
except requests.exceptions.RequestException as e:
    print(f"Error al conectar con la API para generar la respuesta: {e}")
except (json.JSONDecodeError, KeyError) as e:
    print(f"Error al procesar la respuesta de la API para generar la respuesta: {e}")




D = 0
P = "hola mundo" * D
print(P)