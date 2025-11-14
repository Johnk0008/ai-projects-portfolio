#include <stdio.h>
#include <stdlib.h>

// Function prototypes
double add(double a, double b);
double subtract(double a, double b);
double multiply(double a, double b);
double divide(double a, double b);
void display_menu();

int main() {
    double num1, num2, result;
    char operation;
    int choice;
    
    printf("=== BASIC CALCULATOR PROGRAM ===\n");
    
    do {
        display_menu();
        printf("Enter your choice (1-5): ");
        scanf("%d", &choice);
        
        if(choice == 5) {
            printf("Thank you for using the calculator! Goodbye!\n");
            break;
        }
        
        if(choice < 1 || choice > 5) {
            printf("Invalid choice! Please select between 1-5.\n\n");
            continue;
        }
        
        printf("Enter first number: ");
        scanf("%lf", &num1);
        printf("Enter second number: ");
        scanf("%lf", &num2);
        
        switch(choice) {
            case 1:
                result = add(num1, num2);
                printf("Result: %.2lf + %.2lf = %.2lf\n\n", num1, num2, result);
                break;
                
            case 2:
                result = subtract(num1, num2);
                printf("Result: %.2lf - %.2lf = %.2lf\n\n", num1, num2, result);
                break;
                
            case 3:
                result = multiply(num1, num2);
                printf("Result: %.2lf * %.2lf = %.2lf\n\n", num1, num2, result);
                break;
                
            case 4:
                if(num2 != 0) {
                    result = divide(num1, num2);
                    printf("Result: %.2lf / %.2lf = %.2lf\n\n", num1, num2, result);
                } else {
                    printf("Error: Division by zero is not allowed!\n\n");
                }
                break;
                
            default:
                printf("Invalid operation!\n\n");
        }
        
    } while(choice != 5);
    
    return 0;
}

// Function to display menu
void display_menu() {
    printf("Available Operations:\n");
    printf("1. Addition (+)\n");
    printf("2. Subtraction (-)\n");
    printf("3. Multiplication (*)\n");
    printf("4. Division (/)\n");
    printf("5. Exit\n");
}

// Arithmetic functions
double add(double a, double b) {
    return a + b;
}

double subtract(double a, double b) {
    return a - b;
}

double multiply(double a, double b) {
    return a * b;
}

double divide(double a, double b) {
    return a / b;
}