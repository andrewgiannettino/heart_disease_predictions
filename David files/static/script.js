// JavaScript code to interact with the HTML elements

// Wait for the DOM to fully load before running the script
document.addEventListener('DOMContentLoaded', (event) => {
    // Get references to the HTML elements
    const button = document.getElementById('myButton');
    const message = document.getElementById('message');

    // Add an event listener to the button
    button.addEventListener('click', function() {
        // Update the text content of the paragraph
        message.textContent = 'The button has been clicked!';

        // Change the color of the paragraph text
        message.style.color = 'blue';

        // Optionally, you can add more style changes
        message.style.fontWeight = 'bold';
        message.style.fontSize = '28px';
    });
});