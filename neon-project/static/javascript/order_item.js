async function applyCoupon(event) {
    event.preventDefault();

    let couponId = document.getElementById("coupon_id").value.trim();
    let orderId = localStorage.getItem("viewed_order_id");

    if (!couponId) {
        alert("Coupon_id not inserted");
        return;
    }

    if (!orderId) {
        alert("Order ID not found");
        return;
    }

    try {
        const setCouponResponse = await fetch(
            `/orders/set_coupon?order_id=${encodeURIComponent(orderId)}&coupon_id=${encodeURIComponent(couponId)}`,
            {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json"
                }
            }
        );

        if (!setCouponResponse.ok) {
            alert("Set coupon id failed");
            throw new Error(`Errore HTTP: ${setCouponResponse.status}`);
        }

        const discountResponse = await fetch(
            `/orders/apply_discount?order_id=${encodeURIComponent(orderId)}`,
            {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json"
                }
            }
        );

        if (!discountResponse.ok) {
            alert("Apply coupon failed");
            throw new Error(`Errore HTTP: ${discountResponse.status}`);
        }

        console.log("Coupon applied successfully");

    } catch (error) {
        console.error("Error operation:", error);
    }
}

async function getTotal(event) {
	event.preventDefault();
	let orderId=localStorage.getItem("viewed_order_id");
	let content = document.getElementById("total");

    
	if( orderId==null){
		alert("orderId not present");
	}else{
		try { 
			const response = await fetch(`/orders/get_total_price?order_id=${encodeURIComponent(orderId)}`
		);
			if (!response.ok) {
				alert("Get total failed");
				throw new Error(`Errore HTTP: ${response.status}`); 
			} 
			
			let total = await response.json(); 
			content.textContent = "€"+ "" + total.total_price;
		
		} catch (error) {
			console.error("Error operation:", error); 
			throw error; 
		}	
	}
}

async function calculateTotal(event) {
	event.preventDefault();
	let orderId=localStorage.getItem("viewed_order_id");
    
	if( orderId==null){
		alert("orderId not present");
	}else{
		try { 
			const response = await fetch(`/orders/calculate_total?order_id=${encodeURIComponent(orderId)}`,
            {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json"
                }
            }
        );
			if (!response.ok) {
				alert("Set coupon id failed");
				throw new Error(`Errore HTTP: ${response.status}`); 
			} 
			alert("Total calculated")
		
		} catch (error) {
			console.error("Error operation:", error); 
			throw error; 
		}	
	}
}