#!/usr/bin/env python3
"""Une el "Hola," de una toma de referencia con el nombre de otra toma.
Uso: hola_unico.py <ref.mp3> <fin_hola_ref> <toma.mp3> <inicio_nombre> <salida.mp3>  -> imprime la duración"""
import subprocess, sys, re, os
FF = subprocess.check_output([os.path.join(os.path.dirname(os.path.abspath(__file__)), "vid/bin/python"), "-c", "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"]).decode().strip()
ref, fin, src, ini, out = sys.argv[1], float(sys.argv[2]), sys.argv[3], float(sys.argv[4]), sys.argv[5]
log = subprocess.run([FF, "-i", src, "-af", "silencedetect=noise=-38dB:d=0.1", "-f", "null", "-"], capture_output=True, text=True).stderr
dur = [float(h) * 3600 + float(m) * 60 + float(s) for h, m, s in re.findall(r"Duration: (\d+):(\d+):([\d.]+)", log)][0]
starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
end = dur
for i, s in enumerate(starts):
    e = ends[i] if i < len(ends) else dur
    if s > ini + 0.15 and (e - s >= 0.6 or e >= dur - 0.05): end = min(end, s + 0.12)
X = 0.02  # fundido cruzado en la unión
fc = (f"[0]atrim=0:{fin + X:.3f},asetpts=PTS-STARTPTS[a];[1]atrim={ini - X:.3f}:{end:.3f},asetpts=PTS-STARTPTS[b];"
      f"[a][b]acrossfade=d={X}:c1=tri:c2=tri,afade=t=out:st={fin + end - ini - 0.08:.3f}:d=0.08")
subprocess.check_call([FF, "-y", "-loglevel", "error", "-i", ref, "-i", src, "-filter_complex", fc, "-ac", "1", "-c:a", "libmp3lame", "-b:a", "112k", out])
print(f"{fin + end - ini:.2f}")
