# services/db_sql_handler.py
"""Script con funciones para gestionar la base de datos.
"""


# Librerias
import mysql.connector
import json
from services.logger import logger
from datetime import datetime as dt
from constants import DATETIME_MYSQL_FORMAT, DATE_MYSQL_FORMAT, DBTBDIARIOS, DBTBHORARIOS
from runtimeConstants import DBUSER, DBPWD, DBHOST, DBPORT, DBDB


# Propietario
__author__ = "Francisco Salas"
__copyright__ = "Copyright 2025"
__license__ = "GPL 3.0"
__maintainer__ = "Francisco Salas"
__email__ = "fsalasi93@gmail.com"
__status__ = "Dev"


# Funcion para escribir datos en db
def escribir_datos_diarios(datos):
    """
    Funcion que recibe los datos diarios del i90 y construye una
    query para escribir los datos en DB

    Parameters
    ----------
    datos : dict
        Diccionario con los datos a insertar
    """

    # plantilla de la query para insertar los datos
    query = (("INSERT INTO %TB% " +
             "(fecha, i90dia, id, upuf, parametro, valor) " +
             "VALUES ").
             replace('%TB%', DBTBDIARIOS))

    # plantilla de cada linea de insercion
    query_valores = "('{fecha}', '{i90dia}', {id}, {upuf}, {parametro}, {valor})"

    # final de la query de insercion para actualizar los datos en caso de que la clave primaria este repetida
    query_final = ("ON DUPLICATE KEY UPDATE fecha=VALUES(fecha), i90dia=VALUES(i90dia), " +
                  "id=VALUES(id), upuf = VALUES(upuf), parametro = VALUES(parametro), valor = VALUES(valor)")

    # bucle que construye las lineas de la query a partir de los datos del diccionario de entrada
    i = 0
    for fila in datos:
        fila['fecha'] = (
            dt.fromisoformat(fila['fecha']).strftime(DATE_MYSQL_FORMAT))
        if i == 0:
            i = 1
            query = query + query_valores.format(**fila)
        else:
            query = query + ", " + query_valores.format(**fila)

    # se añade el final de la query
    query = query + " " + query_final

    # se ejecuta la query mediante la funcon interna de escribir
    __sql_escribir_query(query, DBUSER, DBPWD, DBHOST, str(DBPORT), DBDB)


def escribir_datos_horarios(datos):
    """
    Funcion que recibe los datos horarios del i90 y construye una
    query para escribir los datos en DB

    Parameters
    ----------
    datos : dict
        Diccionario con los datos a insertar
    """

    # plantilla de la query para insertar los datos
    query = (("INSERT INTO %TB% " +
             "(id, fechahora_utc, valor) " +
             "VALUES ").
             replace('%TB%', DBTBHORARIOS))

    # plantilla de cada linea de insercion
    query_valores = "({id}, {fechahora_utc}, {valor})"

    # final de la query de insercion para actualizar los datos en caso de que la clave primaria este repetida
    query_final = "ON DUPLICATE KEY UPDATE id=VALUES(id), fechahora_utc=VALUES(fechahora_utc), valor = VALUES(valor)"

    # bucle que construye las lineas de la query a partir de los datos del diccionario de entrada
    i = 0
    for fila in datos:
        fila['fechahora_utc'] = (
            dt.fromisoformat(fila['fechahora_utc']).strftime(DATETIME_MYSQL_FORMAT))
        if i == 0:
            i = 1
            query = query + query_valores.format(**fila)
        else:
            query = query + ", " + query_valores.format(**fila)

    # se añade el final de la query
    query = query + " " + query_final

    # se ejecuta la query mediante la funcon interna de escribir
    __sql_escribir_query(query, DBUSER, DBPWD, DBHOST, str(DBPORT), DBDB)


# Funcion para crear las tablas en db
def crear_tablas():
    """
    Funcion que crea las tablas necesarias para la aplicación
    en caso de que no existan
    """

    # Se indica la query para crear las tablas
    query1 = (("CREATE TABLE IF NOT EXISTS %TB% ("
             "fecha DATE, "
             "i90dia TINYINT, "
             "id VARCHAR(50), "
             "upuf VARCHAR(50), "
             "parametro VARCHAR(100), "
             "valor DECIMAL(14, 4), "
             "PRIMARY KEY (id));").
             replace('%TB%', DBTBDIARIOS))

    query2 = (("CREATE TABLE IF NOT EXISTS %TB% ("
               "id VARCHAR(50), "
               "fechahora_utc DATETIME, "
               "valor DECIMAL(14, 4), "
               "PRIMARY KEY (id, fechahora_utc));").
              replace('%TB%', DBTBHORARIOS))
    
    # se ejecuta la query mediante la funcon interna de escribir
    __sql_escribir_query(query1, DBUSER, DBPWD, DBHOST, str(DBPORT), DBDB)
    __sql_escribir_query(query2, DBUSER, DBPWD, DBHOST, str(DBPORT), DBDB)


# Funcion para ejecutar querys de escritura en base de datos
def __sql_escribir_query(sql_query, user, pwd, host, port, db):
    """
    Ejecuta una query de escritura
    sql en la base de datos proporcionada.

    Parameters
    ----------
    sql_query : str
        Query que se quiere ejecutar.
    user : str
        Usuario para acceder a la db
    pwd : str
        Contraseña para acceder a la db
    host : str
        IP o direccion del host a conectar
    port : str
        Puerto del host a conectar
    db : str
        base de datos a la que conectarse
    """

    # MYSQL CONNECTION - Carga de datos en MYSQL
    logger.debug("Conectando con DB...")

    conn = mysql.connector.connect(user=user, password=pwd, host=host, port=port, database=db, collation='utf8mb4_bin')

    conn.autocommit = False
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query)
        conn.commit()
        # MSG exito
        logger.debug("query ejecutada con exito")

    except Exception as e:
        # MSG Error
        logger.error(e)

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            logger.debug("Cerrando conexión con la base de datos... Ok")


# Funcion para ejecutar querys de lectura en base de datos
def __sql_leer_query(sql_query, user, pwd, host, port, db):
    """
    Ejecuta una query de lectura
    sql en la base de datos proporcionada.
    y devuelve los datos en formato json

    Parameters
    ----------
    sql_query : str
        Query que se quiere ejecutar.
    user : str
        Usuario para acceder a la db
    pwd : str
        Contraseña para acceder a la db
    host : str
        IP o direccion del host a conectar
    port : str
        Puerto del host a conectar
    db : str
        base de datos a la que conectarse

    Returns
    ------
    datos : str
        datos descargados indexados en formato json.
    """

    # MYSQL CONNECTION - Carga de datos en MYSQL
    logger.info("Conectando con DB...")

    conn = mysql.connector.connect(user=user, password=pwd, host=host, port=port, database=db)
    conn.autocommit = False
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query)
        datos = cursor.fetchall()
        conn.commit()
        # MSG exito
        logger.info("query ejecutada con exito")

    except Exception as e:
        # MSG Error
        logger.error(e)
        datos = {}

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            logger.debug("Cerrando conexión con la base de datos... Ok")

    return json.dumps(dict(datos))
