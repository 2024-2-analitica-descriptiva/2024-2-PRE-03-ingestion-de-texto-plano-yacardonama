"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd
import re

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    abrir= open('./files/input/clusters_report.txt','r').readlines()
    lineas_limpias = [linea.strip() for linea in abrir]

    data = []
    for linea in lineas_limpias[2:]:
        if linea.strip():
            row_data = linea.split('\t')
            data.append(row_data)

    def separate_numeric_and_text(list_of_lists):
        result = []
        for inner_list in list_of_lists:
            string = inner_list[0]
            numeric_part = re.findall(r'\d+(?:,\d+)*\.?\d*', string)
            text_part = re.sub(r'\s+', ' ', re.sub(r'(?<!,)\d+(?:,\d+)*\.?\d*|[%]', '', string))

            result.append((numeric_part, text_part)) 
        return result

    separated_lists = separate_numeric_and_text(data)

    def create_dataframe(data):
        rows = []
        current_row = [None, None, None, ""]

        for first_list, string in data:
            if first_list:
                # Si la primera lista no está vacía, creamos una nueva fila
                if current_row[3]:
                    rows.append(current_row.copy())
                current_row = first_list + [string]
            else:
                # Si la primera lista está vacía, concatenamos el string a la fila actual
                current_row[3] += ' ' + string

        # Agregamos la última fila
        rows.append(current_row)
        # Creamos el DataFrame
        df = pd.DataFrame(rows, columns=['cluster', 'cantidad_de_palabras_clave', 'porcentaje_de_palabras_clave', 'principales_palabras_clave'])
        return df

    df = create_dataframe(separated_lists[1:])

    df['principales_palabras_clave'] = df['principales_palabras_clave'].str.replace('\s+', ' ')
    df['principales_palabras_clave'] = df['principales_palabras_clave'].str.replace('.', '')
    df['principales_palabras_clave'] = df['principales_palabras_clave'].str.strip()
    df['cluster'] = df['cluster'].astype(int)
    df['cantidad_de_palabras_clave'] = df['cantidad_de_palabras_clave'].astype(int)
    df['porcentaje_de_palabras_clave'] = df['porcentaje_de_palabras_clave'].str.replace(',','.')
    df['porcentaje_de_palabras_clave'] = df['porcentaje_de_palabras_clave'].astype(float)
    
    return df


if __name__=="__main__":
    
    print(pregunta_01())