let currentPage = 1;
let searchMode = false;

const alertBox = document.getElementById("alert");
const grid = document.getElementById("grid");
const pagination = document.getElementById("pagination");
const searchForm = document.getElementById("search-form");
const searchInput = document.getElementById("search-input");
const clearSearchBtn = document.getElementById("clear-search");

function renderGrid(products) {
  if (!products || products.length === 0) {
    grid.innerHTML = '<p class="empty">No products found.</p>';
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
        <a class="btn" href="product.html?id=${p.id}">View</a>
      </div>
    </div>
  `
    )
    .join("");
}

function renderPagination(page, itemCount) {
  if (searchMode) {
    pagination.innerHTML = "";
    return;
  }

  pagination.innerHTML = `
    <button id="prev-btn" ${page <= 1 ? "disabled" : ""}>Prev</button>
    <span>Page ${page}</span>
    <button id="next-btn" ${itemCount < 4 ? "disabled" : ""}>Next</button>
  `;

  document.getElementById("prev-btn").addEventListener("click", () => {
    if (currentPage > 1) {
      currentPage -= 1;
      loadPage(currentPage);
    }
  });
  document.getElementById("next-btn").addEventListener("click", () => {
    currentPage += 1;
    loadPage(currentPage);
  });
}

async function loadPage(page) {
  alertBox.innerHTML = "";
  searchMode = false;
  try {
    const result = await apiFetch(`/product/bypage?page=${page}`);
    renderGrid(result.data);
    renderPagination(page, result.data.length);
  } catch (err) {
    renderGrid([]);
    renderPagination(page, 0);
  }
}

async function runSearch(title) {
  alertBox.innerHTML = "";
  searchMode = true;
  try {
    const products = await apiFetch(`/products/search?title=${encodeURIComponent(title)}`);
    renderGrid(products);
    renderPagination(1, 0);
  } catch (err) {
    renderGrid([]);
  }
}

searchForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const title = searchInput.value.trim();
  if (!title) return;
  runSearch(title);
});

clearSearchBtn.addEventListener("click", () => {
  searchInput.value = "";
  currentPage = 1;
  loadPage(currentPage);
});

loadPage(currentPage);
