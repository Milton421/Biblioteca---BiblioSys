
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    loadCategorias();

    setupModalListeners();
    setupSearchFilters();
});

// --- HELPER DE NOTIFICACIONES TOAST ---
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    let icon = 'bi-check-circle-fill';
    if (type === 'error') icon = 'bi-exclamation-triangle-fill';
    if (type === 'info') icon = 'bi-info-circle-fill';

    toast.innerHTML = `
        <i class="bi ${icon}"></i>
        <span>${escapeHtml(message)}</span>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

function showConfirm(message, title = 'Confirmar Acción', isDanger = false) {
    return new Promise((resolve) => {
        const modal = document.getElementById('modal-confirm');
        const msgEl = document.getElementById('confirm-message');
        const titleEl = document.getElementById('confirm-title');
        const btnAccept = document.getElementById('btn-confirm-accept');
        const btnCancel = document.getElementById('btn-confirm-cancel');
        const iconEl = document.getElementById('confirm-icon');

        if (!modal) {
            resolve(window.confirm(message));
            return;
        }

        msgEl.textContent = message;
        titleEl.textContent = title;

        if (isDanger) {
            btnAccept.className = 'btn btn-danger';
            iconEl.style.background = '#fef2f2';
            iconEl.style.color = '#dc2626';
            iconEl.innerHTML = '<i class="bi bi-exclamation-triangle-fill"></i>';
        } else {
            btnAccept.className = 'btn btn-primary';
            iconEl.style.background = '#eff6ff';
            iconEl.style.color = '#2563eb';
            iconEl.innerHTML = '<i class="bi bi-question-circle-fill"></i>';
        }

        modal.classList.add('active');

        function cleanup(result) {
            modal.classList.remove('active');
            btnAccept.removeEventListener('click', onAccept);
            btnCancel.removeEventListener('click', onCancel);
            resolve(result);
        }

        function onAccept() { cleanup(true); }
        function onCancel() { cleanup(false); }

        btnAccept.addEventListener('click', onAccept);
        btnCancel.addEventListener('click', onCancel);
    });
}

function formatDate(dateStr) {
    if (!dateStr) return 'N/A';
    if (dateStr.includes('GMT') || dateStr.includes(':')) {
        dateStr = dateStr.split(' ')[0] || dateStr;
    }
    const parts = dateStr.split('-');
    if (parts.length === 3) {
        const months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
        const day = parts[2].padStart(2, '0');
        const monthIndex = parseInt(parts[1], 10) - 1;
        const year = parts[0];
        if (monthIndex >= 0 && monthIndex < 12) {
            return `${day} ${months[monthIndex]} ${year}`;
        }
    }
    return dateStr;
}

function initNavigation() {
    const initialSection = getSectionFromPath() || document.body.dataset.activeSection || 'dashboard';
    switchSection(initialSection);

    const navLinks = document.querySelectorAll('.nav-item a');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetSection = link.dataset.section;
            const href = link.getAttribute('href');

            history.pushState({ section: targetSection }, '', href);
            switchSection(targetSection);
        });
    });

    window.addEventListener('popstate', (e) => {
        const section = e.state?.section || getSectionFromPath();
        switchSection(section);
    });
}

function getSectionFromPath() {
    const path = window.location.pathname;
    if (path.includes('/libros')) return 'libros';
    if (path.includes('/usuarios')) return 'usuarios';
    if (path.includes('/prestamos')) return 'prestamos';
    if (path.includes('/multas')) return 'multas';
    return 'dashboard';
}

function switchSection(targetSection) {
    const sections = document.querySelectorAll('.view-section');
    const navItems = document.querySelectorAll('.nav-item');

    navItems.forEach(li => {
        const link = li.querySelector('a');
        if (link && link.dataset.section === targetSection) {
            li.classList.add('active');
        } else {
            li.classList.remove('active');
        }
    });

    sections.forEach(sec => {
        if (sec.id === `section-${targetSection}`) {
            sec.classList.add('active');
        } else {
            sec.classList.remove('active');
        }
    });

    // Cargar datos correspondientes al apartado activo
    if (targetSection === 'dashboard') loadDashboardStats();
    if (targetSection === 'libros') loadLibros();
    if (targetSection === 'usuarios') loadUsuarios();
    if (targetSection === 'prestamos') loadPrestamos();
    if (targetSection === 'multas') loadMultas();
}

// --- DASHBOARD ---
async function loadDashboardStats() {
    try {
        const res = await fetch('/api/stats');
        const data = await res.json();

        document.getElementById('stat-total-libros').textContent = data.total_libros || 0;
        document.getElementById('stat-libros-prestados').textContent = data.libros_prestados || 0;
        document.getElementById('stat-usuarios-activos').textContent = data.usuarios_activos || 0;
        document.getElementById('stat-multas-pendientes').textContent = `Q ${data.multas_pendientes.toFixed(2)}`;

        const tbody = document.getElementById('table-recientes-body');
        tbody.innerHTML = '';
        if (!data.recientes || data.recientes.length === 0) {
            tbody.innerHTML = `<tr><td colspan="4" style="text-align:center; color: var(--text-muted);">Sin actividad reciente registrada</td></tr>`;
            return;
        }

        data.recientes.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${escapeHtml(row.titulo)}</strong></td>
                <td>${escapeHtml(row.usuario)}</td>
                <td>${formatDate(row.fecha_prestamo)}</td>
                <td><span class="badge badge-${row.estado.toLowerCase()}">${row.estado}</span></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error('Error al cargar estadísticas:', err);
    }
}

// --- CATEGORÍAS ---
let categoriasCache = [];
async function loadCategorias() {
    try {
        const res = await fetch('/api/categorias');
        categoriasCache = await res.json();

        const selectFiltro = document.getElementById('filter-categoria');
        const selectForm = document.getElementById('libro-categoria');

        if (selectFiltro) {
            selectFiltro.innerHTML = '<option value="">Todas las Categorías</option>';
            categoriasCache.forEach(c => {
                selectFiltro.innerHTML += `<option value="${c.id}">${escapeHtml(c.nombre)}</option>`;
            });
        }

        if (selectForm) {
            selectForm.innerHTML = '<option value="">Seleccionar Categoría</option>';
            categoriasCache.forEach(c => {
                selectForm.innerHTML += `<option value="${c.id}">${escapeHtml(c.nombre)}</option>`;
            });
        }
    } catch (err) {
        console.error('Error al cargar categorías:', err);
    }
}

// --- LIBROS ---
async function loadLibros() {
    const q = document.getElementById('search-libros')?.value || '';
    const cat = document.getElementById('filter-categoria')?.value || '';

    try {
        const res = await fetch(`/api/libros?q=${encodeURIComponent(q)}&categoria=${cat}`);
        const libros = await res.json();

        const grid = document.getElementById('books-grid');
        grid.innerHTML = '';

        if (!libros || libros.length === 0) {
            grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: var(--text-muted);">
                <i class="bi bi-journal-x" style="font-size: 2.2rem; display: block; margin-bottom: 0.5rem; color: var(--text-muted);"></i>
                No se encontraron libros en el catálogo.
            </div>`;
            return;
        }

        libros.forEach(l => {
            const isAvailable = l.stock_disponible > 0;
            const card = document.createElement('div');
            card.className = 'book-card';
            card.innerHTML = `
                <div class="book-cover-wrap">
                    <img src="${escapeHtml(l.portada_url)}" alt="${escapeHtml(l.titulo)}" class="book-cover" onerror="this.src='https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=400&q=80'">
                    <span class="stock-badge ${isAvailable ? 'available' : 'out'}">
                        ${isAvailable ? `${l.stock_disponible}/${l.stock_total} Disp.` : 'Agotado'}
                    </span>
                </div>
                <div class="book-body">
                    <span class="book-category">${escapeHtml(l.categoria_nombre || 'General')}</span>
                    <h4 class="book-title" title="${escapeHtml(l.titulo)}">${escapeHtml(l.titulo)}</h4>
                    <p class="book-author">Por ${escapeHtml(l.autor)}</p>
                    <div class="book-footer">
                        <span style="font-size: 0.75rem; color: var(--text-muted);">ISBN: ${escapeHtml(l.isbn || 'N/A')}</span>
                        <div class="book-actions-btn-group">
                            <button class="icon-action-btn" onclick="editarLibro(${l.id})" title="Editar"><i class="bi bi-pencil-fill"></i></button>
                            <button class="icon-action-btn delete" onclick="eliminarLibro(${l.id})" title="Eliminar"><i class="bi bi-trash-fill"></i></button>
                        </div>
                    </div>
                </div>
            `;
            grid.appendChild(card);
        });
    } catch (err) {
        console.error('Error al cargar libros:', err);
    }
}

