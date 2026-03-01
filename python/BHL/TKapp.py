import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import simpledialog
import BHL as BHL
import os
import json

# --- Configuración de la Ventana Principal ---
window = tk.Tk()
window.title("Aplicación de Personaje BHL")
window.geometry("600x700")
window.configure(bg="#f0f0f0")

# --- Variables de la Aplicación ---
scenario_var = tk.StringVar(value="")
bondad_var = tk.IntVar(value=50)
hostilidad_var = tk.IntVar(value=50)
logica_var = tk.IntVar(value=50)

# --- Funciones de Lógica de la Interfaz ---

def start_chat():
    """Inicia la conversación llamando a la lógica de BHL."""
    scenario = scenario_var.get()
    bondad = bondad_var.get()
    hostilidad = hostilidad_var.get()
    logica = logica_var.get()

    if not scenario:
        messagebox.showerror("Error", "Por favor, describe un escenario.")
        return

    BHL.initialize_game(scenario, bondad, hostilidad, logica)
    show_chat_view()

def send_message():
    """Envía un mensaje del usuario a la lógica del personaje y muestra la respuesta."""
    user_message = entry_message.get("1.0", tk.END).strip()
    if not user_message:
        return

    # Muestra el mensaje del usuario
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"Tú: {user_message}\n", "user")
    chat_display.config(state=tk.DISABLED)
    entry_message.delete("1.0", tk.END)

    # Llama a la lógica del personaje
    try:
        response = BHL.process_user_message(user_message)
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"Personaje: {response}\n\n", "character")
        chat_display.config(state=tk.DISABLED)
        chat_display.see(tk.END) # Auto-scroll
    except Exception as e:
        messagebox.showerror("Error de IA", f"Ocurrió un error al procesar el mensaje: {e}")

def save_state():
    """Guarda el estado del juego."""
    try:
        BHL.save_state()
        messagebox.showinfo("Éxito", "Estado del juego guardado correctamente.")
    except Exception as e:
        messagebox.showerror("Error al guardar", f"No se pudo guardar el estado: {e}")

def load_state():
    """Carga un estado de juego guardado."""
    try:
        state_data = BHL.load_state()
        if state_data:
            # Re-inicializa las variables globales en BHL.py
            BHL.Escenario = state_data.get("escenario", "")
            BHL.a, BHL.b, BHL.c = state_data.get("bhl_values", (50, 50, 50))
            BHL.baño, BHL.hambre, BHL.sueño = state_data.get("chs_values", (50, 50, 50))
            BHL.expB, BHL.expH, BHL.expL = state_data.get("Exp_B", 0), state_data.get("Exp_H", 0), state_data.get("Exp_L", 0)
            BHL.expS, BHL.expHu, BHL.expC = state_data.get("Exp_S", 0), state_data.get("Exp_Hu", 0), state_data.get("Exp_C", 0)
            BHL.chat_history = state_data.get("chat_history", [])

            # Carga el historial en el chat
            show_chat_view()
            chat_display.config(state=tk.NORMAL)
            for msg in BHL.chat_history:
                chat_display.insert(tk.END, f"Tú: {msg['user']}\n", "user")
                chat_display.insert(tk.END, f"Personaje: {msg['character']}\n\n", "character")
            chat_display.config(state=tk.DISABLED)
            chat_display.see(tk.END)
            messagebox.showinfo("Éxito", "Estado cargado correctamente.")
        else:
            messagebox.showinfo("Información", "No se encontró ningún archivo de estado guardado.")
    except Exception as e:
        messagebox.showerror("Error al cargar", f"No se pudo cargar el estado: {e}")

# --- Vistas de la Aplicación ---
def clear_window():
    for widget in window.winfo_children():
        widget.destroy()

