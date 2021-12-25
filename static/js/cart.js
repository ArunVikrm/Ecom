var updateBts = document.getElementsByClassName('update-cart')

for(i=0 ; i<updateBts.length ; i++){
    updateBts[i].addEventListener('click' , function(){
        var product_id = this.dataset.product
        var action = this.dataset.action
        console.log(product_id , action)

        console.log(user)
        if(user == 'AnonymousUser'){
            console.log("user is not authenticated")
        }
        else{
            updateUserOrder(product_id,action)
        }
    })
}

function updateUserOrder(product_id,action){
    console.log("User is authenticated")

    var url = '/update_item/'
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken' : csrftoken,   
        },
        body:JSON.stringify({'product_id':product_id,'action':action})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log('data:',data)
        location.reload()
    })
}