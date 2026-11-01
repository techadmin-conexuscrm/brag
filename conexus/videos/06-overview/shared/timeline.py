"""Builds the voiceover track + word/caption/scene timeline from per-line Kokoro WAVs.
Usage: python3 timeline.py <script.json> <vo_dir> <out_vo.wav> <out_timeline.js>
Word times: each line is split at its audible pauses; if the pauses line up with the
line's punctuation, word groups are snapped to those speech segments, otherwise words
are spread by character length. Good enough for chunked captions.
"""
import json, re, subprocess, sys, wave
import numpy as np

SR = 48000
LEAD_IN = 0.35          # visual hook before the first word
BEAT = 0.5              # 120 BPM grid for scene cuts

script_path, vo_dir, out_wav, out_js = sys.argv[1:5]
script = json.load(open(script_path))

def load(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, '<i2').astype(float) / 32768

def envelope(x, win=0.02):
    n = int(win * SR)
    e = np.sqrt(np.convolve(x ** 2, np.ones(n) / n, 'same'))
    return e

def trim(x, thr_db=-42):
    e = envelope(x); thr = 10 ** (thr_db / 20)
    idx = np.where(e > thr)[0]
    a, b = max(0, idx[0] - int(0.02 * SR)), min(len(x), idx[-1] + int(0.06 * SR))
    return x[a:b]

def segments(x, thr_db=-38, min_pause=0.09):
    e = envelope(x); on = e > 10 ** (thr_db / 20)
    segs, start, quiet = [], None, 0
    for i, v in enumerate(on[::48]):          # 1 ms steps
        t = i / 1000
        if v:
            if start is None: start = t
            quiet = 0; last_on = t
        elif start is not None:
            quiet += 0.001
            if quiet >= min_pause:
                segs.append((start, last_on)); start = None
    if start is not None: segs.append((start, last_on))
    return segs

def spread(words, t0, t1):
    w = np.array([len(re.sub(r'[^\w]', '', x)) + 1.5 for x in words], float)
    edges = t0 + np.concatenate([[0], np.cumsum(w)]) / w.sum() * (t1 - t0)
    return [(float(edges[i]), float(edges[i + 1])) for i in range(len(words))]

vo = []; t = LEAD_IN; words_out = []; lines_out = []
for line in script['lines']:
    x = trim(load(f"{vo_dir}/{line['id']}.wav"))
    dur = len(x) / SR
    words = line['text'].split()
    # word groups split after punctuation
    groups, cur = [], []
    for wd in words:
        cur.append(wd)
        if re.search(r'[,.?!]$', wd): groups.append(cur); cur = []
    if cur: groups.append(cur)
    segs = segments(x)
    if len(segs) == len(groups):
        times = []
        for g, (a, b) in zip(groups, segs): times += spread(g, a, b)
    else:
        times = spread(words, 0, dur)
    start = t
    vo.append((start, x))
    for wd, (a, b) in zip(words, times):
        clean = wd.strip()
        words_out.append({'w': clean, 's': round(start + a, 3), 'e': round(start + b, 3),
                          'em': clean in line['emph'], 'line': line['id']})
    lines_out.append({'id': line['id'], 'scene': line['scene'], 's': round(start, 3), 'e': round(start + dur, 3)})
    t = start + dur + line['gap']

total = round(t, 2)
buf = np.zeros(int(total * SR) + SR)
for s, x in vo:
    i = int(s * SR); buf[i:i + len(x)] += x
buf = buf[:int(total * SR)]
with wave.open(out_wav, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(buf, -1, 1) * 32767).astype('<i2').tobytes())

# scenes
scenes = []
for ln in lines_out:
    if not scenes or scenes[-1]['id'] != ln['scene']:
        # cut in the pause between the previous line and this one, on the 120 BPM grid
        # (0.5s) when a grid point fits in that pause, otherwise mid-pause
        prev_end = lines_out[lines_out.index(ln) - 1]['e'] if lines_out.index(ln) else 0.0
        lo, hi = prev_end + 0.05, ln['s'] - 0.08
        grid = np.ceil(lo / BEAT) * BEAT
        cut = grid if grid <= hi else (lo + hi) / 2
        scenes.append({'id': ln['scene'], 's': 0.0 if not scenes else round(float(cut), 3)})
for i, sc in enumerate(scenes):
    sc['e'] = scenes[i + 1]['s'] if i + 1 < len(scenes) else total

# caption chunks: split at punctuation, then balance long groups into <=4-word pieces
chunks = []
for ln in lines_out:
    ws = [w for w in words_out if w['line'] == ln['id']]
    groups, cur = [], []
    for w in ws:
        cur.append(w)
        if re.search(r'[,.?!]$', w['w']): groups.append(cur); cur = []
    if cur: groups.append(cur)
    for g in groups:
        k = -(-len(g) // 4)
        size = -(-len(g) // k)
        for i in range(0, len(g), size): chunks.append(g[i:i + size])
caps = []
for i, c in enumerate(chunks):
    nxt = chunks[i + 1][0]['s'] if i + 1 < len(chunks) else total
    end = min(nxt, c[-1]['e'] + 0.6)
    caps.append({'s': c[0]['s'], 'e': round(end, 3), 'words': c})

tl = {'total': total, 'scenes': scenes, 'lines': lines_out, 'captions': caps}
open(out_js, 'w').write('window.TL = ' + json.dumps(tl, indent=1) + ';\n')
print('total', total)
for sc in scenes: print('scene', sc['id'], sc['s'], '->', sc['e'])
for c in caps: print(f"{c['s']:6.2f}-{c['e']:6.2f}  " + ' '.join(w['w'] for w in c['words']))
