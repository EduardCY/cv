"""
==============================================================================
HERRAMIENTA DE ENMASCARAMIENTO DE TELÉFONO PARA EXPOSICIÓN PÚBLICA (PII)
Ubicación: /tools/redact_phone_numbers.py
Propósito:
  Sustituir el número de teléfono '+57 314 617 6148' por el formato enmascarado
  aprobado '+57 314 ••• ••••' en:
  - Modelos JSON (Single Source of Truth)
  - Vistas Web (cv_software, cv_creative)
  - Visores ATS y archivos TypeScript
  - Archivos de texto plano
==============================================================================
"""

import os
import re
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASKED_PHONE = "+57 314 ••• ••••"
OLD_PHONE_PATTERN = re.compile(r'\+57\s*314\s*617\s*6148')

def update_json_models():
    print("[1/5] Actualizando modelos JSON de datos maestros...")
    json_files = [
        os.path.join(BASE_DIR, "data", "profile_software.json"),
        os.path.join(BASE_DIR, "data", "profile_software_en.json"),
        os.path.join(BASE_DIR, "data", "profile_creative.json"),
        os.path.join(BASE_DIR, "data", "profile_creative_en.json")
    ]
    for jf in json_files:
        if os.path.exists(jf):
            with open(jf, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            contact_obj = None
            if "contact" in data:
                contact_obj = data["contact"]
            elif "personal" in data and "contact" in data["personal"]:
                contact_obj = data["personal"]["contact"]
            
            if contact_obj:
                contact_obj["phone"] = MASKED_PHONE
                contact_obj["phone_note"] = "Disponible bajo solicitud profesional / Available upon request"
            
            with open(jf, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"  -> Actualizado: {jf}")

def update_web_views():
    print("\n[2/5] Actualizando vistas web HTML...")
    html_files = [
        os.path.join(BASE_DIR, "01_Software_Dev", "cv_web", "cv_software.html"),
        os.path.join(BASE_DIR, "01_Software_Dev", "cv_web", "cv_software_en.html"),
        os.path.join(BASE_DIR, "02_Creative_Arts", "cv_web", "cv_creative.html"),
        os.path.join(BASE_DIR, "02_Creative_Arts", "cv_web", "cv_creative_en.html")
    ]
    for hf in html_files:
        if os.path.exists(hf):
            with open(hf, "r", encoding="utf-8") as f:
                content = f.read()
            # Replace tel links and displays
            content = content.replace("+57 314 617 6148", MASKED_PHONE)
            content = content.replace("+573146176148", "+573140000000")
            content = content.replace(
                "url: `tel:${(c.phone || \"+573140000000\").replace(/\\s+/g, '')}`",
                "url: \"mailto:eduardcriolloyule2004@gmail.com?subject=Solicitud%20de%20Contacto%20Telef%C3%B3nico%20-%20Eduard%20Criollo\""
            )
            with open(hf, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  -> Actualizado: {hf}")

def update_ats_and_ts():
    print("\n[3/5] Actualizando visores ATS y archivos TypeScript...")
    targets = [
        os.path.join(BASE_DIR, "01_Software_Dev", "cv_plain_text", "viewer.html"),
        os.path.join(BASE_DIR, "01_Software_Dev", "cv_plain_text", "viewer_en.html"),
        os.path.join(BASE_DIR, "02_Creative_Arts", "cv_plain_text", "viewer.html"),
        os.path.join(BASE_DIR, "02_Creative_Arts", "cv_plain_text", "viewer_en.html"),
        os.path.join(BASE_DIR, "01_Software_Dev", "cv_plain_text", "cv_software.ts"),
        os.path.join(BASE_DIR, "01_Software_Dev", "cv_plain_text", "cv_software_en.ts"),
        os.path.join(BASE_DIR, "02_Creative_Arts", "cv_plain_text", "cv_creative.ts"),
        os.path.join(BASE_DIR, "02_Creative_Arts", "cv_plain_text", "cv_creative_en.ts")
    ]
    for tf in targets:
        if os.path.exists(tf):
            with open(tf, "r", encoding="utf-8") as f:
                content = f.read()
            content = content.replace("+57 314 617 6148", MASKED_PHONE)
            with open(tf, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  -> Actualizado: {tf}")

def update_txt_documents():
    print("\n[4/5] Actualizando archivos de texto histórico en docs/txt/...")
    txt_files = [
        os.path.join(BASE_DIR, "docs", "txt", "CV_prompt_base.txt"),
        os.path.join(BASE_DIR, "docs", "txt", "CV_final.txt"),
        os.path.join(BASE_DIR, "docs", "txt", "Curriculum Vitae.txt")
    ]
    for tf in txt_files:
        if os.path.exists(tf):
            with open(tf, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            content = content.replace("+57 314 617 6148", MASKED_PHONE)
            with open(tf, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  -> Actualizado: {tf}")

def update_tools():
    print("\n[5/5] Sincronizando scripts de utilidades...")
    tool_files = [
        os.path.join(BASE_DIR, "tools", "upgrade_ats_viewers.py"),
        os.path.join(BASE_DIR, "tools", "upgrade_all_cv_web.py")
    ]
    for tf in tool_files:
        if os.path.exists(tf):
            with open(tf, "r", encoding="utf-8") as f:
                content = f.read()
            content = content.replace("+57 314 617 6148", MASKED_PHONE)
            content = content.replace("+573146176148", "+573140000000")
            with open(tf, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  -> Actualizado: {tf}")

if __name__ == "__main__":
    update_json_models()
    update_web_views()
    update_ats_and_ts()
    update_txt_documents()
    update_tools()
    print("\nEnmascaramiento de teléfono completado.")
