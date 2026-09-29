#!/usr/bin/env python3
"""
tools/upgrade_option_tron.py
============================
Upgrades option_tron (Windows 97 portfolio) with:
1. 8-direction free window resizing with pointer capture & retro bottom-right grip.
2. Edge snapping (Aero/retro snap) to left-half, right-half, and maximize with visual ghost preview.
3. Auto-adjustment window commands:
   - Cascade windows (Ventanas en cascada)
   - Tile horizontally (Mosaico horizontal)
   - Tile vertically (Mosaico vertical)
   - Auto-fit active window (Autoajuste óptimo)
   - Minimize/Restore all windows
4. Taskbar layout button & Desktop/Taskbar context menu.
5. Double-click titlebar to toggle maximize.
6. Viewport resize auto-adjustment so windows never overflow off-screen.
"""

from pathlib import Path
import re

WORKSPACE = Path("f:/Calipso_Online/03_Profesional/Cv/01_Software_Dev/portfolio/option_tron")
HTML_FILE = WORKSPACE / "index.html"
CSS_FILE = WORKSPACE / "style.css"
JS_FILE = WORKSPACE / "app.js"

def upgrade_css():
    with open(CSS_FILE, "r", encoding="utf-8") as f:
        css = f.read()

    new_styles = """
/* ==========================================================================
   WINDOW RESIZING, AUTO-ADJUSTMENT & RETRO CONTROLS (ENHANCED DYNAMICS)
   ========================================================================== */

/* Tiradores de Redimensionamiento Libre (8 Direcciones) */
.win97-resizer {
    position: absolute;
    z-index: 30;
    touch-action: none;
}
.win97-resizer.resizer-t { top: 0; left: 8px; right: 8px; height: 6px; cursor: n-resize; }
.win97-resizer.resizer-b { bottom: 0; left: 8px; right: 8px; height: 6px; cursor: s-resize; }
.win97-resizer.resizer-l { left: 0; top: 8px; bottom: 8px; width: 6px; cursor: w-resize; }
.win97-resizer.resizer-r { right: 0; top: 8px; bottom: 8px; width: 6px; cursor: e-resize; }
.win97-resizer.resizer-tl { top: 0; left: 0; width: 12px; height: 12px; cursor: nw-resize; }
.win97-resizer.resizer-tr { top: 0; right: 0; width: 12px; height: 12px; cursor: ne-resize; }
.win97-resizer.resizer-bl { bottom: 0; left: 0; width: 12px; height: 12px; cursor: sw-resize; }
.win97-resizer.resizer-br {
    bottom: 0;
    right: 0;
    width: 16px;
    height: 16px;
    cursor: se-resize;
}

/* Textura diagonal retro de agarre en la esquina inferior derecha */
.win97-resizer.resizer-br::after {
    content: '';
    position: absolute;
    right: 2px;
    bottom: 2px;
    width: 10px;
    height: 10px;
    background: repeating-linear-gradient(
        -45deg,
        var(--win-gray-dark) 0px,
        var(--win-gray-dark) 1px,
        transparent 1px,
        transparent 3px,
        var(--win-white) 3px,
        var(--win-white) 4px
    );
    pointer-events: none;
}

.win97-window.maximized .win97-resizer {
    display: none !important;
}

/* Indicador Fantasma de Autoajuste / Snapping a bordes */
.win97-snap-preview {
    position: absolute;
    display: none;
    border: 2px dashed #ffffff;
    background: rgba(0, 0, 128, 0.28);
    backdrop-filter: blur(2px);
    z-index: 998;
    pointer-events: none;
    box-shadow: 0 0 12px rgba(0, 0, 0, 0.45);
    transition: all 0.12s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.win97-snap-preview.active {
    display: block;
}

/* Botón de Organización de Ventanas en la Barra de Tareas */
.taskbar-btn-layout {
    background: var(--win-gray);
    border: 2px solid;
    border-color: var(--win-white) var(--win-black) var(--win-black) var(--win-white);
    box-shadow: inset 1px 1px 0 var(--win-gray-light), inset -1px -1px 0 var(--win-gray-dark);
    font-family: var(--win-font);
    font-size: 11px;
    font-weight: bold;
    padding: 2px 7px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    cursor: pointer;
    flex-shrink: 0;
    margin-right: 6px;
    user-select: none;
    color: var(--win-black);
}
.taskbar-btn-layout:active,
.taskbar-btn-layout.active {
    border-color: var(--win-black) var(--win-white) var(--win-white) var(--win-black);
    box-shadow: inset 1px 1px 0 var(--win-black);
    background: var(--win-gray-light);
}

/* Menú Contextual Clásico de Windows 97 */
.win97-context-menu {
    position: fixed;
    display: none;
    background-color: var(--win-gray);
    border: 2px solid;
    border-color: var(--win-white) var(--win-black) var(--win-black) var(--win-white);
    box-shadow: inset 1px 1px 0 var(--win-gray-light), inset -1px -1px 0 var(--win-gray-dark), 3px 3px 10px rgba(0,0,0,0.5);
    z-index: 9999;
    min-width: 200px;
    padding: 2px;
    font-family: var(--win-font);
    font-size: 11px;
    user-select: none;
}
.win97-context-menu.active {
    display: block;
}
.context-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 4px 14px 4px 8px;
    cursor: pointer;
    color: var(--win-black);
}
.context-item:hover {
    background-color: var(--win-blue-sel);
    color: var(--win-text-sel);
}
.context-divider {
    height: 1px;
    background: var(--win-gray-dark);
    border-bottom: 1px solid var(--win-white);
    margin: 4px 2px;
}
.context-icon {
    font-size: 13px;
    width: 16px;
    text-align: center;
}

/* Evitar selección de texto durante redimensionado activo */
body.is-resizing {
    user-select: none !important;
}
body.is-resizing iframe,
body.is-resizing object {
    pointer-events: none !important;
}
"""

    if "WINDOW RESIZING, AUTO-ADJUSTMENT" not in css:
        css = css + "\n" + new_styles
        with open(CSS_FILE, "w", encoding="utf-8") as f:
            f.write(css)
        print("Updated style.css with resizer and layout styles.")

