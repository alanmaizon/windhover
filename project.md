### Project: **Library Management System**

**Overview**:  
Create a simple web-based Library Management System where users can interact with different features of the library like books, authors, members, borrowing history, etc. This will involve Flask for the backend, Python for database queries, SQL for data storage, and HTML for the front end.

Our goal is to provide data consistency between different routes and database operations handling errors and exceptions.

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


### **Entity-Relationship Diagram (ERD)**:
The project can have three core tables:
- **Books**
- **Members**
- **BorrowingHistory**

### **Database Integration**:
- **Python (Flask)**: For handling database connections, queries, and routes to interact with the pages.
- **SQL Queries**: 
  - `SELECT` statements for fetching the data on each page (e.g., list of books, members, borrowing history).
  - `INSERT` statements for adding new books, members, or borrowing records.

### **Navigation Structure**:
- **Home**
- **Books** (View/Add)
- **Members** (View/Add)
- **Borrowing History** (View/Record Transaction)
