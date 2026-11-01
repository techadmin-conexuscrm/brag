"""Shared synth voices for the overview (A minor / C major, 48 kHz)."""
import numpy as np
SR = 48000
rng = np.random.default_rng(11)

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

def pluck(m, level, decay=6.0):
    n = int(0.8 * SR); tt = np.arange(n) / SR; f = hz(m)
    s = np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt) * np.exp(-tt * 10)
    return level * s * np.minimum(1, tt / 0.004) * np.exp(-tt * decay)

def kick(level):
    n = int(0.3 * SR); tt = np.arange(n) / SR
    f = 45 + 70 * np.exp(-tt * 28)
    return level * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 10)

def hat(level):
    n = int(0.05 * SR); x = np.diff(np.concatenate([[0], rng.standard_normal(n)]))
    return level * x * np.exp(-np.arange(n) / SR * 80)

def bass(m, length, level):
    n = int(length * SR); tt = np.arange(n) / SR; f = hz(m)
    return level * (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(4 * np.pi * f * tt)) * adsr(n, 0.01, 0.12, 0.6, 0.1, length - 0.1)

def bell(ms, level, decay=2.4):
    n = int(2.0 * SR); tt = np.arange(n) / SR; s = np.zeros(n)
    for k, m in enumerate(ms):
        f = hz(m)
        s += (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(4 * np.pi * f * tt) * np.exp(-tt * 5)) / (1 + 0.4 * k)
    return level * s * np.minimum(1, tt / 0.003) * np.exp(-tt * decay)

def swell(length, level):
    n = int(length * SR); tt = np.arange(n) / SR
    return level * lowpass(rng.standard_normal(n), 2000) * (tt / length) ** 2.4

def boom(level):
    n = int(1.2 * SR); tt = np.arange(n) / SR
    return level * np.sin(2 * np.pi * (40 + 25 * np.exp(-tt * 8)) * tt) * np.exp(-tt * 3.5)

def read_tl(path):
    import json
    src = open(path).read()
    return json.loads(src[src.index('{'):src.rindex('}') + 1])

def word_time(tl, line, word):
    for c in tl['captions']:
        for w in c['words']:
            clean = ''.join(ch for ch in w['w'] if ch.isalnum() or ch in "$'").lower()
            if w['line'] == line and clean.startswith(word.lower()):
                return w['s']
    raise KeyError(f'no word {word!r} in {line}')
