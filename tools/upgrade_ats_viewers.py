#!/usr/bin/env python3
"""
tools/upgrade_ats_viewers.py
============================
Upgrades:
1. 01_Software_Dev/cv_plain_text/viewer.html -> adds language switch & creates viewer_en.html
2. 02_Creative_Arts/cv_plain_text/viewer.html -> adds language switch & creates viewer_en.html
3. Creates 01_Software_Dev/cv_plain_text/cv_software_en.ts
4. Creates 02_Creative_Arts/cv_plain_text/cv_creative_en.ts
"""

import json
from pathlib import Path

WORKSPACE = Path("f:/Calipso_Online/03_Profesional/Cv")

def upgrade_software_ats():
    fpath = WORKSPACE / "01_Software_Dev" / "cv_plain_text" / "viewer.html"
    with open(fpath, "r", encoding="utf-8") as f:
        html = f.read()

    # Add Language button in toolbar
    old_toolbar = """                <button class="tool-btn" onclick="toggleTheme()" title="Alternar tema visual">
                    Tema
                </button>"""
    new_toolbar = """                <button class="tool-btn" id="langBtn" onclick="toggleLanguage()" title="Switch Language / Cambiar Idioma">
                    🌐 English
                </button>
                <button class="tool-btn" onclick="toggleTheme()" title="Alternar tema visual">
                    Tema
                </button>"""
    if "langBtn" not in html:
        html = html.replace(old_toolbar, new_toolbar)

    # Replace script in viewer.html
    new_script = """
        let showLines = true;
        let currentLang = new URLSearchParams(window.location.search).get('lang') || localStorage.getItem('ats_sw_lang') || 'es';

        function toggleLanguage() {
            currentLang = currentLang === 'es' ? 'en' : 'es';
            localStorage.setItem('ats_sw_lang', currentLang);
            updateLangButton();
            loadData();
        }

        function updateLangButton() {
            const btn = document.getElementById('langBtn');
            if (btn) btn.textContent = currentLang === 'en' ? '🌐 Español' : '🌐 English';
        }

        async function loadData() {
            updateLangButton();
            let bundle = window.CV_DATA;
            let langSource = (currentLang === 'en' && bundle?.en) ? bundle.en : (bundle?.es || bundle);

            let profileData = langSource?.profile_software;
            let projectsData = langSource?.projects || [];
            let certsData = langSource?.certifications || [];

            if (profileData) {
                renderText(generateAtsString(profileData, projectsData, certsData, currentLang));
            }

            // HTTP fetch fallback / refresh
            const suffix = currentLang === 'en' ? '_en' : '';
            try {
                const [resProf, resProj, resCerts] = await Promise.allSettled([
                    fetch(`../../data/profile_software${suffix}.json`).then(r => r.ok ? r.json() : Promise.reject()),
                    fetch(`../../data/projects${suffix}.json`).then(r => r.ok ? r.json() : Promise.reject()),
                    fetch(`../../data/certifications${suffix}.json`).then(r => r.ok ? r.json() : Promise.reject())
                ]);

                if (resProf.status === 'fulfilled') {
                    profileData = resProf.value;
                    if (resProj.status === 'fulfilled') projectsData = resProj.value.projects;
                    if (resCerts.status === 'fulfilled') certsData = resCerts.value.certifications;
                    renderText(generateAtsString(profileData, projectsData, certsData, currentLang));
                }
            } catch (_) {}
        }

        function generateAtsString(data, projects = [], certs = [], lang = 'es') {
            const p = data.personal;
            const c = p.contact || {};
            const swProjects = projects.filter(pr => pr.category === 'software');
            const swCerts = certs.filter(cr => (cr.track || []).includes('software') || (cr.track || []).includes('both'));
            const isEn = lang === 'en';

            if (isEn) {
                return `==============================================================================
 ${p.name.toUpperCase()}
 ${p.headline}
==============================================================================
 Phone    : ${c.phone || '+57 314 ••• ••••'}
 Email    : ${c.email || 'eduardcriolloyule2004@gmail.com'}
 Location : ${p.location}
 LinkedIn : ${c.linkedin || ''}
 GitHub   : ${c.github || ''}
 Platzi   : ${c.platzi || ''}
 Languages: Spanish (Native) | English (C1 Advanced - Oxford Placement Test 93/120)
------------------------------------------------------------------------------

[ PROFESSIONAL PROFILE ]
------------------------------------------------------------------------------
${p.summary_hook}

[ PROFESSIONAL ACCREDITATIONS ]
------------------------------------------------------------------------------
${(data.metrics || []).map(m => `* ${m.title}: ${m.score}\\n  ${m.level} | ${m.breakdown || ''}`).join('\\n\\n')}

[ FEATURED TECHNICAL PROJECTS ]
------------------------------------------------------------------------------
${swProjects.map(pr => `* ${pr.title} (${pr.date || '2025'})\\n  Track: ${pr.sub_category || 'Software Engineering'}\\n  Tech Stack: ${(pr.tech_stack || []).join(' • ')}\\n  Metrics: ${pr.metrics || ''}\\n  Summary: ${pr.summary_executive || pr.description}\\n  Repository: ${pr.is_private ? 'Private / Confidential (Code demo available upon technical request)' : (pr.links?.github || 'Private / Confidential')}`).join('\\n\\n')}

[ PROFESSIONAL CERTIFICATIONS ]
------------------------------------------------------------------------------
${swCerts.map(cr => `* ${cr.title}\\n  Issuer: ${cr.institution} | Date: ${cr.issue_date || 'Accredited'} ${cr.code ? '| ID: ' + cr.code : ''}${cr.credential_url ? '\\n  Verification: ' + cr.credential_url : ''}`).join('\\n\\n')}

[ FORMAL EDUCATION ]
------------------------------------------------------------------------------
${(data.education || []).map(e => `* ${e.degree} (${e.period})\\n  Institution: ${e.institution}\\n  ${(e.highlights || []).join(' • ')}`).join('\\n\\n')}

[ EXPERIENCE & TECHNICAL SUPPORT ]
------------------------------------------------------------------------------
${(data.experience || []).map(exp => `* ${exp.role} — ${exp.organization || exp.company}\\n  Period: ${exp.period}\\n  Key Responsibilities:\\n${(exp.responsibilities || []).map(r => `   - ${r}`).join('\\n')}`).join('\\n\\n')}

[ TECHNICAL COMPETENCIES / SKILLS MATRIX ]
------------------------------------------------------------------------------
${Object.values(data.skills_matrix || {}).map(g => `* ${g.category}:\\n  ${g.skills.join(' • ')}`).join('\\n\\n')}

[ SOFT SKILLS ]
------------------------------------------------------------------------------
${(data.soft_skills || []).join(' • ')}

[ LANGUAGES ]
------------------------------------------------------------------------------
${(data.languages || []).map(l => `* ${l.language}: ${l.level} ${l.certification ? `(${l.certification})` : ''}`).join('\\n')}

==============================================================================
 End of Document — Optimized ATS Plain Text Resume (English Edition)
==============================================================================`;
            }

            return `==============================================================================
 ${p.name.toUpperCase()}
 ${p.headline}
==============================================================================
 Teléfono : ${c.phone || '+57 314 ••• ••••'}
 Correo   : ${c.email || 'eduardcriolloyule2004@gmail.com'}
 Ubicación: ${p.location}
 LinkedIn : ${c.linkedin || ''}
 GitHub   : ${c.github || ''}
 Platzi   : ${c.platzi || ''}
 Idiomas  : Español (Nativo) | Inglés (C1 Avanzado - Oxford Placement Test 93/120)
------------------------------------------------------------------------------

[ PERFIL PROFESIONAL ]
------------------------------------------------------------------------------
${p.summary_hook}

[ ACREDITACIONES PROFESIONALES ]
------------------------------------------------------------------------------
${(data.metrics || []).map(m => `* ${m.title}: ${m.score}\\n  ${m.level} | ${m.breakdown || ''}`).join('\\n\\n')}

[ PROYECTOS TÉCNICOS DESTACADOS ]
------------------------------------------------------------------------------
${swProjects.map(pr => `* ${pr.title} (${pr.date || '2025'})\\n  Subcategoría: ${pr.sub_category || 'Ingeniería de Software'}\\n  Stack: ${(pr.tech_stack || []).join(' • ')}\\n  Métricas: ${pr.metrics || ''}\\n  Descripción: ${pr.summary_executive || pr.description}\\n  Repositorio: ${pr.is_private ? 'Privado / Confidencial (Código disponible bajo solicitud técnica)' : (pr.links?.github || 'Privado / Confidencial')}`).join('\\n\\n')}

[ CERTIFICACIONES PROFESIONALES ]
------------------------------------------------------------------------------
${swCerts.map(cr => `* ${cr.title}\\n  Emisor: ${cr.institution} | Fecha: ${cr.issue_date || 'Acreditado'} ${cr.code ? '| ID: ' + cr.code : ''}${cr.credential_url ? '\\n  Verificación: ' + cr.credential_url : ''}`).join('\\n\\n')}

[ EDUCACIÓN ]
------------------------------------------------------------------------------
${(data.education || []).map(e => `* ${e.degree} (${e.period})\\n  Institución: ${e.institution}\\n  ${(e.highlights || []).join(' • ')}`).join('\\n\\n')}

[ EXPERIENCIA & COORDINACIÓN TÉCNICA ]
------------------------------------------------------------------------------
${(data.experience || []).map(exp => `* ${exp.role} — ${exp.organization || exp.company}\\n  Periodo: ${exp.period}\\n  Responsabilidades:\\n${(exp.responsibilities || []).map(r => `   - ${r}`).join('\\n')}`).join('\\n\\n')}

[ COMPETENCIAS TÉCNICAS ]
------------------------------------------------------------------------------
${Object.values(data.skills_matrix || {}).map(g => `* ${g.category}:\\n  ${g.skills.join(' • ')}`).join('\\n\\n')}

[ HABILIDADES BLANDAS ]
------------------------------------------------------------------------------
${(data.soft_skills || []).join(' • ')}

[ IDIOMAS ]
------------------------------------------------------------------------------
${(data.languages || []).map(l => `* ${l.language}: ${l.level} ${l.certification ? `(${l.certification})` : ''}`).join('\\n')}

==============================================================================
 Fin del documento — Generado Dinámicamente desde /data/
==============================================================================`;
        }

        function renderText(text) {
            const pre = document.getElementById('plainTextContent');
            if (pre) pre.textContent = text;

            const lines = text.split('\\n');
            const numContainer = document.getElementById('lineNumbers');
            if (numContainer) numContainer.innerHTML = lines.map((_, i) => i + 1).join('<br>');
        }

        function copyToClipboard() {
            const text = document.getElementById('plainTextContent').textContent;
            navigator.clipboard.writeText(text).then(() => {
                const toast = document.getElementById('toast');
                toast.classList.add('show');
                setTimeout(() => toast.classList.remove('show'), 2500);
            });
        }

        function toggleLineNumbers() {
            showLines = !showLines;
            document.getElementById('lineNumbers').classList.toggle('hidden', !showLines);
        }

        function toggleTheme() {
            document.body.classList.toggle('theme-light');
        }

        document.addEventListener('DOMContentLoaded', loadData);
"""

    import re
    # Replace from let showLines = true; to end of script
    script_regex = re.compile(r'let showLines = true;.*?document\.addEventListener\(\'DOMContentLoaded\', loadData\);', re.DOTALL)
    html = script_regex.sub(new_script.strip(), html)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated 01_Software_Dev/cv_plain_text/viewer.html")

    # Generate viewer_en.html
    html_en = html.replace('lang="es"', 'lang="en"')
    html_en = html_en.replace("let currentLang = new URLSearchParams(window.location.search).get('lang') || localStorage.getItem('ats_sw_lang') || 'es';",
                              "let currentLang = 'en';")
    html_en = html_en.replace("<title>ATS Plain Text Viewer — Eduard Criollo Yule (Software)</title>",
                              "<title>ATS Plain Text Viewer — Eduard Criollo Yule (Software) [EN]</title>")
    with open(WORKSPACE / "01_Software_Dev" / "cv_plain_text" / "viewer_en.html", "w", encoding="utf-8") as f:
        f.write(html_en)
    print("Generated 01_Software_Dev/cv_plain_text/viewer_en.html")

