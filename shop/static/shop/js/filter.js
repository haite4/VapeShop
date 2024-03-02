


//  const forms = document.querySelector("form[name=filter]")

// forms.addEventListener("submit", function(e){
//     e.preventDefault()
//     let url =  this.action;
//     let params =  new URLSearchParams(new FormData(this)).toString();
//     getrequestsend(url,params)
// })



// function getrequestsend(url, params){
//             fetch(`${url}?${params}`,{
//                 method:"GET",
//                 headers:{
//                     "Content-Type":"application/x-www-form-urlencoded"
//                 }  
//             })
//             .then((response) => response.json())
//             .then(function(response){
//                 if(response){
//                     updateproduct(response.brand)
//                 }
//             })
//             .catch(error => console.error(error))
// }



// function updateproduct(html){
//     var tempDiv = document.createElement('div');
//     tempDiv.innerHTML = html;

//     // Используем querySelector для поиска нужного блока HTML-кода
//     var wishlistContent = tempDiv.querySelector("#product-container").innerHTML;

//     // Теперь у вас есть только HTML-код блока с классом "favorites-container"
//     const container = document.querySelector("#product-container");
//     container.innerHTML = wishlistContent;
// }