#!/usr/bin/env python3
"""
Odysseus Local Agent
Supports: Linux (Arch) + Windows
Features: UE5 build/launch/remote control, git, file ops, shell
"""

import http.server
import json
import subprocess
import os
import sys
import platform
from datetime import datetime

try:
    import requests
except ImportError:
    print("[WARN] requests not installed. Run: pip install requests")
    requests = None

PORT = 8765
IS_WINDOWS = platform.system() == 'Windows'

# ── Paths (auto-detect OS) ──────────────────────────────────────────────
if IS_WINDOWS:
    UE5_PROJECT   = os.environ.get('UE5_PROJECT',   r'C:\Users\%USERNAME%\Documents\Unreal Projects\Apothic')
    UE5_ENGINE    = os.environ.get('UE5_ENGINE',    r'C:\Program Files\Epic Games\UE_5.3')
    EDITOR_BIN    = os.path.join(UE5_ENGINE, r'Engine\Binaries\Win64\UnrealEditor.exe')
    UBT_PATH      = os.path.join(UE5_ENGINE, r'Engine\Build\BatchFiles\Build.bat')
else:
    UE5_PROJECT   = os.environ.get('UE5_PROJECT',   '/home/anthony/Documents/Unreal Projects/Apothic')
    UE5_ENGINE    = os.environ.get('UE5_ENGINE',    '/mnt/storage/UE5_Engine/UnrealEngine')
    EDITOR_BIN    = os.path.join(UE5_ENGINE, 'Engine/Binaries/Linux/UnrealEditor')
    UBT_PATH      = os.path.join(UE5_ENGINE, 'Engine/Build/BatchFiles/Linux/Build.sh')

UPROJECT = None
if os.path.isdir(UE5_PROJECT):
    for f in os.listdir(UE5_PROJECT):
        if f.endswith('.uproject'):
            UPROJECT = os.path.join(UE5_PROJECT, f)
            break

REMOTE_CONTROL_URL = 'http://localhost:30010/remote/object/call'

log = lambda msg: print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

# ── Helpers ─────────────────────────────────────────────────────────────
def run_shell(cmd, cwd=None, timeout=300, background=False):
    if background:
        if IS_WINDOWS:
            subprocess.Popen(cmd, shell=True, cwd=cwd or UE5_PROJECT)
        else:
            subprocess.Popen(cmd, shell=True, cwd=cwd or UE5_PROJECT,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return {'stdout': '', 'stderr': '', 'returncode': 0}
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                            cwd=cwd or UE5_PROJECT, timeout=timeout)
    return {'stdout': result.stdout[-4000:], 'stderr': result.stderr[-2000:], 'returncode': result.returncode}

def check_ue5():
    engine_ok  = os.path.isfile(EDITOR_BIN)
    project_ok = UPROJECT is not None and os.path.isfile(UPROJECT)
    return {
        'engine_ok':  engine_ok,
        'project_ok': project_ok,
        'engine_bin': EDITOR_BIN,
        'uproject':   UPROJECT,
        'os':         platform.system(),
        'engine_linux': os.path.isfile(EDITOR_BIN) and not IS_WINDOWS,
        'engine_win':   os.path.isfile(EDITOR_BIN) and IS_WINDOWS,
        'project':      project_ok,
    }

def open_editor():
    status = check_ue5()
    if not status['engine_ok']:
        return {'ok': False, 'error': f'Editor binary not found: {EDITOR_BIN}'}
    if not status['project_ok']:
        return {'ok': False, 'error': f'No .uproject found in {UE5_PROJECT}'}
    if IS_WINDOWS:
        cmd = f'"{EDITOR_BIN}" "{UPROJECT}"'
    else:
        cmd = f'"{EDITOR_BIN}" "{UPROJECT}" &'
    run_shell(cmd, background=True)
    return {'ok': True, 'output': f'Editor launched: {EDITOR_BIN}'}

def build_project(config='Development'):
    status = check_ue5()
    if not status['engine_ok']:
        return {'ok': False, 'error': 'UBT not found'}
    if IS_WINDOWS:
        cmd = f'"{UBT_PATH}" Apothic Win64 {config} "{UPROJECT}"'
    else:
        cmd = f'"{UBT_PATH}" Apothic Linux {config} "{UPROJECT}"'
    log(f'Building {config}...')
    result = run_shell(cmd, timeout=600)
    return {'ok': result['returncode'] == 0, 'output': result['stdout'] + result['stderr']}

