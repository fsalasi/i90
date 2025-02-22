# runtimeConstants.py
"""Script que lee el archivo de variables de entorno
y copia sus valores en constantes de python.
"""


# Librerias
from os import environ
from config import load_env_all_files


# Propietario
__author__ = "Francisco Salas"
__copyright__ = "Copyright 2025"
__license__ = "GPL 3.0"
__maintainer__ = "Francisco Salas"
__email__ = "fsalasi93@gmail.com"
__status__ = "Dev"


# Se leen todos los archivos de entorno
load_env_all_files()


# Se escriben las variables de entorno en constantes
APIESIOSHOST = str(environ.get("APIESIOSHOST", "esiosconn"))
APIESIOSPORT = int(environ.get("APIESIOSPORT", "5000"))
DBUSER = str(environ.get("DBUSER"))
DBPWD = str(environ.get("DBPWD"))
DBHOST = str(environ.get("DBHOST", "esiosdb-mariadb"))
DBPORT = int(environ.get("DBPORT", "3306"))
DBDB = str(environ.get("DBDB", "fsiesios"))
DBTB = str(environ.get("DBTB", "tb_esios"))
