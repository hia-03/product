function renderNav() {
  const nav = document.getElementById("nav");
  if (!nav) return;

  const loggedIn = isLoggedIn();

  nav.innerHTML = `
    <span class="brand">Product Shop</span>
    <a href="index.html">Home</a>
    ${loggedIn ? '<a href="my-products.html">My Products</a>' : ""}
    ${loggedIn ? '<a href="admin.html">Admin</a>' : ""}
    ${loggedIn ? '<button id="logout-btn">Logout</button>' : '<a href="login.html">Login</a>'}
    ${loggedIn ? "" : '<a href="register.html">Register</a>'}
  `;

  const logoutBtn = document.getElementById("logout-btn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", logout);
  }
}

async function logout() {
  try {
    await apiFetch("/logout", { method: "POST" });
  } catch (e) {
    // token may already be invalid/expired - clear local state regardless
  }
  clearToken();
  clearUsername();
  window.location.href = "login.html";
}

function requireAuth() {
  if (!isLoggedIn()) {
    window.location.href = "login.html";
    return false;
  }
  return true;
}

document.addEventListener("DOMContentLoaded", renderNav);
