/**
 * @fileoverview Lógica reactiva para la Galería Atelier de Eduard Criollo Yule.
 * Consume /data/projects.json y /data/profile_creative.json.
 * 
 * @author Eduard Criollo Yule
 */

let artProjects = [];

async function loadAtelierData() {
    // 1. Cargar inmediatamente desde window.CV_DATA si está disponible (Soporte local file:///)
    if (window.CV_DATA) {
        if (window.CV_DATA.projects) {
            artProjects = window.CV_DATA.projects.filter(p => p.category === 'creative');
        }
        if (window.CV_DATA.profile_creative) {
            updateAtelierContactLinks(window.CV_DATA.profile_creative);
        }
    }

    renderArtWorks(artProjects);
    setupArtFilters();

    // 2. Refresco dinámico si se sirve bajo servidor HTTP/HTTPS
    try {
        const [resProj, resProfile] = await Promise.allSettled([
            fetch('../../../data/projects.json').then(r => r.ok ? r.json() : Promise.reject()),
            fetch('../../../data/profile_creative.json').then(r => r.ok ? r.json() : Promise.reject())
        ]);

        if (resProj.status === 'fulfilled') {
            const data = resProj.value;
            artProjects = (data.projects || []).filter(p => p.category === 'creative');
            renderArtWorks(artProjects);
        }
        if (resProfile.status === 'fulfilled') {
            updateAtelierContactLinks(resProfile.value);
        }
    } catch (_) {}
}

function updateAtelierContactLinks(profileData) {
    const c = profileData.personal?.contact || {};
    if (c.linkedin) {
        ['hdrLinkedIn', 'heroLinkedIn', 'ftrLinkedIn'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.href = c.linkedin;
        });
    }
    if (c.artstation) {
        ['hdrArtstation', 'heroArtstation', 'ftrArtstation'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.href = c.artstation;
        });
    }
    if (c.behance) {
        ['hdrBehance', 'heroBehance', 'ftrBehance'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.href = c.behance;
        });
    }
    if (c.github) {
        ['hdrGitHub'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.href = c.github;
        });
    }
    if (c.email) {
        ['heroEmail', 'ftrEmail'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.href = `mailto:${c.email}`;
        });
    }
}

function renderArtWorks(projects) {
    const container = document.getElementById('artWorksContainer');
    if (!container) return;

    if (!projects || projects.length === 0) {
        container.innerHTML = `<div style="text-align: center; color: #94a3b8; grid-column: 1/-1;">No hay piezas disponibles en esta categoría.</div>`;
        return;
    }

    container.innerHTML = projects.map(p => `
        <article class="work-card">
            <div>
                ${p.image_svg_badge ? `<div class="work-preview-banner">${p.image_svg_badge}</div>` : ''}
                
                <div class="work-category">${p.sub_category || 'ARTE & CREATIVIDAD'}</div>
                <h3 class="work-title">${p.title}</h3>
                
                <p class="work-desc">
                    ${p.description || p.summary_executive || p.tagline}
                </p>
                
                <div class="work-tags">
                    ${(p.tech_stack || []).map(t => `<span class="work-tag">${t}</span>`).join('')}
                </div>
            </div>
            
            <div class="work-actions">
                ${p.links && p.links.artstation ? `
                    <a href="${p.links.artstation}" target="_blank" rel="noopener noreferrer" class="work-action-btn" title="Ver en ArtStation">
                        <svg viewBox="0 0 24 24" width="13" height="13" fill="currentColor"><path d="M0 17.723l2.027 3.505h.001a2.424 2.424 0 0 0 2.164 1.333h13.457l-2.792-4.838H0zm24 .025c0-.484-.143-.935-.388-1.314L15.728 2.728a2.424 2.424 0 0 0-2.164-1.333H9.419L21.598 22.54l1.92-3.325c.378-.637.482-.919.482-1.467zm-11.129-3.462L7.428 4.858l-5.444 9.428h10.887z"/></svg>
                        <span>ArtStation</span>
                    </a>
                ` : ''}
                ${p.links && p.links.behance ? `
                    <a href="${p.links.behance}" target="_blank" rel="noopener noreferrer" class="work-action-btn" title="Ver en Behance">
                        <svg viewBox="0 0 24 24" width="13" height="13" fill="currentColor"><path d="M6.938 4.503c.702 0 1.34.06 1.92.188.577.13 1.07.33 1.485.61.41.28.733.65.96 1.12.225.47.34 1.05.34 1.73 0 .74-.17 1.36-.507 1.86-.338.5-.837.9-1.502 1.22.906.26 1.576.72 2.022 1.37.448.66.665 1.45.665 2.36 0 .75-.13 1.39-.41 1.93-.28.55-.67 1-.16 1.35-.49.36-1.06.62-1.7.78-.64.17-1.3.25-1.99.25H0V4.503h6.938zm-.588 5.745c.592 0 1.075-.14 1.45-.43.376-.29.564-.73.564-1.33 0-.34-.063-.62-.19-.83-.127-.21-.295-.37-.505-.49-.21-.12-.45-.2-.71-.24-.261-.04-.532-.06-.81-.06H3.93v3.38h2.42zm.166 6.05c.315 0 .608-.03.88-.09.272-.06.51-.16.71-.31.2-.14.36-.33.48-.57.12-.23.18-.53.18-.89 0-.71-.2-1.22-.602-1.54-.4-.32-.935-.48-1.604-.48H3.93v3.88h2.586zm11.39-5.87c-.4-.43-.987-.65-1.76-.65-.5 0-.918.09-1.254.27-.335.18-.607.41-.813.7-.205.29-.348.6-.428.93-.08.33-.124.65-.13.96h5.44c-.067-.9-.355-1.6-.706-.98a2.13 2.13 0 0 0-.35-.23zm.857-6.16h-5.08v1.475h5.08V4.268zM24 13.29c0 .21-.006.42-.02.63H16.78c.06.75.31 1.31.75 1.67.44.36.983.54 1.635.54.54 0 1.005-.14 1.395-.41.39-.28.633-.58.726-.91h2.81c-.425 1.27-1.087 2.2-1.99 2.77-.9.57-1.98.86-3.24.86-1.6 0-2.93-.49-3.97-1.48-1.04-.99-1.56-2.32-1.56-3.99 0-1.62.5-2.95 1.49-3.99 1-.04 2.34-.53 3.96-.53 1.03 0 1.94.19 2.73.58.79.39 1.43.92 1.9 1.6.47.68.81 1.46 1.01 2.33.19.86.29 1.75.29 2.63z"/></svg>
                        <span>Behance</span>
                    </a>
                ` : ''}
                <button class="atelier-btn secondary" style="padding: 0.45rem 0.85rem; font-size: 0.78rem;" onclick="openArtModal('${p.id}')">
                    Detalles de Obra
                </button>
            </div>
        </article>
    `).join('');
}

