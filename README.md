# Sistema Profesional Integral — Eduard Criollo Yule

## Dual-Career Architecture: Software Engineering & Creative Arts

Bienvenido al repositorio centralizado y desacoplado de la presencia profesional de **Eduard Criollo Yule**, diseñado bajo el estándar **Google Antigravity Premium** y estructurado en dos carreras paralelas con sincronización automática mediante Fuente Única de Verdad (SSOT):

1. **01_Software_Dev:** Full Stack Empresarial (Spring Boot & Angular), Inteligencia Artificial & Data Science (FastAPI, Scikit-Learn, Python), Bases de Datos Relacionales (SQL) y Estudiante de Ingeniería de Sistemas (UAO).
2. **02_Creative_Arts:** Bachiller Técnico en Dibujo Técnico Industrial (San Juan Bosco), Ilustrador Digital, Animador 2D/3D (Blender, After Effects) y Escritor Galardonado en certámenes de ficción especulativa.

---

## 🏛️ Centro de Acceso & Arquitectura de Datos

### 🧭 Punto de Entrada Central (Hub)

- **`CV_Eduard_Criollo_Yule.html`**: Portal interactivo central con estética Antigravity Dark Glassmorphism, selector de carreras profesionales, métricas globales dinámicas (+18 acreditaciones, 100% C1 Oxford English, 100% SSOT) e hipervínculos externos directos a perfiles públicos (LinkedIn, GitHub, ArtStation, Platzi).

### 📦 Estructura del Repositorio

```text
/Cv
├── CV_Eduard_Criollo_Yule.html         # 🧭 HUB DE ENTRADA CENTRALIZADO
├── /data                               # 🌟 FUENTE ÚNICA DE VERDAD (SSOT)
│   ├── profile_software.json           # Perfil madre: Software, IA, educación, métricas C1
│   ├── profile_creative.json           # Perfil madre: Arte, dibujo industrial, animación, narrativa
│   ├── certifications.json             # Catálogo global de certificaciones verificadas (18 acreditaciones)
│   ├── projects.json                   # Repositorio global de proyectos con especificación CRUD
│   ├── bundle.js                       # Bundle transpilado determinista para consumo local/offline
│   └── /assets                         # Assets optimizados (foto.png)
│
├── /01_Software_Dev                    # 💻 RAMA DE INGENIERÍA DE SOFTWARE & IA
│   ├── /cv_web
│   │   ├── cv_software.html            # CV web visual interactivo con modo Normal / Compacto (2 Páginas)
│   │   ├── cv_software_completo.pdf    # PDF de alta fidelidad exportado (Catálogo completo)
│   │   ├── cv_software_compacto_2p.pdf # PDF de alta fidelidad exportado (Estricto 2 Páginas)
│   │   └── cv_software.pdf             # Copia sincronizada del PDF principal
│   ├── /cv_plain_text
│   │   ├── cv_software.ts              # Modelo tipado en TypeScript con TSDoc completo
│   │   ├── viewer.html                 # Visor monospaciado ATS tipo terminal con enlaces explícitos
│   │   └── cv_plain.pdf                # PDF ATS optimizado para escáneres de reclutamiento
│   └── /portfolio
│       ├── /option_gothic              # 🏛️ Portafolio: Arquitectura Gótica (Mármol, Arcos, Oro)
│       └── /option_tron                # 💾 Portafolio: Windows 97 Retro Edition (Ventanas 3D, Taskbar, Inicio)
│
├── /02_Creative_Arts                   # 🎨 RAMA DE ARTES CREATIVAS & NARRATIVA
│   ├── /cv_web
│   │   ├── cv_creative.html            # CV web visual interactivo con modo Normal / Compacto (2 Páginas)
│   │   ├── cv_creative_completo.pdf    # PDF artístico exportado (Catálogo completo)
│   │   ├── cv_creative_compacto_2p.pdf # PDF artístico exportado (Estricto 2 Páginas)
│   │   └── cv_creative.pdf             # Copia sincronizada del PDF artístico
│   ├── /cv_plain_text
│   │   ├── cv_creative.ts              # Definición TypeScript para el perfil creativo
│   │   ├── viewer.html                 # Visor monospaciado ATS para narrativa y arte
│   │   └── cv_plain.pdf                # PDF ATS para el sector creativo
│   └── /portfolio
│       └── (index.html, style.css, js) # 🖼️ Galería Atelier de Concept Art, Animación & Textos
│
├── /pdf_archive                        # 📂 ARCHIVO HISTÓRICO DE ACREDITACIONES (SSOT)
│   ├── /academic                       # Acreditaciones académicas y OOPT.pdf (C1 Oxford 115/120)
│   ├── /certifications                 # Diplomas Dev Senior Code y Platzi (18 certificados verificables)
│   └── /legacy_cv                      # Versiones previas de hojas de vida
│
└── /tools                              # 🛠️ HERRAMIENTAS Y SCRIPTS DE AUTOMATIZACIÓN
    ├── build_bundle.py                 # Generador determinista del bundle JS offline (window.CV_DATA)
    ├── export_pdf.py                   # Compilador multiobjetivo de los 6 PDFs vía Headless Chrome + servidor local
    └── pdf_to_txt.py                   # Extractor de texto para documentos PDF
```