def show_start_view():
    clear_window()
    frame = tk.Frame(window, bg="#f0f0f0")
    frame.pack(expand=True, padx=20, pady=20)
    
    label_title = tk.Label(frame, text="Bienvenido a la Aplicación de Personaje", font=("Arial", 20, "bold"), bg="#f0f0f0")
    label_title.pack(pady=20)

    btn_start = tk.Button(frame, text="Definir Personalidad", font=("Arial", 14), width=20, height=2, command=show_setup_view)
    btn_start.pack(pady=10)

    btn_load = tk.Button(frame, text="Cargar Estado Existente", font=("Arial", 14), width=20, height=2, command=load_state)
    btn_load.pack(pady=10)

def show_setup_view():
    clear_window()
    frame = tk.Frame(window, bg="#f0f0f0")
    frame.pack(expand=True, padx=20, pady=20)

    tk.Label(frame, text="Define la Personalidad", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

    tk.Label(frame, text="Describe el escenario:", bg="#f0f0f0").pack(anchor="w")
    entry_scenario = tk.Entry(frame, textvariable=scenario_var, width=50)
    entry_scenario.pack(pady=5)

    tk.Label(frame, text="Bondad:", bg="#f0f0f0").pack(anchor="w")
    scale_bondad = tk.Scale(frame, from_=1, to=100, orient="horizontal", variable=bondad_var, bg="#f0f0f0", highlightthickness=0)
    scale_bondad.pack(fill="x", padx=10)

    tk.Label(frame, text="Hostilidad:", bg="#f0f0f0").pack(anchor="w")
    scale_hostilidad = tk.Scale(frame, from_=1, to=100, orient="horizontal", variable=hostilidad_var, bg="#f0f0f0", highlightthickness=0)
    scale_hostilidad.pack(fill="x", padx=10)

    tk.Label(frame, text="Lógica:", bg="#f0f0f0").pack(anchor="w")
    scale_logica = tk.Scale(frame, from_=1, to=100, orient="horizontal", variable=logica_var, bg="#f0f0f0", highlightthickness=0)
    scale_logica.pack(fill="x", padx=10)

    btn_start = tk.Button(frame, text="Iniciar Conversación", font=("Arial", 12), command=start_chat)
    btn_start.pack(pady=20)

    btn_back = tk.Button(frame, text="Volver", command=show_start_view)
    btn_back.pack()

def show_chat_view():
    clear_window()
    
    # Marco superior para botones
    top_frame = tk.Frame(window, bg="#e0e0e0")
    top_frame.pack(fill="x", pady=5, padx=5)

    tk.Button(top_frame, text="Guardar Estado", command=save_state).pack(side="left", padx=5)
    tk.Button(top_frame, text="Regresar a Inicio", command=show_start_view).pack(side="right", padx=5)

    # Área de visualización del chat
    global chat_display
    chat_display = scrolledtext.ScrolledText(window, wrap=tk.WORD, state=tk.DISABLED, bg="#ffffff", font=("Arial", 12))
    chat_display.pack(expand=True, fill="both", padx=10, pady=10)
    chat_display.tag_config("user", foreground="blue")
    chat_display.tag_config("character", foreground="black", font=("Arial", 12, "bold"))
    
    # Marco inferior para la entrada de texto
    bottom_frame = tk.Frame(window, bg="#e0e0e0")
    bottom_frame.pack(fill="x", padx=10, pady=10)

    global entry_message
    entry_message = scrolledtext.ScrolledText(bottom_frame, wrap=tk.WORD, height=3, font=("Arial", 12))
    entry_message.pack(side="left", fill="x", expand=True, padx=(0, 5))
    
    # Configurar el evento Enter para enviar
    entry_message.bind("<Return>", lambda event: send_message())

    btn_send = tk.Button(bottom_frame, text="Enviar", font=("Arial", 12), width=8, command=send_message)
    btn_send.pack(side="right")

    # Mensaje inicial
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, "Personaje: ¡Hola! ¿Cómo te sientes hoy?\n\n", "character")
    chat_display.config(state=tk.DISABLED)

# --- Iniciar la Aplicación ---
show_start_view()
window.mainloop()