def upgrade_creative_ats():
    fpath = WORKSPACE / "02_Creative_Arts" / "cv_plain_text" / "viewer.html"
    with open(fpath, "r", encoding="utf-8") as f:
        html = f.read()

    # Add Language button in toolbar
    old_toolbar = """                <button class="tool-btn" onclick="toggleTheme()" title="Alternar tema">
                    Tema
                </button>"""
    new_toolbar = """                <button class="tool-btn" id="langArtAtsBtn" onclick="toggleArtLanguage()" title="Switch Language / Cambiar Idioma">
                    🌐 English
                </button>
                <button class="tool-btn" onclick="toggleTheme()" title="Alternar tema">
                    Tema
                </button>"""
    if "langArtAtsBtn" not in html:
        html = html.replace(old_toolbar, new_toolbar)

    new_script = """
        let currentLang = new URLSearchParams(window.location.search).get('lang') || localStorage.getItem('ats_art_lang') || 'es';

        function toggleArtLanguage() {
            currentLang = currentLang === 'es' ? 'en' : 'es';
            localStorage.setItem('ats_art_lang', currentLang);
            updateArtLangBtn();
            initViewer();
        }

        function updateArtLangBtn() {
            const btn = document.getElementById('langArtAtsBtn');
            if (btn) btn.textContent = currentLang === 'en' ? '🌐 Español' : '🌐 English';
        }

        function initViewer() {
            updateArtLangBtn();
            let bundle = window.CV_DATA;
            let langSource = (currentLang === 'en' && bundle?.en) ? bundle.en : (bundle?.es || bundle);

            let artData = langSource?.profile_creative;
            let projData = langSource?.projects || [];
            let certsData = langSource?.certifications || [];

            if (artData) {
                renderText(generateCreativeAtsString(artData, projData, certsData, currentLang));
            }

            const suffix = currentLang === 'en' ? '_en' : '';
            try {
                Promise.allSettled([
                    fetch(`../../data/profile_creative${suffix}.json`).then(r => r.ok ? r.json() : Promise.reject()),
                    fetch(`../../data/projects${suffix}.json`).then(r => r.ok ? r.json() : Promise.reject()),
                    fetch(`../../data/certifications${suffix}.json`).then(r => r.ok ? r.json() : Promise.reject())
                ]).then(([resArt, resProj, resCerts]) => {
                    if (resArt.status === 'fulfilled') {
                        artData = resArt.value;
                        if (resProj.status === 'fulfilled') projData = resProj.value.projects;
                        if (resCerts.status === 'fulfilled') certsData = resCerts.value.certifications;
                        renderText(generateCreativeAtsString(artData, projData, certsData, currentLang));
                    }
                });
            } catch (_) {}
        }

        function generateCreativeAtsString(data, projects = [], certs = [], lang = 'es') {
            const p = data.personal;
            const c = p.contact || {};
            const artProjects = projects.filter(pr => pr.category === 'creative');
            const artCerts = certs.filter(cr => (cr.track || []).includes('creative') || (cr.track || []).includes('both'));
            const isEn = lang === 'en';

            if (isEn) {
                return `==============================================================================
 ${p.name.toUpperCase()}
 ${p.headline}
==============================================================================
 Phone     : ${c.phone || '+57 314 ••• ••••'}
 Email     : ${c.email || 'eduardcriolloyule2004@gmail.com'}
 Location  : ${p.location}
 ArtStation: ${c.artstation || ''}
 Behance   : ${c.behance || ''}
 LinkedIn  : ${c.linkedin || ''}
 Languages : Spanish (Native) | English (C1 Advanced - Oxford Placement Test 93/120)
------------------------------------------------------------------------------

[ ARTISTIC STATEMENT & VISION ]
------------------------------------------------------------------------------
${p.summary_hook}

[ AWARDS & DISTINCTIONS ]
------------------------------------------------------------------------------
${(data.awards_recognitions || []).map(a => `* ${a.title} (${a.year || ''})\\n  ${a.organization ? 'Organization: ' + a.organization + '\\n  ' : ''}${a.description}`).join('\\n\\n')}

[ ACCREDITATIONS & CERTIFICATIONS ]
------------------------------------------------------------------------------
${artCerts.map(cr => `* ${cr.title}\\n  Issuer: ${cr.institution} | Date: ${cr.issue_date || 'Accredited'} ${cr.code ? '| ID: ' + cr.code : ''}${cr.credential_url ? '\\n  Verification: ' + cr.credential_url : ''}`).join('\\n\\n')}

[ SELECTED WORKS & CREATIVE PROJECTS ]
------------------------------------------------------------------------------
${artProjects.map(pr => `* ${pr.title} (${pr.date || '2025'})\\n  Discipline: ${pr.sub_category || 'Digital Art'}\\n  Tools: ${(pr.tech_stack || []).join(' • ')}\\n  Metrics: ${pr.metrics || ''}\\n  Summary: ${pr.summary_executive || pr.description}\\n  Link: ${pr.links?.artstation || pr.links?.behance || pr.links?.github || ''}`).join('\\n\\n')}

[ ARTISTIC DISCIPLINES & AREAS OF SPECIALIZATION ]
------------------------------------------------------------------------------
${(data.artistic_disciplines || []).map(d => `* ${d.name}:\\n  ${d.description}\\n  Tools: ${(d.tools || []).join(' • ')}`).join('\\n\\n')}

[ ACADEMIC & TECHNICAL FORMATION ]
------------------------------------------------------------------------------
${(data.education || []).map(e => `* ${e.degree} (${e.period})\\n  Institution: ${e.institution}\\n  ${(e.highlights || []).join(' • ')}`).join('\\n\\n')}

[ AUDIOVISUAL PRODUCTION & EVENT EXPERIENCE ]
------------------------------------------------------------------------------
${(data.experience || []).map(exp => `* ${exp.role} — ${exp.organization}\\n  Period: ${exp.period}\\n  Responsibilities:\\n${(exp.responsibilities || []).map(r => `   - ${r}`).join('\\n')}`).join('\\n\\n')}

==============================================================================
 End of Document — Creative Profile in Optimized ATS Plain Text (English)
==============================================================================`;
            }

            return `==============================================================================
 ${p.name.toUpperCase()}
 ${p.headline}
==============================================================================
 Teléfono : ${c.phone || '+57 314 ••• ••••'}
 Correo   : ${c.email || 'eduardcriolloyule2004@gmail.com'}
 Ubicación: ${p.location}
 ArtStation: ${c.artstation || ''}
 Behance  : ${c.behance || ''}
 LinkedIn : ${c.linkedin || ''}
 Idiomas  : Español (Nativo) | Inglés (C1 Avanzado - Oxford Placement Test 93/120)
------------------------------------------------------------------------------

[ PERFIL & DECLARACIÓN ARTÍSTICA ]
------------------------------------------------------------------------------
${p.summary_hook}

[ DISTINCIONES & PREMIOS ]
------------------------------------------------------------------------------
${(data.awards_recognitions || []).map(a => `* ${a.title} (${a.year || ''})\\n  ${a.organization ? 'Organización: ' + a.organization + '\\n  ' : ''}${a.description}`).join('\\n\\n')}

[ ACREDITACIONES & CERTIFICACIONES ]
------------------------------------------------------------------------------
${artCerts.map(cr => `* ${cr.title}\\n  Emisor: ${cr.institution} | Fecha: ${cr.issue_date || 'Acreditado'} ${cr.code ? '| ID: ' + cr.code : ''}${cr.credential_url ? '\\n  Verificación: ' + cr.credential_url : ''}`).join('\\n\\n')}

[ OBRAS & PROYECTOS SELECCIONADOS ]
------------------------------------------------------------------------------
${artProjects.map(pr => `* ${pr.title} (${pr.date || '2025'})\\n  Disciplina: ${pr.sub_category || 'Artes Digitales'}\\n  Herramientas: ${(pr.tech_stack || []).join(' • ')}\\n  Métricas: ${pr.metrics || ''}\\n  Descripción: ${pr.summary_executive || pr.description}\\n  Enlace: ${pr.links?.artstation || pr.links?.behance || pr.links?.github || ''}`).join('\\n\\n')}

[ DISCIPLINAS ARTÍSTICAS & COMPETENCIAS ]
------------------------------------------------------------------------------
${(data.artistic_disciplines || []).map(d => `* ${d.name}:\\n  ${d.description}\\n  Herramientas: ${(d.tools || []).join(' • ')}`).join('\\n\\n')}

[ FORMACIÓN ACADÉMICA & TÉCNICA ]
------------------------------------------------------------------------------
${(data.education || []).map(e => `* ${e.degree} (${e.period})\\n  Institución: ${e.institution}\\n  ${(e.highlights || []).join(' • ')}`).join('\\n\\n')}

[ EXPERIENCIA EN PRODUCCIÓN AUDIOVISUAL ]
------------------------------------------------------------------------------
${(data.experience || []).map(exp => `* ${exp.role} — ${exp.organization}\\n  Periodo: ${exp.period}\\n  Responsabilidades:\\n${(exp.responsibilities || []).map(r => `   - ${r}`).join('\\n')}`).join('\\n\\n')}

==============================================================================
 Fin del documento — Perfil Creativo en Formato Texto Plano ATS
==============================================================================`;
        }

        function renderText(text) {
            const pre = document.getElementById('plainContent');
            if (pre) pre.textContent = text;
            const lines = text.split('\\n');
            const lineNums = document.getElementById('lineNums');
            if (lineNums) lineNums.innerHTML = lines.map((_, i) => i + 1).join('<br>');
        }

        function copyText() {
            navigator.clipboard.writeText(document.getElementById('plainContent').textContent).then(() => {
                const t = document.getElementById('toast');
                t.classList.add('show');
                setTimeout(() => t.classList.remove('show'), 2000);
            });
        }

        function toggleLines() {
            document.getElementById('lineNums').classList.toggle('hidden');
        }

        function toggleTheme() {
            document.body.classList.toggle('theme-light');
        }

        document.addEventListener('DOMContentLoaded', initViewer);
"""

    import re
    script_regex = re.compile(r'function initViewer\(\) \{.*?document\.addEventListener\(\'DOMContentLoaded\', initViewer\);', re.DOTALL)
    html = script_regex.sub(new_script.strip(), html)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated 02_Creative_Arts/cv_plain_text/viewer.html")

    html_en = html.replace('lang="es"', 'lang="en"')
    html_en = html_en.replace("let currentLang = new URLSearchParams(window.location.search).get('lang') || localStorage.getItem('ats_art_lang') || 'es';",
                              "let currentLang = 'en';")
    html_en = html_en.replace("<title>ATS Plain Text Viewer — Eduard Criollo Yule (Creative Arts)</title>",
                              "<title>ATS Plain Text Viewer — Eduard Criollo Yule (Creative Arts) [EN]</title>")
    with open(WORKSPACE / "02_Creative_Arts" / "cv_plain_text" / "viewer_en.html", "w", encoding="utf-8") as f:
        f.write(html_en)
    print("Generated 02_Creative_Arts/cv_plain_text/viewer_en.html")

