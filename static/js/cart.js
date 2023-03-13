var updateBtns = document.getElementsByClassName('update-cart')
for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var imageId = this.dataset.imageid
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action, 'imageId:', imageId)
		console.log('USER:', user)

		if (user == 'AnonymousUser'){
			addCookieItem(productId, action, imageId)
		}else{
			updateUserOrder(productId, action, imageId)
		}
	})
}
function updateUserOrder(productId, action, imageId){
	console.log('User is authenticated, sending data...')
	console.log(JSON.stringify({'productId':productId, 'action':action, 'imageId':imageId}))
	var url = '/update_item/'

	fetch(url, {
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
		}, 
		body:JSON.stringify({'productId':productId, 'action':action, 'imageId':imageId})
	})
	.then((response) => {
		return response.json();
	})
	.then((data) => {
		location.href = "/cart"
	});
}

function addCookieItem(productId, action, imageId){
	console.log('User is not authenticated')

	var cartChildId = productId + '@' + imageId
	
	if (action == 'add'){
		if (cart[cartChildId] == undefined){
		cart[cartChildId] = {'quantity':1}
		}else{
			cart[cartChildId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[cartChildId]['quantity'] -= 1

		if (cart[cartChildId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[cartChildId];
		}
	}
	console.log('CART:', JSON.stringify(cart))
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.href = "/cart"

}