from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Juego(db.Model):
    __tablename__ = 'juegos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Numeric(9,2), nullable=False)

class User(db.Model, UserMixin):
    __tablename__ = 'users' 
    
    # Campos de la base de datos
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(256))

    # Propiedad de contraseña (solo escritura)
    @property
    def password(self):
        raise AttributeError('password is write-only')

    # Hashear la contraseña
    @password.setter
    def password(self, pwd): 
        self.password_hash = generate_password_hash(pwd)

    # Verificar la contraseña
    def verify_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)

    def __repr__(self):
        return f'<User {self.username}>'