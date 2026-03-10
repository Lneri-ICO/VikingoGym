import sqlite3
from error_reporter import report_error

DB = "vikingo_gym.db"


# ---------------- CONEXION ----------------
def conectar():
    try:
        return sqlite3.connect(DB)
    except Exception as e:
        report_error(e, "database.py")
        raise


# ---------------- CREAR TABLAS ----------------
def crear_tablas():
    try:
        db = conectar()
        c = db.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS socios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            vencimiento TEXT,
            huella TEXT UNIQUE
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS asistencias(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            socio_id INTEGER,
            fecha TEXT
        )
        """)

        db.commit()

    except Exception as e:
        report_error(e, "database.py")

    finally:
        db.close()


# ---------------- REGISTRAR SOCIO ----------------
def registrar_socio(nombre, telefono, vencimiento, huella):

    try:
        db = conectar()
        c = db.cursor()

        c.execute(
            "INSERT INTO socios(nombre,telefono,vencimiento,huella) VALUES(?,?,?,?)",
            (nombre, telefono, vencimiento, huella)
        )

        db.commit()

    except sqlite3.IntegrityError:
        print("⚠️ Esa huella ya está registrada")

    except Exception as e:
        report_error(e, "database.py")

    finally:
        db.close()


# ---------------- BUSCAR POR HUELLA ----------------
def buscar_por_huella(huella):

    try:
        db = conectar()
        c = db.cursor()

        c.execute(
            "SELECT id,nombre,vencimiento FROM socios WHERE huella=?",
            (huella,)
        )

        dato = c.fetchone()

        return dato

    except Exception as e:
        report_error(e, "database.py")

    finally:
        db.close()


# ---------------- REGISTRAR ASISTENCIA ----------------
def registrar_asistencia(socio_id, fecha):

    try:
        db = conectar()
        c = db.cursor()

        c.execute(
            "INSERT INTO asistencias(socio_id,fecha) VALUES(?,?)",
            (socio_id, fecha)
        )

        db.commit()

    except Exception as e:
        report_error(e, "database.py")

    finally:
        db.close()


def obtener_socios():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, nombre, telefono, vencimiento
        FROM socios
        ORDER BY nombre
    """)

    datos = cur.fetchall()

    conn.close()

    return datos


def buscar_socio_nombre(nombre):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, nombre, telefono, vencimiento
        FROM socios
        WHERE nombre LIKE ?
    """, (f"%{nombre}%",))

    datos = cur.fetchall()

    conn.close()

    return datos