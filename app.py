from flask import Flask, render_template, request
import os
import subprocess
from secrets import token_hex

app = Flask(__name__)

@app.route("/")
def hello():
  return render_template("interpreter.html")

@app.route("/interpret/", methods=["POST"])
def interpret():
  code = request.json["code"]
  inp = request.json["input"]
  flag = request.json["flag"]
  dom = token_hex(64)
  with open(dom + ".cns", "x") as cod, open(dom + ".txt", "x") as inn:
    cod.write(code)
    inn.write(inp)
  c_path = os.path.abspath(dom + ".cns")
  i_path = os.path.abspath(dom + ".txt")
  p_path = "calculus_constructio/main.py"
  try:
    data = subprocess.run(f'python "{p_path}" -p "{c_path}" -i "{i_path}"', capture_output=True, text=True, timeout=60)
    return {"output": data.stdout, "error": data.stderr, "timeout_warning": False}
  except subprocess.TimeoutExpired as e:
    out = e.stdout
    if out is None:
      out = ''
    else:
      out = out.decode('utf-8')
    err = e.stderr
    if err is None:
      err = ''
    else:
      err = err.decode('utf-8')
    return {"output": out, "error": err, "timeout_warning": True}
