const apiUrl = 'http://localhost:8000/category';  // thay đổi nếu server khác

// Tải dữ liệu khi mở trang
window.onload = function () {
    loadCategories();
};

function loadCategories() {
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById("categoryTableBody");
            tbody.innerHTML = "";

            data.forEach(item => {
                const tr = document.createElement("tr");

                tr.innerHTML = `
                    <td>${item.id}</td>
                    <td>${item.madanhmuc}</td>
                    <td>${item.TenDanhMuc}</td>
                    <td><img src="${item.img_url}" alt="hình" width="50"></td>
                    <td>${item.mota || ""}</td>
                    <td>
                        <button onclick='editCategory(${JSON.stringify(item)})'>Sửa</button>
                        <button onclick='deleteCategory(${item.id})'>Xoá</button>
                    </td>
                `;

                tbody.appendChild(tr);
            });
        });

}
document.getElementById("categoryForm").addEventListener("submit", function (e) {
    e.preventDefault(); // Ngăn reload trang
    saveCategory();     // Gọi hàm lưu danh mục
});
// Hàm Lưu: Thêm mới hoặc Cập nhật
async function saveCategory() {
    const id = document.getElementById("id").value;
    const data = {
        madanhmuc: document.getElementById("madanhmuc").value,
        TenDanhMuc: document.getElementById("tendanhmuc").value,
        img_url: document.getElementById("imgurl").value,
        mota: document.getElementById("mota").value
    };

    const method = id ? "PUT" : "POST";
    const url = id ? `${apiUrl}/${id}` : apiUrl;

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            alert("Đã lưu danh mục thành công!");
            document.getElementById("categoryForm").reset();
            document.getElementById("id").value = "";
            loadCategories();
        } else {
            const errorData = await response.json();
            alert("Lỗi khi lưu danh mục: " + JSON.stringify(errorData));
        }
    } catch (error) {
        console.error("Lỗi khi gửi yêu cầu:", error);
        alert("Lỗi mạng hoặc server không phản hồi.");
    }
}

function deleteCategory(id) {
    if (confirm("Bạn có chắc chắn muốn xoá danh mục này?")) {
        fetch(`${apiUrl}/${id}`, {
            method: "DELETE"
        })
            .then(response => {
                if (response.ok) {
                    alert("Đã xoá danh mục thành công!");
                    loadCategories();
                } else {
                    alert("Lỗi khi xoá danh mục.");
                }
            })
            .catch(error => {
                console.error("Lỗi khi gửi yêu cầu xoá:", error);
                alert("Lỗi mạng hoặc server không phản hồi.");
            });
    }
}
function editCategory(item) {
    document.getElementById("id").value = item.id;
    document.getElementById("madanhmuc").value = item.madanhmuc;
    document.getElementById("tendanhmuc").value = item.TenDanhMuc;
    document.getElementById("imgurl").value = item.img_url;
    document.getElementById("mota").value = item.mota || "";
}

function resetForm() {
    document.getElementById("categoryForm").reset();
    document.getElementById("id").value = "";
}



