#!/usr/bin/env python3
"""
tools/export_pdf.py
===================
Script de exportación y generación automática de PDFs para el sistema de CVs
(Eduard Criollo Yule) utilizando servidor HTTP temporal local y Chromium/Edge Headless.

Genera variantes completas y variantes compactas (2 páginas estrictas).
"""

import os
import sys
import shutil
import subprocess
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

# Configuración de codificación UTF-8 para stdout en Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent

# Importar compilador de bundle
try:
    from build_bundle import build_bundle
except ImportError:
    sys.path.append(str(Path(__file__).resolve().parent))
    from build_bundle import build_bundle

TARGETS = [
    {
        "name": "CV Software Web (Completo)",
        "path": "01_Software_Dev/cv_web/cv_software.html",
        "output": WORKSPACE_ROOT / "01_Software_Dev" / "cv_web" / "cv_software_completo.pdf",
        "compat_copy": WORKSPACE_ROOT / "01_Software_Dev" / "cv_web" / "cv_software.pdf"
    },
    {
        "name": "CV Software Web (Compacto - 2 Páginas)",
        "path": "01_Software_Dev/cv_web/cv_software.html?mode=compact",
        "output": WORKSPACE_ROOT / "01_Software_Dev" / "cv_web" / "cv_software_compacto_2p.pdf"
    },
    {
        "name": "CV Software ATS (Texto Plano)",
        "path": "01_Software_Dev/cv_plain_text/viewer.html",
        "output": WORKSPACE_ROOT / "01_Software_Dev" / "cv_plain_text" / "cv_plain.pdf"
    },
    {
        "name": "CV Software Web [EN] (Completo)",
        "path": "01_Software_Dev/cv_web/cv_software_en.html",
        "output": WORKSPACE_ROOT / "01_Software_Dev" / "cv_web" / "cv_software_en_completo.pdf",
        "compat_copy": WORKSPACE_ROOT / "01_Software_Dev" / "cv_web" / "cv_software_en.pdf"
    },
    {
        "name": "CV Software Web [EN] (Compacto - 2 Páginas)",
        "path": "01_Software_Dev/cv_web/cv_software_en.html?mode=compact",
        "output": WORKSPACE_ROOT / "01_Software_Dev" / "cv_web" / "cv_software_en_compacto_2p.pdf"
    },
    {
        "name": "CV Software ATS [EN] (Texto Plano)",
        "path": "01_Software_Dev/cv_plain_text/viewer_en.html",
        "output": WORKSPACE_ROOT / "01_Software_Dev" / "cv_plain_text" / "cv_plain_en.pdf"
    },
    {
        "name": "CV Creative Arts Web (Completo)",
        "path": "02_Creative_Arts/cv_web/cv_creative.html",
        "output": WORKSPACE_ROOT / "02_Creative_Arts" / "cv_web" / "cv_creative_completo.pdf",
        "compat_copy": WORKSPACE_ROOT / "02_Creative_Arts" / "cv_web" / "cv_creative.pdf"
    },
    {
        "name": "CV Creative Arts Web (Compacto - 2 Páginas)",
        "path": "02_Creative_Arts/cv_web/cv_creative.html?mode=compact",
        "output": WORKSPACE_ROOT / "02_Creative_Arts" / "cv_web" / "cv_creative_compacto_2p.pdf"
    },
    {
        "name": "CV Creative Arts ATS (Texto Plano)",
        "path": "02_Creative_Arts/cv_plain_text/viewer.html",
        "output": WORKSPACE_ROOT / "02_Creative_Arts" / "cv_plain_text" / "cv_plain.pdf"
    },
    {
        "name": "CV Creative Arts Web [EN] (Completo)",
        "path": "02_Creative_Arts/cv_web/cv_creative_en.html",
        "output": WORKSPACE_ROOT / "02_Creative_Arts" / "cv_web" / "cv_creative_en_completo.pdf",
        "compat_copy": WORKSPACE_ROOT / "02_Creative_Arts" / "cv_web" / "cv_creative_en.pdf"
    },
    {
        "name": "CV Creative Arts Web [EN] (Compacto - 2 Páginas)",
        "path": "02_Creative_Arts/cv_web/cv_creative_en.html?mode=compact",
        "output": WORKSPACE_ROOT / "02_Creative_Arts" / "cv_web" / "cv_creative_en_compacto_2p.pdf"
    },
    {
        "name": "CV Creative Arts ATS [EN] (Texto Plano)",
        "path": "02_Creative_Arts/cv_plain_text/viewer_en.html",
        "output": WORKSPACE_ROOT / "02_Creative_Arts" / "cv_plain_text" / "cv_plain_en.pdf"
    }
]

