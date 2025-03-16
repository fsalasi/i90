import pandas as pd
import numpy as np
from datetime import datetime as dt
from pandas import to_numeric
from services.logger import logger
import os

FECHA1 = dt(2018, 6, 13)
FECHA2 = dt(2019, 11, 13)
FECHA3 = dt(2020, 11, 7)
FECHA4 = dt(2020, 12, 24)
FECHA5 = dt(2021, 6, 1)
FECHA6 = dt(2024, 6, 14)

def __get_header(hoja):
    """

    :param hoja:
    :return:
    """
    relacion = {
        1:3, 2:3, 3:2, 4:0, 5:2, 6:2, 7:2, 8:2, 9:2, 10:2, 11:2, 12:2, 13:2, 14:2, 144:2, 15:2, 16:0, 17:2, 18:1,
        19:3, 20:3, 21:3, 22:3, 23:3, 24:3, 25:3, 26:3, 27:3, 28:2, 29:1, 299:2, 30:2, 300:2, 31:0, 32:2, 33:1, 34:2,35:2, 36:3
    }
    return relacion[hoja]


def __get_index_h(hoja):
    """

    :param hoja:
    :return:
    """
    relacion = {
        1: ['Unidad de Programación', 'Tipo Oferta'],
        2: ['Unidad de Programación', 'Tipo Oferta'],
        3: ['Unidad de Programación', 'Redespacho', 'Sentido', 'Nm Oferta asignada', 'Tipo Oferta', 'Tipo cálculo', 'Tipo Restricción'],
        4: [],
        5: ['Unidad de Programación', 'Sentido', 'Nm Oferta asignada', 'Tipo Oferta'],
        6: ['Unidad de Programación', 'Sesión', 'Redespacho', 'Sentido', 'Nm Oferta asignada', 'Tipo Oferta'],
        7: ['Unidad de Programación', 'Redespacho', 'Sentido', 'Tipo Oferta'],
        8: ['Unidad de Programación', 'Redespacho', 'Tipo', 'Sentido', 'Tipo Oferta', 'Tipo cálculo', 'Tipo Restricción', 'Signo de Energía'],
        9: ['Unidad de Programación', 'Redespacho', 'Sentido', 'Tipo Oferta', 'Tipo cálculo'],
        10: ['Unidad de Programación', 'Redespacho', 'Tipo', 'Sentido', 'Tipo Oferta', 'Tipo cálculo', 'Signo de Energía'],
        11: ['Redespacho', 'Tipo'],
        12: ['Unidad de Programación'],
        13: ['Sentido', 'Unidad de Programación', 'Bloque', 'Nº Oferta', 'Tipo Oferta', 'Divisibilidad', 'Indicadores'],
        14: ['Sentido', 'Unidad de Programación', 'Bloque', 'Tipo Oferta', 'Divisibilidad', 'Indicadores'],
        144: ['Sesión', 'Sentido', 'Unidad de Programación', 'Bloque', 'Nº Oferta', 'Tipo Oferta', 'Divisibilidad', 'Rampa Maxima Subir', 'Rampa Maxima Bajar', 'Indicadores'],
        15: ['Sentido', 'Unidad de Programación', 'Bloque', 'Tipo Oferta', 'Indicadores'],
        16: ['Unidad Fisica'],
        17: ['Sentido', 'Unidad de Programación', 'Bloque', 'Tipo Oferta', 'Precedencia', 'Indicadores'],
        18: ['Unidad de Programación'],
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
        29: ['Unidad de Programación'],
        299: ['Unidad de Programación', 'Nm Oferta asignada', 'Tipo Oferta'],
        30: ['Redespacho', 'Tipo Redespacho', 'Sentido', 'Tipo QH', 'Indicadores'],
        300: ['Unidad de Programación', 'Bloque', 'Nº Oferta', 'Tipo Oferta', 'Divisibilad', 'Indicadores'],
        31: [],
        32: ['Sentido', 'Unidad de Programación', 'Bloque', 'Tipo Oferta', 'Indicadores'],
        33: ['Unidad de Programación'],
        34: ['Unidad de Programación', 'Sentido', 'Tipo Restricción'],
        35: ['Unidad de Programación', 'Sentido', 'Tipo Restricción', 'Oferta Compleja'],
        36: ['Unidad de Programación', 'Tipo Oferta']
    }

    return relacion[hoja]


