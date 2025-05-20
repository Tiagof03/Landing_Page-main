# database.py
import sqlite3

# Nombre del archivo de la base de datos SQLite.
# Este archivo se creará en el mismo directorio donde ejecutes app.py o database.py.
DATABASE = 'database.db'

def get_db():
    """
    Establece una conexión a la base de datos SQLite y configura el row_factory.
    El row_factory permite acceder a las columnas por nombre (ej. user['username']).
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Inicializa la base de datos creando la tabla 'users' si aún no existe.
    Esta tabla almacenará la información de los usuarios (id, username, password hash).
    """
    with get_db() as db: # Usa 'with' para asegurar que la conexión se cierre correctamente
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        ''')
        db.commit() # Guarda los cambios (creación de la tabla) en la base de datos

if __name__ == '__main__':
    # Si ejecutas este archivo directamente (python3 database.py),
    # inicializará la base de datos y creará la tabla 'users'.
    init_db()
    print(f"Base de datos '{DATABASE}' inicializada y tabla 'users' creada/verificada.")