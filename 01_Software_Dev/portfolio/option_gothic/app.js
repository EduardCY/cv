/**
 * @fileoverview Lógica reactiva para el Portafolio Gótico (The Gothic Sanctuary).
 * Consume /data/projects.json, /data/certifications.json y /data/profile_software.json.
 * 
 * @author Eduard Criollo Yule
 */

let allProjects = [];
let allCertifications = [];
let currentFilter = 'all';

async function loadGothicData() {
    // 1. Cargar inmediatamente desde window.CV_DATA si está disponible (Soporte local file:///)
    if (window.CV_DATA) {
        if (window.CV_DATA.projects) {
            allProjects = window.CV_DATA.projects.filter(p => p.category === 'software');
        }
        if (window.CV_DATA.certifications) {
            allCertifications = window.CV_DATA.certifications.filter(c => (c.track || []).includes('software') || (c.track || []).includes('both'));
        }
    }

    renderProjects(allProjects);
    renderCertifications(allCertifications);
    setupFilters();

    // 2. Refresco dinámico si se sirve bajo servidor HTTP/HTTPS
    try {
        const resProjects = await fetch('../../../data/projects.json');
        if (resProjects.ok) {
            const data = await resProjects.json();
            allProjects = (data.projects || []).filter(p => p.category === 'software');
            renderProjects(allProjects);
        }
    } catch (_) {}

    try {
        const resCerts = await fetch('../../../data/certifications.json');
        if (resCerts.ok) {
            const data = await resCerts.json();
            allCertifications = (data.certifications || []).filter(c => (c.track || []).includes('software') || (c.track || []).includes('both'));
            renderCertifications(allCertifications);
        }
    } catch (_) {}
}

function renderProjects(projects) {
    const container = document.getElementById('projectsContainer');
    if (!container) return;

    if (!projects || projects.length === 0) {
        container.innerHTML = `<div class="loading-state">No se encontraron proyectos en este criterio de búsqueda.</div>`;
        return;
    }

    container.innerHTML = projects.map(p => `
        <article class="project-card">
            <div>
                ${p.image_svg_badge ? `<div class="card-preview-banner">${p.image_svg_badge}</div>` : ''}
                
                <div class="card-kicker">
                    <span>${p.is_private ? '🔒 PRIVADO' : (p.sub_category || 'INGENIERÍA DE SOFTWARE')}</span>
                    <span>${p.date || '2025-2026'}</span>
                </div>
                
                <h3 class="card-title">${p.title}</h3>
                
                <p class="card-desc">
                    ${p.description || p.summary_executive || p.tagline}
                </p>
                
                ${p.metrics ? `<div class="card-metrics">${p.metrics}</div>` : ''}
                
                <div class="card-tags">
                    ${(p.tech_stack || []).map(t => `<span class="card-tag">${t}</span>`).join('')}
                </div>
            </div>
            
            <div class="card-actions">
                ${p.is_private ? `
                    <span class="action-repo-btn" style="opacity: 0.85; cursor: default; border-color: rgba(245, 158, 11, 0.35); color: #f59e0b;" title="Repositorio Privado / Confidencial">
                        <span>🔒 Repositorio Privado</span>
                    </span>
                ` : (p.links && p.links.github ? `
                    <a href="${p.links.github}" target="_blank" class="action-repo-btn" title="Ver Repositorio en GitHub">
                        <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.1-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2z"/></svg>
                        <span>GitHub Repo</span>
                    </a>
                ` : '')}
                <button class="gothic-btn secondary" style="padding: 0.5rem 1rem; font-size: 0.78rem;" onclick="openProjectModal('${p.id}')">
                    Arquitectura & Detalles
                </button>
            </div>
        </article>
    `).join('');
}

function renderCertifications(certs) {
    const container = document.getElementById('certsContainer');
    if (!container) return;

    container.innerHTML = certs.map(c => {
        const pdfLink = c.pdf_archive_path
            ? `<a href="../../../${c.pdf_archive_path}" target="_blank" class="action-repo-btn" style="padding:0.35rem 0.75rem; font-size:0.75rem; border-color:var(--color-gold); color:var(--color-gold);">📄 Ver PDF Oficial</a>`
            : '';
        const verifyLink = c.credential_url
            ? `<a href="${c.credential_url}" target="_blank" class="action-repo-btn" style="padding:0.35rem 0.75rem; font-size:0.75rem;">🔗 Verificar Online</a>`
            : '';

        return `
        <div class="gothic-cert-card">
            <div class="cert-emblem">⚜</div>
            <div style="font-size: 0.72rem; color: var(--color-gold); text-transform: uppercase; letter-spacing: 1px;">${c.institution}</div>
            <h4 class="gothic-cert-title">${c.title}</h4>
            <div class="gothic-cert-org">Fecha: ${c.issue_date || 'Acreditado'} ${c.code ? `• ID: ${c.code.substring(0, 15)}...` : ''}</div>
            <p style="font-size: 0.82rem; color: var(--text-secondary); line-height: 1.5; margin-bottom: 0.75rem;">${c.description}</p>
            <div style="display:flex; gap:0.5rem; flex-wrap:wrap; margin-top:auto;">
                ${pdfLink}
                ${verifyLink}
            </div>
        </div>
        `;
    }).join('');
}

function setupFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const filter = btn.getAttribute('data-filter');
            applyFilter(filter);
        });
    });
}

function applyFilter(filter) {
    if (filter === 'all') {
        renderProjects(allProjects);
    } else if (filter === 'ai') {
        renderProjects(allProjects.filter(p => 
            p.sub_category.toLowerCase().includes('inteligencia') || 
            (p.tech_stack || []).some(t => t.toLowerCase().includes('scikit') || t.toLowerCase().includes('ai'))
        ));
    } else if (filter === 'backend') {
        renderProjects(allProjects.filter(p => 
            p.sub_category.toLowerCase().includes('backend') || 
            p.sub_category.toLowerCase().includes('datos') ||
            (p.tech_stack || []).some(t => t.toLowerCase().includes('spring') || t.toLowerCase().includes('fastapi') || t.toLowerCase().includes('sql'))
        ));
    } else if (filter === 'fullstack') {
        renderProjects(allProjects.filter(p => 
            p.sub_category.toLowerCase().includes('full stack') || 
            p.sub_category.toLowerCase().includes('reactivo') ||
            (p.tech_stack || []).some(t => t.toLowerCase().includes('angular') || t.toLowerCase().includes('javascript'))
        ));
    }
}

function openProjectModal(projectId) {
    const project = allProjects.find(p => p.id === projectId);
    if (!project) return;

    const modal = document.getElementById('projectModal');
    const modalBody = document.getElementById('modalBody');

    modalBody.innerHTML = `
        <div style="color: var(--color-gold); font-size: 0.8rem; letter-spacing: 2px; text-transform: uppercase;">
            ${project.sub_category || 'PROYECTO DE INGENIERÍA'} • ${project.date || '2025'}
        </div>
        <h2 class="modal-title">${project.title}</h2>
        <div class="gold-line" style="margin: 0.75rem 0 1.5rem 0;"></div>

        ${project.is_private ? `
            <div style="background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.3); padding: 0.85rem 1rem; border-radius: 6px; margin-bottom: 1.25rem; font-size: 0.85rem; color: #fbbf24;">
                <strong>🔒 Repositorio Privado / Confidencial:</strong> ${project.access_note || 'Código fuente y demostración técnica disponibles bajo solicitud profesional.'}
            </div>
        ` : ''}
        
        ${project.image_svg_badge ? `<div style="margin-bottom: 1.5rem; border: 1px solid var(--border-gold-subtle); border-radius: 8px; overflow:hidden;">${project.image_svg_badge}</div>` : ''}

        <p style="font-size: 0.95rem; color: var(--text-primary); line-height: 1.8; margin-bottom: 1.25rem;">
            ${project.description}
        </p>

        <h4 style="font-family: var(--font-heading); color: var(--color-gold-bright); font-size: 1rem; margin-bottom: 0.6rem;">Aspectos Técnicos Destacados</h4>
        <ul style="list-style: none; margin-bottom: 1.5rem; display: flex; flex-direction: column; gap: 0.5rem; font-size: 0.88rem; color: var(--text-secondary);">
            ${(project.highlights || []).map(h => `<li style="padding-left: 1.2rem; position: relative;"><span style="position: absolute; left: 0; color: var(--color-gold);">⚜</span>${h}</li>`).join('')}
        </ul>

        ${project.architecture_details ? `
            <div style="background: rgba(212, 175, 55, 0.05); border: 1px solid var(--border-gold-subtle); padding: 1rem; border-radius: 6px; margin-bottom: 1.5rem; font-size: 0.85rem; color: var(--text-secondary);">
                <strong style="color: var(--color-gold-bright);">Arquitectura & Despliegue:</strong> ${project.architecture_details}
            </div>
        ` : ''}

        <div style="display: flex; gap: 0.75rem; flex-wrap: wrap; margin-top: 1.5rem;">
            ${project.links && project.links.github ? `
                <a href="${project.links.github}" target="_blank" class="gothic-btn primary" style="font-size: 0.75rem; padding: 0.5rem 1.2rem;">
                    Ver Código en GitHub
                </a>
            ` : ''}
            <a href="https://www.linkedin.com/in/eduard-criollo-yule/" target="_blank" class="gothic-btn secondary" style="font-size: 0.75rem; padding: 0.5rem 1.2rem;">
                Consultar con el Autor en LinkedIn
            </a>
        </div>
    `;

    modal.classList.add('active');
}

function closeProjectModal() {
    const modal = document.getElementById('projectModal');
    if (modal) modal.classList.remove('active');
}

function closeModalOnBackdrop(e) {
    if (e.target.id === 'projectModal') {
        closeProjectModal();
    }
}

document.addEventListener('DOMContentLoaded', loadGothicData);
