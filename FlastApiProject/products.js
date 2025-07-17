window.addEventListener("DOMContentLoaded", async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const categoryId = urlParams.get("categoryId");

    if (!categoryId) {
        alert("Thiếu ID danh mục!");
        return;
    }

    try {
        const response = await fetch(`http://localhost:8000/products?categoryId=${categoryId}`);
        const data = await response.json();

        const grid = document.getElementById("productGrid");
        data.forEach(item => {
            const div = document.createElement("div");
            div.className = "product-item";
            div.innerHTML = `
                <img src="${item.img_urlprd}" alt="${item.nameprd}">
                <div class="product-name">${item.nameprd}</div>
                <div class="product-price">${item.price.toLocaleString()} VND</div>
                <div class="product-qty">Số lượng: ${item.quantity}</div>
            `;
            grid.appendChild(div);
        });
    } catch (err) {
        console.error("Lỗi khi tải sản phẩm:", err);
        alert("Không thể tải danh sách sản phẩm.");
    }
});