---

## 🚀 Guía de Operación y Visualización

### 1. Visualización Web Interactiva

Puedes abrir cualquiera de los siguientes documentos directamente en cualquier navegador moderno:

- **Punto de Entrada Global:** `CV_Eduard_Criollo_Yule.html`
- **CV Software Web:** `01_Software_Dev/cv_web/cv_software.html`
  - *Modo Normal:* Despliega todo el catálogo de experiencia, proyectos y las 18 certificaciones.
  - *Modo Compacto (2 Páginas):* Pulsa el botón **"📄 Modo 2 Páginas (Compacto)"** o ingresa con `?mode=compact`.
- **CV Creativo Web:** `02_Creative_Arts/cv_web/cv_creative.html`
  - *Modo Normal:* Despliega el catálogo completo y acreditaciones de diseño/dibujo.
  - *Modo Compacto (2 Páginas):* Pulsa el botón **"📄 Modo 2 Páginas (Compacto)"** o ingresa con `?mode=compact`.
- **Portafolios Especializados:**
  - *Software (Gótico):* `01_Software_Dev/portfolio/option_gothic/index.html`
  - *Software (Windows 97):* `01_Software_Dev/portfolio/option_tron/index.html`
  - *Artes Creativas (Atelier):* `02_Creative_Arts/portfolio/index.html`
- **Visores ATS Monospaciados:**
  - `01_Software_Dev/cv_plain_text/viewer.html`
  - `02_Creative_Arts/cv_plain_text/viewer.html`

---

## 🖨️ Generación de PDFs Automatizada (6 Objetivos)

El script `tools/export_pdf.py` realiza automáticamente un pre-flight compilando el bundle de datos, levanta un servidor HTTP local efímero para sortear restricciones de CORS locales y compila los 6 PDFs con Google Chrome Headless:

```bash
python tools/export_pdf.py
```

### Catálogo de PDFs Generados:

1. `01_Software_Dev/cv_web/cv_software_completo.pdf` — Versión web completa software.
2. `01_Software_Dev/cv_web/cv_software_compacto_2p.pdf` — **Versión compacta exacta de 2 páginas** optimizada para reclutadores.
3. `01_Software_Dev/cv_plain_text/cv_plain.pdf` — Versión ATS en texto plano para software.
4. `02_Creative_Arts/cv_web/cv_creative_completo.pdf` — Versión web completa de artes creativas.
5. `02_Creative_Arts/cv_web/cv_creative_compacto_2p.pdf` — **Versión compacta exacta de 2 páginas** para sector creativo.
6. `02_Creative_Arts/cv_plain_text/cv_plain.pdf` — Versión ATS en texto plano para artes creativas.

---

## 📝 Manual Operativo CRUD: Cómo Agregar, Modificar o Eliminar Información

Todo el ecosistema está 100% desacoplado. **Nunca debes editar directamente archivos HTML o visores para cambiar información personal, proyectos o certificaciones.** Solo editas en `/data/` y ejecutas la sincronización.

### Caso A: Agregar o Modificar una Certificación

1. **Guardar el PDF físico:** Coloca el archivo PDF descargado en la carpeta correspondiente:
   - Si es de Platzi: `pdf_archive/certifications/Platzi/diploma-nuevo.pdf`
   - Si es de Dev Senior: `pdf_archive/certifications/DevSeniorCode/diploma-nuevo.pdf`
   - Si es académica: `pdf_archive/academic/diploma-nuevo.pdf`
