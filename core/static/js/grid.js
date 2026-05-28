let GRID_CONFIG = null;
let GRID_TIMER = null;

function initGrid(config) {
    GRID_CONFIG = config;

    bindGridEvents();
    restoreSelection();
}

/* =========================
   ESTADO / FILTROS
========================= */

function getStateFromURL() {
    const url = new URL(window.location.href);

    return {
        orden: url.searchParams.get("orden") || "codigo",
        dir: url.searchParams.get("dir") || "asc",
        page: url.searchParams.get("page") || "1",

        selected: url.searchParams.get("selected"),
        target: url.searchParams.get("target"),
        return: url.searchParams.get("return")
    };
}

function getFilterValues() {
    const form = document.querySelector(".filtros");
    const values = {};

    if (!form) return values;

    new FormData(form).forEach((value, key) => {
        if (["page", "orden", "dir", "selected", "next"].includes(key)) return;
        values[key] = typeof value === "string" ? value.trim() : value;
    });

    return values;
}

function buildParams(overrides = {}) {

    const filters = getFilterValues();
    const state = getStateFromURL();

    const s = { ...filters, ...state, ...overrides };

    const params = new URLSearchParams();

    Object.entries(s).forEach(([key, value]) => {

        if (value === null || value === undefined || value === "") return;

        params.set(key, value);
    });

    if (!params.has("orden")) params.set("orden", "codigo");
    if (!params.has("dir")) params.set("dir", "asc");
    if (!params.has("page")) params.set("page", "1");

    return params;
}

/* =========================
   GRID ACTIONS
========================= */

function refreshGrid() {
    window.location.search = buildParams({ page: 1 }).toString();
}

function goPage(p) {
    window.location.search = buildParams({ page: p }).toString();
}

function autoFilter() {
    clearTimeout(GRID_TIMER);

    GRID_TIMER = setTimeout(() => {
        window.location.search = buildParams({ page: 1 }).toString();
    }, 400);
}

function sortBy(field) {
    const state = getStateFromURL();

    let dir = "asc";

    if (state.orden === field) {
        dir = state.dir === "asc" ? "desc" : "asc";
    }

    window.location.search = buildParams({
        orden: field,
        dir,
        page: 1
    }).toString();
}

function limpiar() {

    document.querySelectorAll(".filtros input, .filtros select, .filtros textarea")
        .forEach(el => {

            if (el.type === "checkbox" || el.type === "radio") {

                el.checked = false;

            } else if (el.tagName === "SELECT") {

                el.selectedIndex = 0;

            } else {

                el.value = "";
            }
        });

    const state = getStateFromURL();

    const params = new URLSearchParams();

    params.set("orden", "codigo");
    params.set("dir", "asc");
    params.set("page", "1");

    if (state.selected) params.set("selected", state.selected);
    if (state.target) params.set("target", state.target);
    if (state.return) params.set("return", state.return);

    window.location.search = params.toString();
}

/* =========================
   SELECCIÓN GRID
========================= */

function selectRow(row) {

    document.querySelectorAll(".row")
        .forEach(r => r.classList.remove("selected"));

    row.classList.add("selected");

    updateButtonsState();
}

function getSelectedRow() {
    return document.querySelector(".row.selected");
}

function getSelectedId() {
    const row = getSelectedRow();
    return row ? row.dataset.id : null;
}

/* =========================
   BOTONES
========================= */

function updateButtonsState() {

    const hasSelection = getSelectedRow() !== null;

    if (!GRID_CONFIG?.buttons) return;

    GRID_CONFIG.buttons.forEach(btn => {

        const el = document.getElementById(btn.id);

        if (!el) return;

        if (!btn.requiresSelection) {
            el.disabled = false;
            return;
        }

        el.disabled = !hasSelection;
    });

    const btnSelect = document.getElementById("btn_seleccionar");

    if (btnSelect) {
        btnSelect.disabled = !hasSelection;
    }
}

/* =========================
   NEXT
========================= */

function getNext() {

    const params = buildParams();

    const id = getSelectedId();

    if (id) {
        params.set("selected", id);
    }

    const url = new URLSearchParams(params);
    return url.toString();
    }

/* =========================
   ACCIONES CRUD
========================= */

function accion(tipo) {

    const id = getSelectedId();
    const cfg = GRID_CONFIG;

    if (!cfg) return;

    if (tipo !== "nuevo" && !id) {
        alert("Selecciona un registro");
        return;
    }

    const next = getNext();

    const urlMap = {
        nuevo: cfg.urls.nuevo,
        ver: cfg.urls.ver,
        editar: cfg.urls.editar,
        eliminar: cfg.urls.eliminar
    };

    if (tipo === "nuevo") {
        const state = getStateFromURL();

        const params = new URLSearchParams();
        params.set("next", next);

        if (state.selected) params.set("selected", state.selected);
        if (state.target) params.set("target", state.target);
        if (state.return) params.set("return", state.return);

        window.location.href = `${urlMap.nuevo}?${params.toString()}`;
        return;
    }

    const baseUrl = urlMap[tipo];
    if (!baseUrl) return;

    const targetUrl = baseUrl.includes("__ID__")
        ? baseUrl.replace("__ID__", id)
        : `${baseUrl}${id}/`;

    const params = new URLSearchParams();
    params.set("next", next);

    window.location.href = `${targetUrl}?${params.toString()}`;
}

/* =========================
   SELECT MODE
========================= */

function accionSeleccionar() {
    const id = getSelectedId();

    if (!id) {
        alert("Selecciona un registro");
        return;
    }

    const url = new URL(window.location.href);

    const target = url.searchParams.get("target");
    const returnUrl = url.searchParams.get("return");

    if (!target || !returnUrl) {
        alert("Faltan parámetros de retorno");
        return;
    }

    const row = getSelectedRow();
    const cells = row ? row.querySelectorAll("td") : [];
    const text = cells.length > 1 ? cells[1].innerText.trim() : (row ? row.innerText.trim() : id);

    const ret = new URL(returnUrl, window.location.origin);
    ret.searchParams.set("lookup_id", id);
    ret.searchParams.set("lookup_text", text);
    ret.searchParams.set("lookup_target", target);

    window.location.href = ret.toString();
}

function cancelarSeleccion() {
    const url = new URL(window.location.href);
    const returnUrl = url.searchParams.get("return");

    if (returnUrl) {
        window.location.href = new URL(returnUrl, window.location.origin).toString();
        return;
    }

    window.history.back();
}

/* =========================
   RESTORE
========================= */

function trySelectRow(selectedId, attempts = 0) {

    const row =
        document.querySelector(`.row[data-id="${selectedId}"]`);

    if (row) {

        selectRow(row);

        row.scrollIntoView({
            block: "center",
            behavior: "smooth"
        });

        updateButtonsState();

        return;
    }

    if (attempts < 20) {
        setTimeout(() => {
            trySelectRow(selectedId, attempts + 1);
        }, 50);
    }
}

function restoreSelection() {

    const url = new URL(window.location.href);

    const selected = url.searchParams.get("selected");

    if (selected) {
        trySelectRow(selected);
    }

    updateButtonsState(); // 👈 IMPORTANTE
}

/* =========================
   EVENTS
========================= */

function bindGridEvents() {

    document.addEventListener("click", (e) => {

        const row = e.target.closest(".row");

        if (row) {
            selectRow(row);
        }
    });
}