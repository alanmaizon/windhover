# Windhover

# Library Management System

Welcome to the **Windhover Library Management System**, a web application where you can browse books, manage member information, and track borrowing history. Link to deployed web service here **[Windhover (on Render)](https://windhover.onrender.com/)** 

---


## Table of Contents

- [User Stories](#user-stories)
- [ER Diagram](#er-diagram)
- [Features](#features)
- [Test & Debug](#testing-and-debugging)
- [Resources](#resources)


## User Stories

1. **As a librarian**, I want to view a list of all books, so I can see what’s in the library.
2. **As a librarian**, I want to add a new book to the library, so I can keep the catalog updated.
3. **As a librarian**, I want to see a list of members, so I can know who is registered with the library.
4. **As a librarian**, I want to register a new member, so I can add them to the system.
5. **As a librarian**, I want to record when a member borrows a book, so I can keep track of the borrowing history.
6. **As a librarian**, I want to record when a member returns a book, so I can update the status in the system.
7. **As a librarian**, I want to view the borrowing history, so I can see which members have borrowed and returned books.

## ER Diagram:
The project can have three core tables:
- **Books**: 
  - `BookID`, `ISBN`, `Title`, `Author`, `Publisher`, `PublicationYear`, `ImagePath`, `Available`, `Deleted`
- **Members**: 
  - `MemberID`, `Name`, `Email`, `JoinDate`, `ProfilePicture`
- **BorrowingHistory**: 
  - `TransactionID`, `BookID` (foreign key), `MemberID` (foreign key), `BorrowDate`, `ReturnDate`

```mermaid
erDiagram
    BOOKS {
        int BookID PK
        int ISBN
        string Title
        string Author
        string Publisher
        int PublicationYear
        string ImagePath
        boolean Available
        boolean Deleted
    }

    MEMBERS {
        int MemberID PK
        string Name
        string Email
        date JoinDate
        string ProfilePicture
    }

    BORROWING_HISTORY {
        int TransactionID PK
        int BookID FK
        int MemberID FK
        date BorrowDate
        date ReturnDate
    }

    BOOKS ||--o{ BORROWING_HISTORY: contains
    MEMBERS ||--o{ BORROWING_HISTORY: borrows
```

## Features

The goal is to provide data consistency between different routes and database operations handling errors and exceptions.

### **Key Features & Pages**:

1. **Home Page**: 
   - Brief introduction of the system, navigation links to the other pages, and general information.
   
2. **Books List**:
   - Displays a list of all available books in the library with options to search, filter by author or category.
   - HTML form to add new books (name, author, genre, publication year, cover).

3. **Members List**:
   - Displays a list of registered members (name, email, membership start date).
   - HTML form to register a new member.

4. **Borrowing History**:
   - Shows the borrowing history (which member borrowed which book, when, and return status).
   - HTML form to record new borrowing/returning transactions.

### Book Management

- View a list of all books.
- Add new books, including uploading cover images.
- Edit and delete existing books.

### Member Management

- View and search member details.
- Add new members and upload profile pictures.
- Edit existing members.

### Borrowing System

- Track borrowing and return of books.
- View history of borrowed books with due and return dates.
- See live trends and stats.

### Testing and Debugging

| **Feature**                     | **Description**                                                                                  | **Progress**           | **Status**           |
|---------------------------------|--------------------------------------------------------------------------------------------------|-------------------------|-----------------------|
| **Database Design**             | Initial database setup with tables for books, members, and borrowing records.                    | Designed and configured | ✅ Completed          |
| **ISBN as Primary Key**         | Experimented with using ISBN as the primary key, encountered issues with data constraints.      | Reverted to `book_id`   | 🔄 Revised           |
| **Data Import Script**          | Developed script to import books from CSV, including validation of ISBN and image handling.     | Adjusted and improved   | ✅ Completed          |
| **Search Functionality**        | Implemented front-end JavaScript and SQL query search for books by title, author, and publisher.| Tested and enhanced     | ✅ Completed          |
| **Frontend Design**             | Styled with Bootstrap, ensuring responsiveness and accessibility; implemented dark mode toggle. | Further enhancements    | 🔄 Ongoing           |
| **Forms and Validation**        | Created and validated forms for adding books, members, and managing loans.                      | JavaScript and backend  | ✅ Completed          |
| **Flask-Migrate Setup**         | Configured Flask-Migrate for database schema migrations and updates.                            | Set up and tested       | ✅ Completed          |
| **Pagination**                  | Integrated pagination for books and members lists in the UI.                                    | Implemented in routes   | ✅ Completed          |
| **Dynamic Stats Display**       | Displayed stats for total books, members, and books borrowed on the homepage.                   | Added to homepage       | ✅ Completed          |
| **Borrowing Rules**             | Established and displayed borrowing policies, such as loan period and renewal limits.           | Documented and applied  | ✅ Completed          |
| **Icons Integration**           | Integrated icons from a python file, styled to adapt to light and dark modes.                     | Set up in templates     | ✅ Completed          |
| **Blueprints**                  | Refactored routes using Flask blueprints for modularity and maintainability.                    | Fully implemented       | ✅ Completed          |
| **Matplotlib Graphs**           | Added dynamic graphs to visualize borrowing trends, integrated into the app using Matplotlib.   | Integrated and tested   | ✅ Completed          |
| **AWS RDS Setup**               | Configured and optimized Amazon RDS PostgreSQL database for reliable storage and backups.       | Setup complete          | ✅ Completed          |
| **Cloud Render Deployment**     | Deployed the app on Render.com for production use, including environment variable setup.         | Successfully deployed   | ✅ Completed          |
| **Testing & Debugging Setup**   | Documented testing practices, added error logging, and provided a debugging guide in README.    | Initial setup complete  | 🔄 Ongoing           |
| **Future Enhancements**         | Noted potential enhancements like admin roles, extended book details, and member stats.         | Planning phase          | 🚧 Planned           |

## Resources

- **[edX CS50's Introduction to Databases with SQL](https://cs50.harvard.edu/sql/)**  
  Harvard's CS50 course on edX provides a comprehensive introduction to databases. Course explains SQLite for portability and PostgreSQL and MySQL for scalability.

- **[Cloud Application Platform (Render)](https://render.com/)**  
  Render helps software teams ship products fast and at any scale, can host applications with hundreds of services, all with a relentless commitment to reliability and uptime.

### Technical Documentation and Tools

- **[Flask Documentation](https://flask.palletsprojects.com/)**  
  Official documentation for Flask, a Python web framework used in this project for routing, handling requests, and rendering templates.

- **[PostgreSQL Documentation](https://www.postgresql.org/docs/)**  
  Comprehensive documentation on PostgreSQL, covering database setup, SQL syntax, and database management practices used in the project.

- **[Bootstrap Documentation](https://getbootstrap.com/docs/)**  
  Bootstrap’s official guide provides resources for responsive design, component usage, and advanced styling, enabling the project to achieve a polished and mobile-friendly frontend.

- **[SQLAlchemy Documentation](https://docs.sqlalchemy.org/)**  
  SQLAlchemy’s ORM (Object Relational Mapper) documentation provides insight into database abstraction techniques, making it easier to interact with PostgreSQL within the project’s Flask application.

- **[AWS RDS Documentation](https://docs.aws.amazon.com/rds/)**  
  Amazon’s RDS documentation for managing PostgreSQL instances on AWS, covering database setup, maintenance, and security.

- **[Psycopg2 Documentation](https://www.psycopg.org/docs/)**  
  Psycopg2 is a PostgreSQL database adapter for Python, crucial for handling database transactions within Flask applications.

### Debugging and Testing Resources

- **[Flask-Testing Documentation](https://flask.palletsprojects.com/)**  
  Guides and best practices for setting up unit tests and handling error logging in Flask applications, supporting a reliable development process.

- **[Chrome DevTools](https://developer.chrome.com/docs/devtools/)**  
  Chrome DevTools is a set of web developer tools built into Google Chrome. Useful for debugging frontend code, inspecting elements, and tracking network activity.

### Design and Accessibility

- **[WCAG (Web Content Accessibility Guidelines)](https://www.w3.org/WAI/WCAG21/quickref/)**  
  Standards and practices for ensuring accessibility, crucial for improving the user experience for people with disabilities.

- **[Font Awesome Icons](https://fontawesome.com/)**  
  Font Awesome provides a wide range of icons for web applications, supporting visual elements used in this project for icons in the footer, buttons, and other UI components.

---

## Module 4 - UCD PA - Alan Maizon