2. **Editar `/data/certifications.json`:** Agrega un nuevo elemento al array `certifications`:
   ```json
   {
     "id": "cert-nueva-01",
     "title": "Nombre de la Certificación o Especialización",
     "issuer": "Platzi | Dev Senior Code | UAO",
     "year": "2026",
     "track": ["software"],
     "category": "ai_ml",
     "verification_url": "https://platzi.com/p/tu-usuario/certificado/token/",
     "archive_pdf": "pdf_archive/certifications/Platzi/diploma-nuevo.pdf",
     "featured": true
   }
   ```

   *Nota sobre `track`:*- Use `["software"]` para que aparezca en el CV de Software y ATS Software.
   - Use `["creative"]` para que aparezca en el CV Creativo y ATS Creativo.
   - Use `["both"]` para que aparezca en ambos perfiles (ej. Bachiller Técnico en Dibujo o C1 English).
3. **Sincronizar:**
   Ejecuta en tu terminal:
   ```bash
   python tools/build_bundle.py
   ```

   *(O directamente `python tools/export_pdf.py`, el cual ya incluye la compilación del bundle y actualiza todos los PDFs).*

### Caso B: Modificar o Agregar Proyectos

1. Abre `/data/projects.json`.
2. Añade o edita un proyecto dentro de `projects`:
   - Para Software: `"category": "software"`.
   - Para Creativo: `"category": "creative"`.
3. Especifica enlaces explícitos a repositorios, demos y tecnologías.
4. Ejecuta `python tools/build_bundle.py`.

### Caso C: Actualizar el Perfil Profesional o Datos Personales

1. **Software:** Edita `/data/profile_software.json`.
   - Si deseas separar párrafos en el resumen profesional (`summary_hook`), utiliza doble salto de línea `\n\n`. El motor web los convertirá automáticamente en etiquetas `<p>` independientes con espaciado profesional.
2. **Creativo:** Edita `/data/profile_creative.json`.
   - Si deseas separar párrafos en la declaración de artista (`artist_statement`), utiliza doble salto de línea `\n\n`.
3. Ejecuta `python tools/build_bundle.py` y `python tools/export_pdf.py`.

---

## 🔍 Protocolo de Verificación Manual (Checklist para el Usuario)

Para verificar de forma manual e independiente que todos los cambios operan al 100%:

1. **Verificación de Párrafos en Perfil:**

   - Abre `01_Software_Dev/cv_web/cv_software.html` y confirma que la sección *Perfil Profesional* muestra párrafos claramente separados y legibles.
   - Abre `02_Creative_Arts/cv_web/cv_creative.html` y confirma que la *Declaración Artística* respeta la separación de párrafos.
2. **Verificación de Enlaces e Hipervínculos Explícitos:**

   - En ambos CVs web, haz clic en los enlaces de contacto (LinkedIn, GitHub, Portafolios) y en los enlaces de verificación de cada acreditación.
   - Abre los visores ATS (`01_Software_Dev/cv_plain_text/viewer.html` y `02_Creative_Arts/cv_plain_text/viewer.html`) y corrobora que las URLs textuales completas son legibles para selección y copia.
3. **Verificación del Modo Compacto (2 Páginas):**

   - En `01_Software_Dev/cv_web/cv_software.html`, pulsa el botón superior **"📄 Modo 2 Páginas (Compacto)"**.
   - Presiona `Ctrl + P` (Imprimir) en tu navegador y revisa la vista previa: debe indicar exactamente 2 páginas, sin desbordamientos a una tercera página en blanco.
   - Abre directamente el archivo generado `01_Software_Dev/cv_web/cv_software_compacto_2p.pdf` en tu lector de PDFs y confirma el recuento de 2 páginas.
   - Repite la verificación para `02_Creative_Arts/cv_web/cv_creative_compacto_2p.pdf`.
4. **Verificación del Inventario de Certificaciones:**

   - En el CV de Software, verifica que aparezcan listadas las certificaciones de Platzi recién agregadas (Python 2019 y Python Básico) junto a los diplomados de Dev Senior Code.
   - En el Hub `CV_Eduard_Criollo_Yule.html`, verifica que la métrica de acreditaciones señale **+18 Acreditaciones Verificadas**.
