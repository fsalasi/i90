# services/extraeri90.py
"""Script con funciones para gestionar la extraccion de datos de
los ficheros i90.

Notas:
- Problema de compatibilidad antiguo nuevo en el 11 -> Ahora precios de RR, antes reservada. A PARTIR DEL 07/10/2020 incluido
- Problema de compatibilidad antiguo nuevo en el 22, 23, 24, 25-> Al eliminarse los intras 4-7 quedan sin datos. A PARTIR DEL 14/06/2024
- Problema de compatibilidad antiguo nuevo en el 29 -> Antes resultado de RPAS, despues los cambiaron por los tiempos de arranque A PARTIR DEL 13/11/2019 reservada, a partir del 24/12/2020 tiempos de arranque
- Problema de compatibilidad antiguo nuevo en el 30 -> Antes ofertas de RPAS, ahora precios terciaria. A PARTIR DEL 13/11/2019 reservada, a partir del 01/06/2021 precios terciaria
- Problema de compatibilidad antiguo nuevo en el 36 -> Antes no existia. A PARTIR DEL 13/06/2018
"""

# Librerias
import pandas as pd
import numpy as np
from pandas import to_numeric
from services.logger import logger
from constants import FECHA1, FECHA2, FECHA3, FECHA4, FECHA5, FECHA6


# Propietario
__author__ = "Francisco Salas"
__copyright__ = "Copyright 2025"
__license__ = "GPL 3.0"
__maintainer__ = "Francisco Salas"
__email__ = "fsalasi93@gmail.com"
__status__ = "Dev"


# Funcion que mapea el numero de filas de header de cada hoja
def __get_header(hoja):
    """
    Funcion que mapea el numero de filas de cabecera de cada hoja
    del i90. Las hojas que han cambiado de formato se identifican repitiendo el
    ultimo numero de cada hoja (la 30 seria la 300) en las versiones mas antiguas
    (queda el numero de hoja correcto de la version mas reciente).

    Parameters
    ----------
    hoja : int
        Identificador (numero) de la hoja del fichero i90.

    Returns
    ------
    relacion : int
        numero de filas de la cabecera de la hoja del fichero excel i90
    """

    # Mapeo de hoja y numero de filas de encabezado
    relacion = {
        1:3, 2:3, 3:2, 4:0, 5:2, 6:2, 7:2, 8:2, 9:2, 10:2, 11:2, 12:2, 13:2, 14:2, 15:2, 16:0, 17:2, 18:1,
        19:3, 20:3, 21:3, 22:3, 23:3, 24:3, 25:3, 26:3, 27:3, 28:2, 29:1, 299:2, 30:2, 300:2, 31:0, 32:2, 33:1, 34:2,35:2, 36:3
    }
    return relacion[hoja]


# Funcion que detecta automaticamente los campos generales previos a los datos horarios
def __get_index_h_inteligent(datos):
    """
    Funcion que detecta automaticamente los campos generales
    previos a los datos horarios, basandose en una serie de campos bisagra.
    Devuelve como resultado una lista con el índice.

    Parameters
    ----------
    datos : pd.DataFrame
        DataFrame de pandas con los datos a tratar.

    Returns
    ------
    index : list
        lista con el nombre de las cloumnas del encabezado
    """

    # Inicializamos las variables
    index = []
    k = 0

    # Identificamos el nombre de los campos visagra
    columnas_a_eliminar = ['Hora', 'Cuarto de Hora del dia', 'Total', 'Total MW',
                           'Total MWh', 'PMP €/MWh', 'Precio Marginal Cuartohorario €/MWh']

    # Se genera una lista con valores booleanos correspondiente a cada campo, siendo "True"
    # si corresponden a un campo bisagra, y "False" en caso contrario
    iterador = [elemento in columnas_a_eliminar for elemento in datos.columns]

    # Se itera sobre la lista booleana, identificando los valores previos a la bisagra
    for i in iterador:
        if not i:
            index.append(datos.columns[k])
        else:
            break
        k = k + 1

    return index


