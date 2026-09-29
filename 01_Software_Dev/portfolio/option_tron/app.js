/**
 * @fileoverview Motor de Interfaz y Gestor de Ventanas para Windows 97 Edition.
 * Controla el ciclo de vida de ventanas (arrastre, enfoque, minimizar, maximizar, cerrar),
 * la barra de tareas, el menú inicio, y el consumo reactivo del catálogo de proyectos y certificaciones.
 * 
 * @author Eduard Criollo Yule
 */

// Estado global de la sesión Windows 97
let highestZIndex = 20;
let currentFilter = 'all';
let allSoftwareProjects = [];
let allCertifications = [];
const windowStates = {}; // Guarda posición previa para restaurar tras maximizar

/**
 * Inicialización principal al cargar el DOM.
 * Configura manejadores de eventos, reloj, arrastre y carga de datos.
 */
document.addEventListener('DOMContentLoaded', () => {
    initClock();
    initDraggableWindows();
    initResizableWindows();
    initWindowSnappingAndLayouts();
    initDesktopIcons();
    initClickOutside();
    loadSystemData();
});

/**
 * Inicializa y mantiene el reloj de la barra de tareas en tiempo real.
 * Proporciona el feedback visual clásico del system tray de Windows 9x.
 */
function initClock() {
    const clockElement = document.getElementById('systemClock');
    if (!clockElement) return;

    function update() {
        const now = new Date();
        let hours = now.getHours();
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');
        const ampm = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12;
        hours = hours ? hours : 12; // Formato 12 horas
        clockElement.textContent = `${hours}:${minutes}:${seconds} ${ampm}`;
    }

    update();
    setInterval(update, 1000);
}

/**
 * Carga los datos maestros desde window.CV_DATA (offline file:///) y refresca vía fetch HTTP/HTTPS.
 * Garantiza persistencia y tolerancia a fallos en cualquier contexto de ejecución.
 */
async function loadSystemData() {
    // 1. Carga inmediata desde bundle local
    if (window.CV_DATA) {
        if (window.CV_DATA.projects) {
            allSoftwareProjects = window.CV_DATA.projects.filter(p => p.category === 'software');
        }
        if (window.CV_DATA.certifications) {
            allCertifications = window.CV_DATA.certifications.filter(c => 
                (c.track || []).includes('software') || (c.track || []).includes('both')
            );
        }
        if (window.CV_DATA.profile_software && window.CV_DATA.profile_software.personal) {
            const summary = window.CV_DATA.profile_software.personal.summary_hook;
            const el = document.getElementById('sysSummaryText');
            if (el && summary) el.textContent = summary;
        }
    }

    renderProjects(allSoftwareProjects);
    renderCertificationsTable(allCertifications);

    // 2. Refresco dinámico si se accede mediante servidor web
    try {
        const resProj = await fetch('../../../data/projects.json');
        if (resProj.ok) {
            const json = await resProj.json();
            allSoftwareProjects = (json.projects || []).filter(p => p.category === 'software');
            renderProjects(allSoftwareProjects);
        }
    } catch (_) {}

    try {
        const resCerts = await fetch('../../../data/certifications.json');
        if (resCerts.ok) {
            const json = await resCerts.json();
            allCertifications = (json.certifications || []).filter(c => 
                (c.track || []).includes('software') || (c.track || []).includes('both')
            );
            renderCertificationsTable(allCertifications);
        }
    } catch (_) {}
}

/**
 * Renderiza las tarjetas de proyectos dentro del panel derecho del Explorador.
 * Cada proyecto adopta la apariencia de un fichero de sistema de Windows 97 con preview y detalles.
 * 
 * @param {Array<Object>} projects Lista de proyectos filtrados a renderizar.
 */
function renderProjects(projects) {
    const container = document.getElementById('projectsContainer');
    const statusCell = document.getElementById('projectsCountStatus');
    if (!container) return;

    if (!projects || projects.length === 0) {
        container.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 30px; color: #808080;">
                <p style="font-size: 14px; margin-bottom: 6px;">📂 Carpeta vacía</p>
                <p>No se encontraron proyectos para el criterio seleccionado.</p>
            </div>
        `;
        if (statusCell) statusCell.textContent = '0 objeto(s) en la carpeta';
        return;
    }

    if (statusCell) {
        statusCell.textContent = `${projects.length} objeto(s) en la carpeta (C:\\Proyectos_Software)`;
    }

    container.innerHTML = projects.map(p => `
        <article class="win97-project-card" data-project-id="${p.id}">
            <div>
                <div class="project-card-header">
                    <span>${p.is_private ? '🔒 PRIVADO' : (p.sub_category || 'SISTEMA')}</span>
                    <span>${p.date || '2025-2026'}</span>
                </div>

                ${p.image_svg_badge ? `
                    <div class="project-preview-wrap">
                        ${p.image_svg_badge}
                    </div>
                ` : ''}

                <h3 class="project-card-title">${p.title}</h3>

                <p class="project-card-desc">
                    ${p.description || p.summary_executive || p.tagline}
                </p>

                <div class="project-card-chips">
                    ${(p.tech_stack || []).slice(0, 4).map(t => `<span class="win97-chip">${t}</span>`).join('')}
                </div>
            </div>

            <div class="project-card-actions">
                <button class="win97-btn default-btn" onclick="openProjectProperties('${p.id}')">
                    Propiedades...
                </button>
                ${p.is_private ? `
                    <span class="win97-btn" style="opacity:0.8; cursor:default; font-size:11px; padding:3px 6px; display:inline-flex; align-items:center;" title="Repositorio privado (código disponible bajo solicitud)">
                        🔒 Privado
                    </span>
                ` : (p.links && p.links.github ? `
                    <a href="${p.links.github}" target="_blank" class="win97-btn" style="text-decoration:none; display:flex; align-items:center; justify-content:center;">
                        GitHub
                    </a>
                ` : '')}
            </div>
        </article>
    `).join('');
}

/**
 * Renderiza la base de datos de certificaciones en formato tabla tabular clásica de Windows.
 * 
 * @param {Array<Object>} certs Lista de certificaciones acreditadas.
 */
function renderCertificationsTable(certs) {
    const tbody = document.getElementById('certsTableBody');
    const status = document.getElementById('certsStatusCell');
    if (!tbody) return;

    if (status) status.textContent = `Total registros: ${certs.length}`;

    if (!certs || certs.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" style="text-align: center; color: #808080;">Sin registros</td></tr>`;
        return;
    }

    tbody.innerHTML = certs.map(c => {
        const pdfLink = c.pdf_archive_path
            ? `<a href="../../../${c.pdf_archive_path}" target="_blank" class="win97-table-link" style="color:#000080; font-weight:bold; margin-right:8px;">📄 Ver PDF</a>`
            : '';
        const verifyLink = c.credential_url
            ? `<a href="${c.credential_url}" target="_blank" rel="noopener noreferrer" class="win97-table-link">🔗 Online</a>`
            : '';

        const actionLinks = (pdfLink || verifyLink) ? `${pdfLink} ${verifyLink}` : '—';
        const dblAction = c.pdf_archive_path ? `ondblclick="window.open('../../../${c.pdf_archive_path}', '_blank')"` : '';

        return `
            <tr ${dblAction} style="cursor:pointer;" title="${c.pdf_archive_path ? 'Doble clic para abrir PDF oficial' : ''}">
                <td><strong>${c.institution}</strong></td>
                <td>${c.title}</td>
                <td style="font-family: var(--win-font-mono); font-size: 10px;">${c.issue_date || 'Acreditado'} ${c.score ? `(${c.score})` : ''}</td>
                <td>${actionLinks}</td>
            </tr>
        `;
    }).join('');
}

