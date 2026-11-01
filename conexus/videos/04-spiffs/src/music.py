"""Soundtrack for video 4: 120 BPM, A minor (Am-F-C-G), 22s, effects on the same beat grid.
Usage: python3 music.py out.wav
"""
import sys, wave
import numpy as np

SR = 48000
DUR = 22.0
BPM = 120
BEAT = 60 / BPM            # 0.5s
N = int(SR * DUR)
t_all = np.arange(N) / SR
rng = np.random.default_rng(7)

def hz(m):                 # midi -> Hz
    return 440.0 * 2 ** ((m - 69) / 12)

def place(buf, sig, start):
    i = int(round(start * SR))
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i]

def env_adsr(n, a, d, s, r, sus_len):
    a_n, d_n, r_n = int(a * SR), int(d * SR), int(r * SR)
    s_n = max(0, int(sus_len * SR) - a_n - d_n)
    e = np.concatenate([np.linspace(0, 1, a_n, endpoint=False),
                        np.linspace(1, s, d_n, endpoint=False),
                        np.full(s_n, s),
                        np.linspace(s, 0, r_n)])
    return e[:n] if len(e) >= n else np.pad(e, (0, n - len(e)))

def lowpass_fft(x, cutoff):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (f / cutoff) ** 4)
    return np.fft.irfft(X, len(x))

def highpass_fft(x, cutoff):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (cutoff / np.maximum(f, 1)) ** 4)
    return np.fft.irfft(X, len(x))

# Chords per bar (2s each). midi notes.
#            root(bass)  chord tones
CHORDS = {'Am': (45, [57, 60, 64, 69]), 'F': (41, [53, 57, 60, 65]),
          'C': (48, [55, 60, 64, 67]), 'G': (43, [55, 59, 62, 67])}
PROG = ['Am', 'F', 'C', 'G', 'Am', 'F', 'C', 'G', 'Am', 'F', 'C']
BAR = 4 * BEAT

pad = np.zeros(N); bass = np.zeros(N); kick = np.zeros(N); hat = np.zeros(N)
pluck = np.zeros(N); sfx = np.zeros(N)

# ---- pad: soft detuned sines with a couple of harmonics, crossfaded per bar
for b, name in enumerate(PROG):
    start = b * BAR
    length = BAR + 0.6 if b < len(PROG) - 1 else DUR - start
    n = int(length * SR)
    tt = np.arange(n) / SR
    sig = np.zeros(n)
    for m in CHORDS[name][1]:
        for det in (-0.12, 0.12):
            f = hz(m) * 2 ** (det / 12)
            sig += np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(4 * np.pi * f * tt) + 0.08 * np.sin(6 * np.pi * f * tt)
    rel = 0.6 if b < len(PROG) - 1 else 2.0
    sig *= env_adsr(n, 0.35, 0.4, 0.8, rel, length - rel)
    place(pad, sig, start)
pad = lowpass_fft(pad, 2200)

# ---- arrangement windows
GROOVE = (4.0, 18.5)       # full drums from scene 2 to end card
LIGHT_KICK = (2.0, 4.0)    # kick enters softly under "Sound familiar?"

def kick_hit(level):
    n = int(0.32 * SR); tt = np.arange(n) / SR
    f = 45 + 75 * np.exp(-tt * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return level * np.sin(ph) * np.exp(-tt * 9)

def hat_hit(level):
    n = int(0.06 * SR)
    noise = rng.standard_normal(n)
    noise = np.diff(np.concatenate([[0], noise]))      # crude high-pass
    return level * noise * np.exp(-np.arange(n) / SR * 70)

def bass_note(m, length, level):
    n = int(length * SR); tt = np.arange(n) / SR
    f = hz(m)
    s = np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)
    return level * s * env_adsr(n, 0.01, 0.15, 0.6, 0.12, length - 0.12)

def pluck_note(m, level, decay=6.0):
    n = int(0.9 * SR); tt = np.arange(n) / SR
    f = hz(m)
    s = np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(4 * np.pi * f * tt) * np.exp(-tt * 10) + 0.12 * np.sin(6 * np.pi * f * tt) * np.exp(-tt * 16)
    a = np.minimum(1, tt / 0.004)
    return level * s * a * np.exp(-tt * decay)

