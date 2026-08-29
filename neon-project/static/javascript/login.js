async function login(event) {
	event.preventDefault();
	let email = document.getElementById("email").value;
	
	try { 
		const response = await fetch(`/users/login?email_address=${encodeURIComponent(email)}`);
		if (!response.ok) {
			alert("Email not found")
			throw new Error(`Errore HTTP: ${response.status}`); 
		} 
		
		const user = await response.json(); 
		console.log("User:", user);
		localStorage.setItem("user_id", user.id)
		return user; 
	} catch (error) {
		console.error("Error unable to find use:", error); 
		throw error; 
	}	

}