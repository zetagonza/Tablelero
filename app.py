import streamlit as st
import pandas as pd

st.title("Procesador de datos por CUIT")

st.markdown("""
Ingrese el **CUIT** y los datos en el formato de tabla.  
El sistema generará un archivo CSV con la **quinta columna** y la jurisdicción.
""")

# Ingreso de CUIT
cuit = st.text_input("Ingrese el CUIT:")

# Ingreso de datos como texto
data_text = st.text_area("Pegá los datos (una línea por fila):")

if st.button("Generar CSV"):
    if not cuit or not data_text.strip():
        st.warning("Ingresá CUIT y datos.")
    else:
        # Separar las líneas
        lines = data_text.strip().split("\n")
        result = []

        for i, line in enumerate(lines):
            parts = line.split()
            
            # Últimos 6 elementos son montos
            if i < len(lines) - 1:
                jurisdiction = " ".join(parts[7:])
            else:
                jurisdiction = "TUCUMAN"
            
            # Quinta columna real
            fifth_value = parts[4]
            
            if fifth_value != "$0,00":
                result.append({
                    "Jurisdiccion": jurisdiction,
                    "A favor Contribuyente": fifth_value
                })

        # Crear DataFrame
        df = pd.DataFrame(result)

        # Agregar fila de encabezado con CUIT
        header_row = pd.DataFrame([{"Jurisdiccion": "CUIT", "A favor Contribuyente": cuit}])
        df = pd.concat([header_row, df], ignore_index=True)

        # Convertir a CSV
        csv = df.to_csv(index=False, sep=",", quoting=1, encoding="utf-8-sig")

        # Botón para descargar CSV
        st.download_button(
            label="Descargar CSV",
            data=csv,
            file_name=f"{cuit}.csv",
            mime="text/csv"
        )

        # Mostrar tabla en pantalla
        st.dataframe(df)
