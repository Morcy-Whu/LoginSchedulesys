const api = {
    addSlot: "/api/slots",
    deleteSlot: id => `/api/slots/${id}`
};

function post(url, body = null) {
    return fetch(url, {
        method: "POST",
        body
    }).then(res => res.json());
}

function initAddSlotForm() {
    const form = document.getElementById("add-slot-form");
    if (!form) return;

    form.addEventListener("submit", e => {
        e.preventDefault();
        post(api.addSlot, new FormData(form))
            .then(r => r.success ? location.reload() : alert(r.error))
            .catch(() => alert("Network error"));
    });
}

function initDeleteButtons() {
    document.querySelectorAll(".delete-btn").forEach(btn => {
        btn.onclick = () => {
            if (!confirm("Delete this time slot?")) return;
            post(api.deleteSlot(btn.dataset.slotId))
                .then(r => r.success && location.reload());
        };
    });
}

document.addEventListener("DOMContentLoaded", () => {
    initAddSlotForm();
    initDeleteButtons();
});
