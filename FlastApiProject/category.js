window.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
        alert("Chưa đăng nhập!");
        window.location.href = "login.html";
        return;
    }

    try {
        const res = await fetch("http://127.0.0.1:8000/profile", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.detail);
        }

        if (window.location.pathname.includes("admin.html") && data.username !== "admin") {
            alert("Bạn không có quyền truy cập trang quản trị!");
            window.location.href = "login.html";
        }
    } catch (err) {
        alert("Phiên đăng nhập không hợp lệ hoặc đã hết hạn!");
        window.location.href = "login.html";
    }

    //  Fetch danh mục
    fetch("http://localhost:8000/category")
        .then(response => response.json())
        .then(data => {
            const grid = document.getElementById("categoryGrid");
            data.forEach(item => {
                const div = document.createElement("div");
                div.className = "category-item";
                div.innerHTML = `
                    <img src="${item.img_url}" alt="${item.TenDanhMuc}">
                    <p>${item.TenDanhMuc}</p>
                `;

                div.dataset.id = item.id;
                div.addEventListener("click", () => {
                    window.location.href = `products.html?categoryId=${item.id}`;
                });

                grid.appendChild(div);
            });
        });
});
