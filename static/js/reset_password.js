function resetPassword() {
    const form = document.getElementById('resetPasswordForm');
    const formData = new FormData(form);
    const email = formData.get('email'); // Get the email from the form data
    const newPassword = formData.get('new_password'); // Get the new password from the form data

    // Create a JSON object to send with the PUT request
    const data = {
        email: email,
        new_password: newPassword
    };

    fetch('/reset_password', {
        method: 'PUT',  // Use PUT request for updating the password
        headers: {
            'Content-Type': 'application/json' // Set content type to JSON
        },
        body: JSON.stringify(data) // Convert the data object to a JSON string
    })
    .then(response => {
        return response.json().then(data => {
            if (response.ok) {
                alert(data.message || "Password updated successfully");
                window.location.href = "/login";  // Redirect on success
            } else {
                alert(data.message || "Error updating password");
            }
        });
    })
    .catch(error => {
        alert("An unexpected error occurred. Please try again.");
        console.error("Error:", error);
    });
}
