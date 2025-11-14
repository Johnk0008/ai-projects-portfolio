#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_ACCOUNTS 100
#define FILENAME "bank_accounts.dat"

// Structure to represent a bank account
typedef struct {
    int account_number;
    char name[100];
    double balance;
    char account_type[20];
} BankAccount;

// Global variables
BankAccount accounts[MAX_ACCOUNTS];
int account_count = 0;

// Function prototypes
void loadAccounts();
void saveAccounts();
void createAccount();
void deposit();
void withdraw();
void balanceEnquiry();
void displayAllAccounts();
int findAccount(int account_number);
void displayMenu();

int main() {
    loadAccounts();
    
    int choice;
    
    printf("🏦 Welcome to Bank Account Management System 🏦\n");
    
    do {
        displayMenu();
        printf("Enter your choice: ");
        scanf("%d", &choice);
        
        switch(choice) {
            case 1:
                createAccount();
                break;
            case 2:
                deposit();
                break;
            case 3:
                withdraw();
                break;
            case 4:
                balanceEnquiry();
                break;
            case 5:
                displayAllAccounts();
                break;
            case 6:
                saveAccounts();
                printf("✅ Thank you for using our banking system!\n");
                printf("👋 Goodbye!\n");
                break;
            default:
                printf("❌ Invalid choice! Please try again.\n");
        }
    } while(choice != 6);
    
    return 0;
}

void displayMenu() {
    printf("\n═══════════════════════════════════════════\n");
    printf("           BANKING SYSTEM MENU\n");
    printf("═══════════════════════════════════════════\n");
    printf("1. 📝 Create New Account\n");
    printf("2. 💰 Deposit Money\n");
    printf("3. 💸 Withdraw Money\n");
    printf("4. 📊 Balance Enquiry\n");
    printf("5. 👥 Display All Accounts\n");
    printf("6. 🚪 Exit\n");
    printf("═══════════════════════════════════════════\n");
}

void loadAccounts() {
    FILE *file = fopen(FILENAME, "rb");
    if (file == NULL) {
        printf("ℹ️  No existing accounts found. Starting fresh.\n");
        return;
    }
    
    account_count = fread(accounts, sizeof(BankAccount), MAX_ACCOUNTS, file);
    fclose(file);
    
    printf("✅ Loaded %d accounts from database.\n", account_count);
}

void saveAccounts() {
    FILE *file = fopen(FILENAME, "wb");
    if (file == NULL) {
        printf("❌ Error: Could not save accounts to file!\n");
        return;
    }
    
    fwrite(accounts, sizeof(BankAccount), account_count, file);
    fclose(file);
    
    printf("✅ Accounts saved successfully!\n");
}

void createAccount() {
    if (account_count >= MAX_ACCOUNTS) {
        printf("❌ Maximum account limit reached!\n");
        return;
    }
    
    BankAccount new_account;
    
    printf("\n📝 CREATE NEW ACCOUNT\n");
    printf("═══════════════════════════════════════════\n");
    
    // Generate account number
    new_account.account_number = 1000 + account_count + 1;
    
    printf("Enter account holder's name: ");
    getchar(); // Clear input buffer
    fgets(new_account.name, sizeof(new_account.name), stdin);
    new_account.name[strcspn(new_account.name, "\n")] = 0; // Remove newline
    
    printf("Enter account type (Savings/Current): ");
    fgets(new_account.account_type, sizeof(new_account.account_type), stdin);
    new_account.account_type[strcspn(new_account.account_type, "\n")] = 0;
    
    printf("Enter initial deposit: ");
    scanf("%lf", &new_account.balance);
    
    if (new_account.balance < 0) {
        printf("❌ Invalid initial deposit amount!\n");
        return;
    }
    
    accounts[account_count] = new_account;
    account_count++;
    
    printf("✅ Account created successfully!\n");
    printf("📋 Account Details:\n");
    printf("   Account Number: %d\n", new_account.account_number);
    printf("   Holder Name: %s\n", new_account.name);
    printf("   Account Type: %s\n", new_account.account_type);
    printf("   Balance: $%.2lf\n", new_account.balance);
}

