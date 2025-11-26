import unittest, json
from app import create_app, db
from models import Juego

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context(); self.ctx.push()
        db.create_all()
        db.session.add(Juego(nombre='X' , descripcion='Y', precio=1.23))
        db.session.commit()

    def tearDown(self):
        db.session.remove(); db.drop_all(); self.ctx.pop()
    
    def test_get_juegos(self):
        resp = self.client.get('/api/juegos')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(data, list)


if __name__ == '__main__':
    unittest.main()