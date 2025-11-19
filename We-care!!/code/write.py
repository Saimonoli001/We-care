import read
import datetime
import os
def calculate_Vat(amount, Vat_percentage=13):
    return amount* (Vat_percentage/100)

def invoice(cart, vendor_name, totalAmount, include_vat):
    try:
        # Create invoice folder if it doesn't exist
        invoice_folder = "invoice"
        if not os.path.exists(invoice_folder):
            os.makedirs(invoice_folder)
            
        # Generate unique timestamp-based filename
        dateTime = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        fileName = os.path.join(invoice_folder, f"{dateTime}-{vendor_name.lower()}.txt")
        
        Vat_amount = 0
        if include_vat:
            Vat_amount = calculate_Vat(totalAmount)
            total_with_vat = totalAmount + Vat_amount
        else:
            total_with_vat = totalAmount

        # Create and write to the invoice file
        with open(fileName, "w") as file:
            file.write("______________________________ RECEIPT _______________________________\n\n")
            file.write(f"                          Date: {dateTime}\n")
            file.write(f"Vendor: {vendor_name}\n")
            file.write("_"*60 +"\n")

            # Write details for each item in the cart
            for item in cart:
                if 'quantity bought' in item:
                    # For customer purchases
                    file.write(f"Product: {item['product'].title()} \nQuantity Bought: {item['quantity bought']} \nFree Items: {item['free quantity']} \nTotal Quantity: {item['total quantity']} \nPrice Per Unit: {item['price per unit']} \nTotal Paid: {item['total paid']}\n")
                else:
                    # For restocking or adding new inventory
                    file.write(f"Product: {item['product'].title()} \nQuantity Added: {item['quantity']} \nPrice Per Unit: {item['price']} \nTotal: {item['total paid']}\n")

            file.write("\n")

            # Always print VAT and total with VAT
            file.write(f"VAT (13%): {Vat_amount:.2f}\n")
            file.write("_"*60 + "\n")
            file.write(f"TOTAL AMOUNT (with VAT): {total_with_vat:.2f}\n")
            file.write("\n_____________________________ THANK YOU! _____________________________\n")
        
        # Check if file was created successfully
        if os.path.exists(fileName):
            print(f"\nInvoice generated: {fileName}")
        else:
            print("\n!!! Invoice file could not be created !!!")

    except Exception as e:
        print(f"\n!!! Error while generating invoice: {e} !!!")
        print(f"Attempted to create file: {fileName if 'fileName' in locals() else 'unknown'}")

