# Constants
"""Script que define las constantes de la aplicacion.
"""

# Librerias
from datetime import datetime as dt

# Propietario
__author__ = "Francisco Salas"
__copyright__ = "Copyright 2025"
__license__ = "GPL 3.0"
__maintainer__ = "Francisco Salas"
__email__ = "fsalasi93@gmail.com"
__status__ = "Dev"


# Constantes de configuracion
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
DATETIME_MYSQL_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_MYSQL_FORMAT = '%Y-%m-%d'
CONFIG_FILE = '/data/config.yml'
DEFAULT_DPOST = 1
DEFAULT_DPRE = 3
DEFAULT_ESIOSID = 600
DEFAULT_ESIOSGEO = '""'
DEFAULT_CRONMIN=0
DEFAULT_CRONHOUR=0
DEFAULT_CRONDAYOFMONTH=1
DEFAULT_CRONMONTH=1
DEFAULT_CRONDAYOFWEEK=1
DOCKER_WORKDIR="/code"
DBTBDIARIOS = 'tb_i90_diario'
DBTBHORARIOS = 'tb_i90_horario'
FECHA1 = dt(2018, 6, 13)
FECHA2 = dt(2019, 11, 13)
FECHA3 = dt(2020, 10, 7)
FECHA4 = dt(2020, 12, 24)
FECHA5 = dt(2021, 6, 1)
FECHA6 = dt(2024, 6, 14)


# Mensajes de error
ERROR_JOB_SIN_DATOS = ("La funcion esios.solicitar_decarga() no ha devuelto datos. " +
                       "Quiza se haya producido un error de lectura. " +
                       "No se ha solicitado ninguna escritura en DB.")

ERROR_LECTURA_CONF = ("Se ha producido un error al leer %VAR% del archivo de configuracion. " +
                      "Escribiendo el valor por defecto... Descripcion del error: ")

ERROR_CREAR_CRONTAB = ("Se ha producido un error al intentar " +
                       "formar el archivo crontab. Descripcion del error: ")
