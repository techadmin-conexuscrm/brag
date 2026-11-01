// Generates one WAV per script line with Kokoro (af_heart). Run from a dir where kokoro-js is installed:
//   node tts.mjs <script.json> <outDir>
import { KokoroTTS } from "kokoro-js";
import fs from "node:fs";
const [scriptPath, outDir] = process.argv.slice(2);
const script = JSON.parse(fs.readFileSync(scriptPath, "utf8"));
const tts = await KokoroTTS.from_pretrained("onnx-community/Kokoro-82M-v1.0-ONNX", { dtype: "fp32", device: "cpu" });
for (const line of script.lines) {
  const audio = await tts.generate(line.say, { voice: script.voice, speed: script.speed });
  audio.save(`${outDir}/${line.id}.wav`);
  console.log(line.id, line.say);
}
