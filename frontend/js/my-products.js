if (requireAuth()) {
  const alertBox = document.getElementById("alert");
  const grid = document.getElementById("grid");
  const form = document.getElementById("product-form");
  const formTitle = document.getElementById("form-title");
  const idField = document.getElementById("product-id");
  const titleField = document.getElementById("title");
  const descriptionField = document.getElementById("description");
  const priceField = document.getElementById("price");
  const submitBtn = document.getElementById("submit-btn");
  const cancelBtn = document.getElementById("cancel-edit");

  function resetForm() {
    idField.value = "";
    titleField.value = "";
    descriptionField.value = "";
    priceField.value = "";
    formTitle.textContent = "Add Product";
    submitBtn.textContent = "Add Product";
    cancelBtn.style.display = "none";
  }

  function fillForm(product) {
    idField.value = product.id;
    titleField.value = product.title;
    descriptionField.value = product.description;
    priceField.value = product.price;
    formTitle.textContent = "Edit Product";
    submitBtn.textContent = "Save Changes";
    cancelBtn.style.display = "inline-block";
  }

  function renderGrid(products) {
    if (!products || products.length === 0) {
      grid.innerHTML = '<p class="empty">You have no products yet.</p>';
      return;
    }

    grid.innerHTML = products
      .map(
        (p) => `
      <div class="card">
        <h3>${escapeHtml(p.title)}</h3>
        <p>${escapeHtml(p.description)}</p>
        <div class="price">$${p.price}</div>
        <div class="card-actions">
          <button class="edit-btn" data-id="${p.id}">Edit</button>
          <button class="danger delete-btn" data-id="${p.id}">Delete</button>
        </div>
      </div>
    `
      )
      .join("");

    grid.querySelectorAll(".edit-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const product = products.find((p) => p.id === Number(btn.dataset.id));
        if (product) fillForm(product);
      });
    });

    grid.querySelectorAll(".delete-btn").forEach((btn) => {
      btn.addEventListener("click", () => deleteProduct(Number(btn.dataset.id)));
    });
  }

  async function loadMyProducts() {
    alertBox.innerHTML = "";
    try {
      const products = await apiFetch("/all-product");
      renderGrid(products);
    } catch (err) {
      renderGrid([]);
    }
  }

  async function deleteProduct(id) {
    if (!confirm("Delete this product?")) return;
    alertBox.innerHTML = "";
    try {
      await apiFetch(`/product/del/${id}`, { method: "DELETE" });
      loadMyProducts();
    } catch (err) {
      showAlert(alertBox, err.message);
    }
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    alertBox.innerHTML = "";

    const payload = {
      title: titleField.value.trim(),
      description: descriptionField.value.trim(),
      price: parseFloat(priceField.value),
    };

    try {
      if (idField.value) {
        await apiFetch(`/product/up/${idField.value}`, {
          method: "PUT",
          body: JSON.stringify(payload),
        });
      } else {
        await apiFetch("/add-product", {
          method: "POST",
          body: JSON.stringify(payload),
        });
      }
      resetForm();
      loadMyProducts();
    } catch (err) {
      showAlert(alertBox, err.message);
    }
  });

  cancelBtn.addEventListener("click", resetForm);

  loadMyProducts();
}
