import urllib3
import datetime as dt
import os
import zipfile
import time


def descargari90(fecha):
    # url-ejemplo: https://api.esios.ree.es/archives/34/download?date_type=datos&end_date=2024-08-15T23%3A59%3A59%2B00%3A00&locale=es&start_date=2024-08-15T00%3A00%3A00%2B00%3A00
    url_base = ("https://api.esios.ree.es/archives/34/download?date_type=datos&end_date=" +
                "%FECHA%T23%3A59%3A59%2B00%3A00&locale=es&start_date=%FECHA%T00%3A00%3A00%2B00%3A00")
    fecha = fecha.strftime("%Y-%m-%d")
    url = url_base.replace("%FECHA%", fecha)
    print(url)
    http = urllib3.PoolManager()
    respuesta = http.request('GET', url)

    ruta = './ficherosi90/' + fecha + '.zip'

    with open(ruta, 'wb') as out:
        out.write(respuesta.data)

    respuesta.release_conn()


def extraer_zips(ruta):
    """
    Extrae todos los ficheros .zip de un directorio.

    Args:
      ruta: La ruta al directorio que contiene los ficheros .zip.
    """

    for fichero in os.listdir(ruta):
        if fichero.endswith(".zip"):
            ruta_completa = os.path.join(ruta, fichero)
            with zipfile.ZipFile(ruta_completa, 'r') as zip_ref:
                zip_ref.extractall(ruta)

    for fichero in os.listdir(ruta):
        if fichero.endswith(".zip"):
            ruta_completa = os.path.join(ruta, fichero)
            with zipfile.ZipFile(ruta_completa, 'r') as zip_ref:
                zip_ref.extractall(ruta)

    for fichero in os.listdir(ruta):
        if fichero.endswith(".zip"):
            ruta_completa = os.path.join(ruta, fichero)
            with zipfile.ZipFile(ruta_completa, 'r') as zip_ref:
                zip_ref.extractall(ruta)


def eliminar_zips(ruta):
  """
  Elimina todos los archivos .zip de un directorio.

  Args:
    ruta: La ruta al directorio que contiene los archivos .zip.
  """

  for fichero in os.listdir(ruta):
    if fichero.endswith(".zip"):
      ruta_completa = os.path.join(ruta, fichero)
      os.remove(ruta_completa)




# inicio = dt.datetime(2020, 1, 1)
# fin = dt.datetime(2025, 1, 1)
#
# errores = ""
# fecha_actual = inicio
# while fecha_actual <= fin:
#     time.sleep(2)
#     try:
#         descargari90(fecha_actual)
#         extraer_zips('./ficherosi90')
#         eliminar_zips('./ficherosi90')
#     except:
#         errores = errores + "\nerror en: " + fecha_actual.strftime("%Y-%m-%d")
#
#     fecha_actual += dt.timedelta(days=1)
#
# print(errores)

