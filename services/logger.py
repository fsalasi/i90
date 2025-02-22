# services/logger.py
"""Script para crear y configurar el logger que
se usara en la aplicacion
"""


# Librerias
import logging


# Propietario
__author__ = "Francisco Salas"
__copyright__ = "Copyright 2025"
__license__ = "GPL 3.0"
__maintainer__ = "Francisco Salas"
__email__ = "fsalasi93@gmail.com"
__status__ = "Dev"


# Configuracion basica del logger
logging.basicConfig(
    format="%(asctime)s (%(levelname)s) %(message)s",
    datefmt="[%Y-%m-%d %H:%M:%S]",
)

# Creamos el logger para usar en la aplicacion
logger = logging.getLogger(__name__)

# Configuramos el nivel de logging deseado
logger.setLevel(logging.DEBUG)
