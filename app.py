# app.py
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime # Importamos datetime para usar la fecha en el footer de home.html

# Importamos las funciones de la base de datos que definiremos en database.py
from database import get_db, init_db

# Inicializa la aplicación Flask
# static_folder='.' le dice a Flask que busque archivos estáticos (CSS, JS, imágenes)
app = Flask(__name__, static_folder='.', template_folder='templates')


app.secret_key = os.urandom(24)

# --- Configuración de la Base de Datos ---
with app.app_context():
    init_db()


@app.route('/css/<path:filename>')
def serve_css(filename):
    """Sirve archivos CSS desde la carpeta 'css'."""
    return send_from_directory('css', filename)

@app.route('/JS/<path:filename>') # Importante: la carpeta es 'JS' (mayúscula)
def serve_js(filename):
    """Sirve archivos JavaScript desde la carpeta 'JS'."""
    return send_from_directory('JS', filename)

@app.route('/img/<path:filename>')
def serve_img(filename):
    """Sirve archivos de imagen desde la carpeta 'img'."""
    return send_from_directory('img', filename)

@app.route('/iconos-productos/<path:filename>')
def serve_iconos_productos(filename):
    """Sirve archivos de iconos de productos desde la carpeta 'iconos-productos'."""
    return send_from_directory('iconos-productos', filename)


@app.route('/')
def index():
    """Ruta principal de la aplicación. Redirige a 'home' si el usuario está logueado,
    de lo contrario, redirige a 'login'.
    Puedes cambiar esto para que cargue tu index.html original si prefieres que la landing sea pública."""
    if 'username' in session:
        return render_template('home.html', username=session['username'], now=datetime.now())
    return redirect(url_for('login'))

@app.route('/home')
def home():
    """Página de inicio para usuarios logueados (estilo AMD)."""
    if 'username' in session:
        return render_template('home.html', username=session['username'], now=datetime.now())
    flash('Necesitas iniciar sesión para acceder a esta página.', 'warning')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Maneja el registro de nuevos usuarios."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not username or not password or not confirm_password:
            flash('Todos los campos son obligatorios.', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'danger')
            return render_template('register.html')

        hashed_password = generate_password_hash(password)

        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                           (username, hashed_password))
            db.commit() # Guarda los cambios en la base de datos
            flash('Registro exitoso. ¡Ahora puedes iniciar sesión!', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('El nombre de usuario ya existe. Por favor, elige otro.', 'danger')
        except Exception as e:
            flash(f'Ocurrió un error inesperarado: {e}', 'danger')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Maneja el inicio de sesión de usuarios existentes."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone() # Obtiene la primera fila que coincide con el username

        if user and check_password_hash(user['password'], password):
            session['username'] = user['username'] # Almacena el nombre de usuario en la sesión
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('home')) # Redirige a la página de home después del login
        else:
            flash('Nombre de usuario o contraseña incorrectos.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    """Cierra la sesión del usuario."""
    session.pop('username', None) # Elimina la variable 'username' de la sesión
    flash('Has cerrado sesión.', 'info') # Envía un mensaje informativo
    return redirect(url_for('login')) # Redirige al usuario a la página de login


@app.route('/original_index')
def original_index():
    """Sirve tu archivo index.html original."""
    return render_template('index.html')

@app.route('/productos')
def productos():
    """Sirve tu archivo productos.html original."""
    return render_template('productos.html')

# --- Ejecución de la Aplicación Flask ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 