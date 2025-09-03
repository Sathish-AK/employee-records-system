// ==========================
// Generic HTTP helper
// ==========================
async function http(method, url, data, headers = {}) {
  const opts = {
    method,
    headers: { "Content-Type": "application/json", ...headers },
  };
  if (data !== undefined) opts.body = JSON.stringify(data);

  const res = await fetch(url, opts);
  if (!res.ok) {
    const t = await res.text();
    throw new Error(`HTTP ${res.status}: ${t}`);
  }
  return res.json().catch(() => ({ ok: true }));
}

// ==========================
// CSRF Cookie helper
// ==========================
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// ==========================
// Input Restrictions
// ==========================
function applyRestrictions(el) {
  if (el.type === "text") {
    el.setAttribute("maxlength", "50"); // max 10 chars
    console.log("✅ Maxlength=10 applied to text field", el.name || el.id);
  }
  if (el.type === "password") {
    el.setAttribute("maxlength", "20"); // max 20 chars
    console.log("✅ Maxlength=20 applied to password field", el.name || el.id);
  }
  if (el.type === "number") {
    el.setAttribute("min", "1");
    el.setAttribute("max", "100");
    console.log("✅ Number field restricted between 1–100", el.name || el.id);
  }
  if (el.type === "date") {
    el.setAttribute("min", "2000-01-01");
    el.setAttribute("max", "2030-12-31");
    console.log("✅ Date field restricted between 2000–2030", el.name || el.id);
  }
  if (el.tagName.toLowerCase() === "textarea") {
    el.setAttribute("maxlength", "200");
    console.log("✅ Maxlength=200 applied to textarea", el.name || el.id);
  }
}

// ==========================
// Run restrictions on load + dynamic fields
// ==========================
document.addEventListener("DOMContentLoaded", () => {
  console.log("✅ app.js loaded");

  // Apply to existing inputs
  document.querySelectorAll("input, textarea").forEach(applyRestrictions);

  // Watch for dynamically added inputs (like formbuilder fields)
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((node) => {
        if (
          node.tagName &&
          (node.tagName.toLowerCase() === "input" ||
            node.tagName.toLowerCase() === "textarea")
        ) {
          applyRestrictions(node);
        }
        if (node.querySelectorAll) {
          node.querySelectorAll("input, textarea").forEach(applyRestrictions);
        }
      });
    });
  });

  observer.observe(document.body, { childList: true, subtree: true });
});
