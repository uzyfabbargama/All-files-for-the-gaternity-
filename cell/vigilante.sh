#!/bin/bash



# Configuración inicial

ARCHIVO="universo.bin"

VERSION=1



# Función para encontrar la siguiente versión disponible si el script se reinicia

while [ -d "V$VERSION" ]; do

  ((VERSION++))

done



echo "--- Iniciando el Cronista de Transurgencia ---"

echo "Próxima captura: V$VERSION"



# Guardamos el estado inicial de la última modificación

ULTIMA_MOD=$(stat -c %Y "$ARCHIVO" 2>/dev/null)
echo $ULTIMA_MOD


while true; do

  # Obtenemos la fecha de modificación actual

  ACTUAL_MOD=$(stat -c %Y "$ARCHIVO" 2>/dev/null)



  # Si el archivo existe y la fecha cambió respecto a la anterior

  if [[ "$ACTUAL_MOD" != "$ULTIMA_MOD" && -f "$ARCHIVO" ]]; then

    

    FOLDER="V$VERSION"

    mkdir -p "$FOLDER"

    

    # Copiamos el universo al nuevo eón

    cp "$ARCHIVO" "$FOLDER/"

    

    echo "[$(date +%T)] Transurgencia detectada. Eón V$VERSION archivado."

    notify-send "Eón Capturado" "El universo ha evolucionado a la versión V$VERSION." --icon=emblem-synchronizing

    

    # Actualizamos para la siguiente iteración

    ULTIMA_MOD=$ACTUAL_MOD

    ((VERSION++))

  fi



  # Un sueño de 5 segundos es suficiente para capturar cambios sin perder precisión

  sleep 5

done

y el cronista

#!/bin/bash



# Configuración

ARCHIVO="universo.bin"

VERSION=1



# Buscamos la última versión para no sobrescribir si reinicias el script

while [ -d "V$VERSION" ]; do

  ((VERSION++))

done



echo "--- Cronista de Transurgencia Activo ---"

echo "Próximo eón a capturar: V$VERSION"

echo "Almacenamiento disponible: $(df -h . | awk 'NR==2 {print $4}')"



# Estado inicial (basado en tu vigilante.sh)

ULTIMA_MOD=$(stat -c %Y "$ARCHIVO" 2>/dev/null)



while true; do

  if [ -f "$ARCHIVO" ]; then

    ACTUAL_MOD=$(stat -c %Y "$ARCHIVO" 2>/dev/null)



    # Si el archivo cambió, procedemos al archivado

    if [[ "$ACTUAL_MOD" != "$ULTIMA_MOD" ]]; then

      

      FOLDER="V$VERSION"

      mkdir -p "$FOLDER"

      

      # Copia exacta del universo

      cp "$ARCHIVO" "$FOLDER/universo_V$VERSION.bin"

      

      echo "[$(date +%T)] Eón V$VERSION guardado exitosamente."

      

      # Notificación de escritorio (manteniendo tu estilo)

      notify-send "Transurgencia Archivada" "Eón V$VERSION capturado en su carpeta." --icon=emblem-synchronizing

      

      ULTIMA_MOD=$ACTUAL_MOD

      ((VERSION++))

    fi

  fi



  # Pausa de 5 segundos para no estresar el disco

  sleep 5

done
