#!/bin/bash
# Monitor de salud de disco para Uziel
SECTORES=$(sudo smartctl -A /dev/sda | grep "Reallocated_Sector_Ct" | awk '{print $10}')

if [ "$SECTORES" -gt 0 ]; then
    notify-send -u critical "⚠️ ALERTA DE DISCO" "Se han detectado $SECTORES sectores dañados en /dev/sda. ¡Haz un backup ya!"
else
    # Opcional: una notificación silenciosa de que todo sigue bien
    notify-send "Salud del Disco" "Todo bien. Sectores dañados: $SECTORES. Los gatos pueden dormir tranquilos."
fi
