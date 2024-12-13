var updateBtn = document.getElementsByClassName('update-cart');

for (var i = 0; i < updateBtn.length; i++) {
    updateBtn[i].addEventListener('click', function () {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId', productId, 'action', action);
        console.log('user:', user);

        // Kiểm tra xem user đã đăng nhập vào chưa
        if (user === "AnonymousUser") {
            console.log('user not logged in');
        } else {
            // Xác thực phần tử csrfmiddlewaretoken tồn tại trước khi đọc giá trị
            var csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
            if (csrfTokenElement) {
                var csrfToken = csrfTokenElement.value;
                updateUserOrder(productId, action, csrfToken);
            } else {
                console.log('Cannot find CSRF token element');
            }
        }
    });
}

// Định nghĩa hàm update
function updateUserOrder(productId, action, csrfToken) {
    console.log('user login, success add');
    var url = '/update_item/';
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        //  Tìm hiểu vể stringify
        body: JSON.stringify({'productId': productId, 'action': action })
    })
        .then((response) => {
            return response.json();
        })
        .then((data) =>{
            console.log('data', data);
            location.reload();
        });
}