def find_browser_executable() -> str | None:
    """Busca el ejecutable de Microsoft Edge o Chrome en rutas estándar de Windows."""
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        shutil.which("msedge"),
        shutil.which("chrome"),
    ]
    for c in candidates:
        if c and os.path.exists(c):
            return c
    return None

class QuietHandler(SimpleHTTPRequestHandler):
    """Manejador HTTP silencioso para no contaminar la salida de consola."""
    def log_message(self, format, *args):
        pass

def start_local_server():
    """Inicia un servidor HTTP local en un puerto dinámico libre."""
    handler = partial(QuietHandler, directory=str(WORKSPACE_ROOT))
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    port = httpd.server_port
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd, port

def main():
    print("=" * 70, flush=True)
    print(" EXPORTADOR DE PDFs // SISTEMA CV EDUARD CRIOLLO YULE", flush=True)
    print("=" * 70, flush=True)

    # 1. Pre-flight: Compilar bundle.js automáticamente
    print("\n[Paso 1] Ejecutando sincronización previa de bundle.js...", flush=True)
    try:
        build_bundle()
    except Exception as e:
        print(f"[ALERTA] No se pudo compilar bundle.js: {e}", flush=True)

    # 2. Localizar navegador
    browser = find_browser_executable()
    if not browser:
        print("[ERROR] No se encontró Microsoft Edge o Chrome para exportación headless.", flush=True)
        print("        Abra los archivos HTML manualmente y use 'Imprimir -> Guardar como PDF'.", flush=True)
        sys.exit(1)

    print(f"[OK] Navegador detectado: {browser}", flush=True)

    # 3. Iniciar servidor HTTP temporal
    httpd, port = start_local_server()
    base_url = f"http://127.0.0.1:{port}"
    print(f"[OK] Servidor HTTP local iniciado en {base_url}", flush=True)

    try:
        for target in TARGETS:
            rel_path = target["path"]
            out = target["output"]
            name = target["name"]
            url = f"{base_url}/{rel_path}"

            print(f"\nGenerando: {name}...", flush=True)
            print(f"  URL   : {url}", flush=True)
            print(f"  Salida: {out}", flush=True)

            out.parent.mkdir(parents=True, exist_ok=True)

            cmd = [
                browser,
                "--headless",
                "--disable-gpu",
                "--no-pdf-header-footer",
                "--run-all-compositor-stages-before-draw",
                "--virtual-time-budget=3000",
                f"--print-to-pdf={out}",
                url
            ]

            try:
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=40)
                if out.exists() and out.stat().st_size > 0:
                    size_kb = out.stat().st_size / 1024
                    print(f"  [EXITO] PDF generado ({size_kb:.1f} KB)", flush=True)

                    # Si tiene copia de compatibilidad
                    if "compat_copy" in target:
                        shutil.copy2(out, target["compat_copy"])
                        print(f"  [COPIA] Sincronizado en: {target['compat_copy'].name}", flush=True)
                else:
                    print(f"  [FALLO] Error al generar PDF: {res.stderr or 'Archivo vacío'}", flush=True)
            except Exception as ex:
                print(f"  [ERROR] Excepción durante exportación: {ex}", flush=True)

    finally:
        print("\nCerrando servidor HTTP local...", flush=True)
        httpd.shutdown()

    print("=" * 70, flush=True)
    print(" Proceso de exportación finalizado exitosamente.", flush=True)
    print("=" * 70, flush=True)

if __name__ == "__main__":
    main()
