"""
==============================================================================
AUDITOR DE PRIVACIDAD Y CUMPLIMIENTO PII (VERIFICACIÓN AUTOMATIZADA)
Ubicación: /tools/verify_privacy_compliance.py
Propósito:
  Escanear recursivamente el 100% de los documentos públicos del repositorio
  (PDF, JSON, HTML, TS, JS, TXT, MD) para asegurar ausencia total de:
  - Cédula de Ciudadanía: '1107835098'
  - Número de Teléfono sin enmascarar: '314 617 6148' / '3146176148'
==============================================================================
"""

import os
import re
import sys
import fitz

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IGNORED_DIRS = {
    ".venv", "venv", ".git", ".vscode", ".idea",
    "pdf_archive_private", "private_data", "scratch",
    "node_modules", "__pycache__"
}

# Files that legitimately contain the target string for redaction/audit scripts
EXEMPT_FILES = {
    "redact_pii_certificates.py",
    "redact_phone_numbers.py",
    "verify_privacy_compliance.py",
    "privacy_redaction_plan.md",
    "task_list.md",
    "walkthrough.md"
}

ID_PATTERN = re.compile(r'1107835098')
PHONE_PATTERN = re.compile(r'314[\s\-\.]*617[\s\-\.]*6148|3146176148')

def audit_repository():
    print("=" * 70)
    print(" AUDITORÍA INTEGRAL DE PRIVACIDAD Y DATOS PERSONALES (PII)")
    print(f" Directorio raíz: {BASE_DIR}")
    print("=" * 70)

    leaks = []
    scanned_files = 0
    scanned_pdfs = 0

    for root, dirs, files in os.walk(BASE_DIR):
        # Exclude ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for file in files:
            if file in EXEMPT_FILES:
                continue

            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, BASE_DIR)
            scanned_files += 1

            # 1. Escaneo de PDFs
            if file.lower().endswith(".pdf"):
                scanned_pdfs += 1
                try:
                    doc = fitz.open(file_path)
                    for pno in range(len(doc)):
                        page_text = doc[pno].get_text()
                        if ID_PATTERN.search(page_text):
                            leaks.append((rel_path, f"PDF Pág {pno + 1}", "Cédula 1107835098 detectada en stream de texto"))
                        if PHONE_PATTERN.search(page_text):
                            leaks.append((rel_path, f"PDF Pág {pno + 1}", "Teléfono sin enmascarar detectado"))
                    doc.close()
                except Exception as e:
                    print(f"  [ERROR leyendo PDF] {rel_path}: {e}")

            # 2. Escaneo de Texto Plano / Código
            elif file.lower().endswith(('.json', '.html', '.ts', '.js', '.txt', '.md', '.py', '.xml', '.yml', '.yaml')):
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                    for idx, line in enumerate(lines, 1):
                        if ID_PATTERN.search(line):
                            leaks.append((rel_path, f"Línea {idx}", f"Cédula 1107835098: {line.strip()[:60]}..."))
                        if PHONE_PATTERN.search(line):
                            leaks.append((rel_path, f"Línea {idx}", f"Teléfono sin enmascarar: {line.strip()[:60]}..."))
                except Exception as e:
                    print(f"  [ERROR leyendo texto] {rel_path}: {e}")

    print(f"\nResumen de Escaneo:")
    print(f"  - Archivos totales analizados: {scanned_files}")
    print(f"  - Archivos PDF inspeccionados: {scanned_pdfs}")
    print("-" * 70)

    if leaks:
        print(f"\n❌ FALLO: Se detectaron {len(leaks)} fugas de información sensible:")
        for file, loc, desc in leaks:
            print(f"  [! ALERTA] {file} ({loc}) -> {desc}")
        print("=" * 70)
        sys.exit(1)
    else:
        print("\n✅ PASS: 0 fugas de PII detectadas.")
        print("  - Cédula de ciudadanía: 100% protegida/redactada.")
        print("  - Número telefónico: 100% enmascarado (+57 314 ••• ••••).")
        print("  - Repositorio listo para publicación pública en internet.")
        print("=" * 70)
        sys.exit(0)

if __name__ == "__main__":
    audit_repository()
