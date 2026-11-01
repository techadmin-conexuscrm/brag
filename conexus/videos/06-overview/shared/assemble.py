"""Stitch built chapters into one film with a single continuous music bed.
Usage: python3 shared/assemble.py            (run from the 06-overview folder)
Reads chapters.json (order + titles), each chapters/<dir>/out/{video.mp4,vo.wav,sfx.wav,timeline.js}.
Writes build/ (stems) and final/{conexus-overview.mp4, chapters.json, captions.vtt}.
"""
import json, os, subprocess, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from audio_lib import SR, place, pluck, kick, hat, bass, adsr, lowpass, hz, read_tl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT); os.makedirs('build', exist_ok=True); os.makedirs('final', exist_ok=True)
FPS = 30
order = json.load(open('chapters.json'))

def load_mono(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, '<i2').astype(float) / 32768

def frames(p):
    out = subprocess.run(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0', p], capture_output=True, text=True, check=True).stdout
    return int(out.strip())

# ---- layout
chapters, t = [], 0.0
for ch in order:
    d = f"chapters/{ch['dir']}/out"
    tl = read_tl(f'{d}/timeline.js'); nf = frames(f'{d}/video.mp4')
    chapters.append({**ch, 'start': round(t, 3), 'dur': nf / FPS, 'tl': tl, 'd': d})
    t += nf / FPS
DUR = t; N = int(DUR * SR)
print(f'{len(chapters)} chapters, {DUR:.1f}s')

# ---- video: concat (all chapters share codec settings)
with open('build/concat.txt', 'w') as f:
    for c in chapters: f.write(f"file '{os.path.abspath(c['d'])}/video.mp4'\n")
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', 'build/concat.txt', '-c', 'copy', 'build/video_all.mp4'], check=True)

# ---- voice + effects stems
vo = np.zeros(N); fx = np.zeros(N)
for c in chapters:
    place(vo, load_mono(f"{c['d']}/vo.wav"), c['start'])
    place(fx, load_mono(f"{c['d']}/sfx.wav"), c['start'])
vo = vo / max(1e-9, np.max(np.abs(vo))) * 0.85

# ---- music bed: Am-F-C-G at 120 BPM, light groove in the middle, resolves to C on the final chapter
BEAT = 0.5; BAR = 2.0
CH = {'Am': (45, [57, 60, 64, 69]), 'F': (41, [53, 57, 60, 65]), 'C': (48, [55, 60, 64, 67]), 'G': (43, [55, 59, 62, 67])}
PROG = ['Am', 'F', 'C', 'G']
END = chapters[-1]['start']
GROOVE = (chapters[1]['start'] if len(chapters) > 2 else 0, END)
chord_at = lambda x: 'C' if x >= END else PROG[int(x // BAR) % 4]
pad = np.zeros(N); arp = np.zeros(N); drums = np.zeros(N); low = np.zeros(N)
starts = sorted(set([b * BAR for b in range(int(np.ceil(DUR / BAR))) if b * BAR < END] + [END]))
for k, s in enumerate(starts):
    e = starts[k + 1] if k + 1 < len(starts) else DUR
    length = e - s + (0.5 if e < DUR else 0); n = int(length * SR); tt = np.arange(n) / SR; sig = np.zeros(n)
    for m in CH[chord_at(s + 0.01)][1]:
        for det in (-0.1, 0.1):
            f = hz(m) * 2 ** (det / 12)
            sig += np.sin(2 * np.pi * f * tt) + 0.22 * np.sin(4 * np.pi * f * tt) + 0.06 * np.sin(6 * np.pi * f * tt)
    rel = 0.5 if e < DUR else 2.0
    place(pad, sig * adsr(n, 0.4, 0.5, 0.75, rel, length - rel), s)
pad = lowpass(pad, 1800); pad /= np.max(np.abs(pad))
for k in range(int(DUR / BEAT)):
    tb = k * BEAT; root, tones = CH[chord_at(tb + 0.01)]
    if tb < END:
        seq = [tones[0], tones[2], tones[1], tones[3], tones[2], tones[1], tones[3], tones[2]]
        for h in range(2): place(arp, pluck(seq[(k * 2 + h) % 8] + 12, 0.10, 6), tb + h * BEAT / 2)
    if GROOVE[0] <= tb < GROOVE[1]:
        place(drums, kick(0.6), tb); place(drums, hat(0.10), tb + BEAT / 2); place(low, bass(root, BEAT * 0.85, 0.28), tb)
place(low, bass(36, 3.5, 0.3), END); place(drums, kick(0.55), END)
music = 0.30 * pad + arp + 0.8 * drums + low + fx

# ---- ducking under the voice (~ -9 dB), bed well below speech
env = np.sqrt(np.convolve(vo ** 2, np.ones(int(0.03 * SR)) / int(0.03 * SR), 'same'))
active = (env > 0.02).astype(float); step = 48
a_c, r_c = np.exp(-step / SR / 0.06), np.exp(-step / SR / 0.35)
ds = active[::step]; g = np.zeros_like(ds); y = 0.0
for i, v in enumerate(ds):
    c = a_c if v > y else r_c; y = c * y + (1 - c) * v; g[i] = y
duck = 1 - 0.65 * np.repeat(g, step)[:N]
music = music * duck * 0.21
L = vo + music; R = vo + music
d = int(0.011 * SR); R[d:] += ((0.30 * pad + arp) * 0.21 * duck * 0.35)[:-d]
fade = np.clip((DUR - np.arange(N) / SR) / 1.0, 0, 1) * np.minimum(1, np.arange(N) / SR / 0.01)
st = np.tanh(np.stack([L * fade, R * fade], 1) * 1.05); st *= 10 ** (-1 / 20) / np.max(np.abs(st))
with wave.open('build/mix.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype('<i2').tobytes())
speech = np.repeat(g, step)[:N] > 0.5
lv = lambda x: 10 * np.log10(np.mean(x[np.abs(x) > 1e-4] ** 2) + 1e-12)
print(f'voice vs music while speaking: {lv(vo[speech]) - lv(music[speech]):.1f} dB')

# ---- mux
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/video_all.mp4', '-i', 'build/mix.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11',
                '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-shortest', '-movflags', '+faststart', 'final/conexus-overview.mp4'], check=True)

# ---- chapters + captions
json.dump([{'n': i + 1, 'title': c['title'], 'blurb': c.get('blurb', ''), 'status': c.get('status', 'live'),
            'start': c['start'], 'end': round(c['start'] + c['dur'], 3)} for i, c in enumerate(chapters)],
          open('final/chapters.json', 'w'), indent=1)
def ts(x): h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60; return f'{h:02d}:{m:02d}:{s:06.3f}'
with open('final/captions.vtt', 'w') as f:
    f.write('WEBVTT\n\n')
    for c in chapters:
        for cap in c['tl']['captions']:
            f.write(f"{ts(c['start'] + cap['s'])} --> {ts(c['start'] + cap['e'])}\n{' '.join(w['w'] for w in cap['words'])}\n\n")
print('final/conexus-overview.mp4', f'{DUR:.1f}s')
