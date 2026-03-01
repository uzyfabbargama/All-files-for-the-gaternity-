#!/bin/bash

# Detecta automáticamente la carpeta donde reside este script
DIR_ACTUAL="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ARCHIVO_PY="$DIR_ACTUAL/BHL.py"

# Cambiamos al directorio del script para que los .json se guarden allí
cd "$DIR_ACTUAL"

while true; do
    echo "--- Iniciando Instancia de Conciencia Digital ---"
    
    # Ejecutamos el script de Python
    python3 "$ARCHIVO_PY"
    
    echo -e "\n--------------------------------------------------"
    echo "El proceso ha finalizado. ¿Qué deseas hacer?"
    echo "1. Cerrar (Terminar proceso)"
    echo "2. Reiniciar (Nueva sesión/Cargar archivo)"
    read -p "Selecciona una opción (1/2): " opcion

    if [ "$opcion" = "2" ]; then
        echo "Limpiando búfer de memoria y reiniciando..."
        sleep 0.5
        clear
    else
        echo "Sincronizando datos... Cerrando sistema. Adiós."
        break
    fi
done