/**
 * Filtra los proyectos del Explorador según categoría funcional.
 * Actualiza la barra de direcciones y resalta la carpeta activa.
 * 
 * @param {'all'|'ai'|'backend'|'fullstack'} category Categoría seleccionada.
 */
function filterProjects(category) {
    currentFilter = category;

    // Actualizar botones de barra de herramientas
    const btnMap = {
        all: 'btnFilterAll',
        ai: 'btnFilterAI',
        backend: 'btnFilterBackend',
        fullstack: 'btnFilterFullstack'
    };

    ['btnFilterAll', 'btnFilterAI', 'btnFilterBackend', 'btnFilterFullstack'].forEach(id => {
        const btn = document.getElementById(id);
        if (btn) btn.classList.remove('active');
    });

    const activeBtn = document.getElementById(btnMap[category]);
    if (activeBtn) activeBtn.classList.add('active');

    // Actualizar barra de direcciones
    const address = document.getElementById('addressInput');
    if (address) {
        const suffix = category === 'all' ? '' : `\\${category.toUpperCase()}`;
        address.textContent = `C:\\Eduard_Yule\\Proyectos_Software${suffix}`;
    }

    if (category === 'all') {
        renderProjects(allSoftwareProjects);
    } else if (category === 'ai') {
        renderProjects(allSoftwareProjects.filter(p =>
            p.sub_category.toLowerCase().includes('inteligencia') ||
            (p.tech_stack || []).some(t => t.toLowerCase().includes('scikit') || t.toLowerCase().includes('ai'))
        ));
    } else if (category === 'backend') {
        renderProjects(allSoftwareProjects.filter(p =>
            p.sub_category.toLowerCase().includes('backend') ||
            p.sub_category.toLowerCase().includes('datos') ||
            (p.tech_stack || []).some(t => t.toLowerCase().includes('spring') || t.toLowerCase().includes('fastapi') || t.toLowerCase().includes('sql'))
        ));
    } else if (category === 'fullstack') {
        renderProjects(allSoftwareProjects.filter(p =>
            p.sub_category.toLowerCase().includes('full stack') ||
            p.sub_category.toLowerCase().includes('reactivo') ||
            (p.tech_stack || []).some(t => t.toLowerCase().includes('angular') || t.toLowerCase().includes('javascript'))
        ));
    }
}

/**
 * Refresca la vista actual de proyectos.
 */
function refreshProjects() {
    filterProjects(currentFilter);
}

/**
 * Abre el diálogo de Propiedades (inspector) para el proyecto seleccionado.
 * 
 * @param {string} projectId Identificador único del proyecto.
 */
