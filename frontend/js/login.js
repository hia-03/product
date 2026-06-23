const alertBox = document.getElementById("alert");
const form = document.getElementById("login-form");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  alertBox.innerHTML = "";

  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value;

  try {
    const result = await apiFetch("/login", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    });
    setToken(result.access_token);
    setUsername(username);
    window.location.href = "index.html";
  } catch (err) {
    showAlert(alertBox, err.message);
  }
});
