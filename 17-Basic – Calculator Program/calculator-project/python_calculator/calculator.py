"""
Advanced Calculator Program with basic arithmetic operations
"""

class Calculator:
    """A simple calculator class implementing basic operations"""
    
    @staticmethod
    def add(a: float, b: float) -> float:
        """Add two numbers"""
        return a + b
    
    @staticmethod
    def subtract(a: float, b: float) -> float:
        """Subtract second number from first"""
        return a - b
    
    @staticmethod
    def multiply(a: float, b: float) -> float:
        """Multiply two numbers"""
        return a * b
    
    @staticmethod
    def divide(a: float, b: float) -> float:
        """Divide first number by second number"""
        if b == 0:
            raise ValueError("Division by zero is not allowed!")
        return a / b
    
    @staticmethod
    def power(a: float, b: float) -> float:
        """Raise first number to the power of second number"""
        return a ** b
    
    @staticmethod
    def modulo(a: float, b: float) -> float:
        """Calculate modulo of first number by second number"""
        if b == 0:
            raise ValueError("Modulo by zero is not allowed!")
        return a % b


def display_menu() -> None:
    """Display the calculator menu"""
    print("\n" + "="*50)
    print("           ADVANCED CALCULATOR PROGRAM")
    print("="*50)
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    print("5. Power (^)")
    print("6. Modulo (%)")
    print("7. Exit")
    print("="*50)


def get_number_input(prompt: str) -> float:
    """Get valid number input from user"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input! Please enter a valid number.")


def get_operation_choice() -> int:
    """Get valid operation choice from user"""
    while True:
        try:
            choice = int(input("Enter your choice (1-7): "))
            if 1 <= choice <= 7:
                return choice
            else:
                print("Please enter a number between 1 and 7.")
        except ValueError:
            print("Invalid input! Please enter a number between 1 and 7.")


def perform_operation(choice: int, calc: Calculator, num1: float, num2: float) -> None:
    """Perform the selected arithmetic operation"""
    operations = {
        1: ("+", calc.add),
        2: ("-", calc.subtract),
        3: ("*", calc.multiply),
        4: ("/", calc.divide),
        5: ("^", calc.power),
        6: ("%", calc.modulo)
    }
    
    operator, operation_func = operations[choice]
    
    try:
        result = operation_func(num1, num2)
        print(f"Result: {num1} {operator} {num2} = {result}")
    except (ValueError, ZeroDivisionError) as e:
        print(f"Error: {e}")


def main():
    """Main function to run the calculator program"""
    calc = Calculator()  # This line was missing the Calculator class definition
    
    print("Welcome to the Advanced Calculator!")
    
    while True:
        display_menu()
        choice = get_operation_choice()
        
        if choice == 7:
            print("Thank you for using the calculator! Goodbye!")
            break
        
        # Fixed the multi-line string issue
        operation_names = ['Addition', 'Subtraction', 'Multiplication', 'Division', 'Power', 'Modulo']
        print(f"\nOperation selected: {operation_names[choice-1]}")
        
        num1 = get_number_input("Enter first number: ")
        num2 = get_number_input("Enter second number: ")
        
        perform_operation(choice, calc, num1, num2)
        
        # Ask if user wants to continue
        continue_calc = input("\nDo you want to perform another calculation? (y/n): ").lower()
        if continue_calc not in ['y', 'yes']:
            print("Thank you for using the calculator! Goodbye!")
            break


if __name__ == "__main__":
    main()