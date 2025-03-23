import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime as dt
import os


def crear_tablas(ruta_db):
    """

    :param ruta_db:
    :return:
    """

    os.makedirs(os.path.join(ruta_db, "i90db", "i90diario"), exist_ok=True)
    os.makedirs(os.path.join(ruta_db, "i90db", "i90periodos"), exist_ok=True)


def escribir_datos_diarios(ruta_db, datos):
    """

    :param ruta_db:
    :param datos : pandas.DataFrame:
    :return:
    """
    # Obtener las combinaciones únicas de año y mes para las particiones
    partition_cols = ['y', 'm']
    partitions = datos.groupby(partition_cols).groups

    for partition_values in partitions:
        # Crear directorio de partición si no existe
        partition_dir = os.path.join(
            os.path.join(ruta_db, "i90db", "i90diario"),
            f"y={partition_values[0]}", f"m={partition_values[1]}")
        os.makedirs(partition_dir, exist_ok=True)

        # Filtrar el DataFrame para la partición actual
        partition_df = datos[(datos['y'] == partition_values[0]) & (datos['m'] == partition_values[1])]

        # Crear tabla de PyArrow para la partición
        partition_table = pa.Table.from_pandas(partition_df)

        # Generar un nombre de archivo con fecha y hora
        now = dt.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")  # Formato año mes dia, hora minutos segundos
        file_name = f"data_{timestamp}.parquet"

        # Escribir archivo Parquet para la partición
        file_path = os.path.join(partition_dir, file_name)  # Nombre de archivo único
        pq.write_table(partition_table, file_path)


def escribir_datos_periodo(ruta_db, datos):
    """

    :param ruta_db:
    :param datos : pandas.DataFrame:
    :return:
    """
    # Obtener las combinaciones únicas de año y mes para las particiones
    partition_cols = ['y', 'm']
    partitions = datos.groupby(partition_cols).groups

    for partition_values in partitions:
        # Crear directorio de partición si no existe
        partition_dir = os.path.join(
            os.path.join(ruta_db, "i90db", "i90periodos"),
            f"y={partition_values[0]}", f"m={partition_values[1]}")
        os.makedirs(partition_dir, exist_ok=True)

        # Filtrar el DataFrame para la partición actual
        partition_df = datos[(datos['y'] == partition_values[0]) & (datos['m'] == partition_values[1])]

        # Crear tabla de PyArrow para la partición
        partition_table = pa.Table.from_pandas(partition_df)

        # Generar un nombre de archivo con fecha y hora
        now = dt.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")  # Formato año mes dia, hora minutos segundos
        file_name = f"data_{timestamp}.parquet"

        # Escribir archivo Parquet para la partición
        file_path = os.path.join(partition_dir, file_name)  # Nombre de archivo único
        pq.write_table(partition_table, file_path)