# Funcion que devuelve una lista con los nombre del encabezado de cada hoja del fichero i90
def __get_index_h(hoja):
    """
    Funcion que devuelve una lista con los nombres de las columnas comunes a todas
    las horas de cada hoja del fichero i90.

    Parameters
    ----------
    hoja : int
        Identificador (numero) de la hoja del fichero i90.

    Returns
    ------
    relacion : list
        lista con el nombre de las cloumnas del encabezado
    """

    # Mapeo de hoja y nombres de columnas
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
        299: ['Unidad de Programación', 'Nm Oferta asignada', 'Tipo Oferta'],
        30: ['Redespacho', 'Tipo Redespacho', 'Sentido', 'Tipo QH', 'Indicadores'],
        300: ['Unidad de Programación', 'Bloque', 'Nº Oferta', 'Tipo Oferta', 'Divisibilidad', 'Indicadores'],
        31: [],
        32: ['Sentido', 'Unidad de Programación', 'Bloque', 'Tipo Oferta', 'Indicadores'],
        34: ['Unidad de Programación', 'Sentido', 'Tipo Restricción'],
        35: ['Unidad de Programación', 'Sentido', 'Tipo Restricción', 'Oferta Compleja'],
        36: ['Unidad de Programación', 'Tipo Oferta']
    }

    return relacion[hoja]


# Funcion que devuelve una lista con los nombre del encabezado de cada hoja del fichero i90
def __get_index_d(hoja):
    """
    Funcion que devuelve una lista con los nombres de las columnas comunes a todas
    los dias de cada hoja del fichero i90.

    Parameters
    ----------
    hoja : int
        Identificador (numero) de la hoja del fichero i90.

    Returns
    ------
    relacion : list
        lista con el nombre de las cloumnas del encabezado
    """

    # Mapeo de hoja y nombres de columnas
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


