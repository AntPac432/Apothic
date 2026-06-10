import http.server
import json
import subprocess
import os
import requests
from datetime import datetime

PORT = 8765
UE5_PROJECT = "/home/anthony/Documents/Unreal Projects/Apothic/"
UE5_ENGINE  = "/mnt/storage/UE5_Engine/UnrealEngine/"
UBT = os.path.join(UE5_ENGINE, "Engine/Build/BatchFiles/Linux/Build.sh")
EDITOR_BIN  = os.path.join(UE5_ENGINE, "Engine/Binaries/Linux/UnrealEditor")

log = lambda msg: print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def run_shell(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return {"stdout": result.stdout[-3000:], "stderr": result.stderr[-1000:], "returncode": result.returncode}

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    return {"ok": True, "path": path}

def git_commit(message):
    cmds = [
        f'git -C "{UE5_PROJECT}" add -A',
        f'git -C "{UE5_PROJECT}" commit -m "{message}"',
        f'git -C "{UE5_PROJECT}" push'
    ]
    return {"steps": [run_shell(c) for c in cmds]}

def build_project(config="Development"):
    uproject = os.path.join(UE5_PROJECT, "Apothic.uproject")
    cmd = f'"{UBT}" Apothic Linux {config} "{uproject}"'
    log(f"Building {config}...")
    return run_shell(cmd)

def open_editor():
    uproject = os.path.join(UE5_PROJECT, "Apothic.uproject")
    return run_shell(f'"{EDITOR_BIN}" "{uproject}" &')

def download_glb(url, filename):
    dest = os.path.join(UE5_PROJECT, "Content/Assets/", filename)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    r = requests.get(url, timeout=60)
    with open(dest, 'wb') as f:
        f.write(r.content)
    return {"ok": True, "saved_to": dest}

def dispatch(command: str) -> dict:
    cmd = command.strip()
    log(f"CMD: {cmd[:80]}")
    if cmd.startswith("shell:"):
        return run_shell(cmd[6:].strip())
    if cmd.startswith("write_file:"):
        parts = cmd[len("write_file:"):].split("\n---\n", 1)
        if len(parts) == 2:
            return write_file(parts[0].strip(), parts[1])
        return {"error": "format: write_file: path\n---\ncontent"}
    if cmd.startswith("git commit:"):
        return git_commit(cmd[11:].strip())
    if cmd.startswith("build"):
        parts = cmd.split()
        return build_project(parts[1] if len(parts) > 1 else "Development")
    if cmd == "open editor":
        return open_editor()
    if cmd.startswith("download_glb:"):
        parts = cmd[13:].strip().split()
        if len(parts) == 2:
            return download_glb(parts[0], parts[1])
        return {"error": "download_glb: <url> <filename.glb>"}
    return run_shell(cmd)

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body)
            result = dispatch(data.get("command", ""))
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "result": result}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "OdysseusLocal online", "port": PORT}).encode())

if __name__ == '__main__':
    server = http.server.HTTPServer(('0.0.0.0', PORT), Handler)
    log(f"Local agent running on port {PORT}")
    log(f"UE5 Project: {UE5_PROJECT}")
    server.serve_forever()