function openProjectProperties(projectId) {
    const project = allSoftwareProjects.find(p => p.id === projectId);
    if (!project) return;

    const modal = document.getElementById('projectModal');
    const content = document.getElementById('modalContentArea');
    const titlebar = document.getElementById('modalTitlebarText');
    const githubBtn = document.getElementById('modalGithubBtn');

    if (titlebar) titlebar.textContent = `Propiedades de: ${project.title}`;

    if (githubBtn) {
        if (project.links && project.links.github) {
            githubBtn.href = project.links.github;
            githubBtn.style.display = 'inline-block';
        } else {
            githubBtn.style.display = 'none';
        }
    }

    if (content) {
        content.innerHTML = `
            <!-- Tab General -->
            <div class="tab-pane active" id="modGeneral">
                <div style="display: flex; gap: 12px; margin-bottom: 10px;">
                    <span style="font-size: 32px;">${project.is_private ? '🔒' : '💾'}</span>
                    <div>
                        <h3 style="color: var(--win-navy); font-size: 13px; font-weight: bold;">${project.title}</h3>
                        <p style="color: #666; font-size: 10px;">ID Sistema: ${project.id.toUpperCase()} • Fecha: ${project.date || '2025-2026'} ${project.is_private ? '• <strong style="color:#b45309;">🔒 Repositorio Privado</strong>' : ''}</p>
                    </div>
                </div>

                ${project.is_private ? `
                    <fieldset class="win97-groupbox" style="margin-bottom: 8px; border-color: #b45309;">
                        <legend style="color: #b45309; font-weight: bold;">🔒 Estado de Confidencialidad</legend>
                        <p style="font-size: 11px; color: #78350f; line-height: 1.4;">
                            <strong>Repositorio Privado / Confidencial.</strong><br>
                            ${project.access_note || 'Código fuente y demostración técnica disponibles bajo solicitud profesional.'}
                        </p>
                    </fieldset>
                ` : ''}

                ${project.image_svg_badge ? `
                    <div style="background: #090d14; border: 1px solid var(--win-gray-dark); margin-bottom: 10px; overflow: hidden;">
                        ${project.image_svg_badge}
                    </div>
                ` : ''}

                <fieldset class="win97-groupbox">
                    <legend>Descripción Ejecutiva</legend>
                    <p style="line-height: 1.4; font-size: 11px;">${project.description}</p>
                </fieldset>

                ${project.metrics ? `
                    <fieldset class="win97-groupbox" style="margin-top: 6px;">
                        <legend>Métricas de Rendimiento</legend>
                        <p style="font-weight: bold; color: #000080;">${project.metrics}</p>
                    </fieldset>
                ` : ''}
            </div>

            <!-- Tab Arquitectura -->
            <div class="tab-pane" id="modArch">
                <fieldset class="win97-groupbox">
                    <legend>Aspectos Clave de Arquitectura</legend>
                    <ul style="padding-left: 18px; line-height: 1.6; font-size: 11px;">
                        ${(project.highlights || []).map(h => `<li>${h}</li>`).join('')}
                    </ul>
                </fieldset>

                ${project.architecture_details ? `
                    <fieldset class="win97-groupbox" style="margin-top: 8px;">
                        <legend>Nota Técnica del Arquitecto</legend>
                        <p style="font-family: var(--win-font-mono); font-size: 10px; color: #003366; line-height: 1.4;">
                            ${project.architecture_details}
                        </p>
                    </fieldset>
                ` : ''}
            </div>

            <!-- Tab Tecnologías -->
            <div class="tab-pane" id="modTech">
                <fieldset class="win97-groupbox">
                    <legend>Dependencias & Pila Técnica</legend>
                    <div style="display: flex; flex-wrap: wrap; gap: 4px; padding: 4px;">
                        ${(project.tech_stack || []).map(t => `
                            <span class="win97-chip" style="font-size: 11px; padding: 3px 6px;">📦 ${t}</span>
                        `).join('')}
                    </div>
                </fieldset>
            </div>
        `;
    }

    if (modal) modal.classList.add('active');
}

/**
 * Cierra el modal de propiedades del proyecto.
 */
function closeProjectModal() {
    const modal = document.getElementById('projectModal');
    if (modal) modal.classList.remove('active');
}

/**
 * Cierra modal al hacer clic en el telón de fondo.
 * @param {Event} e Evento de clic.
 */
function closeModalOnBackdrop(e) {
    if (e.target.id === 'projectModal') {
        closeProjectModal();
    }
}

/**
 * Alterna entre pestañas del diálogo modal de propiedades.
 * 
 * @param {string} paneId Identificador del panel objetivo.
 * @param {HTMLElement} btn Botón que disparó la acción.
 */
function switchModalTab(paneId, btn) {
    const container = btn.closest('.modal-window');
    if (!container) return;

    container.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    container.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
    const target = container.querySelector(`#${paneId}`);
    if (target) target.classList.add('active');
}

/**
 * Alterna entre pestañas de la ventana Mi PC (Perfil).
 * 
 * @param {string} paneId Identificador del panel a mostrar.
 * @param {HTMLElement} btn Botón que disparó la acción.
 */
function switchProfileTab(paneId, btn) {
    const windowEl = document.getElementById('winProfile');
    if (!windowEl) return;

    windowEl.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    windowEl.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
    const target = document.getElementById(paneId);
    if (target) target.classList.add('active');
}

/**
 * Alterna entre Banner y Foto en el Visor Multimedia.
 * 
 * @param {string} displayId Identificador del visor objetivo ('viewBanner'|'viewPhoto').
 * @param {HTMLElement} btn Botón disparador.
 */
function switchViewerTab(displayId, btn) {
    const win = document.getElementById('winViewer');
    if (!win) return;

    win.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    const viewBanner = document.getElementById('viewBanner');
    const viewPhoto = document.getElementById('viewPhoto');

    if (displayId === 'viewBanner') {
        if (viewBanner) viewBanner.style.display = 'block';
        if (viewPhoto) viewPhoto.style.display = 'none';
    } else {
        if (viewBanner) viewBanner.style.display = 'none';
        if (viewPhoto) viewPhoto.style.display = 'block';
    }
}


/* ==========================================================================
   GESTOR DE VENTANAS (ARRIVAR AL FRENTE, MINIMIZAR, MAXIMIZAR, CERRAR)
   ========================================================================== */

/**
 * Abre y enfoca una ventana por su ID.
 * En pantallas móviles (<=768px) autoajusta al tamaño completo de la pantalla.
 * 
 * @param {string} winId ID de la ventana en el DOM.
 */
function openWindow(winId) {
    const win = document.getElementById(winId);
    const tab = document.getElementById(`tab-${winId}`);
    if (!win) return;

    win.classList.remove('hidden-window', 'minimized');
    win.style.removeProperty('display');
    win.style.display = 'flex';
    if (tab) {
        tab.classList.remove('hidden-tab');
        tab.classList.add('active');
    }
    bringToFront(winId);

    if (window.innerWidth <= 768) {
        win.style.top = '0px';
        win.style.left = '0px';
        win.style.width = '100vw';
        win.style.height = 'calc(100vh - var(--taskbar-height))';
        updateWindowDynamicLayout(win, window.innerWidth, window.innerHeight - 44);
    } else {
        const rect = win.getBoundingClientRect();
        if (rect.width && rect.height) {
            updateWindowDynamicLayout(win, rect.width, rect.height);
        }
    }
}

/**
 * Cierra una ventana ocultándola del escritorio y de la barra de tareas.
 * En pantallas móviles remueve las clases activas y garantiza display: none.
 * 
 * @param {string} winId ID de la ventana.
 */
