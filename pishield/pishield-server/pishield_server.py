from flask import Flask
from routes.api import api
from routes.home import home
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.register_blueprint(api)

app.secret_key = os.environ.get("CHAVE_FLASK")

app.run('0.0.0.0', 80, debug=True)
