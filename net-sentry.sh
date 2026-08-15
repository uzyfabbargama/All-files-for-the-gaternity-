#!/bin/bash

# Configuración
TARGET="server-armed.gl.joinmc.link"
COUNT=50

echo "--- INICIANDO DIAGNÓSTICO DE CAPA FÍSICA ---"
echo "Destino: $TARGET"
echo "Muestras: $COUNT paquetes"
echo "--------------------------------------------"

# Ejecutamos el ping y filtramos la data importante
# -q: modo silencioso para el reporte final
# -c: cantidad de paquetes
ping -q -c $COUNT $TARGET > temp_ping.txt

# Extraemos la pérdida de paquetes (Packet Loss)
LOSS=$(grep -oP '\d+(?=% packet loss)' temp_ping.txt)

# Extraemos el RTT (Latencia) min/avg/max
RTT=$(grep "rtt" temp_ping.txt | awk '{print $4}')

# Lógica de decisión
echo "Resultados:"
echo ">> Pérdida de paquetes: $LOSS%"
echo ">> Latencia (min/avg/max): $RTT ms"

if [ "$LOSS" -ge 20 ]; then
    echo -e "\n[!] ESTADO: CRÍTICO (Viento detectado)"
    echo "Sugerencia: El socket se romperá. No inicies transacciones en BellaBank."
elif [ "$LOSS" -ge 5 ]; then
    echo -e "\n[!] ESTADO: INESTABLE"
    echo "Sugerencia: Posible lag en ComputerCraft. Procede con cuidado."
else
    echo -e "\n[OK] ESTADO: ÓPTIMO"
    echo "Sugerencia: La realidad está sincronizada. ¡A programar!"
fi

rm temp_ping.txt
