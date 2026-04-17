from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello! I am currently not implemented yet!"

@app.route("/interpret/<hex>")
def interpret(hex):
  code = bytes.fromhex(hex)
  return code
