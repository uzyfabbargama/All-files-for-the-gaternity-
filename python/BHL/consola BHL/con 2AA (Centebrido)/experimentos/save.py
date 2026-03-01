save = """
Archivo = input("Elija el nombre de la conversación")
# Nombre del archivo donde se guardará y cargará el estado
print("¿Desea salir? Escriba exit")
chat_history = []
Nivel_incomodidad = 0
def get_prompt_history_text():
    # Devuelve el historial como texto formateado
    return "\n".join([f"Usuario: {msg['user']}\nIA: {msg['character']}" for msg in chat_history])
SAVE_FILE = Archivo + ".json"
def save_state(Numero, expB, expH, expL, Numero1, expS, expHu, expC, chat_history):
    '''Guarda el estado actual del personaje y la conversación en un archivo JSON.'''
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
    '''Carga el estado del personaje y la conversación desde un archivo JSON.'''
    if not os.path.exists(SAVE_FILE):
        print("No se ha encontrado el archivo seleccionado")
        return None
    
    with open(SAVE_FILE, 'r') as f:
        data = json.load(f)
    print(f"\n--- Estado del personaje cargado desde '{SAVE_FILE}' ---")
    return data

"""
