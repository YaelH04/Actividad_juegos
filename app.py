import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from models import db, Juego, User
import controlador_juegos
from auth import auth
from flask_login import LoginManager, login_required
from api import api_bp
from werkzeug.exceptions import HTTPException

# Configuración de Sentry
sentry_sdk.init(
    dsn="https://6f995efacb1ddd93122a390d13cb7628@o4510321944231936.ingest.us.sentry.io/4510321956814848",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0
)

app = Flask(__name__)

if not app.debug:
    file_handler = logging.FileHandler('errors.log')
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(file_handler)
# -----------------------------------------------

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hola123@localhost/juegos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Clave_Super_Secreta'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
login_manager.session_protection = 'strong'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(api_bp, url_prefix='/api')

@app.route("/")
@app.route("/juegos")
def juegos():
    juegos = controlador_juegos.obtener_juegos()
    return render_template("juegos.html", juegos=juegos)

# Rutas protegidas
@app.route("/agregar_juego")
@login_required
def formulario_agregar_juego():
    return render_template("agregar_juego.html")

@app.route("/guardar_juego", methods=["POST"])
@login_required
def guardar_juego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador_juegos.insertar_juego(nombre, descripcion, precio)
    flash('Juego agregado exitosamente', 'success')
    return redirect(url_for("juegos"))

@app.route("/eliminar_juego", methods=["POST"])
@login_required
def eliminar_juego():
    controlador_juegos.eliminar_juego(request.form["id"])
    flash('Juego eliminado', 'success')
    return redirect(url_for("juegos"))

@app.route("/formulario_editar_juego/<int:id>")
@login_required
def editar_juego(id):
    juego = controlador_juegos.obtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=juego)

@app.route("/actualizar_juego", methods=["POST"])
@login_required
def actualizar_juego():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador_juegos.actualizar_juego(nombre, descripcion, precio, id)
    flash('Juego actualizado', 'success')
    return redirect(url_for("juegos"))

@app.route('/test/400')
def test_400():
    abort(400)

@app.route('/test/404')
def test_404():
    abort(404)

@app.route('/test/500')
def test_500():
    x = 1 / 0
    return "No llegaras aquí"
# ------------------------------------------

# --- Manejadores de errores ---
@app.errorhandler(500)
def handle_500(e):
    if request.path.startswith('/api'):
        return jsonify(error="Internal Server Error"), 500
    return render_template('500.html'), 500

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    if request.path.startswith('/api'):
        response = e.get_response()
        response.data = jsonify({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }).data
        response.content_type = "application/json"
        return response

    template_map = {
        400: '400.html',
        404: '404.html',
        405: '405.html',
    }
    template = template_map.get(e.code)
    
    if template:
        return render_template(template, error=e), e.code
    else:
        return e

# --------------------------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)