def sales_invoice(cart, totalAmount, calculate_vat, vat_amount, vendor_name, customer_name=None):
    """
    Generate a specialized sales invoice for customer purchases with
    more detailed formatting and customer information.
    """
    try:
        # Create invoice folder if it doesn't exist
        invoice_folder = "sales_invoices"
        if not os.path.exists(invoice_folder):
            os.makedirs(invoice_folder)
            
        # Get customer name if not provided
        if customer_name is None:
            customer_name = input("Enter customer name: ").strip() or "Guest"
            
        # Generate unique invoice number and timestamp
        invoice_num = f"INV-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        include_vat= input("\nDo you want to include VAT (13%) in the invoice? (y/n): ").lower() =='y'
        vat_amount=0
        if include_vat:
            vat_amount = calculate_Vat(totalAmount)
            totalAmount += vat_amount

        # Create filename
        fileName = os.path.join(invoice_folder, f"{invoice_num}_{customer_name.replace(' ', '_')}.txt")
        
        # Create and write to the invoice file
        with open(fileName, "w") as file:
            # Header
            file.write("="*80 + "\n")
            file.write(f"{'SALES INVOICE':^80}\n")
            file.write("="*80 + "\n\n")
            
            # Invoice details
            file.write(f"{'Invoice Number:':<20} {invoice_num}\n")
            file.write(f"{'Date:':<20} {current_date}\n")
            file.write(f"{'Customer Name:':<20} {customer_name}\n\n")
            
            # Items table header
            file.write("-"*80 + "\n")
            file.write(f"{'Product':<30} {'Qty':<8} {'Free':<8} {'Price':<15} {'Total':<15}\n")
            file.write("-"*80 + "\n")
            
            # Items
            for item in cart:
                product_name = item['product'].title()
                qty = item.get('quantity bought', item.get('quantity', 0))
                free_qty = item.get('free quantity', 0)
                price = item.get('price per unit',0)
                if price is None:
                    price= item.get('price')
                total = item.get('total paid', 0)
                
                file.write(f"{product_name:<30} {qty:<8} {free_qty:<8} {price:<15} {total:<15}\n")

                
                include_vat = input("\nDo you want to include VAT (13%) in the invoice? (y/n):").lower()=='y'
                if include_vat:
                    vat_amount=calculate_vat(totalAmount)
                    totalAmount += vat_amount
            # Generate invoice with all provided data, no prompts
                invoice(cart, vendor_name, totalAmount, include_vat)
           
            # Summary
            file.write("-"*80 + "\n")
            if include_vat:
                file.write(f"{'VAT (13%)':<46} {vat_amount:>30.2f}\n")
            file.write(f"{'TOTAL AMOUNT:':<46} {totalAmount:>30.2f}\n")
            
            # Additional information about free items promotion
            if any('free quantity' in item and item['free quantity'] > 0 for item in cart):
                file.write("\n")
                file.write("*"*80 + "\n")
                file.write("Special Promotion: Buy 3 Get 1 Free!\n")
                file.write("*"*80 + "\n")
            
            # Footer
            file.write("\n" + "="*80 + "\n")
            file.write(f"{'THANK YOU FOR YOUR PURCHASE!':^80}\n")
            file.write(f"{'Please come again!':^80}\n")
            file.write("="*80 + "\n")
        
        print(f"\nSales invoice generated: {fileName}")
        return fileName

    except Exception as e:
        print(f"\n!!! Error while generating sales invoice: {e} !!!")
        return None
    
def writeUpdatedStock(stocks):
    try:
        with open("product.txt", "w") as fStock:
            for i in stocks:
                fStock.write(f"{i['name'].strip().title()}, {i['model'].strip().title()}, {i['quantity']}, {i['price']}, {i['made_in'].strip()}\n")
        print("\nStock updated successfully!")
        return True
    except Exception as e:
        print(f"Error writing to file: {e}")
        return False

def manage_inventory():
    """Function to manage inventory with options to add or restock items"""
    stocks = read.readFile()
    
    while True:
        print("\n----- Inventory Management -----")
        print("1. Add new items")
        print("2. Restock existing items")
        print("3. Return to main menu")
        
        try:
            choice = int(input("\nEnter your choice (1-3): "))
            
            if choice == 1:
                add_new_items(stocks)
            elif choice == 2:
                restock_items(stocks)
            elif choice == 3:
                print("Returning to main menu...")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {e}")

