import sqlite3
URL_DB = 'AIM.db'

def cargardatos(sql) ->list:
    """"voy a hacer una consulta a la base de datos"""
    try:
        with sqlite3.connect(URL_DB) as conec:
            cur = conec.cursor()
            res = cur.execute(sql).fetchall()
    except Exception:
        res = None
    return res
