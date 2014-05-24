#!/usr/bin/env python3
from flask import Flask, request, url_for, redirect
import pymarkovchain

app = Flask(__name__)

mc = pymarkovchain.MarkovChain('./lekturov')

history = []

@app.route('/favicon.ico')
def favicon():
  return redirect(url_for('static', filename='favicon.ico'))

def getrandom():
  ret = ""
  while len(ret) < 10:
    ret = mc.generateString()
  history.append(ret)
  return "%s." % ret

@app.route('/')
def randomhtml():
  return """<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Suche Lektury</title></head><body><h1>Suche lektury</h1><blockquote>%s</blockquote><a href="%s">Generuj</a></body></html>""" % (getrandom(), url_for("randomhtml"))

@app.route('/txt')
def randomtxt():
  return getrandom()

@app.route('/history')
def historyhtml():
  return """<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Suche Lektury</title></head><body><h1>Suche Lektury</h1><h2>Historia</h2><ul><li>%s</li></ul></body></html>""" % "</li><li>".join(history)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8082)
