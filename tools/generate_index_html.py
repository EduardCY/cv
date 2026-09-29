"""
==============================================================================
GENERADOR DE INDEX.HTML CANÓNICO PARA GITHUB PAGES Y PRODUCCIÓN WEB
Ubicación: /tools/generate_index_html.py
==============================================================================
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_HUB = os.path.join(BASE_DIR, "CV_Eduard_Criollo_Yule.html")
DEST_INDEX = os.path.join(BASE_DIR, "index.html")

OG_TAGS = """    <!-- OpenGraph & Redes Sociales (LinkedIn, WhatsApp, X) -->
    <link rel="canonical" href="https://eduardcy.github.io/cv/">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Eduard Criollo Yule — Professional Portfolio">
    <meta property="og:title" content="Eduard Criollo Yule — Sistemas, IA & Tecnologías Creativas">
    <meta property="og:description" content="Portafolio profesional interactivo, credenciales de ingeniería de software (Spring Boot, Angular, IA), certificación de inglés C1 y artes técnicas.">
    <meta property="og:image" content="https://eduardcy.github.io/cv/foto.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:url" content="https://eduardcy.github.io/cv/">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Eduard Criollo Yule — Systems Engineer & Creative Technologist">
    <meta name="twitter:description" content="Interactive bilingual CV and portfolio: Full Stack development, Applied AI, C1 English and Technical Art.">
    <meta name="twitter:image" content="https://eduardcy.github.io/cv/foto.png">
"""

with open(SRC_HUB, "r", encoding="utf-8") as f:
    html = f.read()

# Insert OpenGraph tags right before Google Fonts link
html = html.replace("<!-- Google Fonts -->", OG_TAGS + "\n    <!-- Google Fonts -->")

# Upgrade language detection logic in script
old_lang_logic = "let currentLang = new URLSearchParams(window.location.search).get('lang') || localStorage.getItem('hub_lang') || 'es';"
new_lang_logic = "let currentLang = new URLSearchParams(window.location.search).get('lang') || localStorage.getItem('hub_lang') || ((navigator.language || '').toLowerCase().startsWith('en') ? 'en' : 'es');"
html = html.replace(old_lang_logic, new_lang_logic)

with open(DEST_INDEX, "w", encoding="utf-8") as f:
    f.write(html)

print(f"[EXITO] index.html generado en: {DEST_INDEX}")