def add_new_items(stocks):
    """Add new items to inventory"""
    cart = []
    totalAmount = 0
    
    # Get vendor (supplier) information first
    vendor_name = input("\nEnter the vendor/supplier name: ").strip()
    
    
    want_to_add = "y"
    while want_to_add.lower() == 'y':
        try:
            # Get product details
            name = input("\nEnter the name of the new product: ").strip()
            
            if name.isdigit():
                    raise ValueError("Product name cannot be an integer. please provide a valid name")
        except ValueError as ve:
            print(f"Error:{ve}")
            input("Press enter to continue......")
            continue

            # Check if product already exists
        if any(item["name"].lower() == name.lower() for item in stocks):
                print("\nThis product already exists! Use restock option to add more quantity.")
                want_to_add = input("\nDo you want to add another new product? (y/n): ")
                continue
                
        model = input("Enter the brand/model: ").strip()
            
        try:
                quantity = int(input("Enter the initial quantity: "))
                if quantity <= 0:
                    print("Please enter a positive quantity.")
                    continue
                    
                price = int(input("Enter the cost price: "))
                if price <= 0:
                    print("Please enter a positive price.")
                    continue
        except ValueError:
                print("Please enter valid numbers for quantity and price.")
                continue
        try:        
            made_in = input("Enter country of origin: ").strip()
            
            # Add to stocks
            new_item = {
                'name': name,
                'model': model,
                'quantity': quantity,
                'price': price,
                'made_in': made_in
            }
            
            stocks.append(new_item)
            
            # Add to cart for invoice
            cart.append({
                "product": name,
                "quantity": quantity,
                "price": price,
                "total paid": price * quantity
            })
            
            totalAmount += price * quantity 
            print(f"\n{name} added to inventory successfully!")
            
        except Exception as e:
            print(f"\n!!! Error adding item: {e} !!!")
           

            
        want_to_add = input("\nDo you want to add another new product? (y/n): ")
    
    if cart:
        if writeUpdatedStock(stocks):
            include_vat = input("\nDo you want to include VAT (13%) in the invoice? (y/n):").lower()=='y'
            # Generate invoice with all provided data, no prompts
            invoice(cart, vendor_name, include_vat, totalAmount)
    else:
        print("No new products added.")

def restock_items(stocks):
    """Restock existing items in inventory"""
    cart = []
    totalAmount = 0
    
    # Get vendor (supplier) information first
    vendor_name = input("\nEnter the vendor/supplier name: ").strip()
    
    if not stocks:
        print("\nNo items in inventory. Please add items first.")
        return
        
    want_to_restock = "y"
    while want_to_restock.lower() == 'y':
        try:
            # Display available products
            print("\nAvailable Products:")
            for idx, item in enumerate(stocks, start=1):
                print(f"{idx}. {item['name']} ({item['model']}) - Current quantity: {item['quantity']}")
            
            try:
                choice = int(input("\nEnter product number to restock (0 to cancel): "))
                if choice == 0:
                    break
                if choice < 1 or choice > len(stocks):
                    print("Invalid product number.")
                    continue
                
                selected_item = stocks[choice - 1]
                name = selected_item ['name']
                
                try:
                    add_quantity = int(input(f"Current quantity: {selected_item['quantity']}. Enter additional quantity: "))
                    if add_quantity <= 0:
                        print("Please enter a positive quantity.")
                        continue
                        
                    price = int(input("Enter the cost price: "))
                    if price <= 0:
                        print("Please enter a positive price.")
                        continue
                except ValueError:
                    print("Please enter valid numbers for quantity and price.")
                    continue
                
                # Update stock quantity
                stocks[choice - 1]['quantity'] += add_quantity
                
                # Add to cart for invoice
                cart.append({
                    "product": name,
                    "quantity": add_quantity,
                    "price": price,
                    "total paid": price * add_quantity
                })
                
                totalAmount += price * add_quantity
                print(f"\n{name} restocked successfully! New quantity: {stocks[choice - 1]['quantity']}")
                
            except ValueError:
                print("Please enter a valid number.")
                continue
                
        except Exception as e:
            print(f"\n!!! Error restocking item: {e} !!!")

            try:
                name =input("Enter the product name").strip()
                if name.isdigit():
                    raise ValueError("Product name cannot be an integer. please provide a valid name")
            except ValueError as ve:
                print(f"Error:{ve}")
                
            
        want_to_restock = input("\nDo you want to restock another product? (y/n): ")
    
    if cart:
        if writeUpdatedStock(stocks):
            include_vat = input("\n Do you want to include VAT (13%) in the invoice? (y/n): ").lower()=='y'
            # Generate invoice with all provided data, no prompts
            invoice(cart, vendor_name, totalAmount, include_vat)
    else:
        print("No items restocked.")

