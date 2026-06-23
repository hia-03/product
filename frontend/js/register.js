const alertBox = document.getElementById("alert");
const form = document.getElementById("register-form");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  alertBox.innerHTML = "";

  const payload = {
    username: document.getElementById("username").value.trim(),
    name: document.getElementById("name").value.trim(),
    password: document.getElementById("password").value,
    confirm_password: document.getElementById("confirm_password").value,
  };

  try {
    await apiFetch("/register", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    showAlert(alertBox, "Registered successfully. Redirecting to login...", "success");
    setTimeout(() => {
      window.location.href = "login.html";
    }, 1200);
  } catch (err) {
    showAlert(alertBox, err.message);
  }
});