def __get_index_d(hoja):
    """

    :param hoja:
    :return:
    """
    relacion = {
        1: ['Unidad de Programación'],
        2: ['Unidad de Programación'],
        3: ['Unidad de Programación'],
        4: [],
        5: ['Unidad de Programación'],
        6: ['Unidad de Programación'],
        7: ['Unidad de Programación'],
        8: ['Unidad de Programación'],
        9: ['Unidad de Programación'],
        10: ['Unidad de Programación'],
        11: [],
        12: ['Unidad de Programación'],
        13: ['Unidad de Programación'],
        14: ['Unidad de Programación'],
        144: ['Unidad de Programación'],
        15: ['Unidad de Programación'],
        16: ['Unidad Fisica'],
        17: ['Unidad de Programación'],
        18: ['Unidad de Programación'],
        19: ['Unidad de Programación'],
        20: ['Unidad de Programación'],
        21: ['Unidad de Programación'],
        22: ['Unidad de Programación'],
        23: ['Unidad de Programación'],
        24: ['Unidad de Programación'],
        25: ['Unidad de Programación'],
        26: ['Unidad de Programación'],
        27: ['Unidad de Programación'],
        28: ['Unidad de Programación'],
        29: ['Unidad de Programación'],
        299: ['Unidad de Programación'],
        30: [],
        300: ['Unidad de Programación'],
        31: [],
        32: ['Unidad de Programación'],
        33: ['Unidad de Programación'],
        34: ['Unidad de Programación'],
        35: ['Unidad de Programación'],
        36: ['Unidad de Programación']
    }

    return relacion[hoja]


def __parsear_hora(hora_str):
    """

    :param hora_str:
    :return:
    """
    hora_str = str(hora_str)
    if hora_str[-1].lower() == 'a':
        hora_parseada = to_numeric(hora_str[:-1].split('-')[0])
    elif hora_str[-1].lower() == 'b':
        hora_parseada = to_numeric(hora_str[:-1].split('-')[1])
    else:
        hora_parseada = to_numeric(hora_str.split('-')[0])
        hora_parseada = hora_parseada if hora_parseada < 2 else hora_parseada + 1

    return hora_parseada


