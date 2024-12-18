document.addEventListener("DOMContentLoaded", function () {
    const body = document.querySelector('body');
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const darkModeStatus = document.getElementById('dark-mode-status'); // New element for displaying status
    const svgGroups = document.querySelectorAll('svg g'); // Select all <g> elements in SVGs

    // Function to update the fill color for all SVG <g> elements
    function updateSvgFill() {
        svgGroups.forEach(svgGroup => {
            if (body.classList.contains('dark-mode')) {
                svgGroup.setAttribute('fill', '#ffffff'); // White fill for dark mode
            } else {
                svgGroup.setAttribute('fill', '#000000'); // Black fill for light mode
            }
        });
    }

    // Function to update the dark mode status text
    function updateDarkModeStatus() {
        const isDarkMode = body.classList.contains('dark-mode');
        if (darkModeStatus) {
            darkModeStatus.textContent = `Dark mode: ${isDarkMode ? 'ON' : 'OFF'}`;
        }
    }

    // Check the dark mode preference in localStorage and apply it
    if (localStorage.getItem('dark-mode') === 'enabled') {
        body.classList.add('dark-mode');
    }

    updateDarkModeStatus(); // Initial status update
    updateSvgFill(); // Initial SVG fill update

    // Event listener for the dark mode toggle
    darkModeToggle.addEventListener('click', function () {
        body.classList.toggle('dark-mode');

        // Save the dark mode preference in localStorage
        if (body.classList.contains('dark-mode')) {
            localStorage.setItem('dark-mode', 'enabled');
        } else {
            localStorage.setItem('dark-mode', 'disabled');
        }

        updateDarkModeStatus(); // Update the status after toggling
        updateSvgFill(); // Update the SVG fill color on toggle
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
            const author = book.querySelector('.author').textContent.toLowerCase();
            const publisher = book.querySelector('.publisher').textContent.toLowerCase();
            const publicationYear = book.querySelector('.publication-year').textContent.toLowerCase();

            if (
                title.includes(searchQuery) ||
                author.includes(searchQuery) ||
                publisher.includes(searchQuery) ||
                publicationYear.includes(searchQuery)
            ) {
                book.style.display = '';  // Show matching books
            } else {
                book.style.display = 'none';  // Hide non-matching books
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    // Add Book form validation
    const form = document.querySelector('.add-form');
    form.addEventListener('submit', function (event) {
        const isbn = document.getElementById('isbn').value.trim();
        const title = document.getElementById('title').value.trim();
        const author = document.getElementById('author').value.trim();
        const publisher = document.getElementById('publisher').value.trim();
        const publicationYear = document.getElementById('publicationyear').value.trim();
        const isbnRegex = /^\d{10}|\d{13}$/;  // ISBN must be either 10 or 13 digits

        // Check if required fields are filled
        if (!isbn || !title || !author || !publisher || !publicationYear) {
            alert('Please fill out all required fields.');
            event.preventDefault();  // Prevent form submission
            return;
        }

        // Validate ISBN format
        if (!isbnRegex.test(isbn)) {
            alert('ISBN must be either 10 or 13 digits.');
            event.preventDefault();
            return;
        }

        // Validate publication year within the allowed range
        const publicationYearNum = parseInt(publicationYear, 10);
        if (publicationYearNum < 1000 || publicationYearNum > 2099) {
            alert('Please select a valid publication year.');
            event.preventDefault();
            return;
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    // Member form validation
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

document.addEventListener("DOMContentLoaded", function() {
    const checkboxes = document.querySelectorAll(".publisher-checkbox");
    const filterForm = document.getElementById("filter-form");
    checkboxes.forEach((checkbox) => {
        checkbox.addEventListener("change", () => {
            filterForm.submit();
        });
    });
});

function filterDropdown(inputId, optionClass) {
    var input, filter, ul, li, a, i;
    input = document.getElementById(inputId);
    filter = input.value.toUpperCase();
    div = input.closest('.dropdown');
    a = div.getElementsByClassName(optionClass);
    for (i = 0; i < a.length; i++) {
        txtValue = a[i].textContent || a[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            a[i].style.display = "";
        } else {
            a[i].style.display = "none";
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // For Member dropdown
    document.querySelectorAll('.member-option').forEach(item => {
        item.addEventListener('click', event => {
            event.preventDefault();
            document.getElementById('memberDropdown').textContent = item.textContent;
            document.getElementById('selectedMemberId').value = item.getAttribute('data-value');
            console.log('Selected Member ID:', document.getElementById('selectedMemberId').value);  // Add this line
        });
    });

    // For Book dropdown
    document.querySelectorAll('.book-option').forEach(item => {
        item.addEventListener('click', event => {
            event.preventDefault();
            document.getElementById('bookDropdown').textContent = item.textContent;
            document.getElementById('selectedBookId').value = item.getAttribute('data-value');
            console.log('Selected Book ID:', document.getElementById('selectedBookId').value);  // Add this line
        });
    });
});

document.getElementById('borrowForm').addEventListener('submit', function(event) {
    var memberId = document.getElementById('selectedMemberId').value;
    var bookId = document.getElementById('selectedBookId').value;
    document.getElementById('debugMemberId').textContent = memberId;
    document.getElementById('debugBookId').textContent = bookId;
    console.log('Form submitted with Member ID:', memberId, 'and Book ID:', bookId);
});

function populateEditFormFromData(button) {
    const bookid = button.dataset.bookid;
    const title = button.dataset.title;
    const author = button.dataset.author;
    const publisher = button.dataset.publisher;
    const publicationYear = button.dataset.publicationyear;

    const form = document.getElementById('editBookForm');
    form.action = `/books/edit_book/${bookid}`;

    document.getElementById('editTitle').value = title;
    document.getElementById('editAuthor').value = author;
    document.getElementById('editPublisher').value = publisher;
    document.getElementById('editPublicationYear').value = publicationYear;
    document.getElementById('editBookModal').addEventListener('hide.bs.modal', function () {
        document.getElementById('editBookForm').reset();
    });
}

function setDeleteFormAction(bookid) {
    document.getElementById('deleteBookForm').action = `/books/delete_book/${bookid}`;
}

function openEditModal(id, firstname, lastname, email, profilePicture) {
    // Populate modal fields with the member's data
    document.getElementById('memberid').value = id;
    document.getElementById('firstname').value = firstname;
    document.getElementById('lastname').value = lastname;
    document.getElementById('email').value = email;
    
    // Set the profile picture
    var profilePicElement = document.getElementById('modalProfilePicture');
    profilePicElement.src = profilePicture ? profilePicture : '/static/default-profile.jpg';
    
    // Show the modal
    var editMemberModal = new bootstrap.Modal(document.getElementById('editMemberModal'));
    editMemberModal.show();
}