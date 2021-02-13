import unittest
from flask_webtest import TestApp
from main import app


class ExampleTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.w = TestApp(self.app)

    def test(self):
        r = self.w.get('/')
        self.assertEqual(r.text, 'Hello!')


if __name__ == '__main__':
    unittest.main()