function closeWindow(winId) {
    const win = document.getElementById(winId);
    const tab = document.getElementById(`tab-${winId}`);
    if (win) {
        win.classList.remove('active', 'maximized');
        win.classList.add('hidden-window');
        win.style.setProperty('display', 'none', 'important');
    }
    if (tab) {
        tab.classList.add('hidden-tab');
        tab.classList.remove('active');
    }

    // Transferir foco a la siguiente ventana abierta visible si existe
    const remainingOpenWindows = Array.from(document.querySelectorAll('.win97-window'))
        .filter(w => w.id !== winId && !w.classList.contains('hidden-window') && !w.classList.contains('minimized') && w.style.display !== 'none');
    if (remainingOpenWindows.length > 0) {
        bringToFront(remainingOpenWindows[remainingOpenWindows.length - 1].id);
    }
}

/**
 * Minimiza una ventana ocultándola visualmente pero manteniéndola en la barra de tareas.
 * 
 * @param {string} winId ID de la ventana.
 */
function minimizeWindow(winId) {
    const win = document.getElementById(winId);
    const tab = document.getElementById(`tab-${winId}`);
    if (win) {
        win.classList.remove('active');
        win.classList.add('minimized');
        win.style.setProperty('display', 'none', 'important');
    }
    if (tab) {
        tab.classList.remove('active');
    }

    // Transferir foco a la siguiente ventana abierta si existe
    const remainingOpenWindows = Array.from(document.querySelectorAll('.win97-window'))
        .filter(w => w.id !== winId && !w.classList.contains('hidden-window') && !w.classList.contains('minimized') && w.style.display !== 'none');
    if (remainingOpenWindows.length > 0) {
        bringToFront(remainingOpenWindows[remainingOpenWindows.length - 1].id);
    }
}

/**
 * Alterna el estado maximizado / restaurado de una ventana.
 * 
 * @param {string} winId ID de la ventana.
 */
function maximizeWindow(winId) {
    const win = document.getElementById(winId);
    if (!win) return;

    if (win.classList.contains('maximized')) {
        // Restaurar estado anterior
        const st = windowStates[winId] || { top: '50px', left: '100px', width: '640px', height: '480px' };
        win.classList.remove('maximized');
        win.style.top = st.top;
        win.style.left = st.left;
        win.style.width = st.width;
        win.style.height = st.height;
        updateWindowDynamicLayout(win, parseFloat(st.width) || 640, parseFloat(st.height) || 480);
    } else {
        // Guardar estado actual y maximizar
        windowStates[winId] = {
            top: win.style.top,
            left: win.style.left,
            width: win.style.width,
            height: win.style.height
        };
        win.classList.add('maximized');
        win.style.top = '0px';
        win.style.left = '0px';
        win.style.width = '100vw';
        win.style.height = 'calc(100vh - var(--taskbar-height))';
        const desktop = document.getElementById('desktop') || document.body;
        updateWindowDynamicLayout(win, desktop.clientWidth, desktop.clientHeight);
    }
    bringToFront(winId);
}

/**
 * Trae una ventana al frente incrementando el z-index global y actualizando el estilo de foco.
 * 
 * @param {string} winId ID de la ventana.
 */
function bringToFront(winId) {
    const win = document.getElementById(winId);
    if (!win) return;

    highestZIndex += 1;
    win.style.zIndex = highestZIndex;

    // Desactivar todas las demás ventanas
    document.querySelectorAll('.win97-window').forEach(w => w.classList.remove('active'));
    win.classList.add('active');
    win.classList.remove('hidden-window', 'minimized');
    win.style.removeProperty('display');
    win.style.display = 'flex';

    // Sincronizar botones de la barra de tareas
    document.querySelectorAll('.taskbar-tab').forEach(t => t.classList.remove('active'));
    const tab = document.getElementById(`tab-${winId}`);
    if (tab) {
        tab.classList.remove('hidden-tab');
        tab.classList.add('active');
    }
}

/**
 * Alterna el estado de una ventana al hacer clic en su pestaña de la barra de tareas.
 * 
 * @param {string} winId ID de la ventana.
 */
function toggleWindowFromTaskbar(winId) {
    const win = document.getElementById(winId);
    if (!win) return;

    if (win.style.display === 'none' || win.classList.contains('minimized') || win.classList.contains('hidden-window')) {
        openWindow(winId);
    } else if (win.classList.contains('active')) {
        minimizeWindow(winId);
    } else {
        bringToFront(winId);
    }
}


/* ==========================================================================
   MOTOR DE ARRASTRE DE VENTANAS (DRAG & DROP)
   ========================================================================== */

/**
 * Inicializa el soporte para arrastrar ventanas mediante puntero (ratón o touch).
 * Aplica restricciones para mantener las ventanas dentro del área visible del escritorio.
 */
