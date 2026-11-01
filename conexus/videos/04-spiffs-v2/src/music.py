"""Music bed + effects for video 4 v2, mixed under the voiceover with ducking.
120 BPM, A minor (Am-F-C-G), resolving to C major on the end card.
Usage: python3 music.py <timeline.js> <vo.wav> <out_mix.wav>
"""
import json, sys, wave
import numpy as np

SR = 48000
BEAT = 0.5
BAR = 4 * BEAT
rng = np.random.default_rng(11)

tl_path, vo_path, out_path = sys.argv[1:4]
src = open(tl_path).read()
TL = json.loads(src[src.index('{'):src.rindex('}') + 1])
DUR = TL['total']
N = int(DUR * SR)
SC = {s['id']: s for s in TL['scenes']}
WORDS = [w for c in TL['captions'] for w in c['words']]

def wt(line, word):
    for w in WORDS:
        clean = ''.join(ch for ch in w['w'] if ch.isalnum() or ch in "$'").lower()
        if w['line'] == line and clean.startswith(word.lower()):
            return w['s']
    raise KeyError(line + ':' + word)

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)

def place(buf, sig, start):
    i = int(round(start * SR))
    if i >= len(buf) or i + len(sig) <= 0: return
    a = max(0, -i); i = max(0, i); j = min(len(buf), i + len(sig) - a)
    buf[i:j] += sig[a:a + j - i]

def adsr(n, a, d, s, r, hold):
    a_n, d_n, r_n = int(a * SR), int(d * SR), int(r * SR)
    s_n = max(0, int(hold * SR) - a_n - d_n)
    e = np.concatenate([np.linspace(0, 1, a_n, endpoint=False), np.linspace(1, s, d_n, endpoint=False), np.full(s_n, s), np.linspace(s, 0, r_n)])
    return e[:n] if len(e) >= n else np.pad(e, (0, n - len(e)))

def lowpass(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / np.sqrt(1 + (f / fc) ** 4), len(x))

CH = {'Am': (45, [57, 60, 64, 69]), 'F': (41, [53, 57, 60, 65]), 'C': (48, [55, 60, 64, 67]), 'G': (43, [55, 59, 62, 67])}
PROG = ['Am', 'F', 'C', 'G']
END = SC['G']['s']                       # end card: resolve to C major
LIFT = SC['D']['s']                      # product section: add kick + bass pulse
FINAL = 'C'

def chord_at(t):
    if t >= END: return FINAL
    return PROG[int(t // BAR) % 4]

pad = np.zeros(N); pluck = np.zeros(N); kick = np.zeros(N); bass = np.zeros(N); hat = np.zeros(N); sfx = np.zeros(N)

# pad — one note-on per bar (or at the end-card cut), soft detuned sines
starts = sorted(set([b * BAR for b in range(int(np.ceil(DUR / BAR))) if b * BAR < END] + [END]))
for k, s in enumerate(starts):
    e = starts[k + 1] if k + 1 < len(starts) else DUR
    length = e - s + (0.5 if e < DUR else 0)
    n = int(length * SR); tt = np.arange(n) / SR; sig = np.zeros(n)
    for m in CH[chord_at(s + 0.01)][1]:
        for det in (-0.1, 0.1):
            f = hz(m) * 2 ** (det / 12)
            sig += np.sin(2 * np.pi * f * tt) + 0.22 * np.sin(4 * np.pi * f * tt) + 0.06 * np.sin(6 * np.pi * f * tt)
    rel = 0.5 if e < DUR else 1.6
    sig *= adsr(n, 0.4, 0.5, 0.75, rel, length - rel)
    place(pad, sig, s)
pad = lowpass(pad, 1800); pad /= np.max(np.abs(pad))

def pluck_note(m, level, decay=6.0):
    n = int(0.8 * SR); tt = np.arange(n) / SR; f = hz(m)
    s = np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt) * np.exp(-tt * 10)
    return level * s * np.minimum(1, tt / 0.004) * np.exp(-tt * decay)

def kick_hit(level):
    n = int(0.3 * SR); tt = np.arange(n) / SR
    f = 45 + 70 * np.exp(-tt * 28)
    return level * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 10)

def hat_hit(level):
    n = int(0.05 * SR); x = np.diff(np.concatenate([[0], rng.standard_normal(n)]))
    return level * x * np.exp(-np.arange(n) / SR * 80)

def bass_note(m, length, level):
    n = int(length * SR); tt = np.arange(n) / SR; f = hz(m)
    return level * (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(4 * np.pi * f * tt)) * adsr(n, 0.01, 0.12, 0.6, 0.1, length - 0.1)

def bell(ms, level, decay=2.4):
    n = int(2.0 * SR); tt = np.arange(n) / SR; s = np.zeros(n)
    for k, m in enumerate(ms):
        f = hz(m)
        s += (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(4 * np.pi * f * tt) * np.exp(-tt * 5)) / (1 + 0.4 * k)
    return level * s * np.minimum(1, tt / 0.003) * np.exp(-tt * decay)

def swell(end, length, level):
    n = int(length * SR); tt = np.arange(n) / SR
    place(sfx, level * lowpass(rng.standard_normal(n), 2000) * (tt / length) ** 2.4, end - length)

