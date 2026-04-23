from flask import Flask, render_template, request
import os
import shlex
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
  dom = "temp_programs/" + token_hex(64)
  no_inp = False
  with open(dom + ".cns", "x") as cod:
    cod.write(code)
  if inp != '':
    with open(dom + ".txt", "x") as inn:
      inn.write(inp)
  else:
      no_inp = True
  c_path = os.path.abspath(dom + ".cns")
  i_path = os.path.abspath(dom + ".txt")
  p_path = "calculus_constructio/main.py"
  try:
    data = subprocess.run(shlex.split(f'python "{p_path}" -p "{c_path}" {f"-i {i_path}" if not no_inp else ""} -f {flag}'), capture_output=True, text=True, timeout=60)
    out_warning = len(data.stdout) > 128000
    err_warning = len(data.stderr) > 128000
    try:
      os.remove(c_path)
    except:
      pass
    try:
      os.remove(i_path)
    except:
      pass
    return {"output": data.stdout[:128000], "error": data.stderr[:128000], "timeout_warning": False, "memory_warning": {"stdout": out_warning, "stderr": err_warning}}
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
    out_warning = len(data.stdout) > 128000
    err_warning = len(data.stderr) > 128000
    try:
      os.remove(c_path)
    except:
      pass
    try:
      os.remove(i_path)
    except:
      pass
    return {"output": out[:128000], "error": err[:128000], "timeout_warning": True, "memory_warning": {"stdout": out_warning, "stderr": err_warning}}