def __transformar_periodos_a_fechahora(datos):
    """
    """
    max_periodo = datos['periodo'].astype(str).str.extract('^(\d+)').astype(int).max()[0]

    if max_periodo == 100:
        datos['periodo'] = datos['periodo'].astype(str).astype(int)
        datos['fechahora'] = datos['fecha'] + pd.to_timedelta((datos['periodo'] - 1) * 900, unit='s')
        condicion_dst = datos['periodo'] > 12
        datos['fechahora'] = np.where(
            condicion_dst,
            datos['fechahora'].dt.tz_localize('Europe/Madrid', ambiguous=False).dt.tz_convert('UTC') - pd.to_timedelta(3600, unit='s'),
            datos['fechahora'].dt.tz_localize('Europe/Madrid', ambiguous=True).dt.tz_convert('UTC'))

    elif max_periodo == 96:
        datos['periodo'] = datos['periodo'].astype(str).astype(int)
        datos['fechahora'] = ((datos['fecha'] + pd.to_timedelta((datos['periodo'] - 1) * 900, unit='s'))
                              .dt.tz_localize('Europe/Madrid').dt.tz_convert('UTC'))

    elif max_periodo == 92:
        datos['periodo'] = datos['periodo'].astype(str).astype(int)
        datos['fechahora'] = datos['fecha'] + pd.to_timedelta((datos['periodo'] - 1) * 900, unit='s')
        condicion_dst = datos['periodo'] > 8
        datos['fechahora'] = np.where(
            condicion_dst,
            datos['fechahora'].dt.tz_localize('Europe/Madrid').dt.tz_convert('UTC') + pd.to_timedelta(3600, unit='s'),
            datos['fechahora'].dt.tz_localize('Europe/Madrid').dt.tz_convert('UTC'))

    elif max_periodo == 23:
        n_periodos = len(datos.groupby('periodo').size().reset_index(name='Cantidad'))
        if n_periodos > 23:
            datos['hora_parseada'] = datos['periodo'].apply(__parsear_hora).astype(int)
            datos['fechahora'] = datos['fecha'] + pd.to_timedelta(datos['hora_parseada'] * 3600, unit='s')
            condicion_dst = datos['hora_parseada'] > 2
            datos['fechahora'] = np.where(
                condicion_dst,
                datos['fechahora'].dt.tz_localize('Europe/Madrid', ambiguous=False).dt.tz_convert(
                    'UTC') - pd.to_timedelta(3600, unit='s'),
                datos['fechahora'].dt.tz_localize('Europe/Madrid', ambiguous=True).dt.tz_convert('UTC'))
            datos = datos.drop(columns=['hora_parseada'])
        else:
            datos['periodo'] = datos['periodo'].astype(str)
            datos['periodo'] = datos['periodo'].str.extract('^(\d+)').astype(int)
            datos['fechahora'] = datos['fecha'] + pd.to_timedelta(datos['periodo'] * 3600, unit='s')
            datos['fechahora'] = ((datos['fecha'] + pd.to_timedelta(datos['periodo'] * 3600, unit='s'))
                                  .dt.tz_localize('Europe/Madrid').dt.tz_convert('UTC'))

    else:
        print("ERROR EN NUMERO DE PERIODOS")

    return datos


def __reajustar_columnas(fichero, datos, hoja, indiceh):
    """

    :param datos:
    :param hoja:
    :param indiceh:
    :return:
    """
    # Eliminamos las columnas que no sirven
    columnas_a_eliminar = ['Hora', 'Cuarto de Hora del dia', 'Total', 'Total MW',
                           'Total MWh', 'PMP €/MWh', 'Precio Marginal Cuartohorario €/MWh']
    datos = datos.drop(columns=columnas_a_eliminar, errors='ignore')

    # Reajustamos las columnas dobles cuando se dan
    if hoja in [13, 14, 144, 15, 17, 32]:
        datos = datos.rename(columns={'Divisibilad': 'Divisibilidad', 'MW': 'MW.0', '€/MW': '€/MW.0', 'MWh': 'MWh.0', '€/MWh': '€/MWh.0'})
        melted_df = pd.melt(datos, id_vars=indiceh, var_name='Grupo_y_Periodo', value_name='Valor')
        melted_df[['Grupo', 'Periodo']] = melted_df['Grupo_y_Periodo'].str.split('.', expand=True)
        melted_df = melted_df.drop('Grupo_y_Periodo', axis=1)

        if melted_df['Periodo'].astype('int').max() > 24:
            melted_df['Periodo'] = melted_df['Periodo'].astype('int') + 1
        else:
            melted_df['Periodo'] = melted_df['Periodo'].astype('int')
        indiceh = (indiceh + ['Grupo'])
        datos = melted_df.pivot(index=indiceh, columns='Periodo', values='Valor').reset_index()

    # Reajustamos la hoja 30 que tiene el encabezado raro
    if hoja in [30]:
        periodos_hoja_30 = pd.read_excel(fichero, sheet_name=30, header=1).columns.tolist()[6:]
        datos.columns = list(datos.columns[:5]) + periodos_hoja_30

    return datos, indiceh


