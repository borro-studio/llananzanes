#!/usr/bin/env python3
"""Descarga y recorta saludos de la tanda.
Uso: baja_saludos.py  (lee pares "identificador url" por la entrada estándar)
Usa tanda/ids.txt (clave identificador) para saber a qué nombre corresponde cada identificador."""
import sys, os, subprocess, urllib.request
T = os.path.expanduser("~/Downloads/llananzanes/_gen/audio/saludos/tanda")
TOOL = os.path.expanduser("~/Downloads/llananzanes/_tools/saludo.py")
key = {}
for l in open(f"{T}/ids.txt"):
    if l.strip(): k, i = l.split(); key[i] = k
n = 0
for l in sys.stdin:
    p = l.split()
    if len(p) != 2: continue
    i, url = p
    if i not in key: print("identificador desconocido:", i); continue
    k = key[i]; raw = f"{T}/raw/{k}.mp3"
    urllib.request.urlretrieve(url, raw)
    d = float(subprocess.check_output(["python3", TOOL, raw, f"{T}/ok/{k}.mp3"]).decode())
    n += 1
    if not 0.45 <= d <= 1.6: print(f"REVISAR {k}: {d:.2f} s")
print(f"descargados {n}; total en ok/: {len(os.listdir(T + '/ok'))}")
