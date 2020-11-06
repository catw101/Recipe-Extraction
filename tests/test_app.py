from .exapp import index
from .exapp import link_route
from flask import Flask
import json

def test_index():
    app = Flask(__name__)
    index()
    client = app.test_client()
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200