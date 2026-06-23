if (requireAuth()) {
  const alertBox = document.getElementById("alert");
  const usersBody = document.getElementById("users-body");
  const productsBody = document.getElementById("products-body");

  async function loadUsers() {
    try {
      const users = await apiFetch("/admin/users");
      usersBody.innerHTML = users
        .map(
          (u) => `
        <tr>
          <td>${u.id}</td>
          <td>${escapeHtml(u.username)}</td>
          <td>${escapeHtml(u.name)}</td>
          <td>${u.is_superuser ? "Yes" : "No"}</td>
          <td>${escapeHtml(u.created_at || "")}</td>
          <td><button class="danger del-user-btn" data-id="${u.id}">Delete</button></td>
        </tr>
      `
        )
        .join("");

      usersBody.querySelectorAll(".del-user-btn").forEach((btn) => {
        btn.addEventListener("click", () => deleteUser(Number(btn.dataset.id)));
      });
    } catch (err) {
      showAlert(alertBox, err.message);
      usersBody.innerHTML = "";
    }
  }

  async function loadProducts() {
    try {
      const products = await apiFetch("/admin/products");
      productsBody.innerHTML = products
        .map(
          (p) => `
        <tr>
          <td>${p.id}</td>
          <td>${escapeHtml(p.title)}</td>
          <td>$${p.price}</td>
          <td>${p.owner_id}</td>
          <td>
            <button class="edit-product-btn" data-id="${p.id}">Edit</button>
            <button class="danger del-product-btn" data-id="${p.id}">Delete</button>
          </td>
        </tr>
      `
        )
        .join("");

      productsBody.querySelectorAll(".edit-product-btn").forEach((btn) => {
        const product = products.find((p) => p.id === Number(btn.dataset.id));
        btn.addEventListener("click", () => editProduct(product));
      });
      productsBody.querySelectorAll(".del-product-btn").forEach((btn) => {
        btn.addEventListener("click", () => deleteProduct(Number(btn.dataset.id)));
      });
    } catch (err) {
      showAlert(alertBox, err.message);
      productsBody.innerHTML = "";
    }
  }

  async function deleteUser(id) {
    if (!confirm("Delete this user?")) return;
    try {
      await apiFetch(`/admin/deluser/${id}`, { method: "DELETE" });
      loadUsers();
    } catch (err) {
      showAlert(alertBox, err.message);
    }
  }

  async function editProduct(product) {
    const title = prompt("Title", product.title);
    if (title === null) return;
    const description = prompt("Description", product.description);
    if (description === null) return;
    const priceStr = prompt("Price", product.price);
    if (priceStr === null) return;

    try {
      await apiFetch(`/admin/updateproduct/${product.id}`, {
        method: "PUT",
        body: JSON.stringify({ title, description, price: parseFloat(priceStr) }),
      });
      loadProducts();
    } catch (err) {
      showAlert(alertBox, err.message);
    }
  }

  async function deleteProduct(id) {
    if (!confirm("Delete this product?")) return;
    try {
      await apiFetch(`/admin/deleteproduct/${id}`, { method: "DELETE" });
      loadProducts();
    } catch (err) {
      showAlert(alertBox, err.message);
    }
  }

  loadUsers();
  loadProducts();
}
