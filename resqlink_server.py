
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import json
import time
import io
import ssl

import numpy as np
from scipy.io import wavfile

HOST = "0.0.0.0"
PORT = 8000
FOLDER = Path(__file__).resolve().parent
LATEST_AUDIO = FOLDER / "latest_received.wav"
LATEST_INFO = FOLDER / "latest_info.json"
SAMPLE_RATE = 16000
REPETITIONS = 3


SENDER_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ResQLink Sender</title>
<style>
body{font-family:Arial,sans-serif;max-width:650px;margin:35px auto;padding:20px;background:#f2f5fb}
main{background:white;padding:25px;border-radius:18px}
button{width:100%;padding:16px;border:0;border-radius:10px;background:#1760ed;color:white;font-size:18px}
p{line-height:1.5}#status{background:#edf0ff;padding:15px;border-radius:10px;margin-top:18px}
a{display:inline-block;margin-top:18px}
</style>
</head>
<body><main>
<h1>ResQLink — Sender</h1>
<p>Record a voice message on this phone and send it through the ResQLink laptop server.</p>
<button id="record">Record 5 Seconds and Send</button>
<div id="status">Ready. Tap the button and allow microphone access.</div>
<a href="/receiver">Open Receiver Page</a>
<script>
const button = document.getElementById('record');
const statusBox = document.getElementById('status');

function makeWav(samples, rate) {
  const buffer = new ArrayBuffer(44 + samples.length * 2);
  const view = new DataView(buffer);
  function str(offset, text) {
    for (let i=0; i<text.length; i++) view.setUint8(offset+i, text.charCodeAt(i));
  }
  str(0,'RIFF'); view.setUint32(4,36+samples.length*2,true);
  str(8,'WAVE'); str(12,'fmt '); view.setUint32(16,16,true);
  view.setUint16(20,1,true); view.setUint16(22,1,true);
  view.setUint32(24,rate,true); view.setUint32(28,rate*2,true);
  view.setUint16(32,2,true); view.setUint16(34,16,true);
  str(36,'data'); view.setUint32(40,samples.length*2,true);
  for(let i=0;i<samples.length;i++) view.setInt16(44+i*2,samples[i],true);
  return new Blob([buffer], {type:'audio/wav'});
}

button.onclick = async () => {
  button.disabled = true;
  let stream, audioContext;
  try {
    statusBox.textContent = 'Requesting microphone access...';
    stream = await navigator.mediaDevices.getUserMedia({audio:true});
    audioContext = new AudioContext();
    await audioContext.resume();

    const source = audioContext.createMediaStreamSource(stream);
    const processor = audioContext.createScriptProcessor(4096,1,1);
    const chunks = [];
    source.connect(processor);
    processor.connect(audioContext.destination);

    statusBox.textContent = 'Recording for 5 seconds. Speak now!';
    processor.onaudioprocess = event => {
      chunks.push(new Float32Array(event.inputBuffer.getChannelData(0)));
    };

    await new Promise(resolve => setTimeout(resolve, 5000));
    processor.onaudioprocess = null;
    source.disconnect();
    processor.disconnect();
    stream.getTracks().forEach(track => track.stop());

    const input = new Float32Array(chunks.reduce((n,c)=>n+c.length,0));
    let offset = 0;
    for(const chunk of chunks){input.set(chunk,offset);offset+=chunk.length;}

    // Downsample to 16 kHz by averaging each input segment.
    const inRate = audioContext.sampleRate;
    const outLength = Math.floor(input.length * 16000 / inRate);
    const pcm = new Int16Array(outLength);
    for(let i=0;i<outLength;i++){
      const start = Math.floor(i*inRate/16000);
      const end = Math.min(input.length,Math.floor((i+1)*inRate/16000));
      let sum=0;
      for(let j=start;j<end;j++) sum+=input[j];
      const sample = sum/Math.max(1,end-start);
      pcm[i] = Math.max(-32768,Math.min(32767,Math.round(sample*32767)));
    }

    statusBox.textContent = 'Uploading your voice to the laptop...';
    const response = await fetch('/upload', {
      method:'POST', headers:{'Content-Type':'audio/wav'},
      body:makeWav(pcm,16000)
    });
    const result = await response.json();
    if(!response.ok) throw new Error(result.error || 'Upload failed');
    statusBox.textContent =
      'Sent successfully! Samples: '+result.samples+
      ' | Simulated BPSK bit errors: '+result.bit_errors+
      '. Open the Receiver page on the other phone.';
  } catch(err) {
    statusBox.textContent = 'Could not record/send: '+err.message+
      '. If microphone access is blocked, see the HTTPS note below.';
  } finally {
    if(stream) stream.getTracks().forEach(track=>track.stop());
    if(audioContext) await audioContext.close().catch(()=>{});
    button.disabled = false;
  }
};
</script>
</main></body></html>"""


RECEIVER_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ResQLink Receiver</title>
<style>
body{font-family:Arial,sans-serif;max-width:650px;margin:35px auto;padding:20px;background:#f2f5fb}
main{background:white;padding:25px;border-radius:18px}
#status{background:#edf0ff;padding:15px;border-radius:10px;margin:18px 0}
audio{width:100%}a{display:inline-block;margin-top:18px}
</style>
</head>
<body><main>
<h1>ResQLink — Receiver</h1>
<p>This page waits for a voice message sent from another phone.</p>
<div id="status">Waiting for a new voice message...</div>
<audio id="player" controls></audio>
<p>When a message arrives, press Play if it does not start automatically.</p>
<a href="/">Open Sender Page</a>
<script>
let lastId = '';
async function checkForMessage(){
  try{
    const response = await fetch('/status', {cache:'no-store'});
    const data = await response.json();
    if(data.id && data.id !== lastId){
      lastId = data.id;
      const player = document.getElementById('player');
      player.src = '/latest.wav?id='+encodeURIComponent(lastId);
      player.load();
      document.getElementById('status').textContent =
        'New voice message received! Tap Play to listen.';
    }
  }catch(e){
    document.getElementById('status').textContent =
      'Cannot reach server. Check that the laptop server is running.';
  }
}
checkForMessage();
setInterval(checkForMessage,2000);
</script>
</main></body></html>"""


class ResQLinkHandler(BaseHTTPRequestHandler):
    def send_bytes(self, status, data, content_type):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/":
            self.send_bytes(200, SENDER_HTML.encode(), "text/html; charset=utf-8")
        elif path == "/receiver":
            self.send_bytes(200, RECEIVER_HTML.encode(), "text/html; charset=utf-8")
        elif path == "/status":
            info = {}
            if LATEST_INFO.exists():
                try:
                    info = json.loads(LATEST_INFO.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError):
                    pass
            self.send_bytes(200, json.dumps(info).encode(), "application/json")
        elif path == "/latest.wav":
            if not LATEST_AUDIO.exists():
                self.send_bytes(404, b"No voice message received yet.", "text/plain")
            else:
                self.send_bytes(200, LATEST_AUDIO.read_bytes(), "audio/wav")
        else:
            self.send_bytes(404, b"Not found", "text/plain")

    def do_POST(self):
        if urlparse(self.path).path != "/upload":
            self.send_bytes(404, b'{"error":"Not found"}', "application/json")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 44 or length > 15_000_000:
                raise ValueError("Audio file is empty or too large")

            uploaded = self.rfile.read(length)
            rate, audio = wavfile.read(io.BytesIO(uploaded))

            if rate != SAMPLE_RATE:
                raise ValueError("Expected 16000 Hz audio")
            if audio.ndim == 2:
                audio = audio.astype(np.int32).mean(axis=1).astype(np.int16)
            if audio.dtype != np.int16:
                raise ValueError("Expected 16-bit PCM WAV audio")
            if len(audio) == 0:
                raise ValueError("No audio samples found")

            # Simplified 8-bit PCM -> BPSK simulation -> recovered audio.
            pcm8 = np.clip(
                audio.astype(np.float32) / 256.0 + 128.0, 0, 255
            ).astype(np.uint8)
            bits = np.unpackbits(pcm8)
            symbols = 1.0 - 2.0 * bits.astype(np.float32)
            transmitted = np.repeat(symbols, REPETITIONS)
            noise = np.random.normal(0.0, 0.15, transmitted.size)
            received = transmitted + noise
            decisions = received.reshape(-1, REPETITIONS).mean(axis=1)
            recovered_bits = (decisions < 0).astype(np.uint8)
            bit_errors = int(np.count_nonzero(bits != recovered_bits))
            recovered8 = np.packbits(recovered_bits)
            recovered16 = (
                (recovered8.astype(np.int16) - 128) * 256
            ).astype(np.int16)

            wavfile.write(LATEST_AUDIO, SAMPLE_RATE, recovered16)
            message_id = str(int(time.time() * 1000))
            LATEST_INFO.write_text(
                json.dumps({"id": message_id, "samples": len(recovered16)}),
                encoding="utf-8"
            )

            result = {
                "ok": True,
                "samples": len(recovered16),
                "bit_errors": bit_errors,
                "ber": bit_errors / max(1, len(bits))
            }
            self.send_bytes(200, json.dumps(result).encode(), "application/json")
            print(f"Received phone audio; samples={len(recovered16)}, "
                  f"bit_errors={bit_errors}. Available to receiver.")

        except Exception as exc:
            print("Upload error:", repr(exc))
            body = json.dumps({"error": str(exc)}).encode()
            self.send_bytes(400, body, "application/json")


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), ResQLinkHandler)

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(
        certfile=str(FOLDER / "10.10.20.158+2.pem"),
        keyfile=str(FOLDER / "10.10.20.158+2-key.pem")
    )

    server.socket = ssl_context.wrap_socket(
        server.socket,
        server_side=True
    )

    print("ResQLink HTTPS server running on port 8000")
    print("Sender:   https://10.10.20.158:8000/")
    print("Receiver: https://10.10.20.158:8000/receiver")

    server.serve_forever()