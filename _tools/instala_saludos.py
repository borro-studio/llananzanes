#!/usr/bin/env python3
"""Instala en la web los saludos recortados de la tanda.
Cada saludo se coloca al final de un hueco fijo de 2,9 s (silencio delante) para que
termine justo cuando arranca la locución, y se regenera saludos/index.json.
Uso: instala_saludos.py [carpeta_ok] [--pisar]
Sin --pisar no toca los saludos que ya están en la web."""
import json, os, re, subprocess, sys
R = os.path.expanduser("~/Downloads/llananzanes")
args = [a for a in sys.argv[1:] if not a.startswith("--")]
PISAR = "--pisar" in sys.argv
OK, WEB = (os.path.abspath(args[0]) if args else f"{R}/_gen/audio/saludos/tanda/ok"), f"{R}/web/assets/audio/saludos"
FF = subprocess.check_output([f"{R}/_tools/vid/bin/python", "-c", "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"]).decode().strip()
HUECO = 2.9
nombres = json.load(open(f"{R}/_gen/audio/saludos/nombres.json"))
n = 0
for k in sorted(nombres):
    out = f"{WEB}/{k}.mp3"
    if os.path.exists(out) and not PISAR: continue
    src = f"{OK}/{k}.mp3"
    if not os.path.exists(src): print(f"FALTA {k}"); continue
    log = subprocess.run([FF, "-i", src, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", log).groups()
    d = float(h) * 3600 + float(m) * 60 + float(s)
    pico = float(re.search(r"max_volume: (-?[\d.]+) dB", log).group(1))
    if pico < -6 or pico > -0.3: print(f"REVISAR volumen {k}: pico {pico} dB")
    ms = max(0, round((HUECO - d) * 1000))
    subprocess.check_call([FF, "-y", "-loglevel", "error", "-i", src, "-af", f"adelay={ms},apad=whole_dur={HUECO}",
        "-ac", "1", "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "64k", out])
    n += 1
claves = sorted(f[:-4] for f in os.listdir(WEB) if f.endswith(".mp3") and f != "generico.mp3")
json.dump(claves, open(f"{WEB}/index.json", "w"), separators=(",", ":"))
print(f"instalados {n}; en la web: {len(claves)} nombres")
