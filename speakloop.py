#!/usr/bin/env python3
import pymarkovchain, subprocess
mc = pymarkovchain.MarkovChain('./lekturov.dat')
while True:
  ret = "%s." % mc.generateString()
  print(ret)
  subprocess.call(["espeak","-v","pl",ret])
