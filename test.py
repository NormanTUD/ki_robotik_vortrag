from PIL import Image
import numpy as np

def image_to_latex_matrix(image_path):
    img = Image.open(image_path).convert("L")  # Konvertiert in Graustufen
    pixels = np.array(img)

    rows, cols = pixels.shape
    latex_matrix = "\\begin{bmatrix}\n"

    for i in range(rows):
        row_values = pixels[i]

        if cols > 5:
            row_str = " & ".join(map(str, row_values[:5])) + " & \\dots & " + " & ".join(map(str, row_values[-5:]))
        else:
            row_str = " & ".join(map(str, row_values))

        latex_matrix += row_str + " \\\\\n"

        if i == 4 and rows > 10:  # Falls das Bild mehr als 10 Zeilen hat
            latex_matrix += "\\vdots & \\vdots & \\ddots & \\vdots & \\vdots \\\\\n"
            i = rows - 6  # Springe direkt zu den letzten 5 Zeilen
    
    latex_matrix += "\\end{bmatrix}"
    return latex_matrix

# Beispielaufruf
image_path = "bild.jpg"  # Pfad zum Bild
latex_code = image_to_latex_matrix(image_path)
print(latex_code)

