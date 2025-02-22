# config.py
"""Script que define la funcion para leer
los archivos con variables de entorno.
"""

# Librerias
import os
from dotenv import load_dotenv
from constants import DOCKER_WORKDIR


# Propietario
__author__ = "Francisco Salas"
__copyright__ = "Copyright 2025"
__license__ = "GPL 3.0"
__maintainer__ = "Francisco Salas"
__email__ = "fsalasi93@gmail.com"
__status__ = "Dev"


# Funcion para leer archivos de variables de entornio
def load_env_all_files():
    """
    Funcion que busca y lee todos los archivos con variables
    de entorno segun el directorio de configuracion.
    """

    # Se lee el directorio
    env_folder = DOCKER_WORKDIR

    # Se buscan todos los archivos .env en el directorio
    for file_name in os.listdir(env_folder):
        if file_name == '.env':
            env_file = os.path.join(env_folder, file_name)
            # Se procesa el arvhico .env con la libreria dotenv
            load_dotenv(env_file)
