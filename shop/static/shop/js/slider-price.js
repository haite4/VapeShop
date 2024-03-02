


$(document).ready(function () {

    function updateProducts(data) {
  
        $('#product-container').empty();
        
      
        $('#product-container').html(data);
       
          
        
    }

    function showLoader() {
        $('#loading-indicator').show();
    }
    function hideLoader() {
        $('#loading-indicator').hide();
    }

   
    function filterProducts() {
        showLoader();
        const categorySlug = $('#category-slug').val();
        const minPrice = $('#min-price').text();
        const maxPrice = $('#max_price').val();
        const brand = $("#brand").val();   
        const flavor = $("#flavor").val();
        const fortress = $("#fortress").val();
        console.log(brand)
      

     
        $.ajax({
            url: `/shop/category/${categorySlug}/filter/?price_min=${minPrice}&price_max=${maxPrice}&brand=${brand}&flavor=${flavor}&fortress=${fortress}`,
            method: 'GET',
            success: function (data) {
                hideLoader();
                updateProducts(data.data);
              
            },
            error: function (error) {
                console.error('Error during AJAX request:', error);
            }
        });
    }
    $('#max_price').on('input', function () {
    const newValue = $(this).val();
    $('#price-range').val(newValue);
        });

    $('#price-range').on('input', function () {
        const currentValue = $(this).val();
        $('#max_price').val(currentValue);
    });

  
    $('#price-filter-btn').on('click', function () {
        filterProducts();
    });

   
    filterProducts();
});
