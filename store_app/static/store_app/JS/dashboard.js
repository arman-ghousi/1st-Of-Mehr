// On document load control menu bar functionality for both mobile (Hamburger menu) and Desktop
document.addEventListener('DOMContentLoaded', () => {
    // Create a variable for navbar item
    const navbar = document.getElementById('navbar');
    const menuButton = document.getElementById('menu-button');

    // Initially display purchase history section and hide other sections
    document.getElementById('history-section').style.display = "block";
    document.getElementById('favorites-section').style.display = "none";
    document.getElementById('reviews-section').style.display = "none";
    document.getElementById('settings-section').style.display = "none";
    
    // Toggle function to control visibility
    const toggle = (element) => {
        if (element.style.display == "none") {
            element.style.display = "block";
        }
        else {
            element.style.display = "none";
        }
    }

    // If view port is a tablet or mobile display Hamburger menu
    if (window.screen.width <= 769) {
        navbar.style.display = "none";
        menuButton.style.display = "block";
    }
    // Otherwise display long desktop menu
    else {
        navbar.style.display = "block";
        menuButton.style.display = "none";
    }

    // When menu button is click toggle visibility
    menuButton.onclick = () => {
        toggle(navbar);
    }

    // Declare button nodeList and Array for later manipulation
    const buttonList = document.querySelectorAll('.button');
    const buttonArray = Array.from(buttonList);

    // Add click event to each button and display the corresponding section
    buttonList.forEach(button => button.onclick = () => {
        let buttonIndex = buttonArray.indexOf(button);
        for (let element of buttonList) {
            let elementIndex = buttonArray.indexOf(element);

            if (buttonIndex != elementIndex) {
                document.getElementById(`${element.id}-section`).style.display = "none";
            }
            else {
                document.getElementById(`${element.id}-section`).style.display = "block";
            }
        }
    });
});