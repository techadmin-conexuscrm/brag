"""Build the interactive page bundle in page/out/ from final/.
Usage: python3 page/build_page.py   (from 06-overview)
- injects final/chapters.json into page/template.html -> page/out/index.html
- encodes a web copy of the film (720x1280, sized to stay under 14 MB) -> page/out/conexus-overview-web.mp4
- copies captions.vtt and a poster frame
"""
import json, os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
os.makedirs('page/out', exist_ok=True)
ch = json.load(open('final/chapters.json'))
dur = ch[-1]['end']
html = open('page/template.html').read().replace('__CHAPTERS__', json.dumps(ch)).replace('__DURATION__', f"{int(dur // 60)} min {int(dur % 60)} s")
open('page/out/index.html', 'w').write(html)
# two-pass encode to a size budget: 13.5 MB total, 96 kbps audio
budget_bits = 13.5 * 8 * 1024 * 1024
vkbps = int(budget_bits / dur / 1000) - 96
src = 'final/conexus-overview.mp4'
common = ['-vf', 'scale=720:1280:flags=lanczos', '-c:v', 'libx264', '-preset', 'slow', '-b:v', f'{vkbps}k', '-pix_fmt', 'yuv420p']
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', src, *common, '-pass', '1', '-passlogfile', 'build/x264', '-an', '-f', 'mp4', '/dev/null'], check=True)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', src, *common, '-pass', '2', '-passlogfile', 'build/x264', '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', 'page/out/conexus-overview-web.mp4'], check=True)
subprocess.run(['cp', 'final/captions.vtt', 'page/out/captions.vtt'], check=True)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(ch[0]['start'] + 6.5), '-i', src, '-frames:v', '1', '-vf', 'scale=720:1280', 'page/out/poster.jpg'], check=True)
mb = os.path.getsize('page/out/conexus-overview-web.mp4') / 1e6
print(f'page/out ready: {len(ch)} chapters, {dur:.1f}s, web video {mb:.1f} MB at {vkbps} kbps')