def upgrade_html():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Add snap preview element inside #desktop
    if 'id="snapPreview"' not in html:
        html = html.replace('<div class="desktop" id="desktop">',
                            '<div class="desktop" id="desktop">\n\n        <!-- CONTORNO FANTASMA PARA AUTOSNAPPING -->\n        <div class="win97-snap-preview" id="snapPreview"></div>')

    # 2. Add layout button in taskbar before system-tray
    old_taskbar_tail = """        <!-- Área de notificación / Reloj del sistema -->
        <div class="system-tray">"""

    new_taskbar_tail = """        <!-- Botón de Autoajuste y Disposición de Ventanas -->
        <button class="taskbar-btn-layout" id="btnWindowLayouts" onclick="toggleTaskbarContextMenu(event)" title="Organizar y Autoajustar Ventanas (Cascada, Mosaico, Autoajuste)">
            <span>📐</span>
            <span>Organizar</span>
        </button>

        <!-- Área de notificación / Reloj del sistema -->
        <div class="system-tray">"""

    if "btnWindowLayouts" not in html:
        html = html.replace(old_taskbar_tail, new_taskbar_tail)

    # 3. Add context menu before </body>
    context_menu_html = """
    <!-- MENÚ CONTEXTUAL PARA AUTODISPOSICIÓN DE VENTANAS (TASKBAR & DESKTOP) -->
    <div class="win97-context-menu" id="taskbarContextMenu">
        <div class="context-item" onclick="cascadeWindows()">
            <span class="context-icon">🗔</span>
            <span>Ventanas en <u>c</u>ascada</span>
        </div>
        <div class="context-item" onclick="tileWindowsHorizontally()">
            <span class="context-icon">🗖</span>
            <span>Mosaico <u>h</u>orizontal</span>
        </div>
        <div class="context-item" onclick="tileWindowsVertically()">
            <span class="context-icon">🗗</span>
            <span>Mosaico <u>v</u>ertical</span>
        </div>
        <div class="context-item" onclick="autoFitActiveWindow()">
            <span class="context-icon">📐</span>
            <span><u>A</u>utoajustar ventana activa</span>
        </div>
        <div class="context-divider"></div>
        <div class="context-item" onclick="minimizeAllWindows()">
            <span class="context-icon">🗕</span>
            <span><u>M</u>inimizar todas las ventanas</span>
        </div>
        <div class="context-item" onclick="restoreAllWindows()">
            <span class="context-icon">🗖</span>
            <span><u>R</u>estaurar todas las ventanas</span>
        </div>
    </div>
"""
    if "taskbarContextMenu" not in html:
        html = html.replace('</body>', context_menu_html + '\n</body>')

    # 4. Add "Organizar Ventanas" option in Start Menu
    start_menu_target = """            <div class="start-item" onclick="toggleDesktopWallpaper(); toggleStartMenu();">
                <span class="start-icon icon-settings-mini"></span>
                <span class="start-label">Cambiar <u>F</u>ondo...</span>
            </div>"""

    new_start_menu_item = """            <div class="start-item" onclick="toggleTaskbarContextMenu(event); toggleStartMenu();">
                <span class="start-icon icon-settings-mini"></span>
                <span class="start-label">📐 <u>O</u>rganizar Ventanas...</span>
            </div>
            <div class="start-item" onclick="toggleDesktopWallpaper(); toggleStartMenu();">
                <span class="start-icon icon-settings-mini"></span>
                <span class="start-label">Cambiar <u>F</u>ondo...</span>
            </div>"""

    if "📐 <u>O</u>rganizar Ventanas" not in html:
        html = html.replace(start_menu_target, new_start_menu_item)

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated index.html with layout controls and context menu.")