function initDraggableWindows() {
    const windows = document.querySelectorAll('.win97-window');

    windows.forEach(win => {
        const handle = win.querySelector('[data-drag-handle]');
        if (!handle) return;

        // Clic en cualquier parte de la ventana la trae al frente
        win.addEventListener('pointerdown', () => {
            bringToFront(win.id);
        });

        let isDragging = false;
        let startX = 0;
        let startY = 0;
        let initialLeft = 0;
        let initialTop = 0;

        handle.addEventListener('pointerdown', (e) => {
            // Ignorar si se hizo clic en los botones de control
            if (e.target.closest('.win97-btn-box')) return;
            if (window.innerWidth <= 768 || win.classList.contains('maximized')) return;

            isDragging = true;
            startX = e.clientX;
            startY = e.clientY;

            const rect = win.getBoundingClientRect();
            initialLeft = rect.left;
            initialTop = rect.top;

            handle.setPointerCapture(e.pointerId);
            bringToFront(win.id);
        });

        handle.addEventListener('pointermove', (e) => {
            if (!isDragging) return;

            const dx = e.clientX - startX;
            const dy = e.clientY - startY;

            let newLeft = initialLeft + dx;
            let newTop = initialTop + dy;

            // Restringir a los bordes del escritorio
            const desktop = document.getElementById('desktop') || document.body;
            const dw = desktop.clientWidth;
            const dh = desktop.clientHeight;
            const maxLeft = dw - 60;
            const maxTop = dh - 60;

            newLeft = Math.max(0, Math.min(newLeft, maxLeft));
            newTop = Math.max(0, Math.min(newTop, maxTop));

            win.style.left = `${newLeft}px`;
            win.style.top = `${newTop}px`;

            // Verificación de Snap Magnético a bordes con previsualización
            const snapGhost = document.getElementById('snapPreview');
            const snapThreshold = 22;
            pendingSnapAction = null;

            if (e.clientY <= snapThreshold) {
                // Ajustar a pantalla completa
                pendingSnapAction = { type: 'maximize', winId: win.id };
                if (snapGhost) {
                    snapGhost.style.left = '2px';
                    snapGhost.style.top = '2px';
                    snapGhost.style.width = `${dw - 4}px`;
                    snapGhost.style.height = `${dh - 4}px`;
                    snapGhost.classList.add('active');
                }
            } else if (e.clientX <= snapThreshold) {
                // Ajustar a mitad izquierda
                pendingSnapAction = { type: 'left', winId: win.id };
                if (snapGhost) {
                    snapGhost.style.left = '2px';
                    snapGhost.style.top = '2px';
                    snapGhost.style.width = `${Math.floor(dw / 2) - 4}px`;
                    snapGhost.style.height = `${dh - 4}px`;
                    snapGhost.classList.add('active');
                }
            } else if (e.clientX >= dw - snapThreshold) {
                // Ajustar a mitad derecha
                pendingSnapAction = { type: 'right', winId: win.id };
                if (snapGhost) {
                    snapGhost.style.left = `${Math.floor(dw / 2) + 2}px`;
                    snapGhost.style.top = '2px';
                    snapGhost.style.width = `${Math.floor(dw / 2) - 4}px`;
                    snapGhost.style.height = `${dh - 4}px`;
                    snapGhost.classList.add('active');
                }
            } else {
                if (snapGhost) snapGhost.classList.remove('active');
            }
        });

        const stopDrag = (e) => {
            if (isDragging) {
                isDragging = false;
                try {
                    handle.releasePointerCapture(e.pointerId);
                } catch (_) {}

                const snapGhost = document.getElementById('snapPreview');
                if (snapGhost) snapGhost.classList.remove('active');

                // Aplicar Snap pendiente
                if (pendingSnapAction && pendingSnapAction.winId === win.id) {
                    const desktop = document.getElementById('desktop') || document.body;
                    const dw = desktop.clientWidth;
                    const dh = desktop.clientHeight;

                    if (pendingSnapAction.type === 'maximize') {
                        maximizeWindow(win.id);
                    } else if (pendingSnapAction.type === 'left') {
                        win.classList.remove('maximized');
                        const targetW = Math.floor(dw / 2) - 4;
                        const targetH = dh - 4;
                        win.style.left = '2px';
                        win.style.top = '2px';
                        win.style.width = `${targetW}px`;
                        win.style.height = `${targetH}px`;
                        updateWindowDynamicLayout(win, targetW, targetH);
                    } else if (pendingSnapAction.type === 'right') {
                        win.classList.remove('maximized');
                        const targetW = Math.floor(dw / 2) - 4;
                        const targetH = dh - 4;
                        win.style.left = `${Math.floor(dw / 2) + 2}px`;
                        win.style.top = '2px';
                        win.style.width = `${targetW}px`;
                        win.style.height = `${targetH}px`;
                        updateWindowDynamicLayout(win, targetW, targetH);
                    }
                    pendingSnapAction = null;
                }
            }
        };

        handle.addEventListener('pointerup', stopDrag);
        handle.addEventListener('pointercancel', stopDrag);
    });
}


/* ==========================================================================
   ICONOS DEL ESCRITORIO
   ========================================================================== */

/**
 * Inicializa los eventos de selección y doble clic para los iconos del escritorio.
 */
function initDesktopIcons() {
    const icons = document.querySelectorAll('.desktop-icon');

    icons.forEach(icon => {
        // Selección al hacer clic simple (y abrir inmediatamente en móvil)
        icon.addEventListener('click', (e) => {
            icons.forEach(i => i.classList.remove('active-icon'));
            icon.classList.add('active-icon');

            if (window.innerWidth <= 768) {
                const winTarget = icon.getAttribute('data-window');
                if (winTarget) {
                    openWindow(winTarget);
                }
            }
        });

        // Doble clic abre la ventana asociada
        icon.addEventListener('dblclick', () => {
            const winTarget = icon.getAttribute('data-window');
            if (winTarget) {
                openWindow(winTarget);
            }
        });

        // Soporte táctil / tecla Enter
        icon.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                const winTarget = icon.getAttribute('data-window');
                if (winTarget) openWindow(winTarget);
            }
        });
    });
}


/* ==========================================================================
   MENÚ INICIO & DIÁLOGOS RETRO
   ========================================================================== */

/**
 * Alterna la visibilidad del Menú Inicio clásico de Windows 97.
 */
function toggleStartMenu() {
    const menu = document.getElementById('startMenu');
    const btn = document.getElementById('startButton');
    if (!menu || !btn) return;

    menu.classList.toggle('active');
    btn.classList.toggle('active');
}

/**
 * Cierra menús contextuales al hacer clic fuera de ellos.
 */
function initClickOutside() {
    document.addEventListener('click', (e) => {
        const startMenu = document.getElementById('startMenu');
        const startBtn = document.getElementById('startButton');

        if (startMenu && startMenu.classList.contains('active')) {
            if (!startMenu.contains(e.target) && !startBtn.contains(e.target)) {
                startMenu.classList.remove('active');
                startBtn.classList.remove('active');
            }
        }
    });
}

/**
 * Alterna el fondo de pantalla del escritorio entre paletas icónicas de la era 90s.
 */
