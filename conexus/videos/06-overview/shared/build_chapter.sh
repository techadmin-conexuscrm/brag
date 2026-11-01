#!/usr/bin/env bash
# Build one overview chapter.
#   shared/build_chapter.sh chapters/NN-name            full build -> out/video.mp4 (silent), out/preview.mp4, out/sheet.png
#   shared/build_chapter.sh chapters/NN-name stills 1.0,4.5,9.0   quick stills -> out/stills/, out/stills.png
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
CH="$(cd "$1" && pwd)"; MODE="${2:-full}"
TTS_DIR=/tmp/claude-0/-home-user/bcd41ee7-406f-5e52-9e89-3caae16fbbc0/scratchpad/tts
mkdir -p "$CH/out/vo" "$CH/out/frames" "$CH/out/stills"
# 1. voice — only (re)generate lines whose spoken text changed
python3 -I - "$CH" <<'PY'
import json, os, sys
ch = sys.argv[1]; s = json.load(open(f'{ch}/script.json'))
todo = [l for l in s['lines'] if not (os.path.exists(f"{ch}/out/vo/{l['id']}.wav") and os.path.exists(f"{ch}/out/vo/{l['id']}.txt") and open(f"{ch}/out/vo/{l['id']}.txt").read() == l['say'])]
json.dump({**s, 'lines': todo}, open(f'{ch}/out/vo/todo.json', 'w'))
print('tts lines to generate:', [l['id'] for l in todo])
PY
if python3 -c "import json,sys;sys.exit(0 if json.load(open('$CH/out/vo/todo.json'))['lines'] else 1)"; then
  cp "$HERE/tts.mjs" "$TTS_DIR/tts.mjs"
  (cd "$TTS_DIR" && node tts.mjs "$CH/out/vo/todo.json" "$CH/out/vo")
  python3 -I -c "
import json; s=json.load(open('$CH/out/vo/todo.json'))
for l in s['lines']: open('$CH/out/vo/'+l['id']+'.txt','w').write(l['say'])"
fi
# 2. timeline + voice track
python3 -I "$HERE/timeline.py" "$CH/script.json" "$CH/out/vo" "$CH/out/vo.wav" "$CH/out/timeline.js" > "$CH/out/timeline.txt"
cat "$CH/out/timeline.txt" | head -3
# 3. sound effects track
python3 -I "$HERE/sfx.py" "$CH/script.json" "$CH/out/timeline.js" "$CH/out/sfx.wav"
if [ "$MODE" = "stills" ]; then
  node "$HERE/capture.js" "$CH" "$CH/out/stills" 30 "$3"
  python3 -I - "$CH" <<'PY'
import glob, sys
from PIL import Image
ch = sys.argv[1]
fs = sorted(glob.glob(f'{ch}/out/stills/still_*.png'), key=lambda f: float(f.rsplit('_', 1)[1][:-4]))
w, h = 360, 640; cols = min(6, len(fs)); rows = (len(fs) + cols - 1) // cols
s = Image.new('RGB', (cols * w, rows * h), (255, 0, 255))
for i, f in enumerate(fs): s.paste(Image.open(f).convert('RGB').resize((w, h)), ((i % cols) * w, (i // cols) * h))
s.save(f'{ch}/out/stills.png'); print('contact sheet:', f'{ch}/out/stills.png')
PY
  exit 0
fi
# 4. frames -> silent video
find "$CH/out/frames" -name 'f*.png' -delete
node "$HERE/capture.js" "$CH" "$CH/out/frames" 30
ffmpeg -y -hide_banner -loglevel error -framerate 30 -i "$CH/out/frames/f%04d.png" -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -r 30 "$CH/out/video.mp4"
# 5. preview with voice + effects (no music bed — that is added once for the whole film)
ffmpeg -y -hide_banner -loglevel error -i "$CH/out/video.mp4" -i "$CH/out/vo.wav" -i "$CH/out/sfx.wav" \
  -filter_complex "[2:a]volume=0.3[s];[1:a][s]amix=inputs=2:normalize=0[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 160k -shortest "$CH/out/preview.mp4"
ffmpeg -y -hide_banner -loglevel error -i "$CH/out/video.mp4" -vf "fps=1/2,scale=216:384,tile=8x3" -frames:v 1 "$CH/out/sheet.png"
echo "done: $CH/out/video.mp4  preview: $CH/out/preview.mp4  sheet: $CH/out/sheet.png"
