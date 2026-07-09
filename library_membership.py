class BorrowLimitExceeded(Exception):
    """Custom exception raised when a member attempts to borrow more books than their limit."""
    def __init__(self, message="Borrow limit exceeded."):
        self.message = message
        super().__init__(self.message)

class Member:
    # Class-level set to enforce unique Member IDs across all instances
    _existing_ids = set()

    def __init__(self, member_id: str, name: str, membership_type: str):
        if not isinstance(member_id, str) or not (1 <= len(member_id) <= 10):
            raise ValueError("Member ID must contain at most 10 characters.")
        if member_id in Member._existing_ids:
            raise ValueError(f"Member ID '{member_id}' already exists and must be unique.")
        if not isinstance(name, str) or not (1 <= len(name) <= 50):
            raise ValueError("Name must contain at most 50 characters.")
        if membership_type not in ("Regular", "Premium"):
            raise ValueError("Membership Type must be either Regular or Premium.")
        
        self.member_id = member_id
        Member._existing_ids.add(self.member_id)
        
        self.name = name
        self.membership_type = membership_type
        
        # Encapsulation: Making the number of borrowed books a private attribute
        self.__borrowed_books = 0

    # Getter method
    def get_borrowed_books(self):
        return self.__borrowed_books

    # Setter method
    def set_borrowed_books(self, count):
        if not isinstance(count, int) or count < 0:
            raise ValueError("Number of books to borrow and return must be non-negative integers.")
        self.__borrowed_books = count

    def borrow_book(self, num_books):
        if not isinstance(num_books, int) or num_books < 0:
            raise ValueError("Number of books to borrow must be a non-negative integer.")
        self.set_borrowed_books(self.get_borrowed_books() + num_books)

    def return_book(self, num_books):
        if not isinstance(num_books, int) or num_books < 0:
            raise ValueError("Number of books to return must be a non-negative integer.")
        if num_books > self.get_borrowed_books():
            raise ValueError("A member cannot return more books than they have currently borrowed.")
        self.set_borrowed_books(self.get_borrowed_books() - num_books)

    def display_details(self, max_limit=0):
        print(f"Member ID: {self.member_id}")
        print(f"Name: {self.name}")
        print(f"Membership Type: {self.membership_type}")
        print(f"Number of Books Borrowed: {self.get_borrowed_books()}")
        print(f"Remaining Borrow Limit: {max_limit - self.get_borrowed_books()}")
        print("-" * 40)


class RegularMember(Member):
    MAX_LIMIT = 3
    
    def __init__(self, member_id: str, name: str):
        super().__init__(member_id, name, "Regular")

    # Method overriding for borrow_book
    def borrow_book(self, num_books):
        if not isinstance(num_books, int) or num_books < 0:
            raise ValueError("Number of books to borrow must be a non-negative integer.")
        if self.get_borrowed_books() + num_books > self.MAX_LIMIT:
            raise BorrowLimitExceeded(
                f"Borrow limit exceeded for Regular Member '{self.name}'. Limit is {self.MAX_LIMIT} books."
            )
        super().borrow_book(num_books)
        
    # Method overriding for display_details to show correct remaining limit
    def display_details(self):
        super().display_details(max_limit=self.MAX_LIMIT)


class PremiumMember(Member):
    MAX_LIMIT = 10
    
    def __init__(self, member_id: str, name: str):
        super().__init__(member_id, name, "Premium")

    # Method overriding for borrow_book
    def borrow_book(self, num_books):
        if not isinstance(num_books, int) or num_books < 0:
            raise ValueError("Number of books to borrow must be a non-negative integer.")
        if self.get_borrowed_books() + num_books > self.MAX_LIMIT:
            raise BorrowLimitExceeded(
                f"Borrow limit exceeded for Premium Member '{self.name}'. Limit is {self.MAX_LIMIT} books."
            )
        super().borrow_book(num_books)

    # Method overriding for display_details to show correct remaining limit
    def display_details(self):
        super().display_details(max_limit=self.MAX_LIMIT)


def main():
    # 1. Store objects of both member types in a single list to demonstrate polymorphism
    members = []
    
    # 2. Create at least two RegularMember objects and two PremiumMember objects
    try:
        members.append(RegularMember("RM001", "Alice Smith"))
        members.append(RegularMember("RM002", "Bob Jones"))
        members.append(PremiumMember("PM001", "Charlie Brown"))
        members.append(PremiumMember("PM002", "Diana Prince"))
    except ValueError as e:
        print(f"Error creating members: {e}")
        return

    print("=== Initial Member Details ===")
    # 3. Invoking the display_details() method for each object using a loop
    for member in members:
        member.display_details()

    print("\n=== Performing Transactions ===")
    
    # Valid borrowing for Regular Member
    try:
        print("-> Alice (Regular) attempts to borrow 2 books:")
        members[0].borrow_book(2)
        print("Success.")
    except Exception as e:
        print(f"Error: {e}")
        
    # Valid borrowing for Premium Member
    try:
        print("\n-> Charlie (Premium) attempts to borrow 8 books:")
        members[2].borrow_book(8)
        print("Success.")
    except Exception as e:
        print(f"Error: {e}")

    # Invalid borrowing (exceeds limit) - raises custom BorrowLimitExceeded
    try:
        print("\n-> Bob (Regular) attempts to borrow 4 books:")
        members[1].borrow_book(4)
        print("Success.")
    except BorrowLimitExceeded as e:
        print(f"Exception caught (BorrowLimitExceeded): {e}")
    except Exception as e:
        print(f"Error: {e}")

    # Valid returning
    try:
        print("\n-> Charlie (Premium) returns 3 books:")
        members[2].return_book(3)
        print("Success.")
    except Exception as e:
        print(f"Error: {e}")

    # Invalid returning (returning more than borrowed)
    try:
        print("\n-> Alice (Regular) attempts to return 3 books (only borrowed 2):")
        members[0].return_book(3)
        print("Success.")
    except ValueError as e:
        print(f"Exception caught (ValueError): {e}")

    print("\n=== Member Details After Transactions ===")
    # Demonstrate polymorphism again after state changes
    for member in members:
        member.display_details()


if __name__ == "__main__":
    main()