function toggleDesktopWallpaper() {
    const themes = ['theme-classic-teal', 'theme-clouds', 'theme-slate', 'theme-matrix'];
    const currentTheme = themes.find(t => document.body.classList.contains(t)) || 'theme-classic-teal';
    const nextIndex = (themes.indexOf(currentTheme) + 1) % themes.length;

    themes.forEach(t => document.body.classList.remove(t));
    document.body.classList.add(themes[nextIndex]);
}

/**
 * Muestra el diálogo clásico "Acerca de Windows / Eduard Criollo Yule".
 */
function showAboutDialog() {
    alert(
        "Microsoft Windows 97 Professional\n" +
        "Portafolio Arquitectónico de Eduard Criollo Yule\n\n" +
        "• Especialidad: Full Stack Developer & AI Specialist\n" +
        "• Dominio: Spring Boot, Angular, FastAPI, Machine Learning\n" +
        "• Idioma: Inglés C1 CEFR (Oxford University Press)\n" +
        "• Universidad Autónoma de Occidente • Cali, Colombia\n\n" +
        "Copyright © 2026 Eduard Criollo Yule. Todos los derechos reservados."
    );
}

/**
 * Muestra el diálogo clásico de confirmación de apagado.
 */
function showShutdownDialog() {
    const ok = confirm("¿Desea apagar el sistema y regresar al Portal Principal de Software?");
    if (ok) {
        window.location.href = '../../../index.html';
    }
}


/* ==========================================================================
   MOTOR DE REDIMENSIONAMIENTO LIBRE & AUTODISPOSICIÓN DE VENTANAS
   ========================================================================== */

let pendingSnapAction = null; // 'left' | 'right' | 'top' | null

/**
 * Adapta dinámicamente las propiedades de texto, escala tipográfica, espaciado y
 * límites verticales de las ventanas en función de sus dimensiones de alto y ancho reales.
 * 
 * @param {HTMLElement} win Elemento de la ventana.
 * @param {number} [width] Ancho actual en px.
 * @param {number} [height] Alto actual en px.
 */
function updateWindowDynamicLayout(win, width, height) {
    if (!win) return;

    // En pantallas táctiles o móviles, fijar escala legible sin recorte forzado
    if (window.innerWidth <= 768) {
        win.style.setProperty('--win-w', '100vw');
        win.style.setProperty('--win-h', 'calc(100vh - var(--taskbar-height))');
        win.style.setProperty('--win-scale', '1');
        win.style.setProperty('--win-font-base', '12px');
        win.style.setProperty('--win-font-sm', '10.5px');
        win.style.setProperty('--win-font-lg', '13.5px');
        win.style.setProperty('--win-line-height', '1.45');
        win.style.setProperty('--project-desc-lines', '8');
        return;
    }

    const w = width || win.offsetWidth;
    const h = height || win.offsetHeight;
    if (!w || !h) return;

    // Factor de escala armónico considerando tanto ancho como alto
    const scaleW = w / 640;
    const scaleH = h / 450;
    const scale = Math.min(1.3, Math.max(0.85, (scaleW * 0.45 + scaleH * 0.55)));

    const baseFontSize = (11 * scale).toFixed(1);
    const smFontSize = (10 * scale).toFixed(1);
    const lgFontSize = (12 * scale).toFixed(1);
    const lineHeight = (1.4 * Math.min(1.25, Math.max(0.9, scaleH))).toFixed(2);

    // Cantidad de líneas permitidas en descripciones antes de recorte según altura
    let descLines = 3;
    if (h >= 620) descLines = 8;
    else if (h >= 500) descLines = 5;
    else if (h >= 400) descLines = 3;
    else descLines = 2;

    win.style.setProperty('--win-w', `${w}px`);
    win.style.setProperty('--win-h', `${h}px`);
    win.style.setProperty('--win-scale', scale.toFixed(3));
    win.style.setProperty('--win-font-base', `${baseFontSize}px`);
    win.style.setProperty('--win-font-sm', `${smFontSize}px`);
    win.style.setProperty('--win-font-lg', `${lgFontSize}px`);
    win.style.setProperty('--win-line-height', lineHeight);
    win.style.setProperty('--project-desc-lines', descLines);
}

/**
 * Inicializa tiradores interactivos de redimensionamiento (8 direcciones) en cada ventana.
 * Permite al usuario estirar y redimensionar libremente desde cualquier borde o esquina.
 */
