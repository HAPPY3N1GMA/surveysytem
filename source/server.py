from flask import Flask
app = Flask(__name__)
app.config["SECRET_KEY"] = "Highly secret key"


users = {"admin":"password"}