def upgrade_js():
    with open(JS_FILE, "r", encoding="utf-8") as f:
        js = f.read()

    # Add initResizableWindows and initWindowAutoSnapping in DOMContentLoaded
    if "initResizableWindows();" not in js:
        js = js.replace("initDraggableWindows();",
                        "initDraggableWindows();\n    initResizableWindows();\n    initWindowSnappingAndLayouts();")

    # Add resize and auto-adjustment engine before end of file
    new_engine = """
/* ==========================================================================
   MOTOR DE REDIMENSIONAMIENTO LIBRE & AUTODISPOSICIÓN DE VENTANAS
   ========================================================================== */

let pendingSnapAction = null; // 'left' | 'right' | 'top' | null

/**
 * Inicializa tiradores interactivos de redimensionamiento (8 direcciones) en cada ventana.
 * Permite al usuario estirar y redimensionar libremente desde cualquier borde o esquina.
 */
function initResizableWindows() {
    const windows = document.querySelectorAll('.win97-window');
    const directions = ['t', 'b', 'l', 'r', 'tl', 'tr', 'bl', 'br'];

    windows.forEach(win => {
        // Evitar duplicar resizers si ya existen
        if (win.querySelector('.win97-resizer')) return;

        directions.forEach(dir => {
            const resizer = document.createElement('div');
            resizer.className = `win97-resizer resizer-${dir}`;
            resizer.setAttribute('data-direction', dir);
            win.appendChild(resizer);

            resizer.addEventListener('pointerdown', (e) => {
                if (win.classList.contains('maximized')) return;
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
                const minH = 190;
                const desktop = document.getElementById('desktop') || document.body;
                const maxW = desktop.clientWidth;
                const maxH = desktop.clientHeight;

                resizer.setPointerCapture(e.pointerId);

                const onPointerMove = (moveEvt) => {
                    const dx = moveEvt.clientX - startX;
                    const dy = moveEvt.clientY - startY;

                    // Ajuste horizontal
                    if (dir.includes('r')) {
                        const newWidth = Math.max(minW, Math.min(startWidth + dx, maxW - startLeft));
                        win.style.width = `${newWidth}px`;
                    } else if (dir.includes('l')) {
                        const newWidth = Math.max(minW, startWidth - dx);
                        if (newWidth > minW || dx < 0) {
                            const newLeft = Math.max(0, startLeft + (startWidth - newWidth));
                            win.style.width = `${newWidth}px`;
                            win.style.left = `${newLeft}px`;
                        }
                    }

                    // Ajuste vertical
                    if (dir.includes('b')) {
                        const newHeight = Math.max(minH, Math.min(startHeight + dy, maxH - startTop));
                        win.style.height = `${newHeight}px`;
                    } else if (dir.includes('t')) {
                        const newHeight = Math.max(minH, startHeight - dy);
                        if (newHeight > minH || dy < 0) {
                            const newTop = Math.max(0, startTop + (startHeight - newHeight));
                            win.style.height = `${newHeight}px`;
                            win.style.top = `${newTop}px`;
                        }
                    }
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

    document.querySelectorAll('.win97-window').forEach(w => {
        if (w.classList.contains('maximized')) return;
        const rect = w.getBoundingClientRect();
        if (rect.right > dw) {
            const newLeft = Math.max(0, dw - rect.width - 10);
            w.style.left = `${newLeft}px`;
        }
        if (rect.bottom > dh) {
            const newTop = Math.max(0, dh - rect.height - 10);
            w.style.top = `${newTop}px`;
        }
    });
}
"""

    if "MOTOR DE REDIMENSIONAMIENTO LIBRE" not in js:
        # Also upgrade pointermove and pointerup inside initDraggableWindows for snapping
        # Find handle.addEventListener('pointermove', (e) => { ... })
        old_drag_snippet = """            // Restringir a los bordes del escritorio
            const maxLeft = window.innerWidth - 60;
            const maxTop = window.innerHeight - 60;

            newLeft = Math.max(0, Math.min(newLeft, maxLeft));
            newTop = Math.max(0, Math.min(newTop, maxTop));

            win.style.left = `${newLeft}px`;
            win.style.top = `${newTop}px`;
        });

        const stopDrag = (e) => {
            if (isDragging) {
                isDragging = false;
                try {
                    handle.releasePointerCapture(e.pointerId);
                } catch (_) {}
            }
        };"""

        new_drag_snippet = """            // Restringir a los bordes del escritorio
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
                        win.style.left = '2px';
                        win.style.top = '2px';
                        win.style.width = `${Math.floor(dw / 2) - 4}px`;
                        win.style.height = `${dh - 4}px`;
                    } else if (pendingSnapAction.type === 'right') {
                        win.classList.remove('maximized');
                        win.style.left = `${Math.floor(dw / 2) + 2}px`;
                        win.style.top = '2px';
                        win.style.width = `${Math.floor(dw / 2) - 4}px`;
                        win.style.height = `${dh - 4}px`;
                    }
                    pendingSnapAction = null;
                }
            }
        };"""

        if old_drag_snippet in js:
            js = js.replace(old_drag_snippet, new_drag_snippet)

        js = js + "\n" + new_engine
        with open(JS_FILE, "w", encoding="utf-8") as f:
            f.write(js)
        print("Updated app.js with resize, snapping, and layout functions.")

if __name__ == "__main__":
    upgrade_css()
    upgrade_html()
    upgrade_js()