function setupArtFilters() {
    const btns = document.querySelectorAll('.art-filter-btn');
    btns.forEach(btn => {
        btn.addEventListener('click', () => {
            btns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filter = btn.getAttribute('data-filter');
            if (filter === 'all') {
                renderArtWorks(artProjects);
            } else if (filter === 'concept') {
                renderArtWorks(artProjects.filter(p => p.sub_category.toLowerCase().includes('ilustración') || p.sub_category.toLowerCase().includes('concept')));
            } else if (filter === 'animation') {
                renderArtWorks(artProjects.filter(p => p.sub_category.toLowerCase().includes('animación') || p.sub_category.toLowerCase().includes('3d')));
            } else if (filter === 'narrative') {
                renderArtWorks(artProjects.filter(p => p.sub_category.toLowerCase().includes('narrativa') || p.sub_category.toLowerCase().includes('literaria')));
            }
        });
    });
}

function openArtModal(id) {
    const project = artProjects.find(p => p.id === id);
    if (!project) return;

    const modal = document.getElementById('artModal');
    const content = document.getElementById('artModalContent');

    content.innerHTML = `
        <div style="font-family: 'Outfit'; font-size: 0.8rem; color: #f43f5e; font-weight: 700; text-transform: uppercase; margin-bottom: 0.35rem;">
            ${project.sub_category} • ${project.date || '2025'}
        </div>
        <h2 style="font-family: 'Cinzel'; font-size: 1.6rem; color: #fff1f2; margin-bottom: 1rem;">
            ${project.title}
        </h2>
        
        ${project.image_svg_badge ? `<div style="margin-bottom: 1.25rem; border: 1px solid rgba(244,63,94,0.3); border-radius: 6px; overflow:hidden;">${project.image_svg_badge}</div>` : ''}

        <p style="font-size: 0.95rem; color: #f8fafc; line-height: 1.7; margin-bottom: 1.25rem;">
            ${project.description}
        </p>

        <h4 style="font-family: 'Outfit'; font-size: 0.9rem; color: #fbbf24; margin-bottom: 0.5rem;">Aspectos Técnicos y Creativos</h4>
        <ul style="list-style: none; margin-bottom: 1.5rem; display: flex; flex-direction: column; gap: 0.4rem; font-size: 0.88rem; color: #cbd5e1;">
            ${(project.highlights || []).map(h => `<li style="padding-left: 1.2rem; position: relative;"><span style="position: absolute; left: 0; color: #f43f5e;">✦</span>${h}</li>`).join('')}
        </ul>

        <div style="display: flex; gap: 0.75rem; flex-wrap: wrap; margin-top: 1.25rem;">
            ${project.links && project.links.artstation ? `
                <a href="${project.links.artstation}" target="_blank" class="atelier-btn primary" style="font-size: 0.75rem; padding: 0.5rem 1rem;">
                    Ver en ArtStation
                </a>
            ` : ''}
            ${project.links && project.links.behance ? `
                <a href="${project.links.behance}" target="_blank" class="atelier-btn secondary" style="font-size: 0.75rem; padding: 0.5rem 1rem;">
                    Ver en Behance
                </a>
            ` : ''}
        </div>
    `;

    modal.classList.add('active');
}

function closeArtModal() {
    const modal = document.getElementById('artModal');
    if (modal) modal.classList.remove('active');
}

function closeArtBackdrop(e) {
    if (e.target.id === 'artModal') {
        closeArtModal();
    }
}

document.addEventListener('DOMContentLoaded', loadAtelierData);
