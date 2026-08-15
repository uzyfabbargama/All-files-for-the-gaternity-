#!/bin/bash

# Configuración
ARCHIVO="universo.bin"
VERSION=1

# Buscamos la última versión para no sobrescribir si reinicias el script
while [ -d "V$VERSION" ]; do
  ((VERSION++))
done

echo "--- Cronista de Transurgencia Activo ---"
# Estado inicial
ULTIMA_MOD=$(stat -c %Y "$ARCHIVO" 2>/dev/null)

while true; do
  # Agregamos la limpieza de pantalla y la visualización de la fecha
  clear
  echo "--- Cronista de Transurgencia Activo ---"
  echo "Próximo eón a capturar: V$VERSION"
  echo "Almacenamiento disponible: $(df -h . | awk 'NR==2 {print $4}')"
  echo "--------------------------------------------------------"
  
  if [ -f "$ARCHIVO" ]; then
    # Mostramos la fecha y detalles como en el Vigilante
    ls -l "$ARCHIVO"
    TAMANO=$(stat -c %s "$ARCHIVO" 2>/dev/null)
    ACTUAL_MOD=$(stat -c %Y "$ARCHIVO" 2>/dev/null)
    
    # Si el archivo cambió, procedemos al archivado
    if [[ "$ACTUAL_MOD" != "$ULTIMA_MOD" && "$TAMANO" -eq 1000000 ]]; then
      FOLDER="V$VERSION"
      mkdir -p "$FOLDER"
      
      # Copia exacta del universo
      cp "$ARCHIVO" "$FOLDER/universo_V$VERSION.bin"
      
      echo "[$(date +%T)] Eón V$VERSION guardado exitosamente."
      
      # Notificación de escritorio
      notify-send "Transurgencia Archivada" "Eón V$VERSION capturado." --icon=emblem-synchronizing
      
      ULTIMA_MOD=$ACTUAL_MOD
      ((VERSION++))
    fi
  else
    echo "Esperando a que aparezca $ARCHIVO..."
  fi

  # Pausa de 5 segundos para no estresar el sistema
  sleep 5
done
