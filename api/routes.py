from flask_restful import Resource, reqparse, fields, marshal_with, marshal
from flask import request
from . import api

from models import Juego, db

juego_fields = {
    'id': fields.Integer,
    'nombre': fields.String,
    'descripcion': fields.String,
    'precio': fields.Float  # Usar fields.Float o fields.String para el precio
}

class JuegoList(Resource):

    # Maneja la lista de juegos. Permite obtener todos los juegos y crear uno nuevo.

    @marshal_with(juego_fields) 
    def get(self):
        """Obtiene la lista completa de juegos."""
        juegos = Juego.query.all()
        return juegos

    def post(self):
        # Crea un nuevo juego.
        # Requiere 'id', 'nombre', 'descripcion' y 'precio' en el cuerpo del JSON.
        # Devuelve 400 si los datos son insuficientes.
        data = request.json
        
        # Validar que todos los campos requeridos estén presentes
        required_fields = ['nombre', 'descripcion', 'precio']
        if not data or not all(field in data for field in required_fields):
            return {'error': 'Datos insuficientes. Se requieren los campos: nombre, descripcion, precio.'}, 400

        nuevo_juego = Juego(
            nombre=data['nombre'],
            descripcion=data.get('descripcion'),
            precio=data.get('precio')
        )
        db.session.add(nuevo_juego)
        db.session.commit()
        return marshal(nuevo_juego, juego_fields), 201

class JuegoResource(Resource):
    # Maneja un juego individual. Permite obtener, actualizar o eliminar un juego por su ID.

    @marshal_with(juego_fields)
    def get(self, id):
        # Obtiene un juego específico por su ID.
        juego = Juego.query.get_or_404(id)
        return juego

    @marshal_with(juego_fields)
    def put(self, id):
        """
        Actualiza un juego existente.
        Los campos a actualizar se envían en el cuerpo del JSON.
        """
        juego = Juego.query.get_or_404(id)
        data = request.json
        
        if not data:
            return {'error': 'No se enviaron datos para actualizar.'}, 400

        # Actualiza los campos
        juego.nombre = data.get('nombre', juego.nombre)
        juego.descripcion = data.get('descripcion', juego.descripcion)
        juego.precio = data.get('precio', juego.precio)
        
        db.session.commit()
        return juego

    def delete(self, id):
        """
        Elimina un juego específico por su ID.
        Devuelve 204 No Content si la eliminación es exitosa.
        """
        juego = Juego.query.get_or_404(id)
        db.session.delete(juego)
        db.session.commit()
        return '', 204

api.add_resource(JuegoList, '/juegos')
api.add_resource(JuegoResource, '/juegos/<int:id>')