int findAccount(int account_number) {
    for (int i = 0; i < account_count; i++) {
        if (accounts[i].account_number == account_number) {
            return i;
        }
    }
    return -1;
}

void deposit() {
    int account_number;
    double amount;
    
    printf("\n💰 DEPOSIT MONEY\n");
    printf("═══════════════════════════════════════════\n");
    
    printf("Enter account number: ");
    scanf("%d", &account_number);
    
    int index = findAccount(account_number);
    if (index == -1) {
        printf("❌ Account not found!\n");
        return;
    }
    
    printf("Account Holder: %s\n", accounts[index].name);
    printf("Current Balance: $%.2lf\n", accounts[index].balance);
    
    printf("Enter amount to deposit: ");
    scanf("%lf", &amount);
    
    if (amount <= 0) {
        printf("❌ Invalid deposit amount!\n");
        return;
    }
    
    accounts[index].balance += amount;
    
    printf("✅ Deposit successful!\n");
    printf("💰 New Balance: $%.2lf\n", accounts[index].balance);
    
    saveAccounts();
}

void withdraw() {
    int account_number;
    double amount;
    
    printf("\n💸 WITHDRAW MONEY\n");
    printf("═══════════════════════════════════════════\n");
    
    printf("Enter account number: ");
    scanf("%d", &account_number);
    
    int index = findAccount(account_number);
    if (index == -1) {
        printf("❌ Account not found!\n");
        return;
    }
    
    printf("Account Holder: %s\n", accounts[index].name);
    printf("Current Balance: $%.2lf\n", accounts[index].balance);
    
    printf("Enter amount to withdraw: ");
    scanf("%lf", &amount);
    
    if (amount <= 0) {
        printf("❌ Invalid withdrawal amount!\n");
        return;
    }
    
    if (amount > accounts[index].balance) {
        printf("❌ Insufficient funds!\n");
        return;
    }
    
    accounts[index].balance -= amount;
    
    printf("✅ Withdrawal successful!\n");
    printf("💰 New Balance: $%.2lf\n", accounts[index].balance);
    
    saveAccounts();
}

void balanceEnquiry() {
    int account_number;
    
    printf("\n📊 BALANCE ENQUIRY\n");
    printf("═══════════════════════════════════════════\n");
    
    printf("Enter account number: ");
    scanf("%d", &account_number);
    
    int index = findAccount(account_number);
    if (index == -1) {
        printf("❌ Account not found!\n");
        return;
    }
    
    printf("\n📋 Account Details:\n");
    printf("═══════════════════════════════════════════\n");
    printf("Account Number: %d\n", accounts[index].account_number);
    printf("Holder Name: %s\n", accounts[index].name);
    printf("Account Type: %s\n", accounts[index].account_type);
    printf("Current Balance: $%.2lf\n", accounts[index].balance);
    printf("═══════════════════════════════════════════\n");
}

void displayAllAccounts() {
    if (account_count == 0) {
        printf("❌ No accounts found!\n");
        return;
    }
    
    printf("\n👥 ALL ACCOUNTS\n");
    printf("═══════════════════════════════════════════\n");
    printf("%-15s %-20s %-15s %-10s\n", 
           "Account No.", "Holder Name", "Account Type", "Balance");
    printf("═══════════════════════════════════════════\n");
    
    double total_balance = 0;
    for (int i = 0; i < account_count; i++) {
        printf("%-15d %-20s %-15s $%-9.2lf\n", 
               accounts[i].account_number,
               accounts[i].name,
               accounts[i].account_type,
               accounts[i].balance);
        total_balance += accounts[i].balance;
    }
    
    printf("═══════════════════════════════════════════\n");
    printf("Total Accounts: %d\n", account_count);
    printf("Total Balance: $%.2lf\n", total_balance);
    printf("═══════════════════════════════════════════\n");
}