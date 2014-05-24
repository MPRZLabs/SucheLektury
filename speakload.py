#!/usr/bin/env python3
import urllib.request, subprocess
while True:
  ret = urllib.request.urlopen("http://127.0.0.1:8082/txt").read()
  print(ret.decode())
  subprocess.call(["espeak","-v","pl",ret])
