import sqlite3

def get_db():
    # ruta a la base de datos
    conn = sqlite3.connect("data/incendios.db") 
    conn.row_factory = sqlite3.Row
    return conn

