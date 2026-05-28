(function () {
    const DEFAULT_IGNORE_FIELDS = new Set([
        "csrfmiddlewaretoken",
        "next"
    ]);

    function getFormStorageKey(form) {
        if (!form) return null;
        return form.dataset.lookupStorage || null;
    }

    function serializeForm(form) {
        const data = {};

        form.querySelectorAll("input, select, textarea").forEach((el) => {
            if (!el.name) return;
            if (DEFAULT_IGNORE_FIELDS.has(el.name)) return;

            if (el.type === "checkbox") {
                data[el.name] = el.checked ? "on" : "";
                return;
            }

            if (el.type === "radio") {
                if (el.checked) data[el.name] = el.value;
                return;
            }

            data[el.name] = el.value;
        });

        return data;
    }

    function persistFormState(form) {
        const key = getFormStorageKey(form);
        if (!form || !key) return;

        sessionStorage.setItem(key, JSON.stringify(serializeForm(form)));
    }

    function restoreFormState(form) {
        const key = getFormStorageKey(form);
        if (!form || !key) return;

        const raw = sessionStorage.getItem(key);
        if (!raw) return;

        try {
            const data = JSON.parse(raw);

            Object.entries(data).forEach(([name, value]) => {
                const el = form.querySelector(`[name="${name}"]`);
                if (!el) return;

                if (el.type === "checkbox") {
                    el.checked = value === "on";
                    return;
                }

                if (el.type === "radio") {
                    const radio = form.querySelector(`[name="${name}"][value="${value}"]`);
                    if (radio) radio.checked = true;
                    return;
                }

                el.value = value;
            });
        } catch (e) {
            console.error("Error restaurando estado de formulario:", e);
        }
    }

    function clearFormState(form) {
        const key = getFormStorageKey(form);
        if (!form || !key) return;

        sessionStorage.removeItem(key);
    }

    function open(button) {
        const form = button.closest("form");
        if (!form) return;

        const lookupUrl = button.dataset.lookupUrl;
        const target = button.dataset.lookupTarget;

        if (!lookupUrl || !target) {
            console.error("Lookup.open: faltan data-lookup-url o data-lookup-target");
            return;
        }

        persistFormState(form);

        const currentUrl = window.location.pathname + window.location.search;
        const url = new URL(lookupUrl, window.location.origin);

        url.searchParams.set("select", "1");
        url.searchParams.set("target", target);
        url.searchParams.set("return", currentUrl);

        window.location.href = url.toString();
    }

    function cancel(button) {
        const form = button.closest("form");
        if (form) clearFormState(form);

        const cancelUrl =
            button.dataset.cancelUrl ||
            (form ? form.dataset.cancelUrl : "");

        if (cancelUrl) {
            window.location.href = cancelUrl;
            return;
        }

        window.history.back();
    }

    function applyLookupResult() {
        const params = new URLSearchParams(window.location.search);

        const lookupId = params.get("lookup_id");
        const lookupText = params.get("lookup_text");
        const lookupTarget = params.get("lookup_target");

        if (!lookupId || !lookupTarget) return;

        const targetEl = document.getElementById(lookupTarget);
        if (!targetEl) return;

        // =========================
        // SET VALOR
        // =========================
        if (targetEl.tagName === "SELECT") {
            let option = targetEl.querySelector(`option[value="${lookupId}"]`);

            if (!option) {
                option = document.createElement("option");
                option.value = lookupId;
                option.text = lookupText || lookupId;
                targetEl.appendChild(option);
            }

            targetEl.value = lookupId;

        } else {
            targetEl.value = lookupId;
        }

        // =========================
        // EVENTOS BASE (compatibilidad)
        // =========================
        targetEl.dispatchEvent(new Event("change", { bubbles: true }));
        targetEl.dispatchEvent(new Event("input", { bubbles: true }));

        // =========================
        // 🔥 NUEVO EVENTO GLOBAL (ESTANDARIZADO)
        // =========================
        const form = targetEl.closest("form");

        document.dispatchEvent(new CustomEvent("lookup:change", {
            detail: {
                target: lookupTarget,
                value: lookupId,
                text: lookupText,
                form: form ? form.id : null
            }
        }));

        // =========================
        // LIMPIEZA STATE
        // =========================
        if (form) {
            const key = form.dataset.lookupStorage;
            if (key) sessionStorage.removeItem(key);
        }

        // =========================
        // LIMPIAR URL
        // =========================
        params.delete("lookup_id");
        params.delete("lookup_text");
        params.delete("lookup_target");

        const cleanUrl =
            window.location.pathname +
            (params.toString() ? "?" + params.toString() : "");

        window.history.replaceState({}, "", cleanUrl);
    }

    function bindForm(form) {
        if (!form || form.dataset.lookupBound === "1") return;
        form.dataset.lookupBound = "1";

        restoreFormState(form);

        form.addEventListener("input", () => persistFormState(form));
        form.addEventListener("change", () => persistFormState(form));
        form.addEventListener("submit", () => clearFormState(form));
    }

    function boot() {
        document.querySelectorAll("form[data-lookup-storage]").forEach(bindForm);
        applyLookupResult();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", boot);
    } else {
        boot();
    }

    window.Lookup = {
        open,
        cancel,
        persistFormState,
        restoreFormState,
        clearFormState,
        applyLookupResult,
        bindForm
    };
})();