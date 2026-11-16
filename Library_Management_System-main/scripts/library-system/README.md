# Library Management System

A complete console-based Library Management System built with Python. This application allows managing books, patrons (library users), and borrowing/returning operations using JSON files for data persistence.

## Features

### Book Management
- **Add Book**: Add new books with auto-generated unique IDs
- **Update Book**: Modify book details (title, author, year)
- **Delete Book**: Remove books (with check for borrowed status)
- **List All Books**: View all books with pagination support
- **Search Books**: Search by title, author, or availability status

### Patron Management
- **Add Patron**: Register new library patrons
- **Update Patron**: Modify patron information
- **Delete Patron**: Remove patrons (with check for borrowed books)
- **View All Patrons**: List all registered patrons
- **View Patron Details**: See detailed info including borrowed books

### Library Operations
- **Borrow Book**: Check out available books to patrons
- **Return Book**: Process book returns with validation

### Additional Features
- Auto-generated unique IDs for books and patrons
- Timestamps for borrowed books
- Pretty-printed tables in console
- Pagination for long lists
- Comprehensive error handling
- Data persistence using JSON files

## File Structure

```
/library-system
│
├── models/
│   ├── __init__.py
│   ├── book.py          # Book data model
│   └── patron.py        # Patron data model
│
├── services/
│   ├── __init__.py
│   └── library_service.py    # Business logic and data operations
│
├── data/
│   ├── books.json       # Book data storage
│   └── patrons.json     # Patron data storage
│
├── main.py              # Main application entry point
└── README.md            # This file
```

## How to Run

### Prerequisites
- Python 3.7 or higher

### Running the Application

1. Navigate to the library-system directory:
   ```bash
   cd scripts/library-system
   ```

2. Run the main application:
   ```bash
   python main.py
   ```

   Or with Python 3 explicitly:
   ```bash
   python3 main.py
   ```

## Example Usage

### Main Menu
```
============================================================
              LIBRARY MANAGEMENT SYSTEM
============================================================

  Total Books: 5
  Available: 4 | Checked Out: 1
  Total Patrons: 3 | Active: 1

  Main Menu:
  -------------------------
  1. Manage Books
  2. Manage Patrons
  3. Borrow Book
  4. Return Book
  5. Exit

  Enter your choice (1-5):
```

### Adding a Book
```
============================================================
                    ADD NEW BOOK
============================================================

  Enter book details:

  Title: The Catcher in the Rye
  Author: J.D. Salinger
  Publication Year: 1951

  Book 'The Catcher in the Rye' added successfully with ID 6.
```

### Borrowing a Book
```
============================================================
                    BORROW BOOK
============================================================

  Available Books:
ID    Title                         Author                   Year    Status
-------------------------------------------------------------------------------------
1     To Kill a Mockingbird         Harper Lee               1960    Available

  Patrons:
ID      Name                          Books Borrowed
-----------------------------------------------------
1       John Smith                    1

  Enter borrowing details:
  Book ID: 1
  Patron ID: 2

  Book 'To Kill a Mockingbird' borrowed successfully by Emily Johnson.
```

### Searching Books
```
============================================================
                   SEARCH RESULTS
============================================================

  Search: Author: 'Orwell'
  Found: 1 book(s)
------------------------------------------------------------
ID    Title                         Author                   Year    Status
-------------------------------------------------------------------------------------
2     1984                          George Orwell            1949    Available
```

## Data Storage

The system uses two JSON files for data persistence:

### books.json
```json
[
  {
    "id": 1,
    "title": "To Kill a Mockingbird",
    "author": "Harper Lee",
    "year": 1960,
    "status": "Available",
    "borrowed_date": null
  }
]
```

### patrons.json
```json
[
  {
    "id": 1,
    "name": "John Smith",
    "books_checked_out": [3]
  }
]
```

## Error Handling

The system handles various error scenarios:
- Invalid input (letters instead of numbers, empty input)
- Non-existing IDs
- Duplicate IDs (when manually specified)
- Borrowing unavailable books
- Returning books not borrowed
- Deleting books that are checked out
- Deleting patrons with borrowed books
- Corrupted or empty JSON files

All errors display clear messages and the program continues running without crashes.

## Code Quality

- Object-Oriented Programming principles
- Clear function names and documentation
- Docstrings for all classes and methods
- Modular and readable code structure
- Type hints for better code clarity
- Separation of concerns (models, services, UI)