def ue5_remote(object_path, function_name, params=None):
    """Send a command to a running UE5 editor via Remote Control API"""
    if requests is None:
        return {'error': 'requests not installed'}
    payload = {
        'objectPath': object_path,
        'functionName': function_name,
        'parameters': params or {},
        'generateTransaction': True
    }
    r = requests.post(REMOTE_CONTROL_URL, json=payload, timeout=5)
    return r.json()

def ue5_console(cmd):
    """Execute a console command in the running UE5 editor"""
    return ue5_remote('/Engine/LevelEditor.LevelEditor', 'ExecuteConsoleCommand',
                      {'Command': cmd})

def write_file(path, content):
    if not os.path.isabs(path):
        path = os.path.join(UE5_PROJECT, path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return {'ok': True, 'path': path}

def git_commit(message):
    steps = [
        run_shell(f'git -C "{UE5_PROJECT}" add -A'),
        run_shell(f'git -C "{UE5_PROJECT}" commit -m "{message}"'),
        run_shell(f'git -C "{UE5_PROJECT}" push'),
    ]
    return {'ok': all(s['returncode'] == 0 for s in steps), 'steps': steps}

def download_glb(url, filename):
    if requests is None:
        return {'error': 'requests not installed'}
    dest = os.path.join(UE5_PROJECT, 'Content', 'Assets', filename)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    r = requests.get(url, timeout=60)
    with open(dest, 'wb') as f:
        f.write(r.content)
    return {'ok': True, 'saved_to': dest}

# ── Command Dispatcher ───────────────────────────────────────────────────
def dispatch(command: str) -> dict:
    cmd = command.strip()
    log(f'CMD: {cmd[:100]}')

    if cmd in ('status', 'ping'):
        s = check_ue5()
        s['agent'] = 'OdysseusLocal'
        s['port'] = PORT
        return s

    if cmd.startswith('shell:') or cmd.startswith('exec:'):
        return run_shell(cmd.split(':', 1)[1].strip())

    if cmd.startswith('write_file:'):
        parts = cmd[len('write_file:'):].split('\n---\n', 1)
        if len(parts) == 2:
            return write_file(parts[0].strip(), parts[1])
        return {'error': 'format: write_file: path\n---\ncontent'}

    if cmd.startswith('git commit:'):
        return git_commit(cmd[11:].strip())

    if cmd.startswith('build'):
        parts = cmd.split()
        config = parts[1] if len(parts) > 1 else 'Development'
        return build_project(config)

    if cmd in ('open editor', 'launch editor', 'open unreal'):
        return open_editor()

    if cmd.startswith('ue5_console:'):
        return ue5_console(cmd[12:].strip())

    if cmd.startswith('ue5_remote:'):
        try:
            payload = json.loads(cmd[11:].strip())
            return ue5_remote(payload['object'], payload['function'], payload.get('params'))
        except Exception as e:
            return {'error': str(e)}

    if cmd.startswith('download_glb:'):
        parts = cmd[13:].strip().split(None, 1)
        if len(parts) == 2:
            return download_glb(parts[0], parts[1])
        return {'error': 'download_glb: <url> <filename.glb>'}

    # default: treat as shell command
    return run_shell(cmd)

# ── HTTP Server ──────────────────────────────────────────────────────────
class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def _send_json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        self._send_json(200, check_ue5() | {'agent': 'OdysseusLocal', 'port': PORT})

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body)
            result = dispatch(data.get('command', 'status'))
            self._send_json(200, {'ok': True, 'result': result})
        except Exception as e:
            self._send_json(500, {'ok': False, 'error': str(e)})

if __name__ == '__main__':
    print('=' * 56)
    print('  ODYSSEUS LOCAL AGENT  —  Game Director Command Center')
    print('=' * 56)
    print(f'  OS:      {platform.system()}')
    print(f'  Project: {UE5_PROJECT}')
    print(f'  Engine:  {UE5_ENGINE}')
    print(f'  Editor:  {EDITOR_BIN}  [{"FOUND" if os.path.isfile(EDITOR_BIN) else "NOT FOUND"}]')
    print(f'  Uproject:{UPROJECT or "NOT FOUND"}')
    print(f'  Port:    {PORT}')
    print()
    server = http.server.HTTPServer(('0.0.0.0', PORT), Handler)
    log(f'Agent listening on port {PORT}')
    server.serve_forever()
