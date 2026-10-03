#!/usr/bin/env python3
"""Transcribe los saludos de la web y marca los que no dicen "Hola, <nombre>".
Uso: vid/bin/python revisa_saludos.py [clave ...]   (sin claves: todos)"""
import json, os, sys, unicodedata, difflib
from faster_whisper import WhisperModel
R = os.path.expanduser("~/Downloads/llananzanes")
WEB = f"{R}/web/assets/audio/saludos"
nombres = json.load(open(f"{R}/_gen/audio/saludos/nombres.json"))
plano = lambda t: "".join(c for c in unicodedata.normalize("NFD", t.lower()) if c.isalpha())
m = WhisperModel("small", device="cpu", compute_type="int8")
claves = sys.argv[1:] or sorted(nombres)
mal = []
for k in claves:
    seg, _ = m.transcribe(f"{WEB}/{k}.mp3", language="es", beam_size=5, condition_on_previous_text=False)
    txt = " ".join(s.text.strip() for s in seg)
    p = plano(txt)
    hola = p.startswith("hola")
    resto = p[4:] if hola else p
    sim = max(difflib.SequenceMatcher(None, resto, plano(x)).ratio() for x in (nombres[k]["nombre"], nombres[k]["voz"]))
    if not hola or sim < 0.6:
        mal.append(k)
        print(f"REVISAR {k}: «{txt}» (hola={hola}, parecido={sim:.2f})", flush=True)
print(f"revisados {len(claves)}; dudosos {len(mal)}: {' '.join(mal)}")
