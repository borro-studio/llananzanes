#!/usr/bin/env python3
"""Recorta un saludo generado ("Hola... Nombre.") a su parte hablada y lo deja listo para la web.
Uso: saludo.py <entrada.mp3> <salida.mp3>   -> imprime la duración final"""
import subprocess, sys, re, os
FF = subprocess.check_output([os.path.join(os.path.dirname(os.path.abspath(__file__)), "vid/bin/python"), "-c", "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"]).decode().strip()
src, out = sys.argv[1], sys.argv[2]
log = subprocess.run([FF, "-i", src, "-af", "silencedetect=noise=-38dB:d=0.1", "-f", "null", "-"], capture_output=True, text=True).stderr
dur = [float(h) * 3600 + float(m) * 60 + float(s) for h, m, s in re.findall(r"Duration: (\d+):(\d+):([\d.]+)", log)][0]
starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
sil = [(s, ends[i] if i < len(ends) else dur) for i, s in enumerate(starts)]
begin = sil[0][1] - 0.03 if sil and sil[0][0] < 0.05 else 0.0
# fin de la voz: inicio del último silencio largo (>= 0,6 s) o del que llega hasta el final
end = dur
for s, e in sil:
    if s > begin + 0.2 and (e - s >= 0.6 or e >= dur - 0.05): end = s + 0.12
end = min(end, dur)
subprocess.check_call([FF, "-y", "-loglevel", "error", "-ss", f"{begin:.3f}", "-t", f"{end - begin:.3f}", "-i", src,
    "-af", f"afade=t=out:st={max(0, end - begin - 0.08):.3f}:d=0.08", "-c:a", "libmp3lame", "-b:a", "112k", out])
print(f"{end - begin:.2f}")
