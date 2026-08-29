async function createOrder(event){
	event.preventDefault();
	let userId= localStorage.getItem("user_id")
	if(userId === null){
		alert("No user logged");
		return;
	}
	let currentDate = new Date().toJSON().slice(0, 10);
	try{
		const response = await fetch("/orders/create_order", { 
			method: "POST", 
			headers: { "Content-Type": "application/json" }, 
			body: JSON.stringify({ 
				user_id : userId,
				created_at : currentDate
			})
		});
		console.log("prima di json");
		console.log("Response:", response);
        console.log("Status:", response.status);
        console.log("OK:", response.ok);
		const order = await response.json(); 
		console.log("Order:", order);
		localStorage.setItem("order_id", order.id);
		
	}catch(error){
		console.error("Error order creation:", error); 
		throw error; 	
	}
		
}

async function addToCart(productId) {
	let quantity_id= "quantity-"+ "" + productId;
	let quantity = document.getElementById(quantity_id).value;
	let orderId= localStorage.getItem("order_id")
	
	if(orderId ===null){
		alert("No order created");
		return null;
	}
	console.log("orderId:", orderId);
	console.log("productId:", productId);
	console.log("quantity:", quantity);
	
	try { 
		const response = await fetch("/order_items/create_order_item", { 
			method: "POST", 
			headers: { "Content-Type": "application/json" }, 
			body: JSON.stringify({ 
				order_id: orderId, 
				product_id: productId,
				quantity: quantity 
			})
		});
		if (!response.ok) {
			throw new Error(`Errore HTTP: ${response.status}`); 
		} 
		const data = await response.json(); 
		console.log("Order item creato:", data);
		return data; 
	} catch (error) {
		console.error("Error order item creation:", error); 
		throw error; 
	}	

    }
