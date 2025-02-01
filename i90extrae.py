import pandas as pd


def get_header(hoja):
    relacion = {1: 3, 2:3, 3:2, 5:2, 6:2, 7:2, 8:2, 9:2}
    return relacion[hoja]


def get_index_vars(hoja):
    relacion = {
        1: ['up', 'Tipo Oferta'],
        2: ['up', 'Tipo Oferta'],
        3: ['up', 'Redespacho', 'Sentido', 'Nm Oferta asignada', 'Tipo Oferta', 'Tipo cálculo', 'Tipo Restricción'],
        5: ['up', 'Sentido', 'Nm Oferta asignada', 'Tipo Oferta'],
        6: ['up', 'Sesión', 'Redespacho', 'Sentido', 'Nm Oferta asignada', 'Tipo Oferta'],
        7: ['up', 'Redespacho', 'Sentido', 'Tipo Oferta'],
        8: ['up', 'Redespacho', 'Tipo', 'Sentido', 'Tipo Oferta', 'Tipo cálculo', 'Tipo Restricción', 'Signo de Energía'],
        9: ['up', 'Redespacho', 'Sentido', 'Tipo Oferta', 'Tipo cálculo']
    }

    return relacion[hoja]


def leer_i90_dia(fichero, hoja):
    # Leemos la hoja del fichero i90
    datos = pd.read_excel(fichero, sheet_name=hoja, header=get_header(hoja))
    # Eliminamos las columnas que no sirven
    try:
        datos = datos.drop('Hora', axis=1)
    except:
        pass
    try:
        datos = datos.drop('Cuarto de Hora del dia', axis=1)
    except:
        pass
    try:
        datos = datos.drop('Total', axis=1)
    except:
        pass
    # Renombramos
    datos = datos.rename(columns={'Unidad de Programación': 'up'})
    # Cambiamos las columnas de horas en filas
    datos = datos.melt(id_vars=get_index_vars(hoja), var_name='periodo', value_name='valor')
    # Tratamos los datos: eliminamos las filas con NAN
    datos = datos.dropna(axis=0, how='any')
    # Añadimos la fecha
    fecha = pd.read_excel(fichero).iloc[4, 0]
    datos['fecha'] = fecha
    # Añadimos el indicador
    datos['i90id'] = hoja
    # Tratamos los datos: convertirmos la hora en fechahora. TODO: falta manejar la hora repetida de otoño
    try:
        datos['periodo'] = pd.to_numeric(datos['periodo'])
    except:
        datos['periodo'] = datos['periodo'].str.extract('^(\d{2})')
        datos['periodo'] = pd.to_numeric(datos['periodo'])
    if max(datos['periodo']) <= 24:
        datos['fechahora'] = fecha + pd.to_timedelta(datos['periodo'] * 3600, unit='s')
    else:
        datos['fechahora'] = fecha + pd.to_timedelta((datos['periodo']-1) * 900, unit='s')
    # eliminamos el periodo y la fecha
    datos = datos.drop('periodo', axis=1)
    datos = datos.drop('fecha', axis=1)

    return datos


fichero = './ficherosi90/I90DIA_20241102.xls'
datos = leer_i90_dia(fichero, 9)
print(datos)
