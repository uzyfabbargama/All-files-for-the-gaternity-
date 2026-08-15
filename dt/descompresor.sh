#!/bin/bash

# 1. Verificar si se pasó un argumento
if [[ -z "$1" ]]; then
    echo "Uso: $0 <archivo>"
    exit 1
fi

# 2. Verificar si el archivo realmente existe
if [[ ! -f "$1" ]]; then
    echo "Error: El archivo '$1' no existe."
    exit 1
fi

ARCH="$1"

# 3. Evaluar según la extensión del archivo
case "$ARCH" in
    *.tar.bz2|*.tbz2) tar xjf "$ARCH"    ;;
    *.tar.gz|*.tgz)   tar xzf "$ARCH"    ;;
    *.tar.xz)         tar xJf "$ARCH"    ;;
    *.tar)            tar xvf "$ARCH"    ;;
    *.bz2)            bunzip2 "$ARCH"    ;;
    *.rar)            unrar x "$ARCH"    ;;
    *.gz)             gunzip "$ARCH"     ;;
    *.zip)            unzip "$ARCH"      ;;
    *.7z)             7z x "$ARCH"       ;;
    *)
        echo "El formato/extensión de '$ARCH' no es soportado o no existe."
        echo "Se agregará soporte en el futuro."
        ;;
esac
