import os
import unittest

from src import app

class BasicTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def register(self, email, password, confirm):
        return self.app.post(
            '/register',
            data=dict(email=email, password=password, confirm=confirm),
            follow_redirects=True
        )
 
    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )
    
    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

if __name__ == "__main__":
    unittest.main()