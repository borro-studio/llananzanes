#!/usr/bin/env python3
"""Estabiliza cada plano del máster de portada por separado (vidstab, dos pasadas) y los une por corte.
Uso: estabiliza.py <master_1080p.mp4> <salida_estabilizada.mp4> <carpeta_trabajo>
Imprime, por plano, el temblor medido antes y después (px por fotograma, media de la 2ª diferencia del movimiento global)."""
import subprocess, sys, os, re, statistics
FF = subprocess.check_output([os.path.join(os.path.dirname(os.path.abspath(__file__)), "vid/bin/python"), "-c", "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"]).decode().strip()
src, out, work = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(work, exist_ok=True)
# tramos limpios del máster (fuera de los fundidos)
SEG = [(0.0, 5.4), (6.0, 9.8), (10.4, 15.2), (15.8, 19.6), (20.2, 24.0), (24.6, 29.4), (30.0, 35.0)]
def run(*a): subprocess.check_call([FF, "-y", "-loglevel", "error", *a])
def jitter(video, trf):
    run("-i", video, "-vf", f"vidstabdetect=shakiness=6:accuracy=15:result={trf}:fileformat=ascii", "-f", "null", "-")
    gx, gy = [], []
    for line in open(trf, errors="ignore"):
        v = re.findall(r"\(LM (-?\d+) (-?\d+) ", line)
        if not v: continue
        gx.append(statistics.median(int(a) for a, _ in v)); gy.append(statistics.median(int(b) for _, b in v))
    d2 = [abs(gx[i+1] - 2*gx[i] + gx[i-1]) + abs(gy[i+1] - 2*gy[i] + gy[i-1]) for i in range(1, len(gx) - 1)]
    return sum(d2) / max(1, len(d2))
parts = []
for i, (a, b) in enumerate(SEG):
    raw, trf, st = f"{work}/s{i}.mp4", f"{work}/s{i}.trf", f"{work}/s{i}-estab.mp4"
    run("-ss", str(a), "-t", f"{b-a:.3f}", "-i", src, "-an", "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", raw)
    before = jitter(raw, trf)
    run("-i", raw, "-vf", f"vidstabtransform=input={trf}:smoothing=24:optzoom=1:zoomspeed=0:interpol=bicubic:crop=black,unsharp=5:5:0.5:3:3:0.0,deflicker=size=5:mode=am",
        "-an", "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", st)
    after = jitter(st, f"{work}/s{i}-post.trf")
    print(f"plano {i+1} ({a:.1f}-{b:.1f} s): temblor {before:.2f} -> {after:.2f}"); parts.append(st)
lst = f"{work}/lista.txt"; open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
run("-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out); print("salida:", out)
