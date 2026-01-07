import os
import re
import subprocess
import sys
import tempfile
import time
from typing import Optional, Tuple

import requests


_VERSION_RE = re.compile(r"\b\d+(?:\.\d+){1,3}\b")


def extract_version_from_filename(filename: str) -> Optional[str]:
    if not filename:
        return None
    m = _VERSION_RE.search(filename)
    return m.group(0) if m else None


def _version_tuple(v: str) -> Optional[Tuple[int, ...]]:
    if not v:
        return None
    parts = v.split(".")
    try:
        return tuple(int(p) for p in parts)
    except Exception:
        return None


def is_newer(current_version: str, remote_version: str) -> bool:
    ct = _version_tuple(current_version)
    rt = _version_tuple(remote_version)
    if ct is None or rt is None:
        return current_version.strip() != remote_version.strip()

    max_len = max(len(ct), len(rt))
    ct = ct + (0,) * (max_len - len(ct))
    rt = rt + (0,) * (max_len - len(rt))
    return rt > ct


def _is_frozen() -> bool:
    return bool(getattr(sys, "frozen", False))


def _extract_filename_from_headers(resp: requests.Response) -> Optional[str]:
    cd = resp.headers.get("Content-Disposition") or resp.headers.get("content-disposition")
    if not cd:
        return None
    m = re.search(r"filename\*=UTF-8''([^;]+)", cd, flags=re.IGNORECASE)
    if m:
        return requests.utils.unquote(m.group(1).strip().strip('"'))
    m = re.search(r"filename=([^;]+)", cd, flags=re.IGNORECASE)
    if m:
        return m.group(1).strip().strip('"')
    return None


def _current_version() -> str:
    # Prefer exe filename version, fallback to env.
    exe_name = os.path.basename(sys.executable)
    v = extract_version_from_filename(exe_name)
    if v:
        return v
    return os.environ.get("CHECKIT_VERSION", "0.0.0")


def _show_message_box(title: str, message: str) -> None:
    try:
        import ctypes

        ctypes.windll.user32.MessageBoxW(0, message, title, 0x00000040)  # MB_ICONINFORMATION
    except Exception:
        pass


def download_remote_exe(update_url: str, timeout_s: int = 30) -> Tuple[str, str, str]:
    """Downloads EXE from update_url to temp dir.

    Returns (download_path, filename, remote_version).
    """
    resp = requests.get(update_url, stream=True, allow_redirects=True, timeout=timeout_s)
    resp.raise_for_status()

    filename = _extract_filename_from_headers(resp)
    if not filename:
        filename = os.path.basename(requests.utils.urlparse(resp.url).path) or "CheckIt_update.exe"

    remote_version = extract_version_from_filename(filename) or ""

    dest_path = os.path.join(tempfile.gettempdir(), filename)
    with open(dest_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=1024 * 256):
            if chunk:
                f.write(chunk)

    return dest_path, filename, remote_version


def _write_replace_script_ps1(
    *,
    pid: int,
    source_exe: str,
    target_exe: str,
    new_version: str,
    restart_args: list[str],
) -> str:
    ts = int(time.time())
    script_path = os.path.join(tempfile.gettempdir(), f"checkit_replace_{ts}.ps1")

    # Quote args for PowerShell Start-Process
    arg_list = " ".join([f'"{a}"' for a in restart_args])

    script = f"""param(
  [int]$Pid,
  [string]$SourceExe,
  [string]$TargetExe,
  [string]$RestartArgs
)

$ErrorActionPreference = 'Stop'

Write-Host "CheckIt updater: waiting for PID $Pid..."
for ($i = 0; $i -lt 240; $i++) {{
  $p = Get-Process -Id $Pid -ErrorAction SilentlyContinue
  if (-not $p) {{ break }}
  Start-Sleep -Milliseconds 500
}}

Write-Host "Replacing $TargetExe with $SourceExe"
Copy-Item -Path $SourceExe -Destination $TargetExe -Force

[Environment]::SetEnvironmentVariable('CHECKIT_VERSION', '{new_version.replace("'", "")}', 'User')

Write-Host "Starting updated app..."
if ([string]::IsNullOrWhiteSpace($RestartArgs)) {{
  Start-Process -FilePath $TargetExe
}} else {{
  Start-Process -FilePath $TargetExe -ArgumentList $RestartArgs
}}
"""

    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script)

    return script_path


def check_and_maybe_update(
    *,
    update_url: Optional[str],
    show_ui: bool = True,
) -> None:
    """Downloads remote EXE, compares version from filename, and updates if newer.

    Behaviour requested:
    - show "Checking update" (handled by caller)
    - download remote exe
    - if newer: notify user, close app, open console to run replace script, restart updated exe
    """

    if not update_url:
        return

    if not _is_frozen():
        # Only safe for packaged EXE
        return

    current_v = _current_version()

    download_path, filename, remote_v = download_remote_exe(update_url)
    if not remote_v:
        # If server doesn't provide version in filename, we can't compare.
        return

    if not is_newer(current_v, remote_v):
        return

    if show_ui:
        _show_message_box(
            "CheckIt - Aktualizacja",
            f"Znaleziono nowszą wersję aplikacji ({remote_v}). Rozpoczynam aktualizację...",
        )

    pid = os.getpid()
    target_exe = sys.executable
    restart_args = [a for a in sys.argv[1:] if a not in ("--update-url",) and not a.startswith("--update-")]
    script_path = _write_replace_script_ps1(
        pid=pid,
        source_exe=download_path,
        target_exe=target_exe,
        new_version=remote_v,
        restart_args=restart_args,
    )

    # Open console and run script
    cmd = [
        "powershell.exe",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-NoExit",
        "-File",
        script_path,
        "-Pid",
        str(pid),
        "-SourceExe",
        download_path,
        "-TargetExe",
        target_exe,
        "-RestartArgs",
        " ".join([f'\"{a}\"' for a in restart_args]) if restart_args else "",
    ]

    subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
    raise SystemExit(0)
