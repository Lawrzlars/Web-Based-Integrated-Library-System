"""
Library Service for the Library Management System.
Handles all business logic including data persistence, book management,
patron management, and library operations (borrow/return).
"""

import json
import os
from typing import List, Optional, Tuple

from models.book import Book
from models.patron import Patron


class LibraryService:
    """
    Service class that handles all library operations.
    Manages data persistence using JSON files and provides methods
    for book management, patron management, and borrowing operations.
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the LibraryService.
        
        Args:
            data_dir: Directory path for storing JSON data files
        """
        self.data_dir = data_dir
        self.books_file = os.path.join(data_dir, "books.json")
        self.patrons_file = os.path.join(data_dir, "patrons.json")
        
        # Ensure data directory exists
        self._ensure_data_directory()
        
        # Load data from files
        self.books: List[Book] = []
        self.patrons: List[Patron] = []
        self._load_all_data()
    
    def _ensure_data_directory(self) -> None:
        """Create the data directory if it doesn't exist."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    # ==================== DATA PERSISTENCE ====================
    
    def load_books(self) -> List[Book]:
        """
        Load books from the JSON file.
        
        Returns:
            List[Book]: List of Book objects
        """
        try:
            if os.path.exists(self.books_file):
                with open(self.books_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        data = json.loads(content)
                        return [Book.from_dict(book) for book in data]
            return []
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"Warning: Could not load books.json (corrupted/invalid). Starting fresh. Error: {e}")
            return []
    
    def save_books(self) -> bool:
        """
        Save books to the JSON file.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(self.books_file, 'w', encoding='utf-8') as f:
                data = [book.to_dict() for book in self.books]
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except (IOError, OSError) as e:
            print(f"Error saving books: {e}")
            return False
    
    def load_patrons(self) -> List[Patron]:
        """
        Load patrons from the JSON file.
        
        Returns:
            List[Patron]: List of Patron objects
        """
        try:
            if os.path.exists(self.patrons_file):
                with open(self.patrons_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        data = json.loads(content)
                        return [Patron.from_dict(patron) for patron in data]
            return []
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"Warning: Could not load patrons.json (corrupted/invalid). Starting fresh. Error: {e}")
            return []
    
    def save_patrons(self) -> bool:
        """
        Save patrons to the JSON file.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(self.patrons_file, 'w', encoding='utf-8') as f:
                data = [patron.to_dict() for patron in self.patrons]
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except (IOError, OSError) as e:
            print(f"Error saving patrons: {e}")
            return False
    
    def _load_all_data(self) -> None:
        """Load all data from JSON files."""
        self.books = self.load_books()
        self.patrons = self.load_patrons()
    
    def _save_all_data(self) -> bool:
        """Save all data to JSON files."""
        return self.save_books() and self.save_patrons()
    
    # ==================== ID GENERATION ====================
    
    def _generate_book_id(self) -> int:
        """
        Generate a unique ID for a new book.
        
        Returns:
            int: A unique book ID
        """
        if not self.books:
            return 1
        return max(book.id for book in self.books) + 1
    
    def _generate_patron_id(self) -> int:
        """
        Generate a unique ID for a new patron.
        
        Returns:
            int: A unique patron ID
        """
        if not self.patrons:
            return 1
        return max(patron.id for patron in self.patrons) + 1
    
    # ==================== BOOK MANAGEMENT ====================
    
    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """
        Find a book by its ID.
        
        Args:
            book_id: The ID of the book to find
            
        Returns:
            Book or None: The book if found, None otherwise
        """
        for book in self.books:
            if book.id == book_id:
                return book
        return None
    
    def add_book(self, title: str, author: str, year: int, book_id: int = None) -> Tuple[bool, str]:
        """
        Add a new book to the library.
        
        Args:
            title: Title of the book
            author: Author of the book
            year: Publication year
            book_id: Optional specific ID (auto-generated if not provided)
            
        Returns:
            Tuple[bool, str]: Success status and message
        """
        # Auto-generate ID if not provided
        if book_id is None:
            book_id = self._generate_book_id()
        else:
            # Check for duplicate ID
            if self.get_book_by_id(book_id):
                return False, f"Error: Book with ID {book_id} already exists."
        
        # Create and add the book
        new_book = Book(book_id=book_id, title=title, author=author, year=year)
        self.books.append(new_book)
        self.save_books()
        
        return True, f"Book '{title}' added successfully with ID {book_id}."
    
    def update_book(self, book_id: int, title: str = None, author: str = None, year: int = None) -> Tuple[bool, str]:
        """
        Update an existing book's information.
        
        Args:
            book_id: ID of the book to update
            title: New title (optional)
            author: New author (optional)
            year: New publication year (optional)
            
        Returns:
            Tuple[bool, str]: Success status and message
        """
        book = self.get_book_by_id(book_id)
        if not book:
            return False, f"Error: Book with ID {book_id} not found."
        
        # Update fields if provided
        if title:
            book.title = title
        if author:
            book.author = author
        if year:
            book.year = year
        
        self.save_books()
        return True, f"Book ID {book_id} updated successfully."
    
    def delete_book(self, book_id: int) -> Tuple[bool, str]:
        """
        Delete a book from the library.
        
        Args:
            book_id: ID of the book to delete
            
        Returns:
            Tuple[bool, str]: Success status and message
        """
        book = self.get_book_by_id(book_id)
        if not book:
            return False, f"Error: Book with ID {book_id} not found."
        
        # Check if book is currently borrowed
        if not book.is_available():
            return False, f"Error: Cannot delete book '{book.title}' - it is currently checked out."
        
        self.books.remove(book)
        self.save_books()
        return True, f"Book '{book.title}' deleted successfully."
    
    def list_all_books(self) -> List[Book]:
        """
        Get all books in the library.
        
        Returns:
            List[Book]: List of all books
        """
        return self.books.copy()
    
    def search_books_by_title(self, title: str) -> List[Book]:
        """
        Search books by title (case-insensitive partial match).
        
        Args:
            title: Search term
            
        Returns:
            List[Book]: Matching books
        """
        title_lower = title.lower()
        return [book for book in self.books if title_lower in book.title.lower()]
    
    def search_books_by_author(self, author: str) -> List[Book]:
        """
        Search books by author (case-insensitive partial match).
        
        Args:
            author: Search term
            
        Returns:
            List[Book]: Matching books
        """
        author_lower = author.lower()
        return [book for book in self.books if author_lower in book.author.lower()]
    
    def search_books_by_status(self, status: str) -> List[Book]:
        """
        Search books by status.
        
        Args:
            status: "Available" or "Checked Out"
            
        Returns:
            List[Book]: Matching books
        """
        return [book for book in self.books if book.status.lower() == status.lower()]
    
    # ==================== PATRON MANAGEMENT ====================
    
    def get_patron_by_id(self, patron_id: int) -> Optional[Patron]:
        """
        Find a patron by their ID.
        
        Args:
            patron_id: The ID of the patron to find
            
        Returns:
            Patron or None: The patron if found, None otherwise
        """
        for patron in self.patrons:
            if patron.id == patron_id:
                return patron
        return None
    
    def add_patron(self, name: str, patron_id: int = None) -> Tuple[bool, str]:
        """
        Add a new patron to the library.
        
        Args:
            name: Name of the patron
            patron_id: Optional specific ID (auto-generated if not provided)
            
        Returns:
            Tuple[bool, str]: Success status and message
        """
        # Auto-generate ID if not provided
        if patron_id is None:
            patron_id = self._generate_patron_id()
        else:
            # Check for duplicate ID
            if self.get_patron_by_id(patron_id):
                return False, f"Error: Patron with ID {patron_id} already exists."
        
        # Create and add the patron
        new_patron = Patron(patron_id=patron_id, name=name)
        self.patrons.append(new_patron)
        self.save_patrons()
        
        return True, f"Patron '{name}' added successfully with ID {patron_id}."
    
    def update_patron(self, patron_id: int, name: str) -> Tuple[bool, str]:
        """
        Update a patron's information.
        
        Args:
            patron_id: ID of the patron to update
            name: New name
            
        Returns:
            Tuple[bool, str]: Success status and message
        """
        patron = self.get_patron_by_id(patron_id)
        if not patron:
            return False, f"Error: Patron with ID {patron_id} not found."
        
        patron.name = name
        self.save_patrons()
        return True, f"Patron ID {patron_id} updated successfully."
    
    def delete_patron(self, patron_id: int) -> Tuple[bool, str]:
        """
        Delete a patron from the library.
        
        Args:
            patron_id: ID of the patron to delete
            
        Returns:
            Tuple[bool, str]: Success status and message
        """
        patron = self.get_patron_by_id(patron_id)
        if not patron:
            return False, f"Error: Patron with ID {patron_id} not found."
        
        # Check if patron has borrowed books
        if patron.get_borrowed_count() > 0:
            return False, f"Error: Cannot delete patron '{patron.name}' - they have {patron.get_borrowed_count()} book(s) checked out."
        
        self.patrons.remove(patron)
        self.save_patrons()
        return True, f"Patron '{patron.name}' deleted successfully."
    
    def list_all_patrons(self) -> List[Patron]:
        """
        Get all patrons in the library.
        
        Returns:
            List[Patron]: List of all patrons
        """
        return self.patrons.copy()
    
    def get_patron_details(self, patron_id: int) -> Tuple[Optional[Patron], List[Book]]:
        """
        Get detailed information about a patron including their borrowed books.
        
        Args:
            patron_id: ID of the patron
            
        Returns:
            Tuple[Patron, List[Book]]: Patron and their borrowed books
        """
        patron = self.get_patron_by_id(patron_id)
        if not patron:
            return None, []
        
        borrowed_books = [self.get_book_by_id(book_id) for book_id in patron.books_checked_out]
        borrowed_books = [book for book in borrowed_books if book is not None]
        
        return patron, borrowed_books
    
    # ==================== LIBRARY OPERATIONS ====================
    
    def borrow_book(self, book_id: int, patron_id: int) -> Tuple[bool, str]:
        """
        Process a book borrowing transaction.
        
        Args:
            book_id: ID of the book to borrow
            patron_id: ID of the patron borrowing the book
            
        Returns:
            Tuple[bool, str]: Success status and message
        """
        # Check if book exists
        book = self.get_book_by_id(book_id)
        if not book:
            return False, f"Error: Book with ID {book_id} not found."
        
        # Check if patron exists
        patron = self.get_patron_by_id(patron_id)
        if not patron:
            return False, f"Error: Patron with ID {patron_id} not found."
        
        # Check if book is available
        if not book.is_available():
            return False, f"Error: Book '{book.title}' is currently checked out."
        
        # Process the borrow
        book.check_out()
        patron.borrow_book(book_id)
        
        self._save_all_data()
        return True, f"Book '{book.title}' borrowed successfully by {patron.name}."
    
    def return_book(self, book_id: int, patron_id: int) -> Tuple[bool, str]:
        """
        Process a book return transaction.
        
        Args:
            book_id: ID of the book to return
            patron_id: ID of the patron returning the book
            
        Returns:
            Tuple[bool, str]: Success status and message
        """
        # Check if book exists
        book = self.get_book_by_id(book_id)
        if not book:
            return False, f"Error: Book with ID {book_id} not found."
        
        # Check if patron exists
        patron = self.get_patron_by_id(patron_id)
        if not patron:
            return False, f"Error: Patron with ID {patron_id} not found."
        
        # Check if patron has this book
        if not patron.has_book(book_id):
            return False, f"Error: Patron '{patron.name}' does not have book '{book.title}' checked out."
        
        # Process the return
        book.return_book()
        patron.return_book(book_id)
        
        self._save_all_data()
        return True, f"Book '{book.title}' returned successfully by {patron.name}."
    
    # ==================== STATISTICS ====================
    
    def get_statistics(self) -> dict:
        """
        Get library statistics.
        
        Returns:
            dict: Statistics about the library
        """
        total_books = len(self.books)
        available_books = len([b for b in self.books if b.is_available()])
        checked_out_books = total_books - available_books
        total_patrons = len(self.patrons)
        active_patrons = len([p for p in self.patrons if p.get_borrowed_count() > 0])
        
        return {
            "total_books": total_books,
            "available_books": available_books,
            "checked_out_books": checked_out_books,
            "total_patrons": total_patrons,
            "active_patrons": active_patrons
        }
