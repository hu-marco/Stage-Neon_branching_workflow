function viewOrder(orderId){
	localStorage.setItem("viewed_order_id", orderId);
	document.location.href = "/order_item_site";
}