def bell(ms, level, decay=2.6):
    n = int(2.2 * SR); tt = np.arange(n) / SR
    s = np.zeros(n)
    for k, m in enumerate(ms):
        f = hz(m)
        s += (np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(2 * np.pi * f * 2.0 * tt) * np.exp(-tt * 5)
              + 0.15 * np.sin(2 * np.pi * f * 3.0 * tt) * np.exp(-tt * 8)) / (1 + k * 0.4)
    return level * s * np.minimum(1, tt / 0.003) * np.exp(-tt * decay)

def swell(end, length, level):
    n = int(length * SR); tt = np.arange(n) / SR
    noise = lowpass_fft(rng.standard_normal(n), 1800)
    e = (tt / length) ** 2.2
    place(sfx, level * noise * e, end - length)

n_beats = int(DUR / BEAT)
for k in range(n_beats):
    tb = k * BEAT
    bar = int(tb // BAR)
    name = PROG[min(bar, len(PROG) - 1)]
    root, tones = CHORDS[name]
    if GROOVE[0] <= tb < GROOVE[1]:
        place(kick, kick_hit(0.9), tb)
        place(hat, hat_hit(0.22), tb + BEAT / 2)
        place(bass, bass_note(root, BEAT * 0.9, 0.5), tb)
    elif LIGHT_KICK[0] <= tb < LIGHT_KICK[1] and k % 2 == 0:
        place(kick, kick_hit(0.55), tb)
    if tb < 18.5:
        # 8th-note arpeggio, up-down through the chord, an octave up
        seq = [tones[0], tones[1], tones[2], tones[3], tones[2], tones[1], tones[0], tones[2]]
        for h in range(2):
            step = (k * 2 + h) % 8
            lvl = 0.16 if tb >= 4.0 else 0.11
            place(pluck, pluck_note(seq[step] + 12, lvl), tb + h * BEAT / 2)

# end card: low root + final chord ring
place(bass, bass_note(36, 3.0, 0.45), 18.5)
place(kick, kick_hit(0.8), 18.5)

# ---- sound effects (in key, on the grid)
for tm in (0.5, 1.5):                          # chat messages pop in
    place(sfx, pluck_note(81 if tm == 0.5 else 76, 0.22, decay=14), tm)
for tm in (4.5, 6.0, 10.0, 10.5, 11.0, 12.0, 12.5, 14.75, 15.0, 15.25, 15.5, 15.75):
    place(sfx, pluck_note(88, 0.07, decay=22), tm)   # soft ticks on card entrances
place(sfx, bell([81, 88], 0.20), 7.0)          # credit chime (+$25)
place(sfx, bell([76, 81, 88], 0.20), 16.5)     # balance total
place(sfx, bell([72, 76, 79, 84], 0.16, decay=1.4), 18.75)   # logo reveal shimmer (C major)
for cut in (4.0, 9.5, 14.5, 18.5):
    swell(cut, 0.5, 0.05)

mix = 0.9 * pad / np.max(np.abs(pad)) * 0.32 + bass + kick * 0.85 + hat + pluck + sfx
# gentle end fade + 10 ms fade-in
mix *= np.minimum(1, t_all / 0.01) * np.clip((DUR - t_all) / 0.5, 0, 1)
# soft clip + normalize to -1 dBFS
mix = np.tanh(mix * 1.1)
mix *= 10 ** (-1 / 20) / np.max(np.abs(mix))
stereo = np.stack([mix, mix], axis=1)
# a touch of width on pad/pluck via small delay on the right channel
d = int(0.012 * SR)
wide = (0.9 * pad / np.max(np.abs(pad)) * 0.32 + pluck) * 0.25
stereo[d:, 1] += wide[:-d] * 0.5
stereo *= 10 ** (-1 / 20) / np.max(np.abs(stereo))

out = sys.argv[1]
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((stereo * 32767).astype('<i2').tobytes())
print('wrote', out, f'{DUR}s')
