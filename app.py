#!/usr/bin/env python3
from flask import Flask, request, url_for, redirect, g, render_template
import pymarkovchain, sqlite3, logging, json

app = Flask(__name__)
DATABASE = "stuff.sqlite"
mc = pymarkovchain.MarkovChain('./lekturov.dat')
bookfile = logging.getLogger("book")
bookfile.setLevel(logging.DEBUG)
bookfileh = logging.FileHandler("lekturov.txt")
bookfilef = logging.Formatter("%(message)s ")
bookfileh.setFormatter(bookfilef)
bookfile.addHandler(bookfileh)

history = []
for row in sqlite3.connect(DATABASE).cursor().execute("SELECT stuffie FROM stuff"):
  history.append(row[0])

def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = sqlite3.connect(DATABASE)
  return db

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()

@app.route('/favicon.ico')
def favicon():
  return redirect(url_for('static', filename='favicon.ico'))

def getrandom():
  ret = ""
  while len(ret) < 10:
    ret = "%s." % mc.generateString()
  history.append(str(ret))
  bookfile.warning(str(ret))
  get_db().cursor().execute("INSERT INTO stuff (stuffie) VALUES (?)", (str(ret),))
  get_db().commit()
  return ret

@app.route('/')
def randomhtml():
  return render_template("home.html", text=getrandom(), linkclear=url_for("randomhtml"), linkhistory=url_for("historyhtml"), linkjson=url_for("randomjson"))

@app.route('/txt')
def randomtxt():
  return getrandom()

@app.route('/json')
def randomjson():
  return json.dumps({"text":getrandom()})

@app.route('/history')
def historyhtml():
  getrandom()
  return render_template("history.html", text=" ".join(history), linkjson=url_for("randomjson"))

@app.route('/history/txt')
def historytxt():
  getrandom()
  return " ".join(history)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8084)
