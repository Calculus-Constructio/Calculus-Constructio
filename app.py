from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
  return render_template("interpreter.html")

@app.route("/interpret/<hex_code>/<hex_input>/<flags>")
def interpret(hex_code, hex_input, flags):
  try:
    code = bytes.fromhex(hex_code)
    inp = bytes.fromhex(hex_input)
    flag = int(flags)
    return code, inp, flags
  except ValueError:
    return "ValueError, you didn't specify something correctly!"
