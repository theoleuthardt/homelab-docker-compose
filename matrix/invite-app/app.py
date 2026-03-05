#!/usr/bin/env python3
import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

HOMESERVER = "http://192.168.12.151:8008"
PUBLIC_URL = "https://matrix.theocloud.dev"
ADMIN_USER = "admin"

HTML = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Matrix Einladung</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: system-ui, sans-serif; background: #0d1117; color: #e6edf3; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
  .card {{ background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 2rem; width: 100%; max-width: 420px; }}
  h1 {{ font-size: 1.25rem; margin-bottom: 1.5rem; color: #58a6ff; }}
  label {{ display: block; font-size: 0.85rem; color: #8b949e; margin-bottom: 0.4rem; margin-top: 1rem; }}
  input {{ width: 100%; padding: 0.6rem 0.8rem; background: #0d1117; border: 1px solid #30363d; border-radius: 6px; color: #e6edf3; font-size: 1rem; }}
  input:focus {{ outline: none; border-color: #58a6ff; }}
  button {{ margin-top: 1.5rem; width: 100%; padding: 0.7rem; background: #238636; border: none; border-radius: 6px; color: #fff; font-size: 1rem; cursor: pointer; }}
  button:hover {{ background: #2ea043; }}
  .result {{ margin-top: 1.5rem; padding: 1rem; background: #0d1117; border: 1px solid #30363d; border-radius: 6px; word-break: break-all; }}
  .result a {{ color: #58a6ff; }}
  .error {{ margin-top: 1.5rem; padding: 1rem; background: #2d1117; border: 1px solid #f85149; border-radius: 6px; color: #f85149; font-size: 0.9rem; }}
  .meta {{ font-size: 0.8rem; color: #8b949e; margin-top: 0.5rem; }}
</style>
</head>
<body>
<div class="card">
  <h1>Matrix Einladungslink</h1>
  <form method="POST">
    <label>Admin-Passwort</label>
    <input type="password" name="password" required autofocus>
    <label>Nutzungen</label>
    <input type="number" name="uses" value="1" min="1">
    <label>Ablauf in Stunden (leer = kein Ablauf)</label>
    <input type="number" name="expires" min="1" placeholder="z.B. 24">
    <button type="submit">Link generieren</button>
  </form>
  {content}
</div>
</body>
</html>"""


def login(password: str) -> str:
    data = json.dumps({
        "type": "m.login.password",
        "user": ADMIN_USER,
        "password": password,
    }).encode()
    req = urllib.request.Request(
        f"{HOMESERVER}/_matrix/client/v3/login",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())["access_token"]


def create_token(access_token: str, uses: int, expires_in_hours: int | None) -> str:
    payload: dict = {"uses_allowed": uses}
    if expires_in_hours:
        expiry = datetime.now() + timedelta(hours=expires_in_hours)
        payload["expiry_time"] = int(expiry.timestamp() * 1000)
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{HOMESERVER}/_synapse/admin/v1/registration_tokens/new",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())["token"]


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def send_html(self, content: str, status: int = 200):
        body = HTML.format(content=content).encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self.send_html("")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode()
        params = parse_qs(body)

        password = params.get("password", [""])[0]
        uses = int(params.get("uses", ["1"])[0] or 1)
        expires_raw = params.get("expires", [""])[0].strip()
        expires_in_hours = int(expires_raw) if expires_raw else None

        try:
            access_token = login(password)
            token = create_token(access_token, uses, expires_in_hours)
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            try:
                msg = json.loads(error_body).get("error", error_body)
            except Exception:
                msg = error_body
            self.send_html(f'<div class="error">{msg}</div>')
            return

        link = f"{PUBLIC_URL}/#/register?token={token}"
        meta_parts = [f"{uses}x nutzbar"]
        if expires_in_hours:
            expires_at = datetime.now() + timedelta(hours=expires_in_hours)
            meta_parts.append(f"gültig bis {expires_at.strftime('%d.%m.%Y %H:%M')}")

        self.send_html(f"""
        <div class="result">
            <a href="{link}" target="_blank">{link}</a>
            <div class="meta">{' · '.join(meta_parts)}</div>
        </div>""")


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8090), Handler)
    print("Invite app running on http://0.0.0.0:8090")
    server.serve_forever()