def __reajustar_filas(datos, hoja, indiceh):
    """

    :param datos:
    :param hoja:
    :param indiceh:
    :return:
    """
    if hoja not in [16, 18, 29, 33]:  # Hojas con datos horarios
        datos = datos.melt(id_vars=indiceh + ['fecha'], var_name='periodo', value_name='valor') # Cambiamos las columnas en filas
        datos = datos.dropna(axis=0, subset=['valor']) # Eliminamos las filas con NAN
        datos = __transformar_periodos_a_fechahora(datos) # Convertimos la hora en fechahora.

    return datos


def __formatear_datos_diarios(datos, hoja, fecha, indiced):
    """

    :param datos:
    :param hoja:
    :param fecha:
    :param indiced:
    :return:
    """
    if hoja not in [16, 18, 29, 33]:  # Hojas con datos horarios
        datosd = datos.drop(columns=['valor', 'fechahora', 'periodo']).drop_duplicates()
    else:
        datosd = datos.drop_duplicates()

    # Creo el id de cada dato diario
    fecha = fecha.strftime('%Y%m%d')
    datosd = datosd.reset_index().drop('index', axis=1)
    datosd['id'] = fecha + str(hoja) + datosd.index.astype(str)

    return datosd


def __formatear_datos_periodo(datos, datos_diarios, hoja, indiceh):
    """

    :param datos:
    :param datos_diarios:
    :param hoja:
    :param indiceh:
    :return:
    """
    if hoja not in [16, 18, 29, 33]:  # Hojas con datos horarios
        datos = datos.drop(columns=['fecha', 'periodo'])
        datos_periodo = (pd.merge(datos_diarios.drop('fecha', axis=1), datos, on=indiceh, how="left").
                         drop(columns=indiceh))
    else:
        datos_periodo = pd.DataFrame()

    return datos_periodo


def leer_i90_dia(fichero, hoja):
    """

    :param fichero:
    :param hoja:
    :return:
    """
    # Leemos la fecha
    fecha = pd.read_excel(fichero).iloc[4, 0]
    logger.debug("leyendo fichero i90: " + fichero + "; hoja: " + str(hoja) + "; fecha: " + fecha.strftime("%Y-%m-%d"))

    # Establecemos exclusiones segun fecha
    if fecha < FECHA1:
        hoja = 144 if hoja == 14 else hoja
        hoja = 300 if hoja == 30 else hoja
        hoja = 299 if hoja == 29 else hoja
        if hoja in [4, 31, 36, 11]:
            return pd.DataFrame(), pd.DataFrame()
    elif fecha < FECHA2:
        hoja = 144 if hoja == 14 else hoja
        hoja = 300 if hoja == 30 else hoja
        hoja = 299 if hoja == 29 else hoja
        if hoja in [4, 31, 11]:
            return pd.DataFrame(), pd.DataFrame()
    elif fecha < FECHA3:
        hoja = 144 if hoja == 14 else hoja
        if hoja in [4, 31, 11, 29, 30]:
            return pd.DataFrame(), pd.DataFrame()
    elif fecha < FECHA4:
        if hoja in [4, 31, 29, 30]:
            return pd.DataFrame(), pd.DataFrame()
    elif fecha < FECHA5:
        if hoja in [4, 31, 30]:
            return pd.DataFrame(), pd.DataFrame()
    elif fecha >= FECHA6:
        if hoja in [4, 31, 22, 23, 24, 25]:
            return pd.DataFrame(), pd.DataFrame()

    # Leemos la hoja del fichero i90
    try:
        datos = pd.read_excel(fichero, sheet_name=hoja, header=__get_header(hoja))
    except Exception as e:
        logger.error(e)
        return pd.DataFrame(), pd.DataFrame()

    # Rescatamos el indice
    indiced = __get_index_d(hoja)
    logger.debug("indiced: " + "; ".join(indiced))
    indiceh = __get_index_h(hoja)
    logger.debug("indiceh: " + "; ".join(indiceh))

    # Reajustamos las columnas necesarias
    logger.debug(datos)
    datos, indiceh = __reajustar_columnas(fichero, datos, hoja, indiceh)
    logger.debug(datos)

    # Añadimos la fecha
    datos['fecha'] = fecha

    # Reajustamos las filas necesarias
    datos = __reajustar_filas(datos, hoja, indiceh)
    logger.debug(datos)

    # Creamos los datos diarios
    datos_diarios = __formatear_datos_diarios(datos, hoja, fecha, indiced)
    logger.debug(datos_diarios)

    # Creo el dataframe de datos por periodo
    datos_periodo = __formatear_datos_periodo(datos, datos_diarios, hoja, indiceh)
    logger.debug(datos_periodo)

    # Ajusto el formato de los datos diarios
    if hoja not in [12]:
        datos_diarios = datos_diarios.melt(id_vars=indiced + ['fecha', 'id'], var_name='parametro',
                             value_name='valor')  # Cambiamos las columnas en filas
    else:
        datos_diarios['parametro'] = ""
        datos_diarios['valor'] = ""
    datos_diarios = datos_diarios.dropna(axis=0, subset=['valor'])  # Eliminamos las filas con NAN

    datos_diarios = datos_diarios.rename(
        columns={'Unidad de Programación': 'upuf', 'Unidad Física': 'upuf', 'Unidad Fisica': 'upuf'})
    if hoja in [11, 30]:  # añado la up vacia en las hojas que no tienen up
        datos_diarios['upuf'] = ""

    return datos_diarios, datos_periodo


