from write import invoice

# Helper function to update stock file
def updateStockFile(stocks):
    try:
        with open("product.txt", "w") as fStock:
            for i in stocks:
                fStock.write(f"{i['name'].strip().title()}, {i['model'].strip().title()}, {i['quantity']}, {i['price']}, {i['made_in'].strip()}\n")
        print("\nStock updated successfully!")
        return True
    except Exception as e:
        print(f"Error writing to file: {e}")
        return False
        

# Helper function to check if the product is in the cart
def isProductInCart(cart, productName):
    return any(item["product"].lower() == productName.lower() for item in cart)

# Customer Operation
def customerOperation(stocks):
    cart = []
    totalAmount = 0
    want = "y"
    vendor_name = input("\nEnter the vendor/supplier name: ").strip()
    if not vendor_name:
        print("customer name is required to procced")

    while want.lower() == 'y':
        try:
            print("\nNote: Please enter the product carefully! The product outside the stocks won't be entered!")
            productName = input("Enter the name of the product you want to sell: ")

            if isProductInCart(cart, productName):
                print("\nYou already bought the product! Please enter another product!")
                continue

            productQuantity = int(input("\nEnter the quantity you want to sell: "))

            found = False
            for i in stocks:
                if i["name"].lower() == productName.lower():
                    found = True
                    freeItems = productQuantity // 3
                    totalQuantity = productQuantity + freeItems

                    if i["quantity"] >= totalQuantity:
                        cart.append({
                            "product": productName,
                            "quantity bought": productQuantity,
                            "free quantity": freeItems,
                            "total quantity": totalQuantity,
                            "price per unit": i['price'] * 2,
                            "total paid": int((i['price'] * 2) * productQuantity),
                            "quantity" : totalQuantity
                        })
                        i["quantity"] -= totalQuantity
                        totalAmount += int((i['price'] * 2) * productQuantity)
                        print(f"\nItem added to cart. You received {freeItems} item(s) free!")
                    else:
                        print(f"\nSorry! Not enough stock. Only {i['quantity']} item(s) left (including free item requirement).")
                    break
            if not found:
                print("\nProduct not found in stock.")
        except ValueError:
            print("\n!!! Input Error: Please enter a valid number !!!")
        except Exception as e:
            print(f"\n!!! Unexpected Error: {e} !!!")

        want = input("\nDo you want to sell another item? (y/n): ")

    if cart:
        if updateStockFile(stocks):
            include_vat = input("\nDo you want to include VAT (13%) in the invoice? (y/n):").lower() == 'y'
            print(include_vat)
            try:
                invoice(cart, vendor_name, totalAmount, include_vat)
                print("\nInvoice generated successfully.")
            except Exception as e:
                print(f"\nError generating invoice: {e}")
    else:
        print("\nNo product in the cart, so invoice can't be generated.")

# Manufacturer Operation
def manufacturerOperation(stocks):
    cart = []
    totalAmount = 0
    want = "y"

    while want.lower() == 'y':
        try:
            print("\nNote: Please enter the product carefully! The product outside the stocks won't be entered!")
            productName = input("Enter the name of the product you want to buy: ")

            if isProductInCart(cart, productName):
                print("\nYou already bought the product! Please enter another product!")
                continue

            productQuantity = int(input("\nEnter the quantity you want to buy: "))

            found = False
            for i in stocks:
                if i["name"].lower() == productName.lower():
                    found = True
                    cart.append({
                        "product": productName.lower(),
                        "quantity": productQuantity,
                        "price": i['price'],
                        "total paid": int(i['price'] * productQuantity)
                    })
                    i["quantity"] += productQuantity
                    totalAmount += int(i['price'] * productQuantity)
                    print("\nItem successfully added to cart.")
                    break
            if not found:
                print("\nProduct not found in stock.")
        except ValueError:
            print("\n!!! Input Error: Please enter a valid number !!!")
        except Exception as e:
            print(f"\n!!! Unexpected Error: {e} !!!")

        want = input("\nDo you again want to buy more items? (y/n): ")

    if cart:
        if updateStockFile(stocks):
            include_vat = input("\nDo you want to include VAT (13%) in the invoice? (y/n):").lower() == 'y'
            try:
                invoice(cart, "Manufacturer's", totalAmount, include_vat)
                print("\nInvoice generated successfully.")
            except Exception as e:
                print(f"\nError generating invoice: {e}")
    else:
        print("\nNo product in the cart, so invoice can't be generated.")
