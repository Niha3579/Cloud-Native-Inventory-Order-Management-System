document.addEventListener('DOMContentLoaded', () => {
    // Check if user is logged in (using userId from our new auth logic)
    if (!localStorage.getItem('userId')) {
        window.location.href = '/frontend/index.html';
    }

    // Set Welcome Message
    const userName = localStorage.getItem('userName');
    if(userName) {
        // You can add an element with id="welcomeMessage" in your sidebar to show this
        console.log(`Welcome, ${userName}`); 
    }

    // Logout functionality
    document.getElementById('logoutBtn').addEventListener('click', () => {
        localStorage.clear();
        window.location.href = '/frontend/index.html';
    });

    // Load initial data
    loadProducts();

    // Tab switch listeners
    const tabElements = document.querySelectorAll('a[data-bs-toggle="pill"]');
    tabElements.forEach(tab => {
        tab.addEventListener('shown.bs.tab', (event) => {
            const targetId = event.target.getAttribute('href');
            if (targetId === '#products-tab') loadProducts();
            if (targetId === '#orders-tab') document.getElementById('orders-content').innerHTML = "Orders coming soon...";
            if (targetId === '#users-tab') document.getElementById('users-content').innerHTML = "Users coming soon...";
        });
    });

    // Add Product Button Listener (Simple prompt for now, can be upgraded to a Modal)
    const addProductBtn = document.querySelector('#products-tab .btn-primary');
    if (addProductBtn) {
        addProductBtn.addEventListener('click', createProduct);
    }
});

// --- Product Functions ---

async function loadProducts() {
    const container = document.getElementById('products-content');
    container.innerHTML = '<div class="spinner-border text-primary" role="status"></div>';
    
    try {
        // Calls GET /products/
        const products = await api.fetch('/products/'); 
        
        if (products.length === 0) {
            container.innerHTML = '<p class="text-muted">No products found.</p>';
            return;
        }

        let html = `
            <table class="table table-striped table-hover align-middle">
                <thead class="table-dark">
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Price</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        products.forEach(p => {
            html += `
                <tr>
                    <td>${p.id}</td>
                    <td class="fw-bold">${p.name}</td>
                    <td>${p.description || '-'}</td>
                    <td>$${p.price.toFixed(2)}</td>
                    <td>
                        <button class="btn btn-sm btn-danger" onclick="deleteProduct(${p.id})">Delete</button>
                    </td>
                </tr>
            `;
        });
        
        html += '</tbody></table>';
        container.innerHTML = html;
    } catch (error) {
        container.innerHTML = `<div class="alert alert-danger">Error loading products: ${error.message}</div>`;
    }
}

async function createProduct() {
    const addProductForm = document.getElementById('addProductForm');
    if (addProductForm) {
        addProductForm.addEventListener('submit', async (e) => {
            e.preventDefault(); // Prevent page reload
            
            // Get values from the modal
            const name = document.getElementById('prodName').value;
            const description = document.getElementById('prodDescription').value;
            const price = parseFloat(document.getElementById('prodPrice').value);

            try {
                // Send data to FastAPI backend
                await api.fetch('/products/', {
                    method: 'POST',
                    body: JSON.stringify({ name, description, price })
                });
                
                // 1. Hide the modal
                const modalElement = document.getElementById('addProductModal');
                const modalInstance = bootstrap.Modal.getInstance(modalElement);
                modalInstance.hide();

                // 2. Clear the form fields for next time
                addProductForm.reset();

                // 3. Reload the table to show the new product
                loadProducts();

            } catch (error) {
                alert(`Failed to create product: ${error.message}`);
            }
        });
    }
}


// Make sure deleteProduct is available globally so inline onclick can access it
window.deleteProduct = async function(id) {
    if (!confirm("Are you sure you want to delete this product?")) return;

    try {
        // Calls DELETE /products/{id}
        await api.fetch(`/products/${id}`, {
            method: 'DELETE'
        });
        
        // Reload table after deletion
        loadProducts();
    } catch (error) {
        alert(`Failed to delete product: ${error.message}`);
    }
}