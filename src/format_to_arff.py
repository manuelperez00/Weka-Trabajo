import pandas as pd

df_complete = pd.read_csv('data/data.csv', sep=';')

columns_to_drop = [
    "Tuition fees up to date",
    "Curricular units 1st sem (credited)",
    "Curricular units 1st sem (enrolled)",
    "Curricular units 1st sem (evaluations)",
    "Curricular units 1st sem (approved)",
    "Curricular units 1st sem (grade)",
    "Curricular units 1st sem (without evaluations)",
    "Curricular units 2nd sem (credited)",
    "Curricular units 2nd sem (enrolled)",
    "Curricular units 2nd sem (evaluations)",
    "Curricular units 2nd sem (approved)",
    "Curricular units 2nd sem (grade)",
    "Curricular units 2nd sem (without evaluations)",
]

df_filtered = df_complete.drop(columns=columns_to_drop, errors='ignore')


def sanitize_attribute_name(name):
    """Reemplaza espacios y comillas simples por guiones bajos"""
    return name.replace(' ', '_').replace("'", '_')


def infer_arff_type(series):
    """Determina si una columna es numérica o de texto."""
    if pd.api.types.is_numeric_dtype(series):
        return 'NUMERIC'
    else:
        return 'STRING'


def generate_arff(df_input, output_path, relation_name):
    arff_lines = []
    arff_lines.append(f"@RELATION {relation_name}\n")

    # 1) Definición de atributos
    for col in df_input.columns:
        if col.upper() == 'TARGET':
            unique_values = sorted(df_input[col].dropna().unique())
            # Los valores no llevan comillas
            values_str = ",".join(str(v) for v in unique_values)
            arff_lines.append(f"@ATTRIBUTE TARGET {{{values_str}}}")
        else:
            col_name = sanitize_attribute_name(col)
            arff_type = infer_arff_type(df_input[col])
            arff_lines.append(f"@ATTRIBUTE {col_name} {arff_type}")

    arff_lines.append("")  # línea en blanco antes de @DATA
    arff_lines.append("@DATA")

    # 2) Generación de cada fila en el formato ARFF
    for _, row in df_input.iterrows():
        row_str_values = []
        for col, val in zip(df_input.columns, row):
            if pd.isna(val):
                row_str_values.append('?')
            elif pd.api.types.is_number(val):
                row_str_values.append(str(val))
            elif col.upper() == 'TARGET':
                row_str_values.append(str(val))  # sin comillas
            else:
                val_str = str(val).replace("'", "\\'")
                row_str_values.append(f"'{val_str}'")

        arff_lines.append(",".join(row_str_values))

    arff_content = "\n".join(arff_lines)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(arff_content)

    print(f"Archivo ARFF generado: {output_path}")


generate_arff(df_complete, 'archivo_completo.arff', "completo")
generate_arff(df_filtered, 'archivo_filtrado.arff', "filtrado")
