// Add your JavaScript code here
function buyProduct(productId) {
    // Make a POST request to the FastAPI endpoint for purchasing the product
    fetch(`http://localhost:8000/buy/${productId}`, {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
