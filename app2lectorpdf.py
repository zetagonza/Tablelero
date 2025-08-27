import re
import pandas as pd
import fitz  # PyMuPDF

# Cambiá la ruta por la de tu PDF
pdf_path = "content.pdf"
txt_output = "salida_cruda.txt"

# Abrir PDF
doc = fitz.open(pdf_path)

with open(txt_output, "w", encoding="utf-8") as f:
    for i, page in enumerate(doc):
        text = page.get_text()
        f.write(f"\n--- Página {i+1} ---\n")
        f.write(text)
        f.write("\n")

print(f"✅ Texto crudo exportado a: {txt_output}")

# --- Leer el texto crudo ---
with open("salida_cruda.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

rows = []
i = 0
cuit = None

while i < len(lines):
    line = lines[i]

    # Detectar inicio de página y resetear CUIT
    if line.startswith("--- Página"):
        cuit = None
        i += 1
        continue

    # Buscar CUIT (solo si no lo tenemos para esta página)
    if not cuit:
        cuit_match = re.match(r'\d{2}-\d{8}-\d', line)
        if cuit_match:
            cuit = cuit_match.group()
            i += 1
            continue

    # Buscar código de jurisdicción
    if re.match(r'^\d{3}$', line):
        codigo = line
        valores = []
        j = i + 1
        # Recorrer siguientes líneas hasta capturar 6 valores monetarios
        while j < len(lines) and len(valores) < 6:
            if lines[j].startswith("$"):
                valores.append(lines[j])
            j += 1

        # La provincia es la línea siguiente al último valor
        provincia = lines[j] if j < len(lines) else ""
        
        # Tomar el 4º valor si hay al menos 4
        if len(valores) >= 4:
            valor_4 = valores[3]
            rows.append([cuit, provincia, valor_4])

        # Avanzar el índice al final del bloque
        i = j + 1
        continue

    i += 1

# Crear DataFrame
df = pd.DataFrame(rows, columns=["CUIT", "Jurisdiccion", "A favor Contribuyente"])

# Guardar CSV
df.to_csv("resultado.csv", index=False, encoding="utf-8-sig")

print(df)
print("Listo. Datos exportados a 'resultado.csv'")
