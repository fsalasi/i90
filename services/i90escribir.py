import pandas as pd
import os
import shutil
from services.db_pq_handler import escribir_datos_diarios
from services.db_pq_handler import escribir_datos_periodo
from services.logger import logger
from services.i90extraer import leer_i90_dia


def insertar_datos_pq():
    i = 0
    k = 0
    for f in sorted(os.listdir("../ficherosi90"))[:-1]:
        k = k + 1
        f1 = "../ficherosi90/" + f
        for h in list(range(1, 37)):
            datos_diarios, datos_periodo = leer_i90_dia(f1, h)
            if i == 0:
                dd = datos_diarios
                dp = datos_periodo
                i = 1
            else:
                dd = pd.concat([dd, datos_diarios])
                dp = pd.concat([dp, datos_periodo])
        if k % 100 == 0:
            dd['y'] = dd['fecha'].dt.year
            dd['m'] = dd['fecha'].dt.month
            dd['d'] = dd['fecha'].dt.day
            dp['y'] = dp['fechahora'].dt.year
            dp['m'] = dp['fechahora'].dt.month
            dp['d'] = dp['fechahora'].dt.day
            dp['h'] = dp['fechahora'].dt.hour
            escribir_datos_diarios('./parquet_db', dd)
            escribir_datos_periodo('./parquet_db', dp)
            i = 0


def insertar_datos_excel():
    for f in sorted(os.listdir("../ficherosi90"))[:-1]:
        f1 = "../ficherosi90/" + f
        for h in list(range(1, 37)):
            datos_diarios, datos_periodo = leer_i90_dia(f1, h)
            # deslocalizamos
            try:
                datos_periodo['fechahora'] = datos_periodo['fechahora'].dt.tz_localize(None)
            except Exception as e:
                if h not in [16, 18, 29, 33]:
                    logger.error("Error al intentar localizar la fechahora en: " + str(h) + " ERROR: " + str(e))

            datos_diarios.to_excel("../i90tratadodia/" + f + "_hoja" + str(h) + "_diario.xlsx")
            datos_periodo.to_excel("../i90tratadoperiodo/" + f + "_hoja" + str(h) + "_periodo.xlsx")
        shutil.move(f1, "../ficherosi90/leidos/" + f)


def insertar_datos_sql():
    """"""

