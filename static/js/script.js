document.addEventListener("DOMContentLoaded", function () {
    const body = document.querySelector('body');
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const logo = document.getElementById('logo');

    // Check the dark mode preference in localStorage and apply it
    if (localStorage.getItem('dark-mode') === 'enabled') {
        body.classList.add('dark-mode');
        logo.src = 'static/images/logo_grey.png';  // Change to dark mode logo
    }

    darkModeToggle.addEventListener('click', function () {
        body.classList.toggle('dark-mode');

        // Update the logo and save dark mode preference
        if (body.classList.contains('dark-mode')) {
            logo.src = 'static/images/logo_grey.png';  // Dark mode logo
            localStorage.setItem('dark-mode', 'enabled');
        } else {
            logo.src = 'static/images/logo_white.png';  // Light mode logo
            localStorage.setItem('dark-mode', 'disabled');
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    // Search functionality
    const searchBar = document.getElementById('search-bar');
    const bookItems = document.querySelectorAll('.scroll-container li');

    searchBar.addEventListener('input', function () {
        const searchQuery = searchBar.value.toLowerCase();
        bookItems.forEach(book => {
            const title = book.querySelector('strong').textContent.toLowerCase();
            if (title.includes(searchQuery)) {
                book.style.display = '';  // Show matching books
            } else {
                book.style.display = 'none';  // Hide non-matching books
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    // Form validation
    const form = document.getElementById('add-member-form');
    form.addEventListener('submit', function (event) {
        const firstName = document.getElementById('firstname').value.trim();
        const lastName = document.getElementById('lastname').value.trim();
        const email = document.getElementById('email').value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;  // Simple email format validation

        if (firstName === '' || lastName === '' || email === '') {
            alert('Please fill out all required fields.');
            event.preventDefault();  // Stop form from submitting
            return;
        }

        if (!emailRegex.test(email)) {
            alert('Please enter a valid email address.');
            event.preventDefault();  // Stop form from submitting
            return;
        }

        // Optionally, validate other form fields if needed
    });
    
});

document.addEventListener('DOMContentLoaded', function () {
    // Initialize Hammer.js for touch-based horizontal scrolling
    var scrollContainer = document.getElementById("scroll-container");
    var hammer = new Hammer(scrollContainer);

    hammer.get("swipe").set({ direction: Hammer.DIRECTION_HORIZONTAL });

    hammer.on("swipeleft", function () {
        scrollContainer.scrollLeft += 300;  // Adjust scroll distance as needed
    });

    hammer.on("swiperight", function () {
        scrollContainer.scrollLeft -= 300;
    });
});