def create_english_ts():
    # 1. 01_Software_Dev/cv_plain_text/cv_software_en.ts
    with open(WORKSPACE / "data" / "profile_software_en.json", "r", encoding="utf-8") as f:
        prof_en = json.load(f)

    ts_sw = f"""/**
 * @fileoverview Typed definition of Eduard Criollo Yule's Professional Resume
 * for Software Development, Artificial Intelligence, and Data Science (English Edition).
 * 
 * @module SoftwareResumeEN
 * @author Eduard Criollo Yule
 * @version 2.1.0
 * @see {{'../../data/profile_software_en.json'}} SSOT Data Source
 */

export interface ContactInfo {{
  phone: string;
  email: string;
  location: string;
  platzi: string;
  github: string;
  linkedin: string;
}}

export interface AcademicMetric {{
  id: string;
  badge: string;
  title: string;
  score: string;
  level: string;
  breakdown: string;
  institution: string;
  date: string;
}}

export interface EducationEntry {{
  degree: string;
  institution: string;
  period: string;
  status: string;
  location: string;
  highlights: string[];
}}

export interface ExperienceEntry {{
  role: string;
  organization: string;
  period: string;
  location: string;
  responsibilities: string[];
  technologies: string[];
}}

export interface SkillCategory {{
  category: string;
  skills: string[];
}}

export interface LanguageProficiency {{
  language: string;
  level: string;
  certification?: string;
  notes: string;
}}

export interface SoftwareProfile {{
  personal: {{
    name: string;
    headline: string;
    subtitle: string;
    location: string;
    contact: ContactInfo;
    summary_hook: string;
  }};
  metrics: AcademicMetric[];
  education: EducationEntry[];
  experience: ExperienceEntry[];
  skills_matrix: Record<string, SkillCategory>;
  soft_skills: string[];
  languages: LanguageProficiency[];
}}

export const SOFTWARE_PROFILE_DATA_EN: SoftwareProfile = {json.dumps(prof_en, indent=2, ensure_ascii=False)};
"""
    with open(WORKSPACE / "01_Software_Dev" / "cv_plain_text" / "cv_software_en.ts", "w", encoding="utf-8") as f:
        f.write(ts_sw)
    print("Created 01_Software_Dev/cv_plain_text/cv_software_en.ts")

    # 2. 02_Creative_Arts/cv_plain_text/cv_creative_en.ts
    with open(WORKSPACE / "data" / "profile_creative_en.json", "r", encoding="utf-8") as f:
        art_en = json.load(f)

    ts_cr = f"""/**
 * @fileoverview Typed definition of Eduard Criollo Yule's Creative Resume
 * for Illustration, 2D/3D Animation, and Creative Writing (English Edition).
 * 
 * @module CreativeResumeEN
 * @author Eduard Criollo Yule
 * @version 2.1.0
 * @see {{'../../data/profile_creative_en.json'}} SSOT Data Source
 */

export interface CreativeContactInfo {{
  phone: string;
  email: string;
  location: string;
  artstation: string;
  behance: string;
  linkedin: string;
  github: string;
}}

export interface ArtisticDiscipline {{
  name: string;
  description: string;
  tools: string[];
}}

export interface AwardRecognition {{
  title: string;
  description: string;
  year?: string;
  organization?: string;
}}

export interface CreativeEducationEntry {{
  degree: string;
  institution: string;
  period: string;
  highlights: string[];
}}

export interface CreativeExperienceEntry {{
  role: string;
  organization: string;
  period: string;
  responsibilities: string[];
}}

export interface CreativeProfile {{
  personal: {{
    name: string;
    headline: string;
    location: string;
    contact: CreativeContactInfo;
    summary_hook: string;
  }};
  artistic_disciplines: ArtisticDiscipline[];
  awards_recognitions: AwardRecognition[];
  education: CreativeEducationEntry[];
  experience: CreativeExperienceEntry[];
  creative_skills_matrix?: Record<string, any>;
  languages: any[];
}}

export const CREATIVE_PROFILE_DATA_EN: CreativeProfile = {json.dumps(art_en, indent=2, ensure_ascii=False)};
"""
    with open(WORKSPACE / "02_Creative_Arts" / "cv_plain_text" / "cv_creative_en.ts", "w", encoding="utf-8") as f:
        f.write(ts_cr)
    print("Created 02_Creative_Arts/cv_plain_text/cv_creative_en.ts")

if __name__ == "__main__":
    upgrade_software_ats()
    upgrade_creative_ats()
    create_english_ts()
