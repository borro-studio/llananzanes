#!/usr/bin/env python3
"""Mide el 'hervor' de píxeles (parpadeo temporal) y la nitidez de un vídeo con distintos filtros.
Uso: hervor.py <video> <inicio_s> <filtro1> [filtro2 ...]   ('null' = sin filtro)
hervor = media de |f[t-1] - 2 f[t] + f[t+1]| en un recorte central (lo que no explica un movimiento uniforme)
nitidez = varianza del laplaciano (más alto = más detalle)"""
import subprocess, sys, os, numpy as np
FF = subprocess.check_output([os.path.join(os.path.dirname(os.path.abspath(__file__)), "vid/bin/python"), "-c", "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"]).decode().strip()
src, t0, filters = sys.argv[1], sys.argv[2], sys.argv[3:]
W = H = 480; N = 50
for f in filters:
    raw = subprocess.run([FF, "-loglevel", "error", "-ss", t0, "-i", src, "-vf", f"{f},crop={W}:{H},format=gray", "-frames:v", str(N), "-f", "rawvideo", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
    d2 = np.abs(a[:-2] - 2 * a[1:-1] + a[2:]).mean()
    lap = (4 * a[:, 1:-1, 1:-1] - a[:, :-2, 1:-1] - a[:, 2:, 1:-1] - a[:, 1:-1, :-2] - a[:, 1:-1, 2:]).var()
    print(f"hervor {d2:5.2f}  nitidez {lap:6.1f}  | {f}")
