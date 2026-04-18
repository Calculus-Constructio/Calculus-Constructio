from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def hello():
  return render_template("interpreter.html")

@app.route("/interpret/", methods=["POST"])
def interpret():
  code = request.form["code"]
  inp = request.form["input"]
  flag = request.form["flag"]
  return str([code, inp, flag])