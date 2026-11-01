"""Render a chapter's sound-effects track from script.json "sfx" events.
Usage: python3 sfx.py <script.json> <timeline.js> <out.wav>

Event: {"at": "l3:credited" | "scene:B" | 12.5, "offset": 0.0, "kind": ..., ...}
kinds:  pluck  notes=[midi], level=0.14, decay=14   — pops: cards/messages landing (use notes from A minor: 69 72 76 79 81 84 88)
        click  level=0.10                             — a cursor click / button press
        tick   level=0.05                             — tiny UI tick (rows appearing)
        typing count=6, spacing=0.12                  — keyboard ticks
        bell   notes=[81,88], level=0.16, decay=2.4  — success / money credited / approval
        thud   level=0.3                              — something bad (missed, rejected, blocked)
        boom   level=0.45                             — big reveal (logo)
Scene cuts automatically get a soft swell.
"""
import json, sys, wave
import numpy as np
sys.path.insert(0, __import__('os').path.dirname(__file__))
from audio_lib import SR, place, pluck, bell, boom, swell, read_tl, word_time

script_path, tl_path, out = sys.argv[1:4]
script = json.load(open(script_path)); tl = read_tl(tl_path)
N = int(tl['total'] * SR); buf = np.zeros(N)
scenes = {s['id']: s for s in tl['scenes']}

def when(ev):
    at = ev['at']
    if isinstance(at, (int, float)): t = float(at)
    elif at.startswith('scene:'): t = scenes[at[6:]]['s']
    else: line, word = at.split(':', 1); t = word_time(tl, line, word)
    return t + ev.get('offset', 0.0)

for s in tl['scenes'][1:]:
    place(buf, swell(0.5, 0.04), s['s'] - 0.5)
for ev in script.get('sfx', []):
    t = when(ev); k = ev['kind']; lv = ev.get('level')
    if k == 'pluck':
        for m in ev.get('notes', [81]): place(buf, pluck(m, lv or 0.14, ev.get('decay', 14)), t)
    elif k == 'click': place(buf, pluck(93, lv or 0.10, 30), t)
    elif k == 'tick': place(buf, pluck(88, lv or 0.05, 24), t)
    elif k == 'typing':
        for i in range(ev.get('count', 6)): place(buf, pluck(96, lv or 0.03, 45), t + i * ev.get('spacing', 0.12))
    elif k == 'bell': place(buf, bell(ev.get('notes', [81, 88]), lv or 0.16, ev.get('decay', 2.4)), t)
    elif k == 'thud': place(buf, pluck(45, lv or 0.3, 4), t)
    elif k == 'boom': place(buf, boom(lv or 0.45), t)
    else: raise ValueError('unknown sfx kind ' + k)
with wave.open(out, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(buf, -1, 1) * 32767).astype('<i2').tobytes())
print('sfx', out, len(script.get('sfx', [])), 'events')
