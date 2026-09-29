#!/usr/bin/env python3
"""
upgrade_cv_software.py
=======================
Upgrades 01_Software_Dev/cv_web/cv_software.html with:
1. Interactive Certification Inspection Modal with verified PDF preview & skills breakdown
2. Dynamic Language Switcher (ES / EN) supporting localStorage & ?lang=en
3. Generates static cv_software_en.html preset to English
"""

import sys
from pathlib import Path

WORKSPACE_ROOT = Path("f:/Calipso_Online/03_Profesional/Cv")
SRC_FILE = WORKSPACE_ROOT / "01_Software_Dev" / "cv_web" / "cv_software.html"
EN_FILE = WORKSPACE_ROOT / "01_Software_Dev" / "cv_web" / "cv_software_en.html"

def main():
    with open(SRC_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add modal CSS before </style>
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
            max-width: 840px;
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

    if "cert-modal-backdrop" not in content:
        content = content.replace("    </style>", modal_css + "\n    </style>")

    # 2. Add Language switch button in action bar
    old_action_bar = """        <button class="action-btn" id="themeToggleBtn" onclick="toggleDarkMode()" title="Alternar Modo Oscuro/Claro">
            Alternar Tema
        </button>"""

    new_action_bar = """        <button class="action-btn" id="themeToggleBtn" onclick="toggleDarkMode()" title="Alternar Modo Oscuro/Claro">
            Alternar Tema
        </button>
        <button class="action-btn" id="langToggleBtn" onclick="toggleLanguage()" title="Switch Language / Cambiar Idioma">
            🌐 English
        </button>"""

    if "langToggleBtn" not in content:
        content = content.replace(old_action_bar, new_action_bar)

    # 3. Add Modal HTML before </div> <!-- SCRIPT DE DATOS GLOBALES -->
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

    if "certModalBackdrop" not in content:
        content = content.replace("    <!-- SCRIPT DE DATOS GLOBALES", modal_html + "\n    <!-- SCRIPT DE DATOS GLOBALES")

    # 4. Enhance JS with full bilingual support & modal functions
    # Let's inspect the script section
    with open(SRC_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated base markup and CSS for cv_software.html")

if __name__ == "__main__":
    main()
