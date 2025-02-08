import numpy as np
import cv2
from PIL import Image
import subprocess
import os

# Bild laden
img = Image.open("bild.jpg").convert("RGB")
r, g, b = img.split()

# Pixelwerte extrahieren
def get_pixel_matrix(channel):
    arr = np.array(channel)
    h, w = arr.shape
    return arr, h, w

r_arr, h, w = get_pixel_matrix(r)
g_arr, _, _ = get_pixel_matrix(g)
b_arr, _, _ = get_pixel_matrix(b)

# LaTeX-Matrix erstellen
def matrix_to_latex(arr):
    first_5_rows = arr[:5, :]
    last_5_rows = arr[-5:, :]
    left_5_cols = arr[:, :5]
    right_5_cols = arr[:, -5:]

    def format_row(row):
        return " & ".join(map(str, row[:5])) + " & \\dots & " + " & ".join(map(str, row[-5:]))

    latex_matrix = "\\begin{pmatrix}\n"
    for row in first_5_rows:
        latex_matrix += format_row(row) + " \\\\\n"
    latex_matrix += "\\vdots & \\vdots & \\ddots & \\vdots & \\vdots \\\\\n"
    for row in last_5_rows:
        latex_matrix += format_row(row) + " \\\\\n"
    latex_matrix += "\\end{pmatrix}"
    return latex_matrix

latex_code = f"""
\\documentclass[varwidth]{{standalone}}
\\usepackage{{amsmath}}
\\begin{{document}}
\\[
R = {matrix_to_latex(r_arr)}
\\]
\\[
G = {matrix_to_latex(g_arr)}
\\]
\\[
B = {matrix_to_latex(b_arr)}
\\]
\\end{{document}}
"""

# LaTeX speichern und kompilieren
with open("output.tex", "w") as f:
    f.write(latex_code)

subprocess.run(["pdflatex", "-interaction=nonstopmode", "output.tex"])

# PDF zu PNG konvertieren und Hintergrund transparent machen
subprocess.run(["magick", "convert", "-density", "300", "output.pdf", "-transparent", "white", "output.png"])

# RGB-Kanäle als PNG mit Transparenz speichern
def save_channel_image(channel_arr, color, filename):
    alpha = (channel_arr > 0).astype(np.uint8) * 255
    color_img = np.zeros((h, w, 4), dtype=np.uint8)
    color_img[:, :, 3] = alpha  # Transparenz setzen

    if color == "r":
        color_img[:, :, 0] = channel_arr
    elif color == "g":
        color_img[:, :, 1] = channel_arr
    elif color == "b":
        color_img[:, :, 2] = channel_arr

    Image.fromarray(color_img).save(filename)

save_channel_image(r_arr, "r", "r_channel.png")
save_channel_image(g_arr, "g", "g_channel.png")
save_channel_image(b_arr, "b", "b_channel.png")

# Aufräumen
for ext in ["aux", "log", "pdf", "tex"]:
    os.remove(f"output.{ext}")

print("Fertig! Die Dateien wurden erstellt.")
