import unittest

class TestAPIBasica(unittest.TestCase):
    def test_import_modulo(self):
        from src.api.app import app, CLASSES_MAP
        self.assertIsNotNone(app)
        self.assertEqual(CLASSES_MAP[0], "Normal")
        self.assertEqual(CLASSES_MAP[3], "Cavitação e Superaquecimento")

    def test_rotas_definidas(self):
        from src.api.app import app
        rotas = [route.path for route in app.routes]
        self.assertIn("/", rotas)
        self.assertIn("/health", rotas)
        self.assertIn("/predict", rotas)

if __name__ == "__main__":
    unittest.main()
