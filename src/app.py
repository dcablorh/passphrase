"""Local two-step demo UI. Serves on 127.0.0.1 only; nothing leaves the machine.

    python -m src.app        then open http://127.0.0.1:8765
"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from src.shorten import WrongSecret, new_short_wallet, restore_phrase

HOST, PORT = "127.0.0.1", 8765

PAGE = """<!doctype html><meta charset=utf-8><title>Recovery Phrase Shortener</title>
<meta name=viewport content="width=device-width,initial-scale=1">
<style>body{font:16px system-ui;max-width:640px;margin:2rem auto;padding:0 16px}
input,button{font:inherit;width:100%;box-sizing:border-box;margin:.25rem 0 .75rem;padding:.5rem}
pre{background:#eee;color:#111;padding:.75rem;white-space:pre-wrap;word-break:break-all}.err{color:#b00}</style>
<h1>Recovery Phrase Shortener</h1><p>Testnet only. Runs on this machine.</p>
<h2>1. Create</h2>
<label>Secret (20+ characters)<input id=s1 type=password autocomplete=off></label>
<button onclick=mk()>Create 6-word wallet</button><pre id=o1></pre>
<h2>2. Restore</h2>
<label>6 words<input id=w></label><label>Account ID<input id=a></label>
<label>Secret<input id=s2 type=password autocomplete=off></label>
<button onclick=rs()>Restore 12-word phrase</button><pre id=o2></pre>
<script>
async function call(path,body,out){const o=document.getElementById(out);o.className='';o.textContent='...';
try{const r=await fetch(path,{method:'POST',body:JSON.stringify(body)});const j=await r.json();
if(!r.ok){o.className='err';o.textContent=j.error;return}return j}catch(e){o.className='err';o.textContent=String(e)}}
async function mk(){const j=await call('/api/new',{secret:s1.value},'o1');
if(j)o1.textContent='Words: '+j.short_words.join(' ')+'\\nAccount ID: '+j.account_id+'\\nSave both. Keep the secret separate.'}
async function rs(){const j=await call('/api/restore',{words:w.value.split(/\\s+/).filter(Boolean),account_id:a.value,secret:s2.value},'o2');
if(j)o2.textContent='Phrase: '+j.phrase}
</script>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: bytes, ctype: str = "application/json") -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, code: int, obj: dict) -> None:
        self._send(code, json.dumps(obj).encode())

    def do_GET(self):
        if self.path == "/":
            self._send(200, PAGE.encode(), "text/html; charset=utf-8")
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self):
        try:
            data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            if self.path == "/api/new":
                w = new_short_wallet(data.get("secret", ""))
                self._json(200, {"short_words": w["short_words"], "account_id": w["account_id"]})
            elif self.path == "/api/restore":
                phrase = restore_phrase(data.get("words", []), data.get("secret", ""), data.get("account_id", ""))
                self._json(200, {"phrase": phrase})
            else:
                self._json(404, {"error": "not found"})
        except WrongSecret as exc:
            self._json(403, {"error": str(exc)})
        except (ValueError, TypeError, AttributeError) as exc:
            self._json(400, {"error": str(exc)})

    def log_message(self, *args):  # never log request data
        pass


if __name__ == "__main__":
    print(f"Open http://{HOST}:{PORT}  (Ctrl+C to stop)")
    HTTPServer((HOST, PORT), Handler).serve_forever()