def boom(t0, level):
    n = int(1.2 * SR); tt = np.arange(n) / SR
    place(sfx, level * np.sin(2 * np.pi * (40 + 25 * np.exp(-tt * 8)) * tt) * np.exp(-tt * 3.5), t0)

for k in range(int(DUR / BEAT)):
    tb = k * BEAT
    root, tones = CH[chord_at(tb + 0.01)]
    if tb < END:
        seq = [tones[0], tones[2], tones[1], tones[3], tones[2], tones[1], tones[3], tones[2]]
        for h in range(2):
            step = (k * 2 + h) % 8
            lvl = 0.12 if tb >= LIFT else 0.08
            if tb < SC['C']['s'] and h == 1: continue          # sparser in the problem section
            place(pluck, pluck_note(seq[step] + 12, lvl), tb + h * BEAT / 2)
    if LIFT <= tb < END:
        place(kick, kick_hit(0.7), tb)
        place(hat, hat_hit(0.12), tb + BEAT / 2)
        place(bass, bass_note(root, BEAT * 0.85, 0.32), tb)
place(bass, bass_note(36, 3.5, 0.32), END); place(kick, kick_hit(0.6), END)

# ---- effects, in key, synced to on-screen actions
A, C, D, E, F, G = (SC[x]['s'] for x in 'ACDEFG')
for tm, m in ((A + 0.45, 81), (A + 0.95, 76), (wt('l2', 'did'), 81)):   # message cards
    place(sfx, pluck_note(m, 0.18, decay=14), tm)
place(sfx, pluck_note(45, 0.35, decay=5), wt('l3', 'missed'))             # low "miss" thud (A)
for cut in (SC['B']['s'], C, D, E, F, G): swell(cut, 0.5, 0.04)
boom(C, 0.5); place(sfx, bell([76, 81, 88], 0.12, decay=1.8), C + 0.2)   # logo reveal
place(sfx, pluck_note(93, 0.10, decay=30), wt('l5', 'once'))              # click
place(sfx, bell([81, 88], 0.16), wt('l6', 'credited'))                    # +$25 chime
place(sfx, pluck_note(88, 0.10, decay=18), wt('l7', 'live') + 0.15)       # leaderboard climb
place(sfx, pluck_note(91, 0.07, decay=18), wt('l7', 'live') + 0.4)
for i in range(4): place(sfx, pluck_note(88, 0.05, decay=24), F + 0.5 + i * 0.18)  # ledger rows (ticks)
place(sfx, bell([76, 81, 88], 0.16), wt('l9', 'payday'))                  # balance total
boom(G, 0.4); place(sfx, bell([72, 76, 79, 84], 0.12, decay=1.4), G + 0.2)  # end-card shimmer

music = 0.30 * pad + pluck + 0.8 * kick + bass + hat + sfx

# ---- voiceover + ducking
raw = wave.open(vo_path)
vo = np.frombuffer(raw.readframes(raw.getnframes()), '<i2').astype(float) / 32768
vo = np.pad(vo, (0, max(0, N - len(vo))))[:N]
vo = vo / np.max(np.abs(vo)) * 0.85
env = np.sqrt(np.convolve(vo ** 2, np.ones(int(0.03 * SR)) / int(0.03 * SR), 'same'))
active = (env > 0.02).astype(float)
# attack 60 ms, release 350 ms (one-pole smoothing, vectorised in blocks)
step = 48; a_c, r_c = np.exp(-step / SR / 0.06), np.exp(-step / SR / 0.35)
ds = active[::step]; g = np.zeros_like(ds); y = 0.0
for i, v in enumerate(ds):
    c = a_c if v > y else r_c
    y = c * y + (1 - c) * v; g[i] = y
duck = 1 - 0.65 * np.repeat(g, step)[:N]         # about -9 dB under speech
music *= duck
music *= 0.30                                    # bed sits well under the voice

mix_l = vo + music; mix_r = vo + music
# a little width: delay the pad/pluck slightly on the right
d = int(0.011 * SR); wide = (0.30 * pad + pluck) * 0.30 * duck * 0.35
mix_r[d:] += wide[:-d]
fade = np.clip((DUR - np.arange(N) / SR) / 0.8, 0, 1) * np.minimum(1, np.arange(N) / SR / 0.01)
st = np.stack([mix_l * fade, mix_r * fade], 1)
st = np.tanh(st * 1.05); st *= 10 ** (-1 / 20) / np.max(np.abs(st))
with wave.open(out_path, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype('<i2').tobytes())
print('mix', out_path, DUR)

def lufs_ish(x):   # K-weighting omitted; relative comparison only
    x = x[np.abs(x) > 1e-4]
    return 10 * np.log10(np.mean(x ** 2) + 1e-12)
speech = np.repeat(g, step)[:N] > 0.5
print(f'voice vs music while speaking: {lufs_ish(vo[speech]) - lufs_ish(music[speech]):.1f} dB')
print(f'music in gaps vs voice:        {lufs_ish(music[~speech]) - lufs_ish(vo[speech]):.1f} dB')
