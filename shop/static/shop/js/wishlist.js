

const removeButtons = document.querySelectorAll('.wishlist-remove-button');




document.addEventListener('click', function(event) {
    console.log(event.target)
    if (event.target.matches('.icon-heart')) {
        const product_id = event.target.getAttribute('data-product-id');
        addWishlist(product_id);
    }
});


const csrftoken = getCSRFToken();

function addWishlist(product_id){
    fetch("/shop/add_to_whishlist/",{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "X-CSRFToken": csrftoken,
        },
        
        body:JSON.stringify(product_id)

    })
    .then(function(response) {
        return response.json();
    })
    .then(function(response) {
        if (response.status) {
            updateWishlistCount()
            Toastify({
                text: response.status,
                duration: 3000, 
                close: true, 
                gravity: "top", 
                backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)" 
            }).showToast();
}  else if (response.failed) {
    Toastify({
        text: response.failed,
        duration: 3000, // Время отображения уведомления в миллисекундах
        close: true, // Позволяет закрыть уведомление
        gravity: "top", // Позиция отображения уведомления (top, bottom)
        backgroundColor: "linear-gradient(to right, #ff0000, #ff6347)" // Цвет фона уведомления
    }).showToast();

   
}})}

  
    
 removeButtons.forEach(function(button) {
     button.addEventListener('click', function() {
         const remove_product_id = this.getAttribute('data-product-id');
         removewishlistitem(remove_product_id);
     })
 })

function removewishlistitem(remove_product_id){
    fetch("/shop/remove_wishlist_item/",{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "X-CSRFToken": csrftoken,
        },
        body:JSON.stringify(remove_product_id)
    })
    .then(function(response) {
        return response.json(); 
    })
    .then(function(response) {
       
        if (response.status) {
            updateWishlistContent()
            Toastify({
                text: response.status,
                duration: 3000, // Время отображения уведомления в миллисекундах
                close: true, // Позволяет закрыть уведомление
                gravity: "top", // Позиция отображения уведомления (top, bottom)
                backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)" // Цвет фона уведомления

            }).showToast();
        }else if (response.error) {
            Toastify({
                text: response.error,
                duration: 3000, // Время отображения уведомления в миллисекундах
                close: true, // Позволяет закрыть уведомление
                gravity: "top", // Позиция отображения уведомления (top, bottom)
                backgroundColor: "linear-gradient(to right, #ff0000, #ff6347)" // Цвет фона уведомления
            }).showToast();

        }})}

        function updateWishlistContent() {
            fetch("/shop/wishlist/")
                .then(response => response.text())
                .then(html => {
                    // Создаем временный элемент div для парсинга HTML-кода
                    var tempDiv = document.createElement('div');
                    tempDiv.innerHTML = html;
        
                    // Используем querySelector для поиска нужного блока HTML-кода
                    var wishlistContent = tempDiv.querySelector(".main-favorite-container").innerHTML;
        
                    // Теперь у вас есть только HTML-код блока с классом "favorites-container"
                    const container = document.querySelector(".main-favorite-container");
                    container.innerHTML = wishlistContent;
                    attachEventListeners();
                    updateWishlistCount()
                
                    
                })
                .catch(error => console.error("Ошибка при обновлении содержимого списка желаний:", error));
        }

        function attachEventListeners() {
            const removeButtons = document.querySelectorAll('.wishlist-remove-button');
            removeButtons.forEach(function(button) {
                button.addEventListener('click', function() {
                    const remove_product_id = this.getAttribute('data-product-id');
                    removewishlistitem(remove_product_id);
                });
            });
        }

function updateWishlistCount() {
    fetch("/shop/get_wishlist_count/")
        .then(response => response.json())
        .then(data => {
                  if(data.wishlist_count){

                      document.getElementById('wishlist-count').innerHTML = data.wishlist_count;
                  }else{
                    document.getElementById('wishlist-count').innerHTML = 0;
                  }
                
          
            // Находим элемент с id 'wishlist-count' и обновляем его содержимое
        })
        
        .catch(error => console.error('Ошибка при получении данных:', error));
}

// Вызываем функцию обновления количества при загрузке страницы
updateWishlistCount();


function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith('csrftoken=')) {
            return cookie.substring('csrftoken='.length, cookie.length);
        }
    }
    return null;
}