function initResizableWindows() {
    const windows = document.querySelectorAll('.win97-window');
    const directions = ['t', 'b', 'l', 'r', 'tl', 'tr', 'bl', 'br'];

    windows.forEach(win => {
        // Inicializar escala y variables dinámicas
        const rectInit = win.getBoundingClientRect();
        if (rectInit.width && rectInit.height) {
            updateWindowDynamicLayout(win, rectInit.width, rectInit.height);
        }

        // Evitar duplicar resizers si ya existen
        if (win.querySelector('.win97-resizer')) return;

        directions.forEach(dir => {
            const resizer = document.createElement('div');
            resizer.className = `win97-resizer resizer-${dir}`;
            resizer.setAttribute('data-direction', dir);
            win.appendChild(resizer);

            resizer.addEventListener('pointerdown', (e) => {
                if (window.innerWidth <= 768 || win.classList.contains('maximized')) return;
                e.stopPropagation();

                bringToFront(win.id);
                document.body.classList.add('is-resizing');

                const rect = win.getBoundingClientRect();
                const startX = e.clientX;
                const startY = e.clientY;
                const startWidth = rect.width;
                const startHeight = rect.height;
                const startLeft = rect.left;
                const startTop = rect.top;

                const minW = 320;
                const minH = 200;
                const desktop = document.getElementById('desktop') || document.body;
                const maxW = desktop.clientWidth;
                const maxH = desktop.clientHeight;

                resizer.setPointerCapture(e.pointerId);

                const onPointerMove = (moveEvt) => {
                    const dx = moveEvt.clientX - startX;
                    const dy = moveEvt.clientY - startY;

                    let currentW = startWidth;
                    let currentH = startHeight;

                    // Ajuste horizontal
                    if (dir.includes('r')) {
                        const newWidth = Math.max(minW, Math.min(startWidth + dx, maxW - startLeft));
                        win.style.width = `${newWidth}px`;
                        currentW = newWidth;
                    } else if (dir.includes('l')) {
                        const newWidth = Math.max(minW, startWidth - dx);
                        if (newWidth > minW || dx < 0) {
                            const newLeft = Math.max(0, startLeft + (startWidth - newWidth));
                            win.style.width = `${newWidth}px`;
                            win.style.left = `${newLeft}px`;
                            currentW = newWidth;
                        }
                    }

                    // Ajuste vertical
                    if (dir.includes('b')) {
                        const newHeight = Math.max(minH, Math.min(startHeight + dy, maxH - startTop));
                        win.style.height = `${newHeight}px`;
                        currentH = newHeight;
                    } else if (dir.includes('t')) {
                        const newHeight = Math.max(minH, startHeight - dy);
                        if (newHeight > minH || dy < 0) {
                            const newTop = Math.max(0, startTop + (startHeight - newHeight));
                            win.style.height = `${newHeight}px`;
                            win.style.top = `${newTop}px`;
                            currentH = newHeight;
                        }
                    }

                    // Autoajuste dinámico de texto y estructura vertical en tiempo real
                    updateWindowDynamicLayout(win, currentW, currentH);
                };

                const onPointerUp = (upEvt) => {
                    document.body.classList.remove('is-resizing');
                    try {
                        resizer.releasePointerCapture(upEvt.pointerId);
                    } catch (_) {}
                    resizer.removeEventListener('pointermove', onPointerMove);
                    resizer.removeEventListener('pointerup', onPointerUp);
                    resizer.removeEventListener('pointercancel', onPointerUp);
                };

                resizer.addEventListener('pointermove', onPointerMove);
                resizer.addEventListener('pointerup', onPointerUp);
                resizer.addEventListener('pointercancel', onPointerUp);
            });
        });
    });
}

/**
 * Inicializa escuchadores para Autoajuste y Snapping magnético a los bordes de la pantalla.
 */
function initWindowSnappingAndLayouts() {
    // 1. Doble clic en titlebar para maximizar/restaurar
    document.querySelectorAll('.win97-titlebar').forEach(tb => {
        tb.addEventListener('dblclick', (e) => {
            if (e.target.closest('.win97-btn-box')) return;
            const win = tb.closest('.win97-window');
            if (win) maximizeWindow(win.id);
        });
    });

    // 2. Clic derecho en el escritorio o barra de tareas para abrir menú contextual
    const taskbar = document.querySelector('.win97-taskbar');
    const desktop = document.getElementById('desktop');

    if (taskbar) {
        taskbar.addEventListener('contextmenu', (e) => {
            if (e.target.closest('.taskbar-tab') || e.target.closest('.start-button')) return;
            e.preventDefault();
            openTaskbarContextMenu(e.clientX, e.clientY);
        });
    }

    if (desktop) {
        desktop.addEventListener('contextmenu', (e) => {
            if (e.target.closest('.win97-window') || e.target.closest('.desktop-icon')) return;
            e.preventDefault();
            openTaskbarContextMenu(e.clientX, e.clientY);
        });
    }

    // 3. Autoajuste responsivo al cambiar tamaño de la pantalla
    window.addEventListener('resize', debounceAutoAdjustWindows, 150);
}

/**
 * Muestra el menú contextual de disposición de ventanas en coordenadas de pantalla.
 */
function openTaskbarContextMenu(x, y) {
    const menu = document.getElementById('taskbarContextMenu');
    if (!menu) return;

    // Calcular límites para que no desborde la pantalla
    const menuWidth = 210;
    const menuHeight = 190;
    const maxX = window.innerWidth - menuWidth - 5;
    const maxY = window.innerHeight - menuHeight - 35;

    const posX = Math.max(5, Math.min(x, maxX));
    const posY = Math.max(5, Math.min(y, maxY));

    menu.style.left = `${posX}px`;
    menu.style.top = `${posY}px`;
    menu.classList.add('active');
}

/**
 * Alterna el menú contextual desde el botón Organizar en la barra de tareas.
 */
function toggleTaskbarContextMenu(e) {
    e.stopPropagation();
    const menu = document.getElementById('taskbarContextMenu');
    const btn = document.getElementById('btnWindowLayouts');
    if (!menu) return;

    if (menu.classList.contains('active')) {
        menu.classList.remove('active');
        if (btn) btn.classList.remove('active');
    } else {
        const rect = btn.getBoundingClientRect();
        openTaskbarContextMenu(rect.left, rect.top - 195);
        if (btn) btn.classList.add('active');
    }
}

/**
 * Cierra el menú contextual al hacer clic fuera.
 */
document.addEventListener('click', (e) => {
    const menu = document.getElementById('taskbarContextMenu');
    const btn = document.getElementById('btnWindowLayouts');
    if (menu && menu.classList.contains('active')) {
        if (!menu.contains(e.target) && (!btn || !btn.contains(e.target))) {
            menu.classList.remove('active');
            if (btn) btn.classList.remove('active');
        }
    }
});

/**
 * Obtiene todas las ventanas visibles actualmente en el escritorio.
 * @returns {Array<HTMLElement>}
 */
function getVisibleWindows() {
    return Array.from(document.querySelectorAll('.win97-window')).filter(w =>
        w.style.display !== 'none' && !w.classList.contains('minimized')
    );
}

/**
 * Dispone todas las ventanas abiertas en Cascada clásica de Windows 97.
 */
