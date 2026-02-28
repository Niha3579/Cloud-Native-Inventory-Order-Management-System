document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;

            try {
                // Calls POST /users/login
                const data = await api.fetch('/users/login', {
                    method: 'POST',
                    body: JSON.stringify({ email, password })
                });
                
                // Save user details to localStorage
                localStorage.setItem('userId', data.user_id);
                localStorage.setItem('userName', data.name);
                
                // Redirect to dashboard
                window.location.href = '/frontend/dashboard.html';
            } catch(err) { 
                alert(`Login failed: ${err.message}`); 
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = document.getElementById('regName').value;
            const email = document.getElementById('regEmail').value;
            const password = document.getElementById('regPassword').value;

            try {
                // Calls POST /users/register
                await api.fetch('/users/register', {
                    method: 'POST',
                    body: JSON.stringify({ name, email, password })
                });
                
                alert('Registration successful! Please log in.');
                
                // Switch from Register modal to Login modal
                const registerModal = bootstrap.Modal.getInstance(document.getElementById('registerModal'));
                registerModal.hide();
                const loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
                loginModal.show();
                
            } catch(err) {
                alert(`Registration failed: ${err.message}`);
            }
        });
    }
});