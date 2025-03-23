import pandas as pd

# Sustituye 'tu_archivo.csv' por la ruta de tu archivo original.
# Asegúrate de que el CSV está realmente separado por punto y coma.
df = pd.read_csv('./data/data.csv', sep=';')

def infer_arff_type(series):
    """Determina si una columna es numérica o de texto."""
    if pd.api.types.is_numeric_dtype(series):
        return 'NUMERIC'
    else:
        return 'STRING'

# Nombre de la relación (puedes cambiarlo si quieres)
relation_name = "data"

arff_lines = []
arff_lines.append(f"@RELATION {relation_name}\n")

# 1) Definición de atributos
for col in df.columns:
    arff_type = infer_arff_type(df[col])
    # En caso de que el nombre de columna tenga espacios o caracteres especiales,
    # puedes envolverlo en comillas simples o cambiarlo a algo más sencillo.
    arff_lines.append(f"@ATTRIBUTE {col} {arff_type}")

arff_lines.append("")  # línea en blanco antes de @DATA
arff_lines.append("@DATA")

# 2) Generación de cada fila en el formato ARFF
for index, row in df.iterrows():
    row_str_values = []
    for val in row:
        if pd.api.types.is_number(val):
            # Es numérico, va sin comillas
            row_str_values.append(str(val))
        else:
            # Es cadena, va entre comillas simples; escapamos comillas internas
            val_str = str(val).replace("'", "\\'")
            row_str_values.append(f"'{val_str}'")
    
    # Unimos los valores con comas
    arff_line = ",".join(row_str_values)
    arff_lines.append(arff_line)

# 3) Unimos todo en un único texto
arff_content = "\n".join(arff_lines)

# 4) Guardamos el contenido en un archivo ARFF
with open('salida.arff', 'w', encoding='utf-8') as f:
    f.write(arff_content)

print("Archivo ARFF generado: salida.arff")