// --- USUARIOS ---
async function loadUsuarios() {
    const q = document.getElementById('search-usuarios')?.value || '';
    try {
        const res = await fetch(`/api/usuarios?q=${encodeURIComponent(q)}`);
        const usuarios = await res.json();

        const tbody = document.getElementById('table-usuarios-body');
        tbody.innerHTML = '';

        if (!usuarios || usuarios.length === 0) {
            tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; color: var(--text-muted);">No hay socios registrados</td></tr>`;
            return;
        }

        usuarios.forEach(u => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${escapeHtml(u.nombre)}</strong></td>
                <td>${escapeHtml(u.email)}</td>
                <td>${escapeHtml(u.telefono || 'N/A')}</td>
                <td>${formatDate(u.fecha_registro)}</td>
                <td>
                    <div style="display:flex; gap:0.35rem;">
                        <button class="icon-action-btn" onclick="editarUsuario(${u.id})"><i class="bi bi-pencil-fill"></i></button>
                        <button class="icon-action-btn delete" onclick="eliminarUsuario(${u.id})"><i class="bi bi-trash-fill"></i></button>
                    </div>
                </td>
            `;
            tbody.appendChild(tr);
        });

        const selectPrestamoUsr = document.getElementById('prestamo-usuario');
        if (selectPrestamoUsr) {
            selectPrestamoUsr.innerHTML = '<option value="">Seleccionar Usuario / Socio</option>';
            usuarios.forEach(u => {
                if (u.activo) {
                    selectPrestamoUsr.innerHTML += `<option value="${u.id}">${escapeHtml(u.nombre)} (${escapeHtml(u.email)})</option>`;
                }
            });
        }
    } catch (err) {
        console.error('Error al cargar usuarios:', err);
    }
}

// --- PRÉSTAMOS ---
async function loadPrestamos() {
    const q = document.getElementById('search-prestamos')?.value || '';
    const estado = document.getElementById('filter-prestamo-estado')?.value || 'ALL';
    try {
        const res = await fetch(`/api/prestamos?q=${encodeURIComponent(q)}&estado=${estado}`);
        const prestamos = await res.json();

        const tbody = document.getElementById('table-prestamos-body');
        tbody.innerHTML = '';

        if (!prestamos || prestamos.length === 0) {
            tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; color: var(--text-muted);">No hay préstamos registrados con este filtro</td></tr>`;
            return;
        }

        prestamos.forEach(p => {
            const isDevuelto = p.estado === 'DEVUELTO';
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${escapeHtml(p.libro_titulo)}</strong></td>
                <td>${escapeHtml(p.usuario_nombre)}</td>
                <td>${formatDate(p.fecha_prestamo)}</td>
                <td>${formatDate(p.fecha_devolucion_esperada)}</td>
                <td><span class="badge badge-${p.estado.toLowerCase()}">${p.estado}</span></td>
                <td>
                    ${!isDevuelto ? `<button class="btn btn-primary btn-sm" onclick="devolverPrestamo(${p.id})"><i class="bi bi-box-arrow-in-left"></i> Devolver</button>` : `<span style="color: var(--text-muted); font-size: 0.8rem;"><i class="bi bi-check2"></i> Devuelto</span>`}
                </td>
            `;
            tbody.appendChild(tr);
        });

        const resLibros = await fetch('/api/libros');
        const libros = await resLibros.json();
        const selectPrestamoLibro = document.getElementById('prestamo-libro');
        if (selectPrestamoLibro) {
            selectPrestamoLibro.innerHTML = '<option value="">Seleccionar Libro Disponible</option>';
            libros.forEach(l => {
                if (l.stock_disponible > 0) {
                    selectPrestamoLibro.innerHTML += `<option value="${l.id}">${escapeHtml(l.titulo)} (${l.stock_disponible} disp.)</option>`;
                }
            });
        }
    } catch (err) {
        console.error('Error al cargar préstamos:', err);
    }
}

// --- MULTAS ---
async function loadMultas() {
    const q = document.getElementById('search-multas')?.value || '';
    try {
        const res = await fetch(`/api/multas?q=${encodeURIComponent(q)}`);
        const multas = await res.json();

        const tbody = document.getElementById('table-multas-body');
        tbody.innerHTML = '';

        if (!multas || multas.length === 0) {
            tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; color: var(--text-muted);">No hay multas registradas</td></tr>`;
            return;
        }

        multas.forEach(m => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${escapeHtml(m.usuario_nombre)}</td>
                <td>${escapeHtml(m.libro_titulo)}</td>
                <td><strong style="color: var(--status-overdue-text);">Q ${parseFloat(m.monto).toFixed(2)}</strong> (${m.dias_retraso}d)</td>
                <td>
                    <span class="badge ${m.pagada ? 'badge-activo' : 'badge-vencido'}">
                        ${m.pagada ? 'Pagada' : 'Pendiente'}
                    </span>
                </td>
                <td>
                    ${!m.pagada ? `<button class="btn btn-secondary btn-sm" onclick="pagarMulta(${m.id})"><i class="bi bi-check-lg"></i> Marcar Pagada</button>` : '<span style="color: var(--text-muted); font-size: 0.8rem;">-</span>'}
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error('Error al cargar multas:', err);
    }
}

// --- ACCIONES CRUD LIBRO ---
function abrirModalLibro() {
    document.getElementById('form-libro').reset();
    document.getElementById('libro-id').value = '';
    document.getElementById('modal-libro-titulo').textContent = 'Registrar Nuevo Libro';
    document.getElementById('modal-libro').classList.add('active');
}

async function editarLibro(id) {
    try {
        const res = await fetch(`/api/libros/${id}`);
        const l = await res.json();

        document.getElementById('libro-id').value = l.id;
        document.getElementById('libro-titulo-input').value = l.titulo;
        document.getElementById('libro-autor-input').value = l.autor;
        document.getElementById('libro-isbn-input').value = l.isbn || '';
        document.getElementById('libro-categoria').value = l.categoria_id || '';
        document.getElementById('libro-anio-input').value = l.anio_publicacion || '';
        document.getElementById('libro-stock-input').value = l.stock_total || 1;
        document.getElementById('libro-portada-input').value = l.portada_url || '';

        document.getElementById('modal-libro-titulo').textContent = 'Editar Libro';
        document.getElementById('modal-libro').classList.add('active');
    } catch (err) {
        showToast('Error al obtener datos del libro', 'error');
    }
}

async function guardarLibro(e) {
    e.preventDefault();
    const id = document.getElementById('libro-id').value;
    const data = {
        titulo: document.getElementById('libro-titulo-input').value,
        autor: document.getElementById('libro-autor-input').value,
        isbn: document.getElementById('libro-isbn-input').value,
        categoria_id: document.getElementById('libro-categoria').value || null,
        anio_publicacion: document.getElementById('libro-anio-input').value || null,
        stock_total: document.getElementById('libro-stock-input').value,
        portada_url: document.getElementById('libro-portada-input').value
    };

    const method = id ? 'PUT' : 'POST';
    const url = id ? `/api/libros/${id}` : '/api/libros';

    const res = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    if (res.ok) {
        cerrarModales();
        showToast(id ? 'Libro actualizado correctamente' : 'Libro registrado exitosamente', 'success');
        loadLibros();
        loadDashboardStats();
    } else {
        const err = await res.json();
        showToast(err.error || 'Error al guardar el libro', 'error');
    }
}

async function eliminarLibro(id) {
    const ok = await showConfirm('¿Estás seguro de eliminar este libro del catálogo?', 'Eliminar Libro', true);
    if (!ok) return;

    const res = await fetch(`/api/libros/${id}`, { method: 'DELETE' });
    if (res.ok) {
        showToast('Libro eliminado del inventario', 'info');
        loadLibros();
        loadDashboardStats();
    } else {
        showToast('No se pudo eliminar el libro', 'error');
    }
}

// --- ACCIONES CRUD USUARIO ---
function abrirModalUsuario() {
    document.getElementById('form-usuario').reset();
    document.getElementById('usuario-id').value = '';
    document.getElementById('modal-usuario-titulo').textContent = 'Registrar Nuevo Socio';
    document.getElementById('modal-usuario').classList.add('active');
}

async function guardarUsuario(e) {
    e.preventDefault();
    const id = document.getElementById('usuario-id').value;
    const data = {
        nombre: document.getElementById('usuario-nombre-input').value,
        email: document.getElementById('usuario-email-input').value,
        telefono: document.getElementById('usuario-telefono-input').value,
        direccion: document.getElementById('usuario-direccion-input').value
    };

    const method = id ? 'PUT' : 'POST';
    const url = id ? `/api/usuarios/${id}` : '/api/usuarios';

    const res = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    if (res.ok) {
        cerrarModales();
        showToast(id ? 'Socio actualizado correctamente' : 'Socio registrado exitosamente', 'success');
        loadUsuarios();
        loadDashboardStats();
    } else {
        const err = await res.json();
        showToast(err.error || 'Error al guardar socio', 'error');
    }
}

async function eliminarUsuario(id) {
    const ok = await showConfirm('¿Deseas eliminar este socio de la biblioteca?', 'Eliminar Socio', true);
    if (!ok) return;

    const res = await fetch(`/api/usuarios/${id}`, { method: 'DELETE' });
    if (res.ok) {
        showToast('Socio eliminado correctamente', 'info');
        loadUsuarios();
        loadDashboardStats();
    }
}

// --- ACCIONES PRÉSTAMOS ---
function abrirModalPrestamo() {
    document.getElementById('form-prestamo').reset();
    document.getElementById('modal-prestamo').classList.add('active');
}

async function guardarPrestamo(e) {
    e.preventDefault();
    const data = {
        libro_id: document.getElementById('prestamo-libro').value,
        usuario_id: document.getElementById('prestamo-usuario').value,
        dias_prestamo: document.getElementById('prestamo-dias').value
    };

    const res = await fetch('/api/prestamos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    if (res.ok) {
        cerrarModales();
        showToast('Préstamo creado correctamente', 'success');
        loadPrestamos();
        loadLibros();
        loadDashboardStats();
    } else {
        const err = await res.json();
        showToast(err.error || 'Error al registrar el préstamo', 'error');
    }
}

async function devolverPrestamo(id) {
    const ok = await showConfirm('¿Confirmar la devolución de este libro prestado?', 'Registrar Devolución', false);
    if (!ok) return;

    const res = await fetch(`/api/prestamos/${id}/devolver`, { method: 'POST' });
    const data = await res.json();

    if (res.ok) {
        showToast(data.message, 'success');
        loadPrestamos();
        loadLibros();
        loadMultas();
        loadDashboardStats();
    } else {
        showToast(data.error || 'Error al procesar la devolución', 'error');
    }
}

async function pagarMulta(id) {
    const ok = await showConfirm('¿Marcar esta multa como pagada?', 'Registrar Pago de Multa', false);
    if (!ok) return;

    const res = await fetch(`/api/multas/${id}/pagar`, { method: 'POST' });
    if (res.ok) {
        showToast('Multa registrada como pagada', 'success');
        loadMultas();
        loadDashboardStats();
    }
}

// --- MODALES & FILTROS ---
function setupModalListeners() {
    document.getElementById('form-libro')?.addEventListener('submit', guardarLibro);
    document.getElementById('form-usuario')?.addEventListener('submit', guardarUsuario);
    document.getElementById('form-prestamo')?.addEventListener('submit', guardarPrestamo);

    document.querySelectorAll('.btn-close-modal').forEach(btn => {
        btn.addEventListener('click', cerrarModales);
    });

    document.querySelectorAll('.modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay && overlay.id !== 'modal-confirm') cerrarModales();
        });
    });
}

function cerrarModales() {
    document.querySelectorAll('.modal-overlay').forEach(m => m.classList.remove('active'));
}

function setupSearchFilters() {
    document.getElementById('search-libros')?.addEventListener('input', debounce(loadLibros, 300));
    document.getElementById('filter-categoria')?.addEventListener('change', loadLibros);
    document.getElementById('search-usuarios')?.addEventListener('input', debounce(loadUsuarios, 300));
    document.getElementById('search-prestamos')?.addEventListener('input', debounce(loadPrestamos, 300));
    document.getElementById('filter-prestamo-estado')?.addEventListener('change', loadPrestamos);
    document.getElementById('search-multas')?.addEventListener('input', debounce(loadMultas, 300));

    document.getElementById('global-search')?.addEventListener('input', (e) => {
        const val = e.target.value;
        const librosSearch = document.getElementById('search-libros');
        if (librosSearch) {
            librosSearch.value = val;
            const currentSection = getSectionFromPath();
            if (currentSection !== 'libros' && val.trim() !== '') {
                history.pushState({ section: 'libros' }, '', '/libros');
                switchSection('libros');
            } else {
                loadLibros();
            }
        }
    });
}

function debounce(func, wait) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
