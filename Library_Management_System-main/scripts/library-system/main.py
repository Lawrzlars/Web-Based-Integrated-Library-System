#!/usr/bin/env python3
"""
Library Management System - Main Application
A console-based application for managing books, patrons, and library operations.
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.library_service import LibraryService


class LibraryApp:
    """
    Main application class for the Library Management System.
    Handles the console UI and user interactions.
    """
    
    def __init__(self):
        """Initialize the Library Application."""
        self.service = LibraryService()
        self.page_size = 10  # Items per page for pagination
    
    # ==================== UTILITY METHODS ====================
    
    def clear_screen(self) -> None:
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str) -> None:
        """Print a formatted header."""
        width = 60
        print("\n" + "=" * width)
        print(f"{title:^{width}}")
        print("=" * width)
    
    def print_separator(self) -> None:
        """Print a separator line."""
        print("-" * 60)
    
    def print_table_header(self, columns: list, widths: list) -> None:
        """Print a formatted table header."""
        header = ""
        for col, width in zip(columns, widths):
            header += f"{col:<{width}}"
        print(header)
        print("-" * sum(widths))
    
    def print_book_table(self, books: list, show_borrowed_date: bool = False) -> None:
        """Print books in a formatted table."""
        if not books:
            print("\n  No books found.")
            return
        
        if show_borrowed_date:
            self.print_table_header(
                ["ID", "Title", "Author", "Year", "Status", "Borrowed Date"],
                [6, 25, 20, 8, 14, 20]
            )
            for book in books:
                borrowed = book.borrowed_date or "N/A"
                print(f"{book.id:<6}{book.title[:23]:<25}{book.author[:18]:<20}{book.year:<8}{book.status:<14}{borrowed:<20}")
        else:
            self.print_table_header(
                ["ID", "Title", "Author", "Year", "Status"],
                [6, 30, 25, 8, 15]
            )
            for book in books:
                print(f"{book.id:<6}{book.title[:28]:<30}{book.author[:23]:<25}{book.year:<8}{book.status:<15}")
    
    def print_patron_table(self, patrons: list) -> None:
        """Print patrons in a formatted table."""
        if not patrons:
            print("\n  No patrons found.")
            return
        
        self.print_table_header(
            ["ID", "Name", "Books Borrowed"],
            [8, 30, 15]
        )
        for patron in patrons:
            print(f"{patron.id:<8}{patron.name[:28]:<30}{patron.get_borrowed_count():<15}")
    
    def get_valid_int(self, prompt: str, allow_empty: bool = False) -> int:
        """
        Get a valid integer input from the user.
        
        Args:
            prompt: The prompt to display
            allow_empty: If True, empty input returns None
            
        Returns:
            int or None: The validated integer
        """
        while True:
            try:
                value = input(prompt).strip()
                if allow_empty and not value:
                    return None
                return int(value)
            except ValueError:
                print("  Invalid input. Please enter a valid number.")
    
    def get_valid_string(self, prompt: str, allow_empty: bool = False) -> str:
        """
        Get a valid string input from the user.
        
        Args:
            prompt: The prompt to display
            allow_empty: If True, empty input is allowed
            
        Returns:
            str or None: The validated string
        """
        while True:
            value = input(prompt).strip()
            if value or allow_empty:
                return value if value else None
            print("  Input cannot be empty. Please try again.")
    
    def press_enter_to_continue(self) -> None:
        """Wait for user to press Enter."""
        input("\nPress Enter to continue...")
    
    def confirm_action(self, message: str) -> bool:
        """
        Ask user to confirm an action.
        
        Args:
            message: Confirmation message
            
        Returns:
            bool: True if confirmed, False otherwise
        """
        response = input(f"{message} (y/n): ").strip().lower()
        return response == 'y' or response == 'yes'
    
    def paginate_list(self, items: list, page: int = 1) -> tuple:
        """
        Paginate a list of items.
        
        Args:
            items: List to paginate
            page: Current page number
            
        Returns:
            tuple: (paginated_items, total_pages, current_page)
        """
        total_pages = max(1, (len(items) + self.page_size - 1) // self.page_size)
        page = max(1, min(page, total_pages))
        start = (page - 1) * self.page_size
        end = start + self.page_size
        return items[start:end], total_pages, page
    
    # ==================== STATISTICS ====================
    
    def show_statistics(self) -> None:
        """Display library statistics."""
        stats = self.service.get_statistics()
        print(f"\n  Total Books: {stats['total_books']}")
        print(f"  Available: {stats['available_books']} | Checked Out: {stats['checked_out_books']}")
        print(f"  Total Patrons: {stats['total_patrons']} | Active: {stats['active_patrons']}")
    
    # ==================== MAIN MENU ====================
    
    def main_menu(self) -> None:
        """Display and handle the main menu."""
        while True:
            self.clear_screen()
            self.print_header("LIBRARY MANAGEMENT SYSTEM")
            self.show_statistics()
            print("\n  Main Menu:")
            print("  " + "-" * 25)
            print("  1. Manage Books")
            print("  2. Manage Patrons")
            print("  3. Borrow Book")
            print("  4. Return Book")
            print("  5. Exit")
            print()
            
            choice = self.get_valid_int("  Enter your choice (1-5): ")
            
            if choice == 1:
                self.book_menu()
            elif choice == 2:
                self.patron_menu()
            elif choice == 3:
                self.borrow_book()
            elif choice == 4:
                self.return_book()
            elif choice == 5:
                if self.confirm_action("\n  Are you sure you want to exit?"):
                    print("\n  Thank you for using the Library Management System!")
                    print("  Goodbye!\n")
                    break
            else:
                print("\n  Invalid choice. Please enter a number between 1 and 5.")
                self.press_enter_to_continue()
    
    # ==================== BOOK MENU ====================
    
    def book_menu(self) -> None:
        """Display and handle the book management menu."""
        while True:
            self.clear_screen()
            self.print_header("BOOK MANAGEMENT")
            print("\n  1. Add Book")
            print("  2. Update Book")
            print("  3. Delete Book")
            print("  4. List All Books")
            print("  5. Search Books")
            print("  6. Back to Main Menu")
            print()
            
            choice = self.get_valid_int("  Enter your choice (1-6): ")
            
            if choice == 1:
                self.add_book()
            elif choice == 2:
                self.update_book()
            elif choice == 3:
                self.delete_book()
            elif choice == 4:
                self.list_books()
            elif choice == 5:
                self.search_books_menu()
            elif choice == 6:
                break
            else:
                print("\n  Invalid choice. Please enter a number between 1 and 6.")
                self.press_enter_to_continue()
    
    def add_book(self) -> None:
        """Handle adding a new book."""
        self.clear_screen()
        self.print_header("ADD NEW BOOK")
        
        print("\n  Enter book details:\n")
        title = self.get_valid_string("  Title: ")
        author = self.get_valid_string("  Author: ")
        year = self.get_valid_int("  Publication Year: ")
        
        # Validate year
        if year and (year < 0 or year > 2100):
            print("\n  Warning: Year seems invalid, but adding anyway.")
        
        success, message = self.service.add_book(title, author, year)
        print(f"\n  {message}")
        self.press_enter_to_continue()
    
    def update_book(self) -> None:
        """Handle updating an existing book."""
        self.clear_screen()
        self.print_header("UPDATE BOOK")
        
        # Show current books
        books = self.service.list_all_books()
        print("\n  Current Books:")
        self.print_book_table(books)
        
        if not books:
            self.press_enter_to_continue()
            return
        
        print("\n  Enter the Book ID to update:")
        book_id = self.get_valid_int("  Book ID: ")
        
        book = self.service.get_book_by_id(book_id)
        if not book:
            print(f"\n  Error: Book with ID {book_id} not found.")
            self.press_enter_to_continue()
            return
        
        print(f"\n  Updating: {book}")
        print("  (Leave blank to keep current value)\n")
        
        title = self.get_valid_string(f"  New Title [{book.title}]: ", allow_empty=True)
        author = self.get_valid_string(f"  New Author [{book.author}]: ", allow_empty=True)
        year = self.get_valid_int(f"  New Year [{book.year}]: ", allow_empty=True)
        
        success, message = self.service.update_book(book_id, title, author, year)
        print(f"\n  {message}")
        self.press_enter_to_continue()
    
    def delete_book(self) -> None:
        """Handle deleting a book."""
        self.clear_screen()
        self.print_header("DELETE BOOK")
        
        # Show current books
        books = self.service.list_all_books()
        print("\n  Current Books:")
        self.print_book_table(books)
        
        if not books:
            self.press_enter_to_continue()
            return
        
        print("\n  Enter the Book ID to delete:")
        book_id = self.get_valid_int("  Book ID: ")
        
        book = self.service.get_book_by_id(book_id)
        if not book:
            print(f"\n  Error: Book with ID {book_id} not found.")
            self.press_enter_to_continue()
            return
        
        if self.confirm_action(f"\n  Are you sure you want to delete '{book.title}'?"):
            success, message = self.service.delete_book(book_id)
            print(f"\n  {message}")
        else:
            print("\n  Deletion cancelled.")
        
        self.press_enter_to_continue()
    
    def list_books(self) -> None:
        """Handle listing all books with pagination."""
        page = 1
        while True:
            self.clear_screen()
            self.print_header("ALL BOOKS")
            
            books = self.service.list_all_books()
            paginated, total_pages, current_page = self.paginate_list(books, page)
            
            print(f"\n  Page {current_page} of {total_pages} (Total: {len(books)} books)")
            self.print_separator()
            self.print_book_table(paginated, show_borrowed_date=True)
            
            print("\n  Navigation: [N]ext | [P]revious | [B]ack")
            choice = input("  Enter choice: ").strip().lower()
            
            if choice == 'n' and current_page < total_pages:
                page += 1
            elif choice == 'p' and current_page > 1:
                page -= 1
            elif choice == 'b':
                break
    
    def search_books_menu(self) -> None:
        """Handle searching books."""
        self.clear_screen()
        self.print_header("SEARCH BOOKS")
        
        print("\n  Search by:")
        print("  1. Title")
        print("  2. Author")
        print("  3. Status (Available/Checked Out)")
        print("  4. Back")
        print()
        
        choice = self.get_valid_int("  Enter your choice (1-4): ")
        
        if choice == 1:
            term = self.get_valid_string("\n  Enter title to search: ")
            results = self.service.search_books_by_title(term)
            self.display_search_results(results, f"Title: '{term}'")
        elif choice == 2:
            term = self.get_valid_string("\n  Enter author to search: ")
            results = self.service.search_books_by_author(term)
            self.display_search_results(results, f"Author: '{term}'")
        elif choice == 3:
            print("\n  1. Available")
            print("  2. Checked Out")
            status_choice = self.get_valid_int("\n  Enter status (1-2): ")
            if status_choice == 1:
                results = self.service.search_books_by_status("Available")
                self.display_search_results(results, "Status: Available")
            elif status_choice == 2:
                results = self.service.search_books_by_status("Checked Out")
                self.display_search_results(results, "Status: Checked Out")
            else:
                print("\n  Invalid status choice.")
                self.press_enter_to_continue()
        elif choice != 4:
            print("\n  Invalid choice.")
            self.press_enter_to_continue()
    
    def display_search_results(self, results: list, search_term: str) -> None:
        """Display search results."""
        self.clear_screen()
        self.print_header("SEARCH RESULTS")
        print(f"\n  Search: {search_term}")
        print(f"  Found: {len(results)} book(s)")
        self.print_separator()
        self.print_book_table(results)
        self.press_enter_to_continue()
    
    # ==================== PATRON MENU ====================
    
    def patron_menu(self) -> None:
        """Display and handle the patron management menu."""
        while True:
            self.clear_screen()
            self.print_header("PATRON MANAGEMENT")
            print("\n  1. Add Patron")
            print("  2. Update Patron")
            print("  3. Delete Patron")
            print("  4. View All Patrons")
            print("  5. View Patron Details")
            print("  6. Back to Main Menu")
            print()
            
            choice = self.get_valid_int("  Enter your choice (1-6): ")
            
            if choice == 1:
                self.add_patron()
            elif choice == 2:
                self.update_patron()
            elif choice == 3:
                self.delete_patron()
            elif choice == 4:
                self.list_patrons()
            elif choice == 5:
                self.view_patron_details()
            elif choice == 6:
                break
            else:
                print("\n  Invalid choice. Please enter a number between 1 and 6.")
                self.press_enter_to_continue()
    
    def add_patron(self) -> None:
        """Handle adding a new patron."""
        self.clear_screen()
        self.print_header("ADD NEW PATRON")
        
        print("\n  Enter patron details:\n")
        name = self.get_valid_string("  Name: ")
        
        success, message = self.service.add_patron(name)
        print(f"\n  {message}")
        self.press_enter_to_continue()
    
    def update_patron(self) -> None:
        """Handle updating an existing patron."""
        self.clear_screen()
        self.print_header("UPDATE PATRON")
        
        # Show current patrons
        patrons = self.service.list_all_patrons()
        print("\n  Current Patrons:")
        self.print_patron_table(patrons)
        
        if not patrons:
            self.press_enter_to_continue()
            return
        
        print("\n  Enter the Patron ID to update:")
        patron_id = self.get_valid_int("  Patron ID: ")
        
        patron = self.service.get_patron_by_id(patron_id)
        if not patron:
            print(f"\n  Error: Patron with ID {patron_id} not found.")
            self.press_enter_to_continue()
            return
        
        print(f"\n  Updating: {patron}")
        name = self.get_valid_string(f"\n  New Name [{patron.name}]: ")
        
        success, message = self.service.update_patron(patron_id, name)
        print(f"\n  {message}")
        self.press_enter_to_continue()
    
    def delete_patron(self) -> None:
        """Handle deleting a patron."""
        self.clear_screen()
        self.print_header("DELETE PATRON")
        
        # Show current patrons
        patrons = self.service.list_all_patrons()
        print("\n  Current Patrons:")
        self.print_patron_table(patrons)
        
        if not patrons:
            self.press_enter_to_continue()
            return
        
        print("\n  Enter the Patron ID to delete:")
        patron_id = self.get_valid_int("  Patron ID: ")
        
        patron = self.service.get_patron_by_id(patron_id)
        if not patron:
            print(f"\n  Error: Patron with ID {patron_id} not found.")
            self.press_enter_to_continue()
            return
        
        if self.confirm_action(f"\n  Are you sure you want to delete '{patron.name}'?"):
            success, message = self.service.delete_patron(patron_id)
            print(f"\n  {message}")
        else:
            print("\n  Deletion cancelled.")
        
        self.press_enter_to_continue()
    
    def list_patrons(self) -> None:
        """Handle listing all patrons with pagination."""
        page = 1
        while True:
            self.clear_screen()
            self.print_header("ALL PATRONS")
            
            patrons = self.service.list_all_patrons()
            paginated, total_pages, current_page = self.paginate_list(patrons, page)
            
            print(f"\n  Page {current_page} of {total_pages} (Total: {len(patrons)} patrons)")
            self.print_separator()
            self.print_patron_table(paginated)
            
            print("\n  Navigation: [N]ext | [P]revious | [B]ack")
            choice = input("  Enter choice: ").strip().lower()
            
            if choice == 'n' and current_page < total_pages:
                page += 1
            elif choice == 'p' and current_page > 1:
                page -= 1
            elif choice == 'b':
                break
    
    def view_patron_details(self) -> None:
        """Handle viewing detailed patron information."""
        self.clear_screen()
        self.print_header("PATRON DETAILS")
        
        # Show current patrons
        patrons = self.service.list_all_patrons()
        print("\n  Current Patrons:")
        self.print_patron_table(patrons)
        
        if not patrons:
            self.press_enter_to_continue()
            return
        
        print("\n  Enter the Patron ID to view details:")
        patron_id = self.get_valid_int("  Patron ID: ")
        
        patron, borrowed_books = self.service.get_patron_details(patron_id)
        
        if not patron:
            print(f"\n  Error: Patron with ID {patron_id} not found.")
            self.press_enter_to_continue()
            return
        
        self.clear_screen()
        self.print_header(f"PATRON: {patron.name}")
        print(f"\n  ID: {patron.id}")
        print(f"  Name: {patron.name}")
        print(f"  Books Borrowed: {patron.get_borrowed_count()}")
        
        if borrowed_books:
            print("\n  Currently Borrowed Books:")
            self.print_separator()
            self.print_book_table(borrowed_books, show_borrowed_date=True)
        else:
            print("\n  No books currently borrowed.")
        
        self.press_enter_to_continue()
    
    # ==================== LIBRARY OPERATIONS ====================
    
    def borrow_book(self) -> None:
        """Handle borrowing a book."""
        self.clear_screen()
        self.print_header("BORROW BOOK")
        
        # Show available books
        available_books = self.service.search_books_by_status("Available")
        print("\n  Available Books:")
        self.print_book_table(available_books)
        
        if not available_books:
            print("\n  No books available for borrowing.")
            self.press_enter_to_continue()
            return
        
        # Show patrons
        patrons = self.service.list_all_patrons()
        print("\n  Patrons:")
        self.print_patron_table(patrons)
        
        if not patrons:
            print("\n  No patrons registered. Please add a patron first.")
            self.press_enter_to_continue()
            return
        
        print("\n  Enter borrowing details:")
        book_id = self.get_valid_int("  Book ID: ")
        patron_id = self.get_valid_int("  Patron ID: ")
        
        success, message = self.service.borrow_book(book_id, patron_id)
        print(f"\n  {message}")
        self.press_enter_to_continue()
    
    def return_book(self) -> None:
        """Handle returning a book."""
        self.clear_screen()
        self.print_header("RETURN BOOK")
        
        # Show checked out books
        checked_out_books = self.service.search_books_by_status("Checked Out")
        print("\n  Checked Out Books:")
        self.print_book_table(checked_out_books, show_borrowed_date=True)
        
        if not checked_out_books:
            print("\n  No books are currently checked out.")
            self.press_enter_to_continue()
            return
        
        # Show patrons with borrowed books
        patrons_with_books = [p for p in self.service.list_all_patrons() if p.get_borrowed_count() > 0]
        print("\n  Patrons with Borrowed Books:")
        self.print_patron_table(patrons_with_books)
        
        print("\n  Enter return details:")
        book_id = self.get_valid_int("  Book ID: ")
        patron_id = self.get_valid_int("  Patron ID: ")
        
        success, message = self.service.return_book(book_id, patron_id)
        print(f"\n  {message}")
        self.press_enter_to_continue()


def main():
    """Main entry point for the application."""
    print("\n  Initializing Library Management System...")
    app = LibraryApp()
    app.main_menu()


if __name__ == "__main__":
    main()
