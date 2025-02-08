#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 input.pdf output.png"
    exit 1
fi

INPUT_PDF="$1"
OUTPUT_PNG="$2"

# PDF in PNG umwandeln (300 DPI)
pdftoppm -png -r 300 "$INPUT_PDF" temp

# Weißen Hintergrund entfernen ohne Schrift zu verlieren
convert temp-1.png \
    -fuzz 5% -fill none -opaque white \
    -alpha set -channel RGBA -evaluate multiply 1.2 +channel "$OUTPUT_PNG"

# Aufräumen
rm temp-1.png

