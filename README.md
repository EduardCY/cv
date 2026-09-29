# Portal Profesional de Software & IA — Eduard Criollo Yule

Bienvenido al repositorio oficial del ecosistema profesional de **Eduard Criollo Yule**, enfocado al 100% en **Ingeniería de Software**, **Desarrollo Full Stack** (Spring Boot 3 & Angular 17+) y **Sistemas de Inteligencia Artificial** (FastAPI, Scikit-Learn, Pipelines de ML).

Diseñado bajo la filosofía **Google Antigravity Premium** (Dark Glassmorphism, accesibilidad WCAG 2.1, soporte bilingüe ES/EN y arquitectura Single Source of Truth).

---

## 🧭 Formatos & Portales Disponibles

| Entorno / Formato | Ruta / Enlace | Descripción |
| :--- | :--- | :--- |
| **💻 Portal Principal (Root)** | [`index.html`](index.html) | Landing ejecutiva con selector bilingüe interactivo, métricas y accesos rápidos. |
| **📄 CV Web Profesional (2P)** | [`01_Software_Dev/cv_web/cv_software.html`](01_Software_Dev/cv_web/cv_software.html) | Hoja de vida interactiva optimizada para comités de selección (lectura ejecutiva en 2 minutos). |
| **🖥️ Portafolio Windows 97** | [`01_Software_Dev/portfolio/option_tron/index.html`](01_Software_Dev/portfolio/option_tron/index.html) | Entorno OS retro interactivo con redimensionamiento 8D libre, auto-snapping magnético y soporte móvil responsive. |
| **📑 Visor ATS en Texto Plano** | [`01_Software_Dev/cv_plain_text/viewer.html`](01_Software_Dev/cv_plain_text/viewer.html) | Formato estandarizado sin ruido gráfico, optimizado para Applicant Tracking Systems y terminales. |
| **📥 Descarga Oficial PDF (2P)** | [`01_Software_Dev/cv_web/cv_software_compacto_2p.pdf`](01_Software_Dev/cv_web/cv_software_compacto_2p.pdf) | Documento A4/Carta de 2 páginas con fidelidad tipográfica estricta. |

---

## 📦 Estructura del Repositorio

```text
/
├── index.html                          # 🧭 PORTAL EJECUTIVO PRINCIPAL (Opción B)
├── sitemap.xml                         # Mapa de sitio para motores de búsqueda
├── robots.txt                          # Directivas de indexación pública
├── .gitignore                          # Exclusión estricta de PII y entornos locales
│
├── /data                               # 🌟 FUENTE ÚNICA DE VERDAD (SSOT)
│   ├── profile_software.json           # Perfil madre (ES): Datos, educación, stacks, métricas C1
│   ├── profile_software_en.json        # Perfil madre (EN): Traducido para mercado internacional
│   ├── certifications.json             # Catálogo de certificaciones acreditadas (ES)
│   ├── certifications_en.json          # Catálogo de certificaciones acreditadas (EN)
│   ├── projects.json                   # Repositorio de proyectos de software & IA (ES)
│   ├── projects_en.json                # Repositorio de proyectos de software & IA (EN)
│   ├── bundle.js                       # Bundle JS determinista offline (window.CV_DATA)
│   ├── /assets                         # Activos visuales y foto de perfil
│   └── /img                            # Fotografías de alta resolución
│
├── /01_Software_Dev                    # 💻 NÚCLEO DE INGENIERÍA DE SOFTWARE & IA
│   ├── /cv_web
│   │   ├── cv_software.html            # CV Web (ES) en modo compacto de 2 páginas
│   │   ├── cv_software_en.html         # CV Web (EN) en modo compacto de 2 páginas
│   │   ├── cv_software_compacto_2p.pdf # PDF oficial de 2 páginas (ES)
│   │   └── cv_software_compacto_2p_en.pdf # PDF oficial de 2 páginas (EN)
│   ├── /cv_plain_text
│   │   ├── viewer.html                 # Visor ATS interactivo (ES)
│   │   ├── viewer_en.html              # Visor ATS interactivo (EN)
│   │   ├── cv_software.ts              # Modelo tipado TypeScript (ES)
│   │   └── cv_software_en.ts           # Modelo tipado TypeScript (EN)
│   └── /portfolio
│       └── /option_tron                # 🖥️ Portafolio Windows 97 (Totalmente responsivo Desktop & Móvil)
│
├── /pdf_archive                        # 📂 ACREDITACIONES PÚBLICAS REDACTADAS (Habéas Data)
│   ├── /academic                       # Resultados ICFES y Oxford Placement Test C1
│   └── /certifications                 # Certificaciones técnicas (Dev Senior Code Miami, Platzi, etc.)
│
├── /export_creative_arts               # 🎨 PAQUETE AUTÓNOMO DE ARTES CREATIVAS (Listo para repo independiente)
│
└── /tools                              # 🛠️ AUTOMATIZACIÓN Y COMPILACIÓN
    ├── build_bundle.py                 # Generador del bundle offline SSOT
    ├── export_pdf.py                   # Exportador de PDFs vía Chromium headless
    └── verify_privacy_compliance.py   # Auditor automatizado de PII (cero fugas)
```

---

## 🔒 Auditoría de Privacidad & Cumplimiento (Habéas Data)

Este repositorio aplica políticas estrictas de protección de datos personales (PII):
- Documentos PDF públicos cuentan con censura visual y remoción binaria de identificadores (`1107••••••`).
- Teléfonos de contacto enmascarados para evitar scraping malicioso (`+57 314 ••• ••••`).
- Copias oficiales originales preservadas fuera de Git en almacenamiento local seguro (`pdf_archive_private/`).

---

## 🛠️ Comandos de Automatización

### Compilación del Bundle de Datos (SSOT)
```bash
python tools/build_bundle.py
```

### Generación Automática de Documentos PDF
```bash
python tools/export_pdf.py
```

### Verificación de Cumplimiento de Privacidad (PII)
```bash
python tools/verify_privacy_compliance.py
```

---

## 🌐 Despliegue en GitHub Pages

1. Repositorio en GitHub: `https://github.com/EduardCY/cv.git`
2. En GitHub: `Settings` → `Pages` → `Branch: main` → `Folder: / (root)`.
3. URL pública: `https://eduardcy.github.io/cv/`

---
Copyright &copy; 2026 Eduard Criollo Yule. Cali, Colombia.
