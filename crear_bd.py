import sqlite3

DB = "vikingo_gym.db"


def crear_base_datos():
    db = sqlite3.connect(DB)
    c = db.cursor()

    # ---------------- SOCIOS ----------------
    c.execute("""
    CREATE TABLE IF NOT EXISTS socios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT,
        huella TEXT UNIQUE,
        fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
        activo INTEGER DEFAULT 1
    )
    """)

    # ---------------- MEMBRESIAS ----------------
    c.execute("""
    CREATE TABLE IF NOT EXISTS membresias(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        socio_id INTEGER,
        fecha_inicio DATE NOT NULL,
        fecha_vencimiento DATE NOT NULL,
        tipo TEXT,
        precio REAL,
        FOREIGN KEY (socio_id) REFERENCES socios(id)
    )
    """)

    # ---------------- ASISTENCIAS ----------------
    c.execute("""
    CREATE TABLE IF NOT EXISTS asistencias(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        socio_id INTEGER,
        fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (socio_id) REFERENCES socios(id)
    )
    """)

    # ---------------- PAGOS ----------------
    c.execute("""
    CREATE TABLE IF NOT EXISTS pagos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        socio_id INTEGER,
        monto REAL,
        metodo TEXT,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (socio_id) REFERENCES socios(id)
    )
    """)

    db.commit()
    db.close()

    print("✅ Base de datos creada correctamente:", DB)


# Ejecutar creación
if __name__ == "__main__":
    crear_base_datos()