# Funcion para interpretar la hora repetida del cambio de hora
def __parsear_hora(hora_str):
    """
    Funcion que lee la hora repetida del dia del cambio de hora y la transforma
    segun su correspondiente hora en UTC y el formato recibido. Dependiendo de si los
    datos corresponden a una hoja con datos horarios o no, la hora sra un entero o
    un string, y podra ser en formato de periodods cuartohorarios o en formato de
    horas. Cuando son horas, el i90 identifica la hora repetida con un caracter 'a'
    o 'b'.

    Parameters
    ----------
    hora_str : str o int
        Identificador (numero) de la hora. Puede ser un periodo (int) o un indicador
        de la hora en formato hh-hh (str)

    Returns
    ------
    hora_parseada : numeric
        hora transformada en entero y con el cambio de hora correcto
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


# Funcion que recibe el dataset con fechas y periodos y los transforma en fechahora
def __transformar_periodos_a_fechahora(datos):
    """
    Funcion que recibe el dataset con fechas y periodos, horarios o cuartohorarios,
    y crea una nueva variable en formato fechahora UTC (ya salvando el cambio de hora).

    Parameters
    ----------
    datos : pd.DataFrame
        DataFrame de pandas con los datos a tratar.

    Returns
    ------
    datos : pd.DataFrame
        DataFrame de pandas con los datos tratados.
    """

    # Obtenemos el periodo maximo para interpretar el tipo de formato en el que se encuentran expresados
    max_periodo = datos['periodo'].astype(str).str.extract('^(\d+)').astype(int).max()[0]

    # Si el periodo maximo es 100, se trata de periodos cuartohorarios y cambio de hora de otoño
    if max_periodo == 100:
        # Nos aseguramos de que todos los datos estan en int
        datos['periodo'] = datos['periodo'].astype(str).astype(int)
        # Creamos la fechahora
        datos['fechahora'] = datos['fecha'] + pd.to_timedelta((datos['periodo'] - 1) * 900, unit='s')
        # Gestionamos el cambio de hora para pasarlo a UTC
        condicion_dst = datos['periodo'] > 12
        datos['fechahora'] = np.where(
            condicion_dst,
            datos['fechahora'].dt.tz_localize('Europe/Madrid', ambiguous=False).dt.tz_convert('UTC') - pd.to_timedelta(3600, unit='s'),
            datos['fechahora'].dt.tz_localize('Europe/Madrid', ambiguous=True).dt.tz_convert('UTC'))

    # Si el periodo maximo es 100, se trata de periodos cuartohorarios
    elif max_periodo == 96:
        # Nos aseguramos de que todos los datos estan en int
        datos['periodo'] = datos['periodo'].astype(str).astype(int)
        # Creamos la fechahora y convertimos a UTC
        datos['fechahora'] = ((datos['fecha'] + pd.to_timedelta((datos['periodo'] - 1) * 900, unit='s'))
                              .dt.tz_localize('Europe/Madrid').dt.tz_convert('UTC'))

    # Si el periodo maximo es 100, se trata de periodos cuartohorarios y cambio de hora de primavera
    elif max_periodo == 92:
        # Nos aseguramos de que todos los datos estan en int
        datos['periodo'] = datos['periodo'].astype(str).astype(int)
        # Creamos la fechahora
        datos['fechahora'] = datos['fecha'] + pd.to_timedelta((datos['periodo'] - 1) * 900, unit='s')
        # Gestionamos el cambio de hora para pasarlo a UTC
        condicion_dst = datos['periodo'] > 8
        datos['fechahora'] = np.where(
            condicion_dst,
            datos['fechahora'].dt.tz_localize('Europe/Madrid').dt.tz_convert('UTC') + pd.to_timedelta(3600, unit='s'),
            datos['fechahora'].dt.tz_localize('Europe/Madrid').dt.tz_convert('UTC'))

    # Si el periodo maximo es 23, se trata de periodos horarios
    elif max_periodo == 23:
        # Calculamos el numero de periodos para verificar si estamos en un dia con cambio de hora
        n_periodos = len(datos.groupby('periodo').size().reset_index(name='Cantidad'))

        if n_periodos > 23: # Cambio de hora de otoño (cuando viene en formato 'a' - 'b'
            # parseamos la hora para que se cambie de forma correcta
            datos['hora_parseada'] = datos['periodo'].apply(__parsear_hora).astype(int)
            # Creamos la variable fechahora
            datos['fechahora'] = datos['fecha'] + pd.to_timedelta(datos['hora_parseada'] * 3600, unit='s')
            # Convertimos en UTC de forma correcta
            condicion_dst = datos['hora_parseada'] > 2
            datos['fechahora'] = np.where(
                condicion_dst,
                datos['fechahora'].dt.tz_localize('Europe/Madrid', ambiguous=False).dt.tz_convert('UTC') -
                pd.to_timedelta(3600, unit='s'),
                datos['fechahora'].dt.tz_localize('Europe/Madrid', ambiguous=True).dt.tz_convert('UTC'))
            datos = datos.drop(columns=['hora_parseada'])
        else: # Resto de casos
            # Aseguramos que todos los registros son string
            datos['periodo'] = datos['periodo'].astype(str)
            # Extraemos la hora de cada identificador (hh1-hh2)
            datos['periodo'] = datos['periodo'].str.extract('^(\d+)').astype(int)
            # Convierto a fechahora
            datos['fechahora'] = datos['fecha'] + pd.to_timedelta(datos['periodo'] * 3600, unit='s')
            # Transformo a UTC
            datos['fechahora'] = datos['fechahora'].dt.tz_localize('Europe/Madrid').dt.tz_convert('UTC')

    # Si el periodo maximo es 22, se trata de periodos horarios y cambio de hora de primavera, y ademas significa
    # que la hora vien en formato entero, no string (corresponde a las hojas con columnas dobles)
    elif max_periodo == 22:
        # Me aseguro de que todos los registros son int
        datos['periodo'] = datos['periodo'].astype(str).astype(int)
        # Gestionamos el cambio de hora y convertimos a UTC
        condicion_dst = datos['periodo'] > 1
        datos['fechahora'] = np.where(
            condicion_dst,
            datos['fecha'] + pd.to_timedelta((datos['periodo'] + 1) * 3600, unit='s'),
            datos['fecha'] + pd.to_timedelta(datos['periodo'] * 3600, unit='s'))
        datos['fechahora'] = datos['fechahora'].dt.tz_localize('Europe/Madrid').dt.tz_convert('UTC')

    # Si el periodo maximo es 24, se trata de periodos horarios y cambio de hora de otoño, y ademas significa
    # que la hora vien en formato entero, no string (corresponde a las hojas con columnas dobles)
    elif max_periodo == 24:
        # Me aseguro de que todos los registros son int
        datos['periodo'] = datos['periodo'].astype(str).astype(int)
        # Convierto todos los registros a fechahora
        datos['fechahora'] = datos['fecha'] + pd.to_timedelta(datos['periodo'] * 3600, unit='s')
        # Gestiono el cambio de hora y transformo a UTC
        condicion_dst = datos['periodo'] > 2
        datos['fechahora'] = np.where(
            condicion_dst,
            datos['fechahora'].dt.tz_localize('Europe/Madrid', ambiguous=False).dt.tz_convert('UTC') -
            pd.to_timedelta(3600, unit='s'),
            datos['fechahora'].dt.tz_localize('Europe/Madrid', ambiguous=True).dt.tz_convert('UTC'))

    else:
        # Si no se corresponde con ninguno de los casos de control, se emite un error ya que no
        # es posible gestionar el caso.
        raise Exception("ERROR EN NUMERO DE PERIODOS")

    return datos


# Funcion para reajustar la estructura y formato de las columnas del DataFrame TODO: limpio hasta aqui
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

    # Ponemos a 0 los NAs de la primera fila para tener datos en todos los periodos
    datos.iloc[0] = datos.iloc[0].fillna(0)

    # Reajustamos las columnas dobles cuando se dan
    if hoja in [13, 14, 15, 17, 300, 32]:
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
    if hoja not in [16, 18, 29, 33]:  # Excluimos las hojas con solo datos diarios
        datos = datos.melt(id_vars=indiceh + ['fecha'], var_name='periodo', value_name='valor') # Cambiamos las columnas en filas
        datos = datos.dropna(axis=0, subset=['valor']) # Eliminamos las filas con NAN
        try:
            datos = __transformar_periodos_a_fechahora(datos) # Convertimos la hora en fechahora.
        except Exception as e:
            raise Exception(str(e))

    return datos


def __formatear_datos_diarios(datos, hoja, fecha):
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
    hoja_ori = hoja
    if fecha < FECHA1:
        hoja = 300 if hoja == 30 else hoja
        hoja = 299 if hoja == 29 else hoja
        if hoja in [4, 31, 36, 11]:
            return pd.DataFrame(), pd.DataFrame()
    elif fecha < FECHA2:
        hoja = 300 if hoja == 30 else hoja
        hoja = 299 if hoja == 29 else hoja
        if hoja in [4, 31, 11]:
            return pd.DataFrame(), pd.DataFrame()
    elif fecha < FECHA3:
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
        datos = pd.read_excel(fichero, sheet_name=hoja_ori, header=__get_header(hoja))
    except Exception as e:
        logger.error("Error al leer el fichero excel: " + str(e))
        return pd.DataFrame(), pd.DataFrame()

    if datos.empty:
        logger.error("No hay datos en la hoja")
        return pd.DataFrame(), pd.DataFrame()

    # Rescatamos el indice
    indiced = __get_index_d(hoja)
    # logger.debug("indiced: " + "; ".join(indiced))
    indiceh = __get_index_h_inteligent(datos)
    # logger.debug("indiceh: " + "; ".join(indiceh))

    # Reajustamos las columnas necesarias
    # logger.debug(datos)
    datos, indiceh = __reajustar_columnas(fichero, datos, hoja, indiceh)
    # logger.debug(datos)

    # Añadimos la fecha
    datos['fecha'] = fecha

    # Reajustamos las filas necesarias
    try:
        datos = __reajustar_filas(datos, hoja, indiceh)
    except Exception as e:
        logger.error("Error al ajustar las filas: " + str(e))
        return pd.DataFrame(), pd.DataFrame()
        # logger.debug(datos)

    # Creamos los datos diarios
    datos_diarios = __formatear_datos_diarios(datos, hoja, fecha)
    # logger.debug(datos_diarios)

    # Creo el dataframe de datos por periodo
    datos_periodo = __formatear_datos_periodo(datos, datos_diarios, hoja, indiceh)
    # logger.debug(datos_periodo)

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
