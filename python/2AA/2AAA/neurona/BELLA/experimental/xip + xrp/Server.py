import tornado.ioloop
import tornado.web
import json
import os
# Importamos la lógica de tu Bella v3.3
# Importamos la lógica y las funciones de persistencia
from BELLAv3_4 import (
    entrenar_con_voz, 
    proyectar_interes_28, 
    exps, 
    guardar_xor_pack_28, 
    cargar_xor_pack # <-- Asegúrate de que esta función exista para recargar
)
cargar_xor_pack()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # Una interfaz simple y oscura para tu celular
        self.write("""
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { background: #0a0a0a; color: #00ff41; font-family: monospace; padding: 20px; }
                #chat { height: 400px; overflow-y: auto; border: 1px solid #333; padding: 10px; margin-bottom: 10px; background: #050505; }
                input { width: 75%; background: #111; border: 1px solid #00ff41; color: #00ff41; padding: 12px; font-size: 16px; }
                button { background: #00ff41; color: black; border: none; padding: 12px; cursor: pointer; font-weight: bold; }
                .stat { font-size: 0.8em; color: #888; margin-top: 5px; }
                .user { color: #00bfff; }
                .bella { color: #ff00ff; }
            </style>
        </head>
        <body>
            <h3>BELLA v3.3 [NÚCLEO REMOTO]</h3>
            <div id="chat"></div>
            <input type="text" id="msg" placeholder="Escribe a Bella..." autocomplete="off">
            <button onclick="send()">ENVIAR</button>
            <div class="stat" id="status">Esperando conexión...</div>

            <script>
                const input = document.getElementById('msg');
                input.addEventListener("keypress", (e) => { if(e.key === 'Enter') send(); });

                async function send() {
                    const text = input.value;
                    if(!text) return;
                    
                    const chat = document.getElementById('chat');
                    chat.innerHTML += "<div class='user'><b>Uziel:</b> " + text + "</div>";
                    input.value = "";
                    chat.scrollTop = chat.scrollHeight;

                    try {
                        const res = await fetch('/chat', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({text: text})
                        });
                        const data = await res.json();
                        
                        chat.innerHTML += "<div class='bella'><b>Bella:</b> " + data.response + "</div>";
                        document.getElementById('status').innerText = data.stats;
                        chat.scrollTop = chat.scrollHeight;
                    } catch (e) {
                        chat.innerHTML += "<div style='color:red'>Error de conexión al núcleo.</div>";
                    }
                }
            </script>
        </body>
        </html>
        """)

class ChatHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        user_input = data.get("text", "")
        print(f"📱 Celular dice: {user_input}") # <-- AGREGA ESTO
        # 1. Proceso de conciencia
        entrenar_con_voz(user_input)
        respuesta = proyectar_interes_28()
        print(f"📱 Bella dice: {respuesta}") # <-- AGREGA ESTO
        # 2. Estadísticas para el móvil
        activas = sum(1 for e in exps if sum(e) > 0)
        p_total = sum(e[2] for e in exps)
        stats = f"Neuronas: {activas} | Presión: {p_total} | Motor: XIP (ASM)"
        
        # 3. Enviar respuesta primero (para que el celular no espere al disco)
        self.write(json.dumps({
            "response": respuesta,
            "stats": stats
        }))
        # 4. Persistencia inmediata (aprovechando la velocidad de XIP)
        guardar_xor_pack_28()
        
        # Nota: cargar_xor_pack() solo es necesario si otro proceso cambió el archivo.
        # Si Bella es el único proceso, no necesitas recargar lo que acabas de guardar.
        
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/chat", ChatHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    # Cambia el puerto si lo necesitas
    app.listen(8888)
    print("--- BELLA v3.3 ONLINE ---")
    print("Accede desde tu celular usando la IP de tu PC puerto 8888")
    print("Ejemplo: http://192.168.1.22:8888")
    tornado.ioloop.IOLoop.current().start()
