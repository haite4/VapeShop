



function validateForm(){
    const query = document.forms[0]["q"].value
    if(query.trim() === ""){
        alert("You cannot submit an empty form")
        return false
    }else{
        return true
    }
}