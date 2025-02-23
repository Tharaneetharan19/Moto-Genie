// Function to handle form submissions for car specification and comparison
document.addEventListener('DOMContentLoaded', function () {
    
    // Car Specification Form Submission
    const carSpecForm = document.querySelector('#carSpecForm');
    if (carSpecForm) {
        carSpecForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const company = document.querySelector('#company').value;
            const model = document.querySelector('#model').value;
            const userQuery = document.querySelector('#user_query').value;

            if (company && model && userQuery) {
                const responseContainer = document.querySelector('.response');
                responseContainer.innerHTML = '<p>Loading...</p>';

                try {
                    const response = await fetch('/api/car-specification', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            company: company,
                            model: model,
                            user_query: userQuery
                        })
                    });

                    const data = await response.json();
                    if (data.error) {
                        responseContainer.innerHTML = `<p>Error: ${data.error}</p>`;
                    } else {
                        responseContainer.innerHTML = `<p>${data.response}</p>`;
                    }
                } catch (error) {
                    responseContainer.innerHTML = `<p>An error occurred: ${error}</p>`;
                }
            } else {
                alert('Please fill out all fields.');
            }
        });
    }

    // Car Comparison Form Submission
    const carComparisonForm = document.querySelector('#carComparisonForm');
    if (carComparisonForm) {
        carComparisonForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const company1 = document.querySelector('#company1').value;
            const model1 = document.querySelector('#model1').value;
            const company2 = document.querySelector('#company2').value;
            const model2 = document.querySelector('#model2').value;
            const userRequirements = document.querySelector('#user_requirements').value;

            if (company1 && model1 && company2 && model2 && userRequirements) {
                const responseContainer = document.querySelector('.response');
                responseContainer.innerHTML = '<p>Loading comparison report...</p>';

                try {
                    const response = await fetch('/api/car-comparison', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            company1: company1,
                            model1: model1,
                            company2: company2,
                            model2: model2,
                            user_requirements: userRequirements
                        })
                    });

                    const data = await response.json();
                    if (data.error) {
                        responseContainer.innerHTML = `<p>Error: ${data.error}</p>`;
                    } else {
                        responseContainer.innerHTML = `<p>${data.response}</p>`;
                    }
                } catch (error) {
                    responseContainer.innerHTML = `<p>An error occurred: ${error}</p>`;
                }
            } else {
                alert('Please fill out all fields.');
            }
        });
    }
    
});

// JavaScript for handling feedback form submission via AJAX
document.getElementById('feedbackForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    
    // Collect form data
    const name = document.getElementById('name').value;
    const contact = document.getElementById('contact').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;

    // Send the data to the server via POST request
    const response = await fetch('/submit_feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, contact, email, message })
    });

    // Handle response
    if (response.ok) {
        alert('Feedback submitted successfully!');
        document.getElementById('feedbackForm').reset();
    } else {
        alert('Failed to submit feedback. Please try again.');
    }
});

