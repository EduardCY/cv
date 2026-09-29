#!/usr/bin/env python3
"""
tools/upgrade_all_cv_web.py
===========================
Upgrades:
1. 01_Software_Dev/cv_web/cv_software.html + generates cv_software_en.html
2. 02_Creative_Arts/cv_web/cv_creative.html + generates cv_creative_en.html

Includes:
- Full English & Spanish bilingual toggling (UI strings, data sources from window.CV_DATA.es / en)
- Certificate inspection modal with PDF viewer and external verification
- Clean event handlers and metadata inspection
"""

import sys
import re
from pathlib import Path

WORKSPACE = Path("f:/Calipso_Online/03_Profesional/Cv")

def upgrade_software():
    sw_file = WORKSPACE / "01_Software_Dev" / "cv_web" / "cv_software.html"
    with open(sw_file, "r", encoding="utf-8") as f:
        html = f.read()

    # CSS for certification modal
    modal_css = """
        /* ==========================================================================
           MODAL INSPECTOR DE CERTIFICACIONES & PDF PREVIEW
           ========================================================================== */
        .cert-modal-backdrop {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(5, 8, 16, 0.85);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            z-index: 1000;
            padding: 2rem 1rem;
            overflow-y: auto;
            align-items: center;
            justify-content: center;
        }
        .cert-modal-backdrop.active {
            display: flex;
        }
        .cert-modal-dialog {
            background: var(--surface-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            max-width: 860px;
            width: 100%;
            max-height: 88vh;
            display: flex;
            flex-direction: column;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
            position: relative;
            animation: modalFadeIn 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            overflow: hidden;
        }
        @keyframes modalFadeIn {
            from { opacity: 0; transform: scale(0.96) translateY(10px); }
            to { opacity: 1; transform: scale(1) translateY(0); }
        }
        .cert-modal-header {
            padding: 1.25rem 1.75rem;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--surface-glass);
        }
        .cert-modal-title {
            font-family: var(--font-heading);
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .cert-modal-close {
            background: rgba(125, 125, 125, 0.1);
            border: 1px solid var(--border);
            color: var(--text-muted);
            font-size: 1.2rem;
            width: 32px;
            height: 32px;
            border-radius: 6px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
        }
        .cert-modal-close:hover {
            color: #ef4444;
            background: rgba(239, 68, 68, 0.1);
            border-color: rgba(239, 68, 68, 0.3);
        }
        .cert-modal-content {
            padding: 1.5rem 1.75rem;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }
        .cert-preview-frame {
            width: 100%;
            height: 480px;
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            background: #0b0f17;
        }
        .cert-modal-meta-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            background: rgba(59, 130, 246, 0.05);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 1rem;
        }
        .cert-meta-item strong {
            display: block;
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--accent);
            margin-bottom: 0.2rem;
        }
        .cert-meta-item span {
            font-size: 0.85rem;
            color: var(--text-main);
            font-weight: 600;
        }
        .cert-modal-actions {
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
            margin-top: 0.5rem;
        }
        .cert-action-btn {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.6rem 1.1rem;
            border-radius: var(--radius-full);
            font-size: 0.82rem;
            font-weight: 600;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .cert-action-btn.primary {
            background: var(--accent);
            color: white;
            border: none;
        }
        .cert-action-btn.secondary {
            background: transparent;
            color: var(--secondary);
            border: 1px solid var(--secondary);
        }
        .cert-action-btn:hover {
            transform: translateY(-1px);
            box-shadow: var(--shadow-md);
        }
        .cert-card {
            cursor: pointer;
            transition: all 0.25s ease;
        }
        .cert-card:hover {
            transform: translateY(-3px);
            border-color: var(--accent);
            box-shadow: 0 8px 20px rgba(59, 130, 246, 0.15);
        }
    """

    if "cert-modal-backdrop" not in html:
        html = html.replace("    </style>", modal_css + "\n    </style>")

    # Replace Action Bar with Language Switcher and updated buttons
    action_bar_pattern = re.compile(r'<div class="action-bar" id="actionBar">.*?</div>', re.DOTALL)
    new_action_bar = """<div class="action-bar" id="actionBar">
        <button class="action-btn primary" id="btnExportPdf" onclick="window.print()" title="Imprimir o Guardar como PDF">
            Exportar PDF
        </button>
        <button class="action-btn" id="compactToggleBtn" onclick="toggleCompactMode()" title="Alternar Vista Compacta de 2 Páginas">
            Modo Compacto (2P)
        </button>
        <button class="action-btn" id="themeToggleBtn" onclick="toggleDarkMode()" title="Alternar Modo Oscuro/Claro">
            Alternar Tema
        </button>
        <button class="action-btn" id="langToggleBtn" onclick="toggleLanguage()" title="Cambiar Idioma / Switch Language">
            🌐 English
        </button>
        <a href="../../CV_Eduard_Criollo_Yule.html" class="action-btn" id="btnNavHub" title="Ir al Portal Hub Principal">
            🏛️ Hub Principal
        </a>
        <a href="../../02_Creative_Arts/cv_web/cv_creative.html" class="action-btn" id="btnNavCreative" title="Ver CV Creativo">
            🎨 CV Artístico
        </a>
        <a href="../portfolio/option_gothic/index.html" class="action-btn" id="btnNavGothic" title="Ver Portafolio Gótico">
            Portafolio Gótico
        </a>
        <a href="../portfolio/option_tron/index.html" class="action-btn" id="btnNavWin97" title="Ver Portafolio Windows 97">
            Portafolio Win97
        </a>
        <a href="../cv_plain_text/viewer.html" class="action-btn" id="btnNavAts" title="Ver Versión ATS en Texto Plano">
            Visor ATS
        </a>
    </div>"""
    html = action_bar_pattern.sub(new_action_bar, html)

    # Section Headers with ID hooks for language switching
    html = html.replace('<h3 class="sidebar-section-title">Redes & Contacto</h3>', '<h3 class="sidebar-section-title" id="secTitleContact">Redes & Contacto</h3>')
    html = html.replace('<h3 class="sidebar-section-title">Acreditaciones</h3>', '<h3 class="sidebar-section-title" id="secTitleMetrics">Acreditaciones</h3>')
    html = html.replace('<h3 class="sidebar-section-title">Competencias</h3>', '<h3 class="sidebar-section-title" id="secTitleSkills">Competencias</h3>')
    html = html.replace('<h3 class="sidebar-section-title">Idiomas</h3>', '<h3 class="sidebar-section-title" id="secTitleLanguages">Idiomas</h3>')
    html = html.replace('<h2 class="section-title">Perfil Profesional</h2>', '<h2 class="section-title" id="secTitleProfile">Perfil Profesional</h2>')
    html = html.replace('<h2 class="section-title">Formación Académica</h2>', '<h2 class="section-title" id="secTitleEducation">Formación Académica</h2>')
    html = html.replace('<h2 class="section-title">Experiencia & Soporte Técnico</h2>', '<h2 class="section-title" id="secTitleExperience">Experiencia & Soporte Técnico</h2>')
    html = html.replace('<h2 class="section-title">Proyectos Seleccionados</h2>', '<h2 class="section-title" id="secTitleProjects">Proyectos Seleccionados</h2>')
    html = html.replace('<h2 class="section-title">Certificaciones Profesionales</h2>', '<h2 class="section-title" id="secTitleCertifications">Certificaciones Profesionales</h2>')

    # Modal HTML
    modal_html = """
    <!-- MODAL DE INSPECCIÓN DETALLADA DE CERTIFICACIONES -->
    <div class="cert-modal-backdrop" id="certModalBackdrop" onclick="if(event.target === this) closeCertModal()">
        <div class="cert-modal-dialog" role="dialog" aria-modal="true" aria-labelledby="certModalHeading">
            <div class="cert-modal-header">
                <h3 class="cert-modal-title" id="certModalHeading">
                    <span>🎓</span> <span id="modalCertTitle">Detalles del Certificado</span>
                </h3>
                <button class="cert-modal-close" onclick="closeCertModal()" aria-label="Cerrar modal">✕</button>
            </div>
            <div class="cert-modal-content" id="certModalContent">
                <!-- Inyectado dinámicamente -->
            </div>
        </div>
    </div>
"""
    if "certModalBackdrop" not in html:
        html = html.replace("    <!-- SCRIPT DE DATOS GLOBALES", modal_html + "\n    <!-- SCRIPT DE DATOS GLOBALES")

    # Full bilingual and inspection JavaScript
    new_script = """
    <!-- SCRIPT DE CARGA REACTIVA Y BILINGÜE -->
    <script>
        /**
         * @fileoverview DataLoader reactivo y desacoplado para CV Software.
         * Consume /data/bundle.js (local file:///) o /data/*.json (HTTP/HTTPS).
         * Soporta conmutación bilingüe instantánea (Español / Inglés) e inspección de certificados.
         * 
         * @author Eduard Criollo Yule
         */

        let currentLang = new URLSearchParams(window.location.search).get('lang') || localStorage.getItem('cv_lang') || 'es';
        let currentCerts = [];

        const UI_TEXT = {
            es: {
                pageTitle: "CV Profesional — Eduard Criollo Yule | Full Stack & AI",
                btnExportPdf: "Exportar PDF",
                btnCompact: "Modo Compacto (2P)",
                btnCompactNormal: "Modo Normal",
                btnThemeDark: "Modo Oscuro",
                btnThemeLight: "Modo Claro",
                btnLang: "🌐 English",
                btnNavHub: "🏛️ Hub Principal",
                btnNavCreative: "🎨 CV Artístico",
                btnNavGothic: "Portafolio Gótico",
                btnNavWin97: "Portafolio Win97",
                btnNavAts: "Visor ATS",
                secContact: "Redes & Contacto",
                secMetrics: "Acreditaciones",
                secSkills: "Competencias",
                secLanguages: "Idiomas",
                secProfile: "Perfil Profesional",
                secEducation: "Formación Académica",
                secExperience: "Experiencia & Soporte Técnico",
                secProjects: "Proyectos Seleccionados",
                secCertifications: "Certificaciones Profesionales",
                certInspectBtn: "🔍 Inspeccionar",
                certPdfBtn: "📄 PDF Certificado",
                certVerifyBtn: "🔗 Verificar Online",
                certAccredited: "Acreditado",
                certVerified: "Verificado",
                repoPrivateTitle: "🔒 Repositorio Privado / Confidencial:",
                repoPrivateDesc: "Demostración y código disponibles bajo solicitud técnica",
                repoGithub: "💻 Repositorio GitHub:",
                repoDemo: "🚀 Demo Online",
                modalIssuer: "Institución Emisora",
                modalDate: "Fecha de Emisión",
                modalCode: "Código / Credencial ID",
                modalScore: "Calificación / Puntaje",
                modalSkills: "Competencias Acreditadas",
                modalPreview: "Vista Previa del Documento Oficial",
                modalNoPdf: "El visor integrado no está disponible. Puede abrir el PDF directamente mediante el botón inferior.",
                modalOpenPdf: "📄 Abrir Documento PDF Oficial",
                modalVerifyOnline: "🔗 Verificar en Plataforma Emisora"
            },
            en: {
                pageTitle: "Professional CV — Eduard Criollo Yule | Full Stack & AI",
                btnExportPdf: "Export PDF",
                btnCompact: "Compact View (2P)",
                btnCompactNormal: "Normal View",
                btnThemeDark: "Dark Mode",
                btnThemeLight: "Light Mode",
                btnLang: "🌐 Español",
                btnNavHub: "🏛️ Main Hub",
                btnNavCreative: "🎨 Creative CV",
                btnNavGothic: "Gothic Portfolio",
                btnNavWin97: "Win97 Portfolio",
                btnNavAts: "ATS Viewer",
                secContact: "Contact & Networks",
                secMetrics: "Accreditations",
                secSkills: "Skills Matrix",
                secLanguages: "Languages",
                secProfile: "Professional Profile",
                secEducation: "Education",
                secExperience: "Experience & Technical Support",
                secProjects: "Selected Projects",
                secCertifications: "Professional Certifications",
                certInspectBtn: "🔍 Inspect",
                certPdfBtn: "📄 PDF Certificate",
                certVerifyBtn: "🔗 Verify Online",
                certAccredited: "Accredited",
                certVerified: "Verified",
                repoPrivateTitle: "🔒 Private / Confidential Repository:",
                repoPrivateDesc: "Architecture demo and source code available upon technical request",
                repoGithub: "💻 GitHub Repository:",
                repoDemo: "🚀 Live Demo",
                modalIssuer: "Issuing Organization",
                modalDate: "Issue Date",
                modalCode: "Credential ID / Code",
                modalScore: "Score / Grade",
                modalSkills: "Validated Competencies",
                modalPreview: "Official Document Preview",
                modalNoPdf: "Embedded viewer not supported. You can open the PDF directly using the button below.",
                modalOpenPdf: "📄 Open Official PDF Document",
                modalVerifyOnline: "🔗 Verify on Issuer Platform"
            }
        };

        function toggleDarkMode() {
            document.body.classList.toggle('dark-mode');
            const isDark = document.body.classList.contains('dark-mode');
            localStorage.setItem('cv_theme', isDark ? 'dark' : 'light');
            updateUIThemeButton();
        }

        function updateUIThemeButton() {
            const btn = document.getElementById('themeToggleBtn');
            const isDark = document.body.classList.contains('dark-mode');
            const t = UI_TEXT[currentLang] || UI_TEXT.es;
            if (btn) btn.textContent = isDark ? t.btnThemeLight : t.btnThemeDark;
        }

        function toggleCompactMode() {
            document.body.classList.toggle('compact-2p');
            const isCompact = document.body.classList.contains('compact-2p');
            const btn = document.getElementById('compactToggleBtn');
            const t = UI_TEXT[currentLang] || UI_TEXT.es;
            if (btn) btn.textContent = isCompact ? t.btnCompactNormal : t.btnCompact;
        }

        function toggleLanguage() {
            setLanguage(currentLang === 'es' ? 'en' : 'es');
        }

        function setLanguage(lang) {
            currentLang = lang;
            localStorage.setItem('cv_lang', lang);
            applyLanguage();
        }

        function updateUITexts() {
            const t = UI_TEXT[currentLang] || UI_TEXT.es;
            document.title = t.pageTitle;
            const btnExport = document.getElementById('btnExportPdf');
            if (btnExport) btnExport.textContent = t.btnExportPdf;

            const btnCompact = document.getElementById('compactToggleBtn');
            if (btnCompact) {
                const isCompact = document.body.classList.contains('compact-2p');
                btnCompact.textContent = isCompact ? t.btnCompactNormal : t.btnCompact;
            }

            updateUIThemeButton();

            const btnLang = document.getElementById('langToggleBtn');
            if (btnLang) btnLang.textContent = t.btnLang;

            const btnHub = document.getElementById('btnNavHub');
            if (btnHub) {
                btnHub.textContent = t.btnNavHub;
                btnHub.href = currentLang === 'en' ? "../../CV_Eduard_Criollo_Yule_en.html" : "../../CV_Eduard_Criollo_Yule.html";
            }

            const btnCreative = document.getElementById('btnNavCreative');
            if (btnCreative) {
                btnCreative.textContent = t.btnNavCreative;
                btnCreative.href = currentLang === 'en' ? "../../02_Creative_Arts/cv_web/cv_creative_en.html" : "../../02_Creative_Arts/cv_web/cv_creative.html";
            }

            const btnGothic = document.getElementById('btnNavGothic');
            if (btnGothic) btnGothic.textContent = t.btnNavGothic;
            const btnWin97 = document.getElementById('btnNavWin97');
            if (btnWin97) btnWin97.textContent = t.btnNavWin97;
            const btnAts = document.getElementById('btnNavAts');
            if (btnAts) {
                btnAts.textContent = t.btnNavAts;
                btnAts.href = currentLang === 'en' ? "../cv_plain_text/viewer_en.html" : "../cv_plain_text/viewer.html";
            }

            const elSecContact = document.getElementById('secTitleContact');
            if (elSecContact) elSecContact.textContent = t.secContact;
            const elSecMetrics = document.getElementById('secTitleMetrics');
            if (elSecMetrics) elSecMetrics.textContent = t.secMetrics;
            const elSecSkills = document.getElementById('secTitleSkills');
            if (elSecSkills) elSecSkills.textContent = t.secSkills;
            const elSecLanguages = document.getElementById('secTitleLanguages');
            if (elSecLanguages) elSecLanguages.textContent = t.secLanguages;
            const elSecProfile = document.getElementById('secTitleProfile');
            if (elSecProfile) elSecProfile.textContent = t.secProfile;
            const elSecEducation = document.getElementById('secTitleEducation');
            if (elSecEducation) elSecEducation.textContent = t.secEducation;
            const elSecExperience = document.getElementById('secTitleExperience');
            if (elSecExperience) elSecExperience.textContent = t.secExperience;
            const elSecProjects = document.getElementById('secTitleProjects');
            if (elSecProjects) elSecProjects.textContent = t.secProjects;
            const elSecCertifications = document.getElementById('secTitleCertifications');
            if (elSecCertifications) elSecCertifications.textContent = t.secCertifications;
        }

        async function applyLanguage() {
            updateUITexts();

            let dataLayer = window.CV_DATA;
            let profileData = null;
            let certsData = [];
            let projectsData = [];

            if (dataLayer) {
                const bundleLang = (currentLang === 'en' && dataLayer.en) ? dataLayer.en : (dataLayer.es || dataLayer);
                profileData = bundleLang.profile_software || dataLayer.profile_software;
                certsData = (bundleLang.certifications || dataLayer.certifications || []).filter(c => (c.track || []).includes('software') || (c.track || []).includes('both'));
                projectsData = (bundleLang.projects || dataLayer.projects || []).filter(p => p.category === 'software');
            }

            currentCerts = certsData;

            if (profileData) renderProfile(profileData);
            if (certsData.length) renderCertifications(certsData);
            if (projectsData.length) renderProjects(projectsData);

            // Refresco dinámico HTTP opcional
            const fileSuffix = currentLang === 'en' ? '_en' : '';
            try {
                const resProf = await fetch(`../../data/profile_software${fileSuffix}.json`);
                if (resProf.ok) {
                    profileData = await resProf.json();
                    renderProfile(profileData);
                }
            } catch (_) {}

            try {
                const resC = await fetch(`../../data/certifications${fileSuffix}.json`);
                if (resC.ok) {
                    const json = await resC.json();
                    currentCerts = (json.certifications || []).filter(c => (c.track || []).includes('software') || (c.track || []).includes('both'));
                    renderCertifications(currentCerts);
                }
            } catch (_) {}

            try {
                const resP = await fetch(`../../data/projects${fileSuffix}.json`);
                if (resP.ok) {
                    const json = await resP.json();
                    projectsData = (json.projects || []).filter(p => p.category === 'software');
                    renderProjects(projectsData);
                }
            } catch (_) {}

            document.body.setAttribute('data-rendered', 'true');
            window.status = 'ready';
        }

        function renderParagraphs(containerId, rawText) {
            const container = document.getElementById(containerId);
            if (!container || !rawText) return;
            const paragraphs = rawText.split(/\\r?\\n\\r?\\n/).filter(p => p.trim().length > 0);
            container.innerHTML = paragraphs.map(p => `<p class="profile-paragraph">${p.trim()}</p>`).join('');
        }

        function renderContacts(personal) {
            const container = document.getElementById('contactList');
            if (!container) return;

            const c = personal.contact || {};
            const isEn = currentLang === 'en';
            const links = [
                {
                    label: isEn ? "LinkedIn — Software Dev & AI" : "LinkedIn — Software Dev & IA",
                    url: c.linkedin || "https://www.linkedin.com/in/eduard-criollo-yule/",
                    display: c.linkedin ? c.linkedin.replace(/^https?:\\/\\/(www\\.)?/, '') : "linkedin.com/in/eduard-criollo-yule/"
                },
                {
                    label: isEn ? "GitHub: Repositories & Code" : "GitHub: Repositorios y Código",
                    url: c.github || "https://github.com/EduardCY",
                    display: c.github ? c.github.replace(/^https?:\\/\\/(www\\.)?/, '') : "github.com/EduardCY"
                },
                {
                    label: isEn ? "Platzi: Training Profile" : "Platzi: Perfil de Formación",
                    url: c.platzi || "https://platzi.com/@EduardYule/",
                    display: c.platzi ? c.platzi.replace(/^https?:\\/\\/(www\\.)?/, '') : "platzi.com/@EduardYule/"
                },
                {
                    label: isEn ? "Email Address" : "Correo Electrónico",
                    url: `mailto:${c.email || "eduardcriolloyule2004@gmail.com"}`,
                    display: c.email || "eduardcriolloyule2004@gmail.com"
                },
                {
                    label: isEn ? "Phone / WhatsApp" : "Teléfono / WhatsApp",
                    url: `tel:${(c.phone || "+573140000000").replace(/\\s+/g, '')}`,
                    display: c.phone || "+57 314 ••• ••••"
                }
            ];

            container.innerHTML = links.map(l => `
                <li style="margin-bottom: 0.6rem;">
                    <a href="${l.url}" target="_blank" rel="noopener noreferrer" class="contact-link">
                        <span>${l.label}</span>
                        <span class="url-text-explicit">${l.display}</span>
                    </a>
                </li>
            `).join('');
        }

        function renderProfile(data) {
            document.getElementById('profileName').textContent = data.personal.name;
            document.getElementById('profileHeadline').textContent = data.personal.headline;
            document.getElementById('profileLocation').textContent = data.personal.location;

            renderParagraphs('profileSummary', data.personal.summary_hook);
            renderContacts(data.personal);

            const metricsContainer = document.getElementById('metricsContainer');
            metricsContainer.innerHTML = (data.metrics || []).map(m => `
                <div class="metric-card">
                    <span class="metric-badge">${m.badge || (currentLang === 'en' ? 'Accreditation' : 'Acreditación')}</span>
                    <div class="metric-title">${m.title}</div>
                    <div class="metric-score">${m.score}</div>
                    <div class="metric-detail">${m.breakdown || m.level}</div>
                </div>
            `).join('');

            const skillsContainer = document.getElementById('skillsContainer');
            skillsContainer.innerHTML = Object.values(data.skills_matrix || {}).map(group => `
                <div class="skill-group">
                    <div class="skill-group-title">${group.category}</div>
                    <div class="skill-tags">
                        ${group.skills.map(s => `<span class="skill-pill">${s}</span>`).join('')}
                    </div>
                </div>
            `).join('');

            const langContainer = document.getElementById('languagesContainer');
            langContainer.innerHTML = (data.languages || []).map(l => `
                <div class="language-item">
                    <div class="lang-name">${l.language}</div>
                    <div class="lang-level">${l.level}</div>
                </div>
            `).join('');

            const eduContainer = document.getElementById('educationContainer');
            eduContainer.innerHTML = (data.education || []).map(edu => `
                <div class="timeline-item">
                    <div class="timeline-role">${edu.degree}</div>
                    <div class="timeline-company">${edu.institution}</div>
                    <div class="timeline-period">${edu.period}</div>
                    <ul class="timeline-desc">
                        ${(edu.highlights || []).map(h => `<li>${h}</li>`).join('')}
                    </ul>
                </div>
            `).join('');

            const expContainer = document.getElementById('experienceContainer');
            expContainer.innerHTML = (data.experience || []).map(exp => `
                <div class="timeline-item">
                    <div class="timeline-role">${exp.role}</div>
                    <div class="timeline-company">${exp.organization || exp.company}</div>
                    <div class="timeline-period">${exp.period}</div>
                    <ul class="timeline-desc">
                        ${(exp.responsibilities || []).map(r => `<li>${r}</li>`).join('')}
                    </ul>
                </div>
            `).join('');
        }

        function renderCertifications(certs) {
            const container = document.getElementById('certificationsContainer');
            if (!container) return;
            const t = UI_TEXT[currentLang] || UI_TEXT.es;

            container.innerHTML = certs.map(c => {
                const verifyLink = c.credential_url
                    ? `<a href="${c.credential_url}" target="_blank" rel="noopener noreferrer" class="cert-verify-link" onclick="event.stopPropagation()">
                         🔗 <span>${t.certVerifyBtn}</span>
                       </a>`
                    : '';
                const archiveLink = c.pdf_archive_path
                    ? `<a href="../../${c.pdf_archive_path}" target="_blank" class="cert-verify-link" style="color:var(--secondary);" onclick="event.stopPropagation()">
                         ${t.certPdfBtn}
                       </a>`
                    : '';

                const certKey = c.id || c.code || c.title;

                return `
                <div class="cert-card" onclick="openCertModal('${encodeURIComponent(certKey)}')">
                    <div>
                        <div class="cert-issuer">${c.institution}</div>
                        <div class="cert-name">${c.title}</div>
                        <div style="display:flex; flex-direction:column; gap:0.35rem; margin-top:0.4rem;">
                            <button type="button" class="cert-verify-link" style="background:none; border:none; padding:0; cursor:pointer; text-align:left; color:var(--accent);">
                                ${t.certInspectBtn}
                            </button>
                            ${verifyLink}
                            ${archiveLink}
                        </div>
                    </div>
                    <div class="cert-footer">
                        <span>📅 ${c.issue_date || t.certAccredited}</span>
                        <span>${c.code ? 'ID: ' + c.code.substring(0, 16) : t.certVerified}</span>
                    </div>
                </div>
                `;
            }).join('');
        }

        function renderProjects(projects) {
            const container = document.getElementById('projectsContainer');
            if (!container || !projects.length) return;
            const t = UI_TEXT[currentLang] || UI_TEXT.es;

            container.innerHTML = projects.map(p => {
                const links = p.links || {};
                const linkItems = [];
                if (p.is_private) {
                    linkItems.push(`<div style="display:inline-flex; align-items:center; gap:0.4rem; font-size:0.78rem; color:#f59e0b; font-family:var(--font-mono); background:rgba(245,158,11,0.08); padding:0.25rem 0.6rem; border:1px solid rgba(245,158,11,0.3); border-radius:4px; width:fit-content; margin-top:0.2rem;">🔒 <strong>${t.repoPrivateTitle}</strong> <span style="color:var(--text-muted);">${t.repoPrivateDesc}</span></div>`);
                } else {
                    if (links.github) linkItems.push(`<a href="${links.github}" target="_blank" class="cert-verify-link">${t.repoGithub} <span class="url-text-explicit">${links.github.replace(/^https?:\\/\\/(www\\.)?/, '')}</span></a>`);
                }
                if (links.demo) linkItems.push(`<a href="${links.demo}" target="_blank" class="cert-verify-link">${t.repoDemo}</a>`);

                const privateBadge = p.is_private ? `<span style="background:rgba(245,158,11,0.15); color:#f59e0b; border:1px solid rgba(245,158,11,0.35); font-size:0.68rem; padding:0.12rem 0.45rem; border-radius:3px; margin-left:0.5rem; font-family:var(--font-mono); font-weight:700;">🔒 ${currentLang === 'en' ? 'PRIVATE' : 'PRIVADO'}</span>` : '';

                return `
                <div class="project-item">
                    <div class="project-title-bar">
                        <span class="project-title">${p.title}${privateBadge}</span>
                        <span style="font-size: 0.78rem; font-family: var(--font-mono); color: var(--accent); font-weight:600;">${p.metrics || p.date || ''}</span>
                    </div>
                    <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 0.5rem;">${p.summary_executive || p.tagline || p.description}</p>
                    <div class="project-tech">
                        ${(p.tech_stack || []).map(tech => `<span class="tech-tag">${tech}</span>`).join('')}
                    </div>
                    <div style="margin-top: 0.5rem; display: flex; flex-direction: column; gap: 0.2rem;">
                        ${linkItems.join('')}
                    </div>
                </div>
                `;
            }).join('');
        }

        /**
         * Abre el modal inspector para una certificación específica.
         */
        function openCertModal(encodedKey) {
            const key = decodeURIComponent(encodedKey);
            const cert = currentCerts.find(c => (c.id === key) || (c.code === key) || (c.title === key));
            if (!cert) return;

            const t = UI_TEXT[currentLang] || UI_TEXT.es;
            const modal = document.getElementById('certModalBackdrop');
            const heading = document.getElementById('modalCertTitle');
            const content = document.getElementById('certModalContent');

            heading.textContent = cert.title;

            const pdfPath = cert.pdf_archive_path ? `../../${cert.pdf_archive_path}` : '';
            const verifyUrl = cert.credential_url || '';

            const skillsHtml = (cert.skills || []).length > 0
                ? `<div style="margin-top:0.75rem;">
                     <strong style="display:block; font-size:0.75rem; text-transform:uppercase; color:var(--accent); margin-bottom:0.4rem;">${t.modalSkills}</strong>
                     <div style="display:flex; flex-wrap:wrap; gap:0.4rem;">
                       ${cert.skills.map(s => `<span class="skill-pill" style="background:rgba(59,130,246,0.1); color:var(--text-main); border-color:rgba(59,130,246,0.25);">${s}</span>`).join('')}
                     </div>
                   </div>`
                : '';

            const previewSection = pdfPath
                ? `<div>
                     <strong style="display:block; font-size:0.75rem; text-transform:uppercase; color:var(--accent); margin-bottom:0.4rem;">${t.modalPreview}</strong>
                     <object data="${pdfPath}" type="application/pdf" class="cert-preview-frame">
                         <div style="padding:2rem; text-align:center; color:var(--text-muted); font-size:0.85rem;">
                             <p>${t.modalNoPdf}</p>
                             <a href="${pdfPath}" target="_blank" class="cert-action-btn primary" style="margin-top:1rem;">${t.modalOpenPdf}</a>
                         </div>
                     </object>
                   </div>`
                : `<div style="padding:1.5rem; background:rgba(0,0,0,0.2); border-radius:var(--radius-md); text-align:center; color:var(--text-muted);">
                     Certificación verificada digitalmente.
                   </div>`;

            content.innerHTML = `
                <div class="cert-modal-meta-grid">
                    <div class="cert-meta-item">
                        <strong>${t.modalIssuer}</strong>
                        <span>${cert.institution}</span>
                    </div>
                    <div class="cert-meta-item">
                        <strong>${t.modalDate}</strong>
                        <span>${cert.issue_date || t.certAccredited}</span>
                    </div>
                    <div class="cert-meta-item">
                        <strong>${t.modalCode}</strong>
                        <span style="font-family:var(--font-mono); font-size:0.75rem;">${cert.code || 'VERIFIED'}</span>
                    </div>
                    ${cert.score ? `
                    <div class="cert-meta-item">
                        <strong>${t.modalScore}</strong>
                        <span style="color:#38bdf8;">${cert.score}</span>
                    </div>` : ''}
                </div>

                <p style="font-size:0.88rem; color:var(--text-muted); line-height:1.5;">${cert.description || ''}</p>

                ${skillsHtml}

                <div class="cert-modal-actions">
                    ${pdfPath ? `<a href="${pdfPath}" target="_blank" class="cert-action-btn primary">${t.modalOpenPdf}</a>` : ''}
                    ${verifyUrl ? `<a href="${verifyUrl}" target="_blank" rel="noopener noreferrer" class="cert-action-btn secondary">${t.modalVerifyOnline}</a>` : ''}
                </div>

                ${previewSection}
            `;

            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function closeCertModal() {
            const modal = document.getElementById('certModalBackdrop');
            if (modal) modal.classList.remove('active');
            document.body.style.overflow = '';
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') closeCertModal();
        });

        // Restaurar tema previo
        if (localStorage.getItem('cv_theme') === 'dark') {
            document.body.classList.add('dark-mode');
        }

        // Modo compacto por URL
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('mode') === 'compact') {
            document.body.classList.add('compact-2p');
        }

        document.addEventListener('DOMContentLoaded', () => {
            applyLanguage();
        });
    </script>
    """

    script_pattern = re.compile(r'<!-- SCRIPT DE CARGA REACTIVA -->.*?</script>', re.DOTALL)
    html = script_pattern.sub(lambda _: new_script.strip(), html)

    with open(sw_file, "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated 01_Software_Dev/cv_web/cv_software.html")

    # Generate static English page cv_software_en.html
    html_en = html.replace('lang="es"', 'lang="en"')
    html_en = html_en.replace("let currentLang = new URLSearchParams(window.location.search).get('lang') || localStorage.getItem('cv_lang') || 'es';",
                            "let currentLang = 'en';")
    with open(WORKSPACE / "01_Software_Dev" / "cv_web" / "cv_software_en.html", "w", encoding="utf-8") as f:
        f.write(html_en)
    print("Generated 01_Software_Dev/cv_web/cv_software_en.html")

