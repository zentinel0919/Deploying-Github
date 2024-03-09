// Add your JavaScript code here
function buyProduct(productName) {
    // Make a POST request to the FastAPI endpoint for purchasing the product
    fetch('/buy', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product_name: productName })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
