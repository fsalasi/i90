import pandas as pd




def leer_i90_dia_01(fichero):
    # Leemos la hoja DIA01 del fichero i80
    datos = pd.read_excel(fichero, sheet_name=1, header=3)
    # Eliminamos las columnas que no sirven
    datos = datos.drop('Hora', axis=1).drop('Total', axis=1)
    # Renombramos
    datos = datos.rename(columns={'Unidad de Programación': 'up', 'Tipo Oferta': 'pvp - tipo de oferta'})
    # Extraemos los datos que no dependen de la hora
    datos_diarios = datos[['up', 'pvp - tipo de oferta']]
    datos_horarios = datos.drop('pvp - tipo de oferta', axis=1)
    # Añadimos la fecha
    fecha = pd.read_excel(fichero).iloc[4, 0]
    datos_diarios['fecha'] = fecha
    # Cambiamos las columnas de horas en filas
    datos_horarios = datos_horarios.melt(id_vars=['up'], var_name='hora', value_name='pvp')
    # Tratamos los datos: eliminamos las filas con NAN
    datos_horarios = datos_horarios.dropna(axis=0, how='any')
    # Tratamos los datos: convertirmos la hora en fechahora. TODO: falta manejar la hora repetida de otoño
    datos_horarios['hora'] = datos_horarios['hora'].str.extract('^(\d{2})')
    datos_horarios['hora'] = pd.to_numeric(datos_horarios['hora'])
    if max(datos_horarios['hora']) <= 24:
        datos_horarios['fechahora'] = fecha + pd.to_timedelta(datos_horarios['hora'] * 3600, unit='s')
    else:
        datos_horarios['fechahora'] = fecha + pd.to_timedelta(datos_horarios['hora'] * 900, unit='s')
    datos_horarios = datos_horarios.drop('hora', axis=1)

    return datos_diarios, datos_horarios


def leer_i90_dia_02(fichero):
    # Leemos la hoja DIA01 del fichero i80
    datos = pd.read_excel(fichero, sheet_name=2, header=3)
    # Eliminamos las columnas que no sirven
    datos = datos.drop('Cuarto de Hora del dia', axis=1).drop('Total', axis=1)
    # Renombramos
    datos = datos.rename(columns={'Unidad de Programación': 'up', 'Tipo Oferta': 'p48 - tipo de oferta'})
    # Extraemos los datos que no dependen de la hora
    datos_diarios = datos[['up', 'p48 - tipo de oferta']]
    datos_horarios = datos.drop('p48 - tipo de oferta', axis=1)
    # Añadimos la fecha
    fecha = pd.read_excel(fichero).iloc[4, 0]
    datos_diarios['fecha'] = fecha
    # Cambiamos las columnas de horas en filas
    datos_horarios = datos_horarios.melt(id_vars=['up'], var_name='hora', value_name='p48')
    # Tratamos los datos: eliminamos las filas con NAN
    datos_horarios = datos_horarios.dropna(axis=0, how='any')
    # Tratamos los datos: convertirmos la hora en fechahora. TODO: falta manejar la hora repetida de otoño
    if datos_horarios['hora'].dtype == 'str':
        datos_horarios['hora'] = datos_horarios['hora'].str.extract('^(\d{2})')
    else:
        datos_horarios['hora'] = datos_horarios['hora'] - 1
    datos_horarios['hora'] = pd.to_numeric(datos_horarios['hora'])
    if max(datos_horarios['hora']) <= 24:
        datos_horarios['fechahora'] = fecha + pd.to_timedelta(datos_horarios['hora'] * 3600, unit='s')
    else:
        datos_horarios['fechahora'] = fecha + pd.to_timedelta(datos_horarios['hora'] * 900, unit='s')
    datos_horarios = datos_horarios.drop('hora', axis=1)

    return datos_diarios, datos_horarios


fichero = './ficherosi90/I90DIA_20241102.xls'
diarios, horarios = leer_i90_dia_02(fichero)
