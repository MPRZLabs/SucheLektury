#!/usr/bin/env python3
import os, pymarkovchain
import logging as l
l.basicConfig(level=l.INFO)
l.info("Opening database file")
mc = pymarkovchain.MarkovChain('./lekturov.dat')
tekst = ""
l.info("Looking for .txt files")
for f in os.listdir():
  if "txt" in os.path.splitext(f)[1]:
    l.info("Appending %s" % f)
    with open(f) as lektura:
      tekst = """%s
%s""" % (tekst, lektura.read())
l.info("Generating database")
mc.generateDatabase(tekst)
l.info("Saving database")
mc.dumpdb()
