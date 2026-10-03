#!/usr/bin/env python3
"""Monta el vídeo de portada (35 s) a partir del promocional del cliente.
Uso: montaje.py <video_origen> <salida.mp4> [ancho alto] [audio.mp3]
Los tiempos son los del vídeo original; cambiar CLIPS para ajustar la selección."""
import subprocess, sys, os
FF = subprocess.check_output([os.path.join(os.path.dirname(__file__), "vid/bin/python"), "-c", "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"]).decode().strip()
src, out = sys.argv[1], sys.argv[2]
W, H = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (640, 360)
audio = sys.argv[5] if len(sys.argv) > 5 else None
X = 0.6  # duración de cada fundido encadenado
CLIPS = [  # (inicio en segundos, duración, descripción)
    (176.5, 6.0, "valle, plano general"),
    (159.5, 5.0, "la casa con el valle detrás"),
    (29.0, 6.0, "órbita cercana a la casa"),
    (70.0, 5.0, "la casa en picado con la finca"),
    (106.0, 5.0, "el mirador: mesas y bancos"),
    (134.0, 6.0, "el mirador con la valla y el valle"),
    (212.2, 5.6, "valle, cierre"),
]
# SIN_ETALONAJE=1 deja el montaje sin corrección de color (para reescalar antes y etalonar después)
grade = "null" if os.environ.get("SIN_ETALONAJE") else "eq=contrast=1.07:saturation=0.9:gamma=0.97,colorbalance=rs=.035:gs=.01:bs=-.04:rm=.02:bm=-.02,vignette=PI/6.5"
args = [FF, "-y", "-loglevel", "error"]
for s, d, _ in CLIPS: args += ["-ss", str(s), "-t", str(d), "-i", src]
if audio: args += ["-i", audio]
fc = [f"[{i}:v]fps=25,scale={W}:{H}:flags=lanczos,setsar=1,{grade},format=yuv420p[v{i}]" for i in range(len(CLIPS))]
prev, off = "v0", 0.0
for i in range(1, len(CLIPS)):
    off += CLIPS[i-1][1] - X
    fc.append(f"[{prev}][v{i}]xfade=transition=fade:duration={X}:offset={off:.2f}[x{i}]"); prev = f"x{i}"
total = sum(d for _, d, _ in CLIPS) - X * (len(CLIPS) - 1)
fc.append(f"[{prev}]null[out]" if os.environ.get("SIN_ETALONAJE") else f"[{prev}]fade=t=in:st=0:d=0.8,fade=t=out:st={total-1.2:.2f}:d=1.2[out]")
args += ["-filter_complex", ";".join(fc), "-map", "[out]"]
if audio: args += ["-map", f"{len(CLIPS)}:a", "-c:a", "aac", "-b:a", "160k", "-shortest"]
else: args += ["-an"]
args += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", os.environ.get("CRF", "20"), "-preset", "slow", "-movflags", "+faststart", out]
subprocess.check_call(args); print(f"{out}: {total:.1f} s, {W}x{H}")
