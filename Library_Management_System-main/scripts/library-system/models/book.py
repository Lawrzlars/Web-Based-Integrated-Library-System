"""
Book model for the Library Management System.
Represents a book entity with all its attributes.
"""

from datetime import datetime
from typing import Optional


class Book:
    """
    Represents a book in the library system.
    
    Attributes:
        id (int): Unique identifier for the book
        title (str): Title of the book
        author (str): Author of the book
        year (int): Publication year
        status (str): Current status - "Available" or "Checked Out"
        borrowed_date (str): Date when the book was borrowed (optional)
    """
    
    AVAILABLE = "Available"
    CHECKED_OUT = "Checked Out"
    
    def __init__(
        self,
        book_id: int,
        title: str,
        author: str,
        year: int,
        status: str = "Available",
        borrowed_date: Optional[str] = None
    ):
        """
        Initialize a new Book instance.
        
        Args:
            book_id: Unique identifier for the book
            title: Title of the book
            author: Author of the book
            year: Publication year
            status: Current availability status
            borrowed_date: Date when book was borrowed (if checked out)
        """
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status
        self.borrowed_date = borrowed_date
    
    def to_dict(self) -> dict:
        """
        Convert the Book instance to a dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary representation of the book
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
            "borrowed_date": self.borrowed_date
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        """
        Create a Book instance from a dictionary.
        
        Args:
            data: Dictionary containing book data
            
        Returns:
            Book: A new Book instance
        """
        return cls(
            book_id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=data.get("status", cls.AVAILABLE),
            borrowed_date=data.get("borrowed_date")
        )
    
    def check_out(self) -> None:
        """Mark the book as checked out and record the borrow date."""
        self.status = self.CHECKED_OUT
        self.borrowed_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def return_book(self) -> None:
        """Mark the book as available and clear the borrow date."""
        self.status = self.AVAILABLE
        self.borrowed_date = None
    
    def is_available(self) -> bool:
        """
        Check if the book is available for borrowing.
        
        Returns:
            bool: True if available, False otherwise
        """
        return self.status == self.AVAILABLE
    
    def __str__(self) -> str:
        """String representation of the book."""
        return f"[{self.id}] {self.title} by {self.author} ({self.year}) - {self.status}"
    
    def __repr__(self) -> str:
        """Developer representation of the book."""
        return f"Book(id={self.id}, title='{self.title}', author='{self.author}', year={self.year}, status='{self.status}')"
