import flet as ft
import BHL as BHL # ¡Importa el archivo BHL.py!
import json
import os

# --- Vistas de la Aplicación ---

# Función para la vista de configuración inicial
def setup_view(page):
    page.clean() # Limpia la página actual
    
    # Contenedor principal
    main_container = ft.Column(
        [
            ft.Text("Define la Personalidad", size=24, weight="bold"),
            ft.TextField(label="Describe el escenario", value=BHL.Escenario),
            ft.Text("Bondad", size=16),
            ft.Slider(min=1, max=100, value=BHL.a, divisions=100, label="{value}"),
            ft.Text("Hostilidad", size=16),
            ft.Slider(min=1, max=100, value=BHL.b, divisions=100, label="{value}"),
            ft.Text("Lógica", size=16),
            ft.Slider(min=1, max=100, value=BHL.c, divisions=100, label="{value}"),
            ft.ElevatedButton("Iniciar Conversación", on_click=lambda e: start_chat(page, e)),
        ],
        alignment="center",
        horizontal_alignment="center",
        scroll=ft.ScrollMode.ADAPTIVE
    )
    
    page.add(main_container)
    page.update()

def start_chat(page, e):
    scenario_input = page.controls[0].controls[1]
    bondad_slider = page.controls[0].controls[3]
    hostilidad_slider = page.controls[0].controls[5]
    logica_slider = page.controls[0].controls[7]
    
    escenario = scenario_input.value
    bondad = int(bondad_slider.value)
    hostilidad = int(hostilidad_slider.value)
    logica = int(logica_slider.value)
    
    try:
        BHL.initialize_game(escenario, bondad, hostilidad, logica)
        page.go("/chat")
    except Exception as ex:
        page.snack_bar = ft.SnackBar(ft.Text(f"Error al iniciar: {ex}"), open=True)
        page.update()

# Función para la vista de chat
def chat_view(page):
    page.clean()
    
    chat_list = ft.ListView(
        controls=[ft.Text("Personaje: ¡Hola! ¿Cómo te sientes hoy?", selectable=True, size=16)],
        expand=1,
        spacing=10,
        auto_scroll=True
    )

    user_input = ft.TextField(hint_text="Escribe un mensaje...", multiline=False, expand=True)
    
    def send_message(e):
        user_message = user_input.value
        if not user_message:
            return
            
        chat_list.controls.append(ft.Text(f"Tú: {user_message}", selectable=True, color="blue", size=16))
        user_input.value = ""
        page.update()
        
        try:
            response_from_ai = BHL.process_user_message(user_message)
            chat_list.controls.append(ft.Text(f"Personaje: {response_from_ai}", selectable=True, size=16))
        except Exception as ex:
            chat_list.controls.append(ft.Text(f"Error: {ex}", color="red"))
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), open=True)
        finally:
            page.update()

    def save_state(e):
        try:
            BHL.save_state()
            page.snack_bar = ft.SnackBar(ft.Text("Estado guardado con éxito."), open=True)
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar: {ex}"), open=True)
        page.update()

    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.IconButton(ft.icons.SAVE_AS, on_click=save_state),
                        ft.Text("Chat del Personaje", size=20, weight="bold"),
                        ft.IconButton(ft.icons.HOME, on_click=lambda e: page.go("/")),
                    ],
                    alignment="spaceBetween",
                ),
                ft.Divider(),
                chat_list,
                ft.Row(
                    [
                        user_input,
                        ft.IconButton(ft.icons.SEND, on_click=send_message),
                    ]
                )
            ],
            expand=True,
            horizontal_alignment="stretch"
        )
    )
    page.update()

# --- Rutas de la Aplicación ---
def main(page: ft.Page):
    page.title = "Aplicación de Personaje BHL"
    page.vertical_alignment = "center"

    def route_change(route):
        page.views.clear()
        
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.Text("¡Bienvenido a la aplicación de personaje!", size=30, weight="bold"),
                        ft.ElevatedButton("Definir Personalidad", on_click=lambda _: page.go("/setup")),
                        ft.ElevatedButton("Cargar Estado Existente", on_click=lambda _: load_existing_session(page)),
                    ],
                    horizontal_alignment="center",
                    vertical_alignment="center",
                )
            )
        elif page.route == "/setup":
            setup_view(page)
        elif page.route == "/chat":
            chat_view(page)
        
        page.update()

    def load_existing_session(page):
        try:
            state = BHL.load_state()
            if state:
                # Si hay estado guardado, inicializa las variables globales en BHL
                BHL.Escenario = state.get("escenario", "")
                BHL.a, BHL.b, BHL.c = state.get("bhl_values")
                BHL.baño, BHL.hambre, BHL.sueño = state.get("chs_values")
                BHL.expB = state.get("Exp_B", 0)
                BHL.expH = state.get("Exp_H", 0)
                BHL.expL = state.get("Exp_L", 0)
                BHL.expS = state.get("Exp_S", 0)
                BHL.expHu = state.get("Exp_Hu", 0)
                BHL.expC = state.get("Exp_C", 0)
                BHL.chat_history = state.get("chat_history", [])
                
                page.snack_bar = ft.SnackBar(ft.Text("Estado cargado con éxito. ¡Continuemos!"), open=True)
                page.go("/chat")
            else:
                page.snack_bar = ft.SnackBar(ft.Text("No se encontró ningún archivo de estado guardado."), open=True)
                page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al cargar: {ex}"), open=True)
            page.update()

    page.on_route_change = route_change
    page.go("/")

if __name__ == "__main__":
    ft.app(target=main)