def upgrade_creative():
    cr_file = WORKSPACE / "02_Creative_Arts" / "cv_web" / "cv_creative.html"
    with open(cr_file, "r", encoding="utf-8") as f:
        html = f.read()

    # Modal CSS
    modal_css = """
        /* ==========================================================================
           MODAL INSPECTOR DE CERTIFICACIONES CREATIVAS & PREVIEW
           ========================================================================== */
        .art-modal-backdrop {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(8, 10, 15, 0.88);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            z-index: 1000;
            padding: 2rem 1rem;
            overflow-y: auto;
            align-items: center;
            justify-content: center;
        }
        .art-modal-backdrop.active {
            display: flex;
        }
        .art-modal-dialog {
            background: var(--surface-sheet);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-lg);
            max-width: 860px;
            width: 100%;
            max-height: 88vh;
            display: flex;
            flex-direction: column;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
            position: relative;
            animation: modalFadeIn 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            overflow: hidden;
        }
        .art-modal-header {
            padding: 1.25rem 1.75rem;
            border-bottom: 1px solid var(--border-light);
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(225, 29, 72, 0.04);
        }
        .art-modal-title {
            font-family: var(--font-display);
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--text-heading);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .art-modal-close {
            background: rgba(125, 125, 125, 0.1);
            border: 1px solid var(--border-light);
            color: var(--text-muted);
            font-size: 1.2rem;
            width: 32px;
            height: 32px;
            border-radius: 6px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
        }
        .art-modal-close:hover {
            color: #ef4444;
            background: rgba(239, 68, 68, 0.1);
            border-color: rgba(239, 68, 68, 0.3);
        }
        .art-modal-content {
            padding: 1.5rem 1.75rem;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }
        .art-preview-frame {
            width: 100%;
            height: 480px;
            border: 1px solid var(--border-light);
            border-radius: var(--radius-md);
            background: #0b0f17;
        }
        .art-modal-meta-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            background: rgba(225, 29, 72, 0.03);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-md);
            padding: 1rem;
        }
        .art-meta-item strong {
            display: block;
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--primary-accent);
            margin-bottom: 0.2rem;
        }
        .art-meta-item span {
            font-size: 0.85rem;
            color: var(--text-heading);
            font-weight: 600;
        }
        .art-modal-actions {
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
            margin-top: 0.5rem;
        }
        .art-action-btn {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.55rem 1.1rem;
            border-radius: 9999px;
            font-size: 0.82rem;
            font-weight: 600;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .art-action-btn.primary {
            background: var(--primary-accent);
            color: white;
            border: none;
        }
        .art-action-btn.secondary {
            background: transparent;
            color: var(--secondary-accent);
            border: 1px solid var(--secondary-accent);
        }
        .art-action-btn:hover {
            transform: translateY(-1px);
        }
        .art-cert-card-interactive {
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .art-cert-card-interactive:hover {
            border-color: var(--primary-accent) !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(225, 29, 72, 0.15);
        }
    """

    if "art-modal-backdrop" not in html:
        html = html.replace("    </style>", modal_css + "\n    </style>")

    # Replace Action Bar in cv_creative
    action_bar_pattern = re.compile(r'<div class="art-action-bar">.*?</div>', re.DOTALL)
    new_action_bar = """<div class="art-action-bar">
        <button class="art-btn primary" id="btnArtExportPdf" onclick="window.print()" title="Imprimir o Guardar como PDF">
            Exportar PDF
        </button>
        <button class="art-btn" id="compactArtToggleBtn" onclick="toggleArtCompactMode()" title="Alternar Vista Compacta de 2 Páginas">
            Modo Compacto (2P)
        </button>
        <button class="art-btn" id="themeArtToggleBtn" onclick="toggleArtTheme()" title="Alternar Modo Oscuro/Claro">
            Alternar Tema
        </button>
        <button class="art-btn" id="langArtToggleBtn" onclick="toggleArtLanguage()" title="Cambiar Idioma / Switch Language">
            🌐 English
        </button>
        <a href="../../CV_Eduard_Criollo_Yule.html" class="art-btn" id="btnArtNavHub" title="Ir al Portal Hub Principal">
            🏛️ Hub Principal
        </a>
        <a href="../../01_Software_Dev/cv_web/cv_software.html" class="art-btn" id="btnArtNavSoftware" title="Ver CV de Software">
            💻 CV Software
        </a>
        <a href="../portfolio/atelier/index.html" class="art-btn" id="btnArtNavAtelier" title="Ver Portafolio Atelier">
            Portafolio Atelier
        </a>
        <a href="../cv_plain_text/viewer.html" class="art-btn" id="btnArtNavAts" title="Ver Versión ATS en Texto Plano">
            Visor ATS
        </a>
    </div>"""
    html = action_bar_pattern.sub(new_action_bar, html)

    # Section Headers with ID hooks
    html = html.replace('<h3 class="art-section-title">Contacto</h3>', '<h3 class="art-section-title" id="artSecContact">Contacto</h3>')
    html = html.replace('<h3 class="art-section-title">Premios & Distinciones</h3>', '<h3 class="art-section-title" id="artSecAwards">Premios & Distinciones</h3>')
    html = html.replace('<h3 class="art-section-title">Herramientas</h3>', '<h3 class="art-section-title" id="artSecTools">Herramientas</h3>')
    html = html.replace('<h3 class="art-section-title">Idiomas</h3>', '<h3 class="art-section-title" id="artSecLanguages">Idiomas</h3>')
    html = html.replace('<h2 class="main-title">Declaración Artística & Visión</h2>', '<h2 class="main-title" id="artSecStatement">Declaración Artística & Visión</h2>')
    html = html.replace('<h2 class="main-title">Disciplinas de Especialización</h2>', '<h2 class="main-title" id="artSecDisciplines">Disciplinas de Especialización</h2>')
    html = html.replace('<h2 class="main-title">Formación Académica & Técnica</h2>', '<h2 class="main-title" id="artSecEducation">Formación Académica & Técnica</h2>')
    html = html.replace('<h2 class="main-title">Producción Audiovisual & Eventos</h2>', '<h2 class="main-title" id="artSecExperience">Producción Audiovisual & Eventos</h2>')
    html = html.replace('<h2 class="main-title">Proyectos Seleccionados & Obras</h2>', '<h2 class="main-title" id="artSecProjects">Proyectos Seleccionados & Obras</h2>')
    html = html.replace('<h2 class="main-title">Acreditaciones & Certificaciones</h2>', '<h2 class="main-title" id="artSecCerts">Acreditaciones & Certificaciones</h2>')

    # Modal HTML
    modal_html = """
    <!-- MODAL DE INSPECCIÓN DETALLADA DE CERTIFICACIONES CREATIVAS -->
    <div class="art-modal-backdrop" id="artModalBackdrop" onclick="if(event.target === this) closeArtCertModal()">
        <div class="art-modal-dialog" role="dialog" aria-modal="true" aria-labelledby="artModalHeading">
            <div class="art-modal-header">
                <h3 class="art-modal-title" id="artModalHeading">
                    <span>🎨</span> <span id="modalArtCertTitle">Detalles de Acreditación</span>
                </h3>
                <button class="art-modal-close" onclick="closeArtCertModal()" aria-label="Cerrar modal">✕</button>
            </div>
            <div class="art-modal-content" id="artModalContent">
                <!-- Inyectado dinámicamente -->
            </div>
        </div>
    </div>
"""
    if "artModalBackdrop" not in html:
        html = html.replace("    <!-- SCRIPT DE DATOS GLOBALES", modal_html + "\n    <!-- SCRIPT DE DATOS GLOBALES")

    # JavaScript for cv_creative
    new_creative_script = """
    <!-- SCRIPT DE CARGA REACTIVA Y BILINGÜE -->
    <script>
        /**
         * @fileoverview DataLoader reactivo y bilingüe para el CV Creativo.
         * Consume /data/bundle.js (local file:///) o /data/profile_creative.json (HTTP/HTTPS).
         * 
         * @author Eduard Criollo Yule
         */

        let currentLang = new URLSearchParams(window.location.search).get('lang') || localStorage.getItem('cv_creative_lang') || 'es';
        let currentCreativeCerts = [];

        const CREATIVE_UI_TEXT = {
            es: {
                pageTitle: "CV Creativo — Eduard Criollo Yule | Ilustrador, Animador & Escritor",
                btnExportPdf: "Exportar PDF",
                btnCompact: "Modo Compacto (2P)",
                btnCompactNormal: "Modo Normal",
                btnThemeDark: "Modo Oscuro",
                btnThemeLight: "Modo Claro",
                btnLang: "🌐 English",
                btnNavHub: "🏛️ Hub Principal",
                btnNavSoftware: "💻 CV Software",
                btnNavAtelier: "Portafolio Atelier",
                btnNavAts: "Visor ATS",
                secContact: "Contacto",
                secAwards: "Premios & Distinciones",
                secTools: "Herramientas",
                secLanguages: "Idiomas",
                secStatement: "Declaración Artística & Visión",
                secDisciplines: "Disciplinas de Especialización",
                secEducation: "Formación Académica & Técnica",
                secExperience: "Producción Audiovisual & Eventos",
                secProjects: "Proyectos Seleccionados & Obras",
                secCerts: "Acreditaciones & Certificaciones",
                certInspectBtn: "🔍 Inspeccionar",
                certPdfBtn: "📄 Documento PDF",
                certVerifyBtn: "🔗 Verificar Online",
                certAccredited: "Acreditado",
                modalIssuer: "Institución Emisora",
                modalDate: "Fecha de Acreditación",
                modalCode: "ID / Código",
                modalScore: "Calificación / Nivel",
                modalSkills: "Habilidades & Técnicas Acreditadas",
                modalPreview: "Visualización del Certificado",
                modalNoPdf: "El visor integrado no está disponible. Puede abrir el PDF directamente mediante el enlace inferior.",
                modalOpenPdf: "📄 Abrir Documento PDF",
                modalVerifyOnline: "🔗 Verificar en Línea"
            },
            en: {
                pageTitle: "Creative CV — Eduard Criollo Yule | Illustrator, Animator & Writer",
                btnExportPdf: "Export PDF",
                btnCompact: "Compact View (2P)",
                btnCompactNormal: "Normal View",
                btnThemeDark: "Dark Mode",
                btnThemeLight: "Light Mode",
                btnLang: "🌐 Español",
                btnNavHub: "🏛️ Main Hub",
                btnNavSoftware: "💻 Software CV",
                btnNavAtelier: "Atelier Portfolio",
                btnNavAts: "ATS Viewer",
                secContact: "Contact",
                secAwards: "Awards & Distinctions",
                secTools: "Creative Tools",
                secLanguages: "Languages",
                secStatement: "Artistic Statement & Vision",
                secDisciplines: "Areas of Specialization",
                secEducation: "Academic & Technical Education",
                secExperience: "Audiovisual Production & Events",
                secProjects: "Selected Works & Projects",
                secCerts: "Accreditations & Certifications",
                certInspectBtn: "🔍 Inspect",
                certPdfBtn: "📄 PDF Document",
                certVerifyBtn: "🔗 Verify Online",
                certAccredited: "Accredited",
                modalIssuer: "Issuing Organization",
                modalDate: "Issue Date",
                modalCode: "ID / Code",
                modalScore: "Grade / Level",
                modalSkills: "Validated Techniques & Skills",
                modalPreview: "Certificate Preview",
                modalNoPdf: "Embedded viewer not supported. You can open the PDF directly using the button below.",
                modalOpenPdf: "📄 Open PDF Document",
                modalVerifyOnline: "🔗 Verify Online"
            }
        };

        function toggleArtTheme() {
            document.body.classList.toggle('dark-mode');
            const isDark = document.body.classList.contains('dark-mode');
            localStorage.setItem('cv_creative_theme', isDark ? 'dark' : 'light');
            updateCreativeThemeBtn();
        }

        function updateCreativeThemeBtn() {
            const btn = document.getElementById('themeArtToggleBtn');
            const isDark = document.body.classList.contains('dark-mode');
            const t = CREATIVE_UI_TEXT[currentLang] || CREATIVE_UI_TEXT.es;
            if (btn) btn.textContent = isDark ? t.btnThemeLight : t.btnThemeDark;
        }

        function toggleArtCompactMode() {
            document.body.classList.toggle('compact-2p');
            const isCompact = document.body.classList.contains('compact-2p');
            const btn = document.getElementById('compactArtToggleBtn');
            const t = CREATIVE_UI_TEXT[currentLang] || CREATIVE_UI_TEXT.es;
            if (btn) btn.textContent = isCompact ? t.btnCompactNormal : t.btnCompact;
        }

        function toggleArtLanguage() {
            setArtLanguage(currentLang === 'es' ? 'en' : 'es');
        }

        function setArtLanguage(lang) {
            currentLang = lang;
            localStorage.setItem('cv_creative_lang', lang);
            applyCreativeLanguage();
        }

        function updateCreativeUITexts() {
            const t = CREATIVE_UI_TEXT[currentLang] || CREATIVE_UI_TEXT.es;
            document.title = t.pageTitle;

            const btnExport = document.getElementById('btnArtExportPdf');
            if (btnExport) btnExport.textContent = t.btnExportPdf;

            const btnCompact = document.getElementById('compactArtToggleBtn');
            if (btnCompact) {
                const isCompact = document.body.classList.contains('compact-2p');
                btnCompact.textContent = isCompact ? t.btnCompactNormal : t.btnCompact;
            }

            updateCreativeThemeBtn();

            const btnLang = document.getElementById('langArtToggleBtn');
            if (btnLang) btnLang.textContent = t.btnLang;

            const btnHub = document.getElementById('btnArtNavHub');
            if (btnHub) {
                btnHub.textContent = t.btnNavHub;
                btnHub.href = currentLang === 'en' ? "../../CV_Eduard_Criollo_Yule_en.html" : "../../CV_Eduard_Criollo_Yule.html";
            }

            const btnSoftware = document.getElementById('btnArtNavSoftware');
            if (btnSoftware) {
                btnSoftware.textContent = t.btnNavSoftware;
                btnSoftware.href = currentLang === 'en' ? "../../01_Software_Dev/cv_web/cv_software_en.html" : "../../01_Software_Dev/cv_web/cv_software.html";
            }

            const btnAtelier = document.getElementById('btnArtNavAtelier');
            if (btnAtelier) btnAtelier.textContent = t.btnNavAtelier;

            const btnAts = document.getElementById('btnArtNavAts');
            if (btnAts) {
                btnAts.textContent = t.btnNavAts;
                btnAts.href = currentLang === 'en' ? "../cv_plain_text/viewer_en.html" : "../cv_plain_text/viewer.html";
            }

            const sContact = document.getElementById('artSecContact');
            if (sContact) sContact.textContent = t.secContact;
            const sAwards = document.getElementById('artSecAwards');
            if (sAwards) sAwards.textContent = t.secAwards;
            const sTools = document.getElementById('artSecTools');
            if (sTools) sTools.textContent = t.secTools;
            const sLanguages = document.getElementById('artSecLanguages');
            if (sLanguages) sLanguages.textContent = t.secLanguages;
            const sStatement = document.getElementById('artSecStatement');
            if (sStatement) sStatement.textContent = t.secStatement;
            const sDisciplines = document.getElementById('artSecDisciplines');
            if (sDisciplines) sDisciplines.textContent = t.secDisciplines;
            const sEducation = document.getElementById('artSecEducation');
            if (sEducation) sEducation.textContent = t.secEducation;
            const sExperience = document.getElementById('artSecExperience');
            if (sExperience) sExperience.textContent = t.secExperience;
            const sProjects = document.getElementById('artSecProjects');
            if (sProjects) sProjects.textContent = t.secProjects;
            const sCerts = document.getElementById('artSecCerts');
            if (sCerts) sCerts.textContent = t.secCerts;
        }

        async function applyCreativeLanguage() {
            updateCreativeUITexts();

            let dataLayer = window.CV_DATA;
            let profileData = null;
            let certsData = [];
            let projectsData = [];

            if (dataLayer) {
                const bundleLang = (currentLang === 'en' && dataLayer.en) ? dataLayer.en : (dataLayer.es || dataLayer);
                profileData = bundleLang.profile_creative || dataLayer.profile_creative;
                certsData = (bundleLang.certifications || dataLayer.certifications || []).filter(c => (c.track || []).includes('creative') || (c.track || []).includes('both'));
                projectsData = (bundleLang.projects || dataLayer.projects || []).filter(p => p.category === 'creative');
            }

            currentCreativeCerts = certsData;

            if (profileData) renderCreativeCV(profileData);
            if (certsData.length) renderCreativeCertifications(certsData);
            if (projectsData.length) renderCreativeProjects(projectsData);

            // Refresco dinámico HTTP opcional
            const fileSuffix = currentLang === 'en' ? '_en' : '';
            try {
                const resProf = await fetch(`../../data/profile_creative${fileSuffix}.json`);
                if (resProf.ok) {
                    profileData = await resProf.json();
                    renderCreativeCV(profileData);
                }
            } catch (_) {}

            try {
                const resC = await fetch(`../../data/certifications${fileSuffix}.json`);
                if (resC.ok) {
                    const json = await resC.json();
                    currentCreativeCerts = (json.certifications || []).filter(c => (c.track || []).includes('creative') || (c.track || []).includes('both'));
                    renderCreativeCertifications(currentCreativeCerts);
                }
            } catch (_) {}

            try {
                const resP = await fetch(`../../data/projects${fileSuffix}.json`);
                if (resP.ok) {
                    const json = await resP.json();
                    projectsData = (json.projects || []).filter(p => p.category === 'creative');
                    renderCreativeProjects(projectsData);
                }
            } catch (_) {}

            document.body.setAttribute('data-rendered', 'true');
            window.status = 'ready';
        }

        function renderParagraphs(containerId, rawText) {
            const container = document.getElementById(containerId);
            if (!container || !rawText) return;
            const paragraphs = rawText.split(/\\r?\\n\\r?\\n/).filter(p => p.trim().length > 0);
            container.innerHTML = paragraphs.map(p => `<p class="profile-paragraph">${p.trim()}</p>`).join('');
        }

        function renderCreativeContacts(personal) {
            const container = document.getElementById('artContactList');
            if (!container) return;

            const c = personal.contact || {};
            const isEn = currentLang === 'en';
            const links = [
                {
                    label: isEn ? "ArtStation — Digital Gallery" : "ArtStation — Galería Digital",
                    url: c.artstation || "https://artstation.com/eduardyule",
                    display: c.artstation ? c.artstation.replace(/^https?:\\/\\/(www\\.)?/, '') : "artstation.com/eduardyule"
                },
                {
                    label: isEn ? "Behance — Visual Portfolio" : "Behance — Portafolio Visual",
                    url: c.behance || "https://behance.net/eduardcriollo",
                    display: c.behance ? c.behance.replace(/^https?:\\/\\/(www\\.)?/, '') : "behance.net/eduardcriollo"
                },
                {
                    label: isEn ? "LinkedIn — Arts & Media" : "LinkedIn — Artes & Audiovisual",
                    url: c.linkedin || "https://www.linkedin.com/in/eduard-criollo-arts/",
                    display: c.linkedin ? c.linkedin.replace(/^https?:\\/\\/(www\\.)?/, '') : "linkedin.com/in/eduard-criollo-arts/"
                },
                {
                    label: isEn ? "GitHub — Scripts & Tools" : "GitHub — Scripts & Tools",
                    url: c.github || "https://github.com/EduardCY",
                    display: c.github ? c.github.replace(/^https?:\\/\\/(www\\.)?/, '') : "github.com/EduardCY"
                },
                {
                    label: isEn ? "Email" : "Correo Electrónico",
                    url: `mailto:${c.email || "eduardcriolloyule2004@gmail.com"}`,
                    display: c.email || "eduardcriolloyule2004@gmail.com"
                },
                {
                    label: isEn ? "Phone / Contact" : "Teléfono / Contacto",
                    url: `tel:${(c.phone || "+573140000000").replace(/\\s+/g, '')}`,
                    display: c.phone || "+57 314 ••• ••••"
                }
            ];

            container.innerHTML = links.map(l => `
                <li style="margin-bottom: 0.55rem;">
                    <a href="${l.url}" target="_blank" rel="noopener noreferrer" class="art-contact-link">
                        <span style="font-weight: 500;">${l.label}</span>
                    </a>
                    <span class="explicit-url-creative">${l.display}</span>
                </li>
            `).join('');
        }

        function renderCreativeCV(data) {
            document.getElementById('artName').textContent = data.personal.name;
            document.getElementById('artHeadline').textContent = data.personal.headline;

            renderParagraphs('artStatement', data.personal.summary_hook);
            renderCreativeContacts(data.personal);

            document.getElementById('artAwardsContainer').innerHTML = (data.awards_recognitions || []).map(a =>
                `<div class="award-badge-card">
                    <div class="award-title">${a.title}</div>
                    <div class="award-desc">${a.description}</div>
                    ${a.year ? `<div style="font-size:0.7rem; color:#94a3b8; margin-top:0.25rem;">📅 ${a.year} • ${a.organization || ''}</div>` : ''}
                </div>`
            ).join('');

            const toolsList = (data.creative_skills_matrix && data.creative_skills_matrix.digital_tools)
                ? data.creative_skills_matrix.digital_tools.skills
                : ["Blender 3D", "Photoshop", "Illustrator", "After Effects", "Premiere Pro", "Clip Studio Paint", "AutoCAD", "Scrivener", "Audacity"];
            document.getElementById('artToolsContainer').innerHTML = toolsList.map(t => `<span class="art-tool-pill">${t}</span>`).join('');

            document.getElementById('artLanguagesContainer').innerHTML = (data.languages || []).map(l =>
                `<p style="margin-bottom:0.35rem;">
                    <strong>${l.language}:</strong> ${l.level} ${l.certification ? `<br><small style="color:#94a3b8;">${l.certification}</small>` : ''}
                </p>`
            ).join('');

            document.getElementById('disciplinesContainer').innerHTML = (data.artistic_disciplines || []).map(d =>
                `<div class="discipline-card">
                    <h3 class="discipline-title">${d.name}</h3>
                    <p class="discipline-desc">${d.description}</p>
                    <div style="margin-top:0.4rem;">${(d.tools || []).map(t => `<span class="art-tool-pill" style="background:#e2e8f0; color:#1e293b; border:none;">${t}</span>`).join('')}</div>
                </div>`
            ).join('');

            document.getElementById('artEducationContainer').innerHTML = (data.education || []).map(e => `
                <div class="art-timeline-item">
                    <div class="art-role">${e.degree}</div>
                    <div class="art-org">${e.institution}</div>
                    <div class="art-period">${e.period}</div>
                    <ul style="padding-left:1rem; font-size:0.85rem; color:var(--text-body); line-height: 1.5;">
                        ${(e.highlights || []).map(h => `<li>${h}</li>`).join('')}
                    </ul>
                </div>`
            ).join('');

            document.getElementById('artExperienceContainer').innerHTML = (data.experience || []).map(exp => `
                <div class="art-timeline-item">
                    <div class="art-role">${exp.role}</div>
                    <div class="art-org">${exp.organization}</div>
                    <div class="art-period">${exp.period}</div>
                    <ul style="padding-left:1rem; font-size:0.85rem; color:var(--text-body); line-height: 1.5;">
                        ${(exp.responsibilities || []).map(r => `<li>${r}</li>`).join('')}
                    </ul>
                </div>`
            ).join('');
        }

        function renderCreativeProjects(projects) {
            const container = document.getElementById('artProjectsContainer');
            if (!container) return;

            container.innerHTML = projects.map(p => {
                const links = p.links || {};
                const linkItems = [];
                if (links.artstation) linkItems.push(`<a href="${links.artstation}" target="_blank" class="cert-verify-link-creative">🎨 ArtStation: <span class="explicit-url-creative">${links.artstation.replace(/^https?:\\/\\/(www\\.)?/, '')}</span></a>`);
                if (links.behance) linkItems.push(`<a href="${links.behance}" target="_blank" class="cert-verify-link-creative">🅱️ Behance: <span class="explicit-url-creative">${links.behance.replace(/^https?:\\/\\/(www\\.)?/, '')}</span></a>`);
                if (links.github) linkItems.push(`<a href="${links.github}" target="_blank" class="cert-verify-link-creative">💻 GitHub: <span class="explicit-url-creative">${links.github.replace(/^https?:\\/\\/(www\\.)?/, '')}</span></a>`);

                return `
                <div class="discipline-card" style="border-left: 3px solid var(--primary-accent);">
                    <div style="font-size: 0.75rem; font-weight: 700; color: var(--primary-accent); text-transform: uppercase; margin-bottom: 0.25rem;">
                        ${p.sub_category} ${p.metrics ? `• ${p.metrics}` : ''}
                    </div>
                    <h3 class="discipline-title" style="margin-bottom: 0.35rem;">${p.title}</h3>
                    <p class="discipline-desc" style="margin-bottom: 0.6rem;">${p.summary_executive || p.description}</p>
                    <div style="margin-bottom:0.4rem;">
                        ${(p.tech_stack || []).map(t => `<span class="art-tool-pill" style="background: rgba(225, 29, 72, 0.08); color: #f43f5e; border: 1px solid rgba(225, 29, 72, 0.2);">${t}</span>`).join('')}
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 0.2rem; margin-top: 0.4rem;">
                        ${linkItems.join('')}
                    </div>
                </div>
                `;
            }).join('');
        }

        function renderCreativeCertifications(certs) {
            const container = document.getElementById('artCertsContainer');
            if (!container) return;
            const t = CREATIVE_UI_TEXT[currentLang] || CREATIVE_UI_TEXT.es;

            container.innerHTML = certs.map(c => {
                const verifyLink = c.credential_url
                    ? `<a href="${c.credential_url}" target="_blank" rel="noopener noreferrer" class="cert-verify-link-creative" onclick="event.stopPropagation()">
                         🔗 <span style="font-size:0.7rem;">${t.certVerifyBtn}</span>
                       </a>`
                    : '';
                const archiveLink = c.pdf_archive_path
                    ? `<a href="../../${c.pdf_archive_path}" target="_blank" class="cert-verify-link-creative" style="color:#8b5cf6;" onclick="event.stopPropagation()">
                         ${t.certPdfBtn}
                       </a>`
                    : '';

                const certKey = c.id || c.code || c.title;

                return `
                <div class="discipline-card art-cert-card-interactive" style="margin-bottom:0; padding:0.85rem;" onclick="openArtCertModal('${encodeURIComponent(certKey)}')">
                    <div style="font-size:0.72rem; color:var(--primary-accent); font-weight:700; text-transform:uppercase;">${c.institution}</div>
                    <div style="font-size:0.88rem; font-weight:700; color:var(--text-heading); margin:0.25rem 0;">${c.title}</div>
                    <div style="font-size:0.75rem; color:var(--text-muted);">${c.score ? `${t.modalScore}: ${c.score}` : (c.issue_date || t.certAccredited)}</div>
                    <div style="display:flex; flex-direction:column; gap:0.25rem; margin-top:0.4rem;">
                        <button type="button" class="cert-verify-link-creative" style="background:none; border:none; padding:0; cursor:pointer; text-align:left; color:var(--primary-accent);">
                            ${t.certInspectBtn}
                        </button>
                        ${verifyLink}
                        ${archiveLink}
                    </div>
                </div>
                `;
            }).join('');
        }

        function openArtCertModal(encodedKey) {
            const key = decodeURIComponent(encodedKey);
            const cert = currentCreativeCerts.find(c => (c.id === key) || (c.code === key) || (c.title === key));
            if (!cert) return;

            const t = CREATIVE_UI_TEXT[currentLang] || CREATIVE_UI_TEXT.es;
            const modal = document.getElementById('artModalBackdrop');
            const heading = document.getElementById('modalArtCertTitle');
            const content = document.getElementById('artModalContent');

            heading.textContent = cert.title;

            const pdfPath = cert.pdf_archive_path ? `../../${cert.pdf_archive_path}` : '';
            const verifyUrl = cert.credential_url || '';

            const skillsHtml = (cert.skills || []).length > 0
                ? `<div style="margin-top:0.75rem;">
                     <strong style="display:block; font-size:0.75rem; text-transform:uppercase; color:var(--primary-accent); margin-bottom:0.4rem;">${t.modalSkills}</strong>
                     <div style="display:flex; flex-wrap:wrap; gap:0.4rem;">
                       ${cert.skills.map(s => `<span class="art-tool-pill" style="background:rgba(225,29,72,0.1); color:var(--text-heading); border-color:rgba(225,29,72,0.25);">${s}</span>`).join('')}
                     </div>
                   </div>`
                : '';

            const previewSection = pdfPath
                ? `<div>
                     <strong style="display:block; font-size:0.75rem; text-transform:uppercase; color:var(--primary-accent); margin-bottom:0.4rem;">${t.modalPreview}</strong>
                     <object data="${pdfPath}" type="application/pdf" class="art-preview-frame">
                         <div style="padding:2rem; text-align:center; color:var(--text-muted); font-size:0.85rem;">
                             <p>${t.modalNoPdf}</p>
                             <a href="${pdfPath}" target="_blank" class="art-action-btn primary" style="margin-top:1rem;">${t.modalOpenPdf}</a>
                         </div>
                     </object>
                   </div>`
                : `<div style="padding:1.5rem; background:rgba(0,0,0,0.05); border-radius:var(--radius-md); text-align:center; color:var(--text-muted);">
                     Acreditación verificada digitalmente.
                   </div>`;

            content.innerHTML = `
                <div class="art-modal-meta-grid">
                    <div class="art-meta-item">
                        <strong>${t.modalIssuer}</strong>
                        <span>${cert.institution}</span>
                    </div>
                    <div class="art-meta-item">
                        <strong>${t.modalDate}</strong>
                        <span>${cert.issue_date || t.certAccredited}</span>
                    </div>
                    <div class="art-meta-item">
                        <strong>${t.modalCode}</strong>
                        <span style="font-family:monospace; font-size:0.75rem;">${cert.code || 'VERIFIED'}</span>
                    </div>
                    ${cert.score ? `
                    <div class="art-meta-item">
                        <strong>${t.modalScore}</strong>
                        <span style="color:var(--primary-accent);">${cert.score}</span>
                    </div>` : ''}
                </div>

                <p style="font-size:0.88rem; color:var(--text-muted); line-height:1.5;">${cert.description || ''}</p>

                ${skillsHtml}

                <div class="art-modal-actions">
                    ${pdfPath ? `<a href="${pdfPath}" target="_blank" class="art-action-btn primary">${t.modalOpenPdf}</a>` : ''}
                    ${verifyUrl ? `<a href="${verifyUrl}" target="_blank" rel="noopener noreferrer" class="art-action-btn secondary">${t.modalVerifyOnline}</a>` : ''}
                </div>

                ${previewSection}
            `;

            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function closeArtCertModal() {
            const modal = document.getElementById('artModalBackdrop');
            if (modal) modal.classList.remove('active');
            document.body.style.overflow = '';
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') closeArtCertModal();
        });

        if (localStorage.getItem('cv_creative_theme') === 'dark') {
            document.body.classList.add('dark-mode');
        }

        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('mode') === 'compact') {
            document.body.classList.add('compact-2p');
        }

        document.addEventListener('DOMContentLoaded', () => {
            applyCreativeLanguage();
        });
    </script>
    """

    script_pattern = re.compile(r'<!-- SCRIPT DE CARGA REACTIVA -->.*?</script>', re.DOTALL)
    html = script_pattern.sub(lambda _: new_creative_script.strip(), html)

    with open(cr_file, "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated 02_Creative_Arts/cv_web/cv_creative.html")

    # Generate static English page cv_creative_en.html
    html_en = html.replace('lang="es"', 'lang="en"')
    html_en = html_en.replace("let currentLang = new URLSearchParams(window.location.search).get('lang') || localStorage.getItem('cv_creative_lang') || 'es';",
                              "let currentLang = 'en';")
    with open(WORKSPACE / "02_Creative_Arts" / "cv_web" / "cv_creative_en.html", "w", encoding="utf-8") as f:
        f.write(html_en)
    print("Generated 02_Creative_Arts/cv_web/cv_creative_en.html")

if __name__ == "__main__":
    upgrade_software()
    upgrade_creative()

