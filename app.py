from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Juego, User
import controlador_juegos
from auth import auth
from flask_login import LoginManager, login_required
from api import api_bp
from werkzeug.exceptions import HTTPException, BadRequest, MethodNotAllowed

login_manager = LoginManager()

def create_app(config_name='default'):
    app = Flask(__name__)

    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hola123@localhost/juegos'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'Clave_Super_Secreta'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
    login_manager.session_protection = 'strong'

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')

    register_routes(app)
    register_error_handlers(app)

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def register_routes(app):
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

def register_error_handlers(app):
    @app.errorhandler(BadRequest)
    def handle_400(e):
        return render_template('400.html'), 400

    @app.errorhandler(404)
    def handle_404(e):
        return render_template('404.html'), 404

    @app.errorhandler(MethodNotAllowed)
    def handle_405(e):
        return render_template('405.html'), 405

    @app.errorhandler(500)
    def handle_500(e):
        return render_template('500.html'), 500

    @app.errorhandler(HTTPException)
    def handle_api_error(e):
        if request.path.startswith('/api'):
            response = e.get_response()
            response.data = jsonify(code=e.code, name=e.name, description=e.description).data
            response.content_type = 'application/json'
            return response
        return e

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)