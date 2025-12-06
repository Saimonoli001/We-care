import os
import read
import Operation
import write


def initialize_program():
    """Check if product.txt exists, if not create it with sample data"""
    if not os.path.exists("product.txt"):
        print("Initializing product inventory file...")
        with open("product.txt", "w") as f:
            f.write("Vitamin C Serum, Garnier, 210, 12000, Spain\n") 
            f.write("Skin Cleanser, Cetaphil, 109, 2400, Switzerland\n")
            f.write("Sunscreen, Aqualogica, 215, 4000, Nepal\n")
        print("Product inventory initialized with sample data.")

def display_header():
    """Display a nicely formatted header for the program"""
    print("               WELCOME TO Wecare MANAGEMENT SYSTEM")

def main():
    initialize_program()
    
    while True:
        try:
            display_header()
            choice = int(input('''
    ┌──────────────── MAIN MENU ────────────────┐
    │                                           │
    │  1. Display all products                  │
    │  2. Buy products from manufacturer        │
    │  3. Sell products to customer             │
    │  4. Exit                                  │
    │                                           │
    └───────────────────────────────────────────┘
    
    Your operation: '''))

            if choice == 1:
                read.display()  # Displays product details
                input("\nPress Enter to continue...")
                
            elif choice == 2:
                write.manage_inventory()
                
            elif choice == 3:
                read.display()  # Displays product details
                Operation.customerOperation(read.readFile())
                input("\nPress Enter to continue...")
            
            elif choice == 4:
                print("\nThank you for using SaimonCare Pharmacy Management System!")
                break  

            else:
                print("\nInvalid option. Please choose between 1 and 4.")
                input("\nPress Enter to continue...")

        except ValueError:
            print("\nInvalid input. Please enter a number between 1 and 4.")
            input("\nPress Enter to continue...")
            
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