#  TODO insertar en ficheros parquet
# pd.set_option('display.max_rows', None)    # Todas las filas
pd.set_option('display.max_columns', None) # Todas las columnas
# pd.set_option('display.width', None)       # Ajustar ancho automáticamente
# pd.set_option('display.max_colwidth', None) #

for f in os.listdir("../ficherosi90"):
    f1 = "../ficherosi90/" + f
    for h in list(range(1, 37)):
        datos_diarios, datos_periodo = leer_i90_dia(f1, h)
        # deslocalizamos
        try:
            datos_periodo['fechahora'] = datos_periodo['fechahora'].dt.tz_localize(None)
        except:
            logger.debug("ERROR fechara en: " + str(h))

        datos_diarios.to_excel("../i90tratadodia/" + f + "_hoja" + str(h) + "_diario.xlsx")
        datos_periodo.to_excel("../i90tratadoperiodo/" + f + "_hoja" + str(h) + "_periodo.xlsx")

# OK Problema de compatibilidad antiguo nuevo en el 11 -> Ahora precios de RR, antes reservada. A PARTIR DEL 07/11/2020 incluido
# OK Problema de compatibilidad antiguo nuevo en el 14 -> Antes habia sesion, numero de oferta, rampa maxima subir, rampa maxima bajar, ahora no aparecen esos campos. A PARTIR DEL 07/11/2020 incluido
# OK Problema de compatibilidad antiguo nuevo en el 22, 23, 24, 25-> Al eliminarse los intras 4-7 quedan sin datos. A PARTIR DEL 14/06/2024
# OK Problema de compatibilidad antiguo nuevo en el 29 -> Antes resultado de RPAS, despues los cambiaron por los tiempos de arranque A PARTIR DEL 13/11/2019 reservada, a partir del 24/12/2020 tiempos de arranque
# OK Problema de compatibilidad antiguo nuevo en el 30 -> Antes ofertas de RPAS, ahora precios terciaria. A PARTIR DEL 13/11/2019 reservada, a partir del 01/06/2021 precios terciaria
# OK Problema de compatibilidad antiguo nuevo en el 36 -> Antes no existia. A PARTIR DEL 13/06/2018
