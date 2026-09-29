#!/usr/bin/env python3
"""
tools/build_bundle.py
=====================
Script para compilar y sincronizar automáticamente la fuente única de verdad
(/data/*.json) hacia /data/bundle.js (window.CV_DATA).

Uso:
    python tools/build_bundle.py
"""

import json
import sys
from pathlib import Path

# Configurar encoding UTF-8 en terminal de Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = WORKSPACE_ROOT / "data"

SW_PATH = DATA_DIR / "profile_software.json"
CR_PATH = DATA_DIR / "profile_creative.json"
CERTS_PATH = DATA_DIR / "certifications.json"
PROJS_PATH = DATA_DIR / "projects.json"

SW_EN_PATH = DATA_DIR / "profile_software_en.json"
CR_EN_PATH = DATA_DIR / "profile_creative_en.json"
CERTS_EN_PATH = DATA_DIR / "certifications_en.json"
PROJS_EN_PATH = DATA_DIR / "projects_en.json"

BUNDLE_PATH = DATA_DIR / "bundle.js"

def load_json(path: Path) -> dict:
    """Carga un archivo JSON garantizando codificación UTF-8."""
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_bundle():
    """Genera data/bundle.js combinando los archivos JSON madre (Español e Inglés)."""
    print("=" * 60)
    print(" COMPILADOR DETERMINISTA DE BUNDLE // SSOT BILINGÜE (ES & EN)")
    print("=" * 60)

    try:
        # Cargar datos en español
        sw_data = load_json(SW_PATH)
        cr_data = load_json(CR_PATH)
        certs_raw = load_json(CERTS_PATH)
        projs_raw = load_json(PROJS_PATH)

        certs_list = certs_raw.get("certifications", [])
        projs_list = projs_raw.get("projects", [])

        # Cargar datos en inglés
        sw_en_data = load_json(SW_EN_PATH)
        cr_en_data = load_json(CR_EN_PATH)
        certs_en_raw = load_json(CERTS_EN_PATH)
        projs_en_raw = load_json(PROJS_EN_PATH)

        certs_en_list = certs_en_raw.get("certifications", [])
        projs_en_list = projs_en_raw.get("projects", [])

        # Objeto principal compatible con la arquitectura existente
        bundle_obj_es = {
            "profile_software": sw_data,
            "profile_creative": cr_data,
            "certifications": certs_list,
            "projects": projs_list
        }

        bundle_obj_en = {
            "profile_software": sw_en_data,
            "profile_creative": cr_en_data,
            "certifications": cert_en_list if (cert_en_list := certs_en_list) else certs_list,
            "projects": projs_en_list if projs_en_list else projs_list
        }

        # Estructura combinada
        bundle_combined = {
            **bundle_obj_es,
            "es": bundle_obj_es,
            "en": bundle_obj_en
        }

        # Generar código JavaScript determinista y seguro
        bundle_content = (
            "/**\n"
            " * @fileoverview Bundle consolidado de datos profesionales (Software & Creative Arts).\n"
            " * Incluye soporte bilingüe (Español / Inglés - C1 CEFR).\n"
            " * Generado automáticamente por tools/build_bundle.py.\n"
            " * NO EDITAR ESTE ARCHIVO DIRECTAMENTE. Edita los archivos en /data/*.json y ejecuta build_bundle.py.\n"
            " * \n"
            " * @author Eduard Criollo Yule\n"
            " */\n\n"
            "window.CV_DATA = " + json.dumps(bundle_combined, ensure_ascii=False, indent=2) + ";\n\n"
            "window.CV_DATA_EN = " + json.dumps(bundle_obj_en, ensure_ascii=False, indent=2) + ";\n"
        )

        with open(BUNDLE_PATH, "w", encoding="utf-8") as f:
            f.write(bundle_content)

        print(f"[EXITO] Bundle compilado en: {BUNDLE_PATH}")
        print(f"  - Perfiles Software (ES & EN): OK")
        print(f"  - Perfiles Creativo (ES & EN): OK")
        print(f"  - Certificaciones: {len(certs_list)} ES / {len(certs_en_list)} EN")
        print(f"  - Proyectos      : {len(projs_list)} ES / {len(projs_en_list)} EN")
        print("=" * 60)

    except Exception as e:
        print(f"[ERROR] Falló la compilación del bundle: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_bundle()
