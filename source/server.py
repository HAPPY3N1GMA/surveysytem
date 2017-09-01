from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "Highly secret key"


users = {"admin": "password"}
authenticated = 0


def errorMSG(filename,msg):
	print("\033[91m {}\033[00m" .format("Server Error:"+" ("+filename+") "+msg))
