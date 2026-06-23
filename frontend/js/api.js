const API_BASE = "http://127.0.0.1:8000";

function getToken() {
  return localStorage.getItem("access_token");
}

function setToken(token) {
  localStorage.setItem("access_token", token);
}

function clearToken() {
  localStorage.removeItem("access_token");
}

function isLoggedIn() {
  return !!getToken();
}

function getUsername() {
  return localStorage.getItem("username") || "";
}

function setUsername(username) {
  localStorage.setItem("username", username);
}

function clearUsername() {
  localStorage.removeItem("username");
}

async function apiFetch(path, options = {}) {
  const token = getToken();
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });

  let data = null;
  try {
    data = await res.json();
  } catch (e) {
    data = null;
  }

  if (!res.ok) {
    const detail = data && data.detail ? data.detail : res.statusText;
    const message = typeof detail === "string" ? detail : JSON.stringify(detail);
    throw new Error(message);
  }

  return data;
}

function showAlert(container, message, type = "error") {
  container.innerHTML = `<div class="alert alert-${type}">${escapeHtml(message)}</div>`;
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
