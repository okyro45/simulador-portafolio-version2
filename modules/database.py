import sqlite3

def conectar():

    conn = sqlite3.connect(
        "data/portfolio.db",
        check_same_thread=False
    )

    return conn


def crear_tablas():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS portfolios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        inversionista TEXT,
        moneda TEXT,
        tipo_cambio REAL,
        fecha_creacion TEXT,
        observaciones TEXT
    )
    """)


    cursor.execute("""
CREATE TABLE IF NOT EXISTS acciones(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emisor TEXT,
    ticker TEXT,
    sector TEXT,
    moneda TEXT,
    numero_acciones REAL,
    precio_accion REAL,
    importe_invertido REAL,
    dividendo_pagado REAL,
    dividendo_esperado REAL,
    fecha_compra TEXT,
    fecha_vencimiento TEXT
)
""")

    cursor.execute("""
CREATE TABLE IF NOT EXISTS bonos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emisor TEXT,
    tipo_bono TEXT,
    moneda TEXT,
    valor_nominal REAL,
    importe_invertido REAL,
    cupon_anual REAL,
    tasa_mercado REAL,
    fecha_emision TEXT,
    fecha_vencimiento TEXT
)
""")

    cursor.execute("""
CREATE TABLE IF NOT EXISTS fondos_inmobiliarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emisor TEXT,
    unidades REAL,
    moneda TEXT,
    importe_invertido REAL,
    tasa_anual REAL,
    fecha_inversion TEXT,
    fecha_vencimiento TEXT
)
""")

    cursor.execute("""
CREATE TABLE IF NOT EXISTS fondos_bancarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entidad TEXT,
    fondo TEXT,
    tipo_fondo TEXT,
    moneda TEXT,
    importe_invertido REAL,
    rendimiento_esperado REAL,
    fecha_inversion TEXT,
    fecha_vencimiento TEXT
)
""")

    cursor.execute("""
CREATE TABLE IF NOT EXISTS depositos_plazo(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entidad TEXT,
    moneda TEXT,
    importe REAL,
    tasa_anual REAL,
    fecha_constitucion TEXT,
    fecha_vencimiento TEXT
)
""")

    conn.commit()
    conn.close()

def eliminar_portafolio(id_portafolio):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM portfolios WHERE id = ?",
        (id_portafolio,)
    )

    conn.commit()
    conn.close()

def guardar_accion(
    emisor,
    ticker,
    sector,
    moneda,
    numero_acciones,
    precio_accion,
    importe_invertido,
    dividendo_pagado,
    dividendo_esperado,
    fecha_compra,
    fecha_vencimiento
):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO acciones(
        emisor,
        ticker,
        sector,
        moneda,
        numero_acciones,
        precio_accion,
        importe_invertido,
        dividendo_pagado,
        dividendo_esperado,
        fecha_compra,
        fecha_vencimiento
    )
    VALUES(?,?,?,?,?,?,?,?,?,?,?)
    """,
    (
        emisor,
        ticker,
        sector,
        moneda,
        numero_acciones,
        precio_accion,
        importe_invertido,
        dividendo_pagado,
        dividendo_esperado,
        str(fecha_compra),
        str(fecha_vencimiento)
    ))

    conn.commit()
    conn.close()

def guardar_bono(
    emisor,
    tipo_bono,
    moneda,
    valor_nominal,
    importe_invertido,
    cupon_anual,
    tasa_mercado,
    fecha_emision,
    fecha_vencimiento
):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO bonos(
        emisor,
        tipo_bono,
        moneda,
        valor_nominal,
        importe_invertido,
        cupon_anual,
        tasa_mercado,
        fecha_emision,
        fecha_vencimiento
    )
    VALUES(?,?,?,?,?,?,?,?,?)
    """,
    (
        emisor,
        tipo_bono,
        moneda,
        valor_nominal,
        importe_invertido,
        cupon_anual,
        tasa_mercado,
        str(fecha_emision),
        str(fecha_vencimiento)
    ))

    conn.commit()
    conn.close()

def guardar_fondo_inmobiliario(
    emisor,
    unidades,
    moneda,
    importe_invertido,
    tasa_anual,
    fecha_inversion,
    fecha_vencimiento
):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO fondos_inmobiliarios(
        emisor,
        unidades,
        moneda,
        importe_invertido,
        tasa_anual,
        fecha_inversion,
        fecha_vencimiento
    )
    VALUES(?,?,?,?,?,?,?)
    """,
    (
        emisor,
        unidades,
        moneda,
        importe_invertido,
        tasa_anual,
        str(fecha_inversion),
        str(fecha_vencimiento)
    ))

    conn.commit()
    conn.close()

def guardar_fondo_bancario(
    entidad,
    fondo,
    tipo_fondo,
    moneda,
    importe_invertido,
    rendimiento_esperado,
    fecha_inversion,
    fecha_vencimiento
):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO fondos_bancarios(
        entidad,
        fondo,
        tipo_fondo,
        moneda,
        importe_invertido,
        rendimiento_esperado,
        fecha_inversion,
        fecha_vencimiento
    )
    VALUES(?,?,?,?,?,?,?,?)
    """,
    (
        entidad,
        fondo,
        tipo_fondo,
        moneda,
        importe_invertido,
        rendimiento_esperado,
        str(fecha_inversion),
        str(fecha_vencimiento)
    ))

    conn.commit()
    conn.close()

def guardar_deposito(
    entidad,
    moneda,
    importe,
    tasa_anual,
    fecha_constitucion,
    fecha_vencimiento
):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO depositos_plazo(
        entidad,
        moneda,
        importe,
        tasa_anual,
        fecha_constitucion,
        fecha_vencimiento
    )
    VALUES(?,?,?,?,?,?)
    """,
    (
        entidad,
        moneda,
        importe,
        tasa_anual,
        str(fecha_constitucion),
        str(fecha_vencimiento)
    ))

    conn.commit()
    conn.close()

def eliminar_accion(id_accion):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM acciones WHERE id = ?",
        (id_accion,)
    )

    conn.commit()
    conn.close()

def eliminar_bono(id_bono):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM bonos WHERE id = ?",
        (id_bono,)
    )

    conn.commit()
    conn.close()

def eliminar_fondo_inmobiliario(id_fondo):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM fondos_inmobiliarios WHERE id = ?",
        (id_fondo,)
    )

    conn.commit()
    conn.close()

def eliminar_fondo_bancario(id_fondo):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM fondos_bancarios WHERE id = ?",
        (id_fondo,)
    )

    conn.commit()
    conn.close()

def eliminar_deposito(id_deposito):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM depositos_plazo WHERE id = ?",
        (id_deposito,)
    )

    conn.commit()
    conn.close()