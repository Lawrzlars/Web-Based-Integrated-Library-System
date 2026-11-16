"""
Patron model for the Library Management System.
Represents a library patron (user) with their information and borrowed books.
"""

from typing import List


class Patron:
    """
    Represents a patron (library user) in the library system.
    
    Attributes:
        id (int): Unique identifier for the patron
        name (str): Name of the patron
        books_checked_out (List[int]): List of book IDs currently borrowed
    """
    
    def __init__(
        self,
        patron_id: int,
        name: str,
        books_checked_out: List[int] = None
    ):
        """
        Initialize a new Patron instance.
        
        Args:
            patron_id: Unique identifier for the patron
            name: Name of the patron
            books_checked_out: List of book IDs borrowed by this patron
        """
        self.id = patron_id
        self.name = name
        self.books_checked_out = books_checked_out if books_checked_out is not None else []
    
    def to_dict(self) -> dict:
        """
        Convert the Patron instance to a dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary representation of the patron
        """
        return {
            "id": self.id,
            "name": self.name,
            "books_checked_out": self.books_checked_out
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Patron":
        """
        Create a Patron instance from a dictionary.
        
        Args:
            data: Dictionary containing patron data
            
        Returns:
            Patron: A new Patron instance
        """
        return cls(
            patron_id=data["id"],
            name=data["name"],
            books_checked_out=data.get("books_checked_out", [])
        )
    
    def borrow_book(self, book_id: int) -> None:
        """
        Add a book to the patron's borrowed list.
        
        Args:
            book_id: ID of the book being borrowed
        """
        if book_id not in self.books_checked_out:
            self.books_checked_out.append(book_id)
    
    def return_book(self, book_id: int) -> bool:
        """
        Remove a book from the patron's borrowed list.
        
        Args:
            book_id: ID of the book being returned
            
        Returns:
            bool: True if book was in the list and removed, False otherwise
        """
        if book_id in self.books_checked_out:
            self.books_checked_out.remove(book_id)
            return True
        return False
    
    def has_book(self, book_id: int) -> bool:
        """
        Check if the patron has borrowed a specific book.
        
        Args:
            book_id: ID of the book to check
            
        Returns:
            bool: True if patron has the book, False otherwise
        """
        return book_id in self.books_checked_out
    
    def get_borrowed_count(self) -> int:
        """
        Get the number of books currently borrowed.
        
        Returns:
            int: Number of borrowed books
        """
        return len(self.books_checked_out)
    
    def __str__(self) -> str:
        """String representation of the patron."""
        return f"[{self.id}] {self.name} - {self.get_borrowed_count()} book(s) borrowed"
    
    def __repr__(self) -> str:
        """Developer representation of the patron."""
        return f"Patron(id={self.id}, name='{self.name}', books_checked_out={self.books_checked_out})"
