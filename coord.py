"""
coord.py — shared coordination board for Artem + Sonnet + Codex
Run: python coord.py
Open: http://localhost:7700
Agents post by appending to coord_log.json directly.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json, os, time
from urllib.parse import parse_qs

DATA_FILE = os.path.join(os.path.dirname(__file__), "coord_log.json")

COLORS = {
    "Artem":  "#4A9EFF",
    "Sonnet": "#B57BFF",
    "Codex":  "#3DD68C",
}

def load():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)

def post(author, text):
    msgs = load()
    msgs.append({"author": author, "text": text.strip(), "time": time.strftime("%H:%M")})
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(msgs, f, ensure_ascii=False, indent=2)

def render_messages(msgs):
    if not msgs:
        return "<div class='empty'>No messages yet.</div>"
    html = ""
    for m in msgs:
        color = COLORS.get(m["author"], "#aaa")
        html += f"""
        <div class="msg">
          <span class="author" style="color:{color}">{m['author']}</span>
          <span class="ts">{m['time']}</span>
          <div class="text">{m['text'].replace(chr(10), '<br>')}</div>
        </div>"""
    return html

HTML_PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>MPNerveBot Coord</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #0e0e12; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; display: flex; flex-direction: column; height: 100vh; }
  header { background: #16161e; padding: 12px 20px; border-bottom: 1px solid #2a2a3a; display: flex; align-items: center; gap: 12px; }
  header h1 { font-size: 15px; font-weight: 600; color: #fff; }
  .dots { display: flex; gap: 8px; margin-left: auto; }
  .dot { width: 10px; height: 10px; border-radius: 50%; }
  .feed { flex: 1; overflow-y: auto; padding: 16px 20px; display: flex; flex-direction: column; gap: 12px; }
  .msg { background: #16161e; border: 1px solid #2a2a3a; border-radius: 8px; padding: 10px 14px; }
  .author { font-weight: 700; font-size: 13px; }
  .ts { font-size: 11px; color: #555; margin-left: 8px; }
  .text { margin-top: 5px; font-size: 14px; line-height: 1.5; color: #d0d0d0; }
  .empty { color: #444; text-align: center; margin-top: 40px; }
  form { background: #16161e; border-top: 1px solid #2a2a3a; padding: 12px 20px; display: flex; gap: 10px; }
  select { background: #0e0e12; color: #e0e0e0; border: 1px solid #2a2a3a; border-radius: 6px; padding: 8px 10px; font-size: 13px; }
  textarea { flex: 1; background: #0e0e12; color: #e0e0e0; border: 1px solid #2a2a3a; border-radius: 6px; padding: 8px 10px; font-size: 14px; resize: none; height: 38px; }
  textarea:focus { outline: none; border-color: #4A9EFF; }
  button { background: #4A9EFF; color: #fff; border: none; border-radius: 6px; padding: 8px 18px; font-size: 14px; cursor: pointer; }
  button:hover { background: #3a8eef; }
</style>
</head>
<body>
<header>
  <h1>MPNerveBot / Coord Board</h1>
  <div class="dots">
    <div class="dot" style="background:#4A9EFF" title="Artem"></div>
    <div class="dot" style="background:#B57BFF" title="Sonnet"></div>
    <div class="dot" style="background:#3DD68C" title="Codex"></div>
  </div>
</header>
<div class="feed" id="feed">
  <div class="empty">Loading...</div>
</div>
<form id="msgForm">
  <select name="author" id="author">
    <option>Artem</option>
    <option>Sonnet</option>
    <option>Codex</option>
  </select>
  <textarea name="text" id="text" placeholder="Type a message... (Enter to send)"></textarea>
  <button type="submit">Send</button>
</form>
<script>
  const COLORS = { Artem: '#4A9EFF', Sonnet: '#B57BFF', Codex: '#3DD68C' };
  let lastCount = 0;

  function renderMsgs(msgs) {
    if (!msgs.length) return '<div class="empty">No messages yet.</div>';
    return msgs.map(m => {
      const color = COLORS[m.author] || '#aaa';
      const text = m.text.replace(/\n/g, '<br>');
      return `<div class="msg">
        <span class="author" style="color:${color}">${m.author}</span>
        <span class="ts">${m.time}</span>
        <div class="text">${text}</div>
      </div>`;
    }).join('');
  }

  function poll() {
    fetch('/api/messages')
      .then(r => r.json())
      .then(msgs => {
        if (msgs.length !== lastCount) {
          lastCount = msgs.length;
          const feed = document.getElementById('feed');
          const atBottom = feed.scrollHeight - feed.scrollTop <= feed.clientHeight + 40;
          feed.innerHTML = renderMsgs(msgs);
          if (atBottom) feed.scrollTop = feed.scrollHeight;
        }
      })
      .catch(() => {});
  }

  document.getElementById('msgForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const author = document.getElementById('author').value;
    const text = document.getElementById('text').value.trim();
    if (!text) return;
    fetch('/post', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: 'author=' + encodeURIComponent(author) + '&text=' + encodeURIComponent(text)
    }).then(() => {
      document.getElementById('text').value = '';
      poll();
    });
  });

  document.getElementById('text').addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      document.getElementById('msgForm').dispatchEvent(new Event('submit'));
    }
  });

  poll();
  setInterval(poll, 4000);
</script>
</body>
</html>"""

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args): pass  # silence default logs

    def do_GET(self):
        if self.path == "/api/messages":
            body = json.dumps(load(), ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", len(body))
            self.end_headers()
            self.wfile.write(body)
        else:
            body = HTML_PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", len(body))
            self.end_headers()
            self.wfile.write(body)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8")
        params = parse_qs(raw)
        author = params.get("author", ["Artem"])[0]
        text = params.get("text", [""])[0]
        if text.strip():
            post(author, text)
        self.send_response(200)
        self.send_header("Content-Length", "0")
        self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(("localhost", 7700), Handler)
    print("Coord board running at http://localhost:7700")
    print("Agents can also write directly to coord_log.json")
    print("Press Ctrl+C to stop.")
    server.serve_forever()
