import pandas as pd


def get_header(hoja):
    relacion = {
        1: 3, 2:3, 3:2, 5:2, 6:2, 7:2, 8:2, 9:2, 10:2, 12:2, 13:2, 14:2, 15:2, 17:2, 19:3, 20:3,
        21:3, 22:3, 23:3, 24:3, 25:3, 26:3, 27:3, 28:2, 29:2, 32:2, 34:2,35:2, 36:3
    }
    return relacion[hoja]


def get_index_vars(hoja):
    relacion = {
        1: ['Unidad de Programación', 'Tipo Oferta'],
        2: ['Unidad de Programación', 'Tipo Oferta'],
        3: ['Unidad de Programación', 'Redespacho', 'Sentido', 'Nm Oferta asignada', 'Tipo Oferta', 'Tipo cálculo', 'Tipo Restricción'],
        5: ['Unidad de Programación', 'Sentido', 'Nm Oferta asignada', 'Tipo Oferta'],
        6: ['Unidad de Programación', 'Sesión', 'Redespacho', 'Sentido', 'Nm Oferta asignada', 'Tipo Oferta'],
        7: ['Unidad de Programación', 'Redespacho', 'Sentido', 'Tipo Oferta'],
        8: ['Unidad de Programación', 'Redespacho', 'Tipo', 'Sentido', 'Tipo Oferta', 'Tipo cálculo', 'Tipo Restricción', 'Signo de Energía'],
        9: ['Unidad de Programación', 'Redespacho', 'Sentido', 'Tipo Oferta', 'Tipo cálculo'],
        10: ['Unidad de Programación', 'Redespacho', 'Tipo', 'Sentido', 'Tipo Oferta', 'Tipo cálculo', 'Signo de Energía'],
        12: ['Unidad de Programación'],
        13: ['Sentido', 'Unidad de Programación', 'Bloque', 'Nº Oferta', 'Tipo Oferta', 'Divisibilidad', 'Indicadores'],
        14: ['Sentido', 'Unidad de Programación', 'Bloque', 'Tipo Oferta', 'Divisibilidad', 'Indicadores'],
        15: ['Sentido', 'Unidad de Programación', 'Bloque', 'Tipo Oferta', 'Indicadores'],
        17: ['Sentido', 'Unidad de Programación', 'Bloque', 'Tipo Oferta', 'Precedencia', 'Indicadores'],
        19: ['Unidad de Programación', 'Tipo Oferta'],
        20: ['Unidad de Programación', 'Tipo Oferta'],
        21: ['Unidad de Programación', 'Tipo Oferta'],
        22: ['Unidad de Programación', 'Tipo Oferta'],
        23: ['Unidad de Programación', 'Tipo Oferta'],
        24: ['Unidad de Programación', 'Tipo Oferta'],
        25: ['Unidad de Programación', 'Tipo Oferta'],
        26: ['Unidad de Programación', 'Tipo Oferta', 'Tipo Transacción'],
        27: ['Unidad de Programación', 'Tipo Oferta', 'Nº contrato'],
        28: ['Unidad de Programación', 'Sentido', 'Nm Oferta asignada', 'Tipo Oferta', 'Origen'],
        29: ['Unidad de Programación', 'Tipo Oferta', 'Nm Oferta asignada'],
        32: ['Sentido', 'Unidad de Programación', 'Bloque', 'Tipo Oferta', 'Indicadores'],
        34: ['Unidad de Programación', 'Sentido', 'Tipo Restricción'],
        35: ['Unidad de Programación', 'Sentido', 'Tipo Restricción', 'Oferta Compleja'],
        36: ['Unidad de Programación', 'Tipo Oferta']
    }

    return relacion[hoja]


def leer_i90_dia(fichero, hoja):
    # Leemos la hoja del fichero i90
    datos = pd.read_excel(fichero, sheet_name=hoja, header=get_header(hoja))

    # Eliminamos las columnas que no sirven
    columnas_a_eliminar = ['Hora', 'Cuarto de Hora del dia', 'Total', 'Total MW', 'Total MWh', 'PMP €/MWh']
    datos = datos.drop(columns=columnas_a_eliminar, errors='ignore')

    # Rescatamos el indice
    indice = get_index_vars(hoja)

    # Reajustamos las columnas dobles cuando se dan
    if hoja in [13, 14, 15, 17, 32]:
        datos = datos.rename(columns={'MW': 'MW.0', '€/MW': '€/MW.0', 'MWh': 'MWh.0', '€/MWh': '€/MWh.0'})
        melted_df = pd.melt(datos, id_vars=indice, var_name='Grupo_y_Periodo', value_name='Valor')
        melted_df[['Grupo', 'Periodo']] = melted_df['Grupo_y_Periodo'].str.split('.', expand=True)
        melted_df = melted_df.drop('Grupo_y_Periodo', axis=1)
        melted_df['Periodo'] = melted_df['Periodo'].astype('int') + 1
        indice = (indice + ['Grupo'])
        datos = melted_df.pivot(index=indice, columns='Periodo', values='Valor').reset_index()

    # Cambiamos las columnas de horas en filas
    datos = datos.melt(id_vars=indice, var_name='periodo', value_name='valor')

    # Tratamos los datos: eliminamos las filas con NAN
    datos = datos.dropna(axis=0, subset=['valor'])

    # Añadimos la fecha
    fecha = pd.read_excel(fichero).iloc[4, 0]
    datos['fecha'] = fecha

    # Tratamos los datos: convertimos la hora en fechahora. TODO: falta manejar la hora repetida de otoño
    datos['periodo'] = datos['periodo'].astype(str)
    datos['periodo'] = datos['periodo'].str.extract('^(\d+)')
    datos['periodo'] = pd.to_numeric(datos['periodo'], errors='coerce')

    max_periodo = datos['periodo'].max()
    es_cuarto_de_hora = max_periodo <= 24 if pd.notna(max_periodo) else False
    datos['fechahora'] = fecha + pd.to_timedelta(datos['periodo'] * 3600, unit='s') \
        if es_cuarto_de_hora else fecha + pd.to_timedelta((datos['periodo']-1) * 900, unit='s')

    # TODO: tratamiento de hojas con solo datos diarios

    # creo el dataframe de datos diarios
    fecha = fecha.strftime('%Y%m%d')
    datos_diarios = datos.drop(columns=['valor', 'fechahora', 'periodo']).drop_duplicates()
    datos_diarios = datos_diarios.reset_index().drop('index', axis=1)
    datos_diarios['id'] = fecha + str(hoja) + datos_diarios.index.astype(str)

    # creo el dataframe de datos por periodo
    datos = datos.drop(columns=['fecha', 'periodo'])
    datos_diarios = datos_diarios.drop('fecha', axis=1)
    datos_periodo = (pd.merge(datos_diarios, datos, on=indice, how="left").
                     drop(columns=indice))

    return datos_diarios, datos_periodo


# TODO insertar en base de datos
pd.set_option('display.max_columns', None)
fichero = './ficherosi90/I90DIA_20150101.xls'
datos_diarios, datos_periodo = leer_i90_dia(fichero, 17)
print(datos_diarios)

# TODO Problema decompatibilidad antiguo nuevo en el 22, 23, 24, 25, 29 -> Al eliminarse los intras 4-7 quedan sin datos
# TODO Problema decompatibilidad antiguo nuevo en el 13, 14 -> Parece que no hay divisibilidad en el antiguo