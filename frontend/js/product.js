const alertBox = document.getElementById("alert");
const detail = document.getElementById("product-detail");

const params = new URLSearchParams(window.location.search);
const productId = params.get("id");

async function loadProduct() {
  if (!productId) {
    showAlert(alertBox, "No product id provided.");
    return;
  }

  try {
    const product = await apiFetch(`/products/${productId}`);
    detail.innerHTML = `
      <h1>${escapeHtml(product.title)}</h1>
      <p>${escapeHtml(product.description)}</p>
      <div class="price">$${product.price}</div>
    `;
  } catch (err) {
    showAlert(alertBox, err.message);
  }
}

loadProduct();