function cascadeWindows() {
    const menu = document.getElementById('taskbarContextMenu');
    if (menu) menu.classList.remove('active');

    let wins = getVisibleWindows();
    if (wins.length === 0) {
        openWindow('winProfile');
        openWindow('winProjects');
        wins = getVisibleWindows();
    }

    const desktop = document.getElementById('desktop') || document.body;
    const dw = desktop.clientWidth;
    const dh = desktop.clientHeight;

    const targetW = Math.max(380, Math.min(680, Math.floor(dw * 0.72)));
    const targetH = Math.max(260, Math.min(480, Math.floor(dh * 0.70)));

    wins.forEach((w, idx) => {
        w.classList.remove('maximized');
        const offset = 26 * idx;
        const left = Math.min(25 + offset, dw - targetW - 10);
        const top = Math.min(20 + offset, dh - targetH - 10);

        w.style.left = `${Math.max(10, left)}px`;
        w.style.top = `${Math.max(10, top)}px`;
        w.style.width = `${targetW}px`;
        w.style.height = `${targetH}px`;
        bringToFront(w.id);
        updateWindowDynamicLayout(w, targetW, targetH);
    });
}

/**
 * Dispone las ventanas abiertas en Mosaico Horizontal (apiladas verticalmente en renglones).
 */
function tileWindowsHorizontally() {
    const menu = document.getElementById('taskbarContextMenu');
    if (menu) menu.classList.remove('active');

    let wins = getVisibleWindows();
    if (wins.length === 0) {
        openWindow('winProfile');
        openWindow('winProjects');
        wins = getVisibleWindows();
    }

    const desktop = document.getElementById('desktop') || document.body;
    const dw = desktop.clientWidth;
    const dh = desktop.clientHeight;
    const count = wins.length;
    const rowH = Math.floor(dh / count);

    wins.forEach((w, idx) => {
        w.classList.remove('maximized');
        w.style.left = '4px';
        w.style.top = `${idx * rowH + 2}px`;
        w.style.width = `${dw - 8}px`;
        w.style.height = `${rowH - 4}px`;
        updateWindowDynamicLayout(w, dw - 8, rowH - 4);
    });
}

/**
 * Dispone las ventanas abiertas en Mosaico Vertical (columnas paralelas lado a lado).
 */
function tileWindowsVertically() {
    const menu = document.getElementById('taskbarContextMenu');
    if (menu) menu.classList.remove('active');

    let wins = getVisibleWindows();
    if (wins.length === 0) {
        openWindow('winProfile');
        openWindow('winProjects');
        wins = getVisibleWindows();
    }

    const desktop = document.getElementById('desktop') || document.body;
    const dw = desktop.clientWidth;
    const dh = desktop.clientHeight;
    const count = wins.length;
    const colW = Math.floor(dw / count);

    wins.forEach((w, idx) => {
        w.classList.remove('maximized');
        w.style.left = `${idx * colW + 2}px`;
        w.style.top = '4px';
        w.style.width = `${colW - 4}px`;
        w.style.height = `${dh - 8}px`;
        updateWindowDynamicLayout(w, colW - 4, dh - 8);
    });
}

/**
 * Autoajusta la ventana activa al centro de la pantalla con dimensiones óptimas.
 */
function autoFitActiveWindow() {
    const menu = document.getElementById('taskbarContextMenu');
    if (menu) menu.classList.remove('active');

    const activeWin = document.querySelector('.win97-window.active') || getVisibleWindows()[0];
    if (!activeWin) {
        openWindow('winProjects');
        return;
    }

    const desktop = document.getElementById('desktop') || document.body;
    const dw = desktop.clientWidth;
    const dh = desktop.clientHeight;

    const optW = Math.max(340, Math.min(840, Math.floor(dw * 0.78)));
    const optH = Math.max(260, Math.min(540, Math.floor(dh * 0.75)));

    activeWin.classList.remove('maximized');
    activeWin.style.width = `${optW}px`;
    activeWin.style.height = `${optH}px`;
    activeWin.style.left = `${Math.floor((dw - optW) / 2)}px`;
    activeWin.style.top = `${Math.floor((dh - optH) / 2)}px`;
    bringToFront(activeWin.id);
    updateWindowDynamicLayout(activeWin, optW, optH);
}

/**
 * Minimiza todas las ventanas visibles para mostrar el escritorio limpio.
 */
function minimizeAllWindows() {
    const menu = document.getElementById('taskbarContextMenu');
    if (menu) menu.classList.remove('active');

    getVisibleWindows().forEach(w => minimizeWindow(w.id));
}

/**
 * Restaura todas las ventanas abiertas en la barra de tareas.
 */
function restoreAllWindows() {
    const menu = document.getElementById('taskbarContextMenu');
    if (menu) menu.classList.remove('active');

    document.querySelectorAll('.taskbar-tab:not(.hidden-tab)').forEach(tab => {
        const winId = tab.id.replace('tab-', '');
        openWindow(winId);
    });
}

/**
 * Evita desbordamiento de ventanas cuando se modifica la resolución del navegador.
 */
function debounceAutoAdjustWindows() {
    const desktop = document.getElementById('desktop');
    if (!desktop) return;
    const dw = desktop.clientWidth;
    const dh = desktop.clientHeight;

    if (window.innerWidth <= 768) {
        document.querySelectorAll('.win97-window').forEach(w => {
            if (w.style.display !== 'none') {
                w.style.top = '0px';
                w.style.left = '0px';
                w.style.width = '100vw';
                w.style.height = 'calc(100vh - var(--taskbar-height))';
                updateWindowDynamicLayout(w, dw, dh);
            }
        });
        return;
    }

    document.querySelectorAll('.win97-window').forEach(w => {
        if (w.classList.contains('maximized')) {
            updateWindowDynamicLayout(w, dw, dh);
            return;
        }
        const rect = w.getBoundingClientRect();
        if (rect.right > dw) {
            const newLeft = Math.max(0, dw - rect.width - 10);
            w.style.left = `${newLeft}px`;
        }
        if (rect.bottom > dh) {
            const newTop = Math.max(0, dh - rect.height - 10);
            w.style.top = `${newTop}px`;
        }
        updateWindowDynamicLayout(w, rect.width, rect.height);
    });
}
