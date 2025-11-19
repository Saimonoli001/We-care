def calculateSellingPrice(baseCost):
    return 2 * int(baseCost)


def readFile():
    inventory = []
    try:
        with open("product.txt", "r") as dataFile:
            records = dataFile.readlines()
            for entry in records:
                line = entry.strip()
                if line:
                    item = line.split(",")
                    if len(item) == 5:
                        inventory.append({
                            'name': item[0].strip(),
                            'model': item[1].strip(),
                            'quantity': int(item[2].strip()),
                            'price': int(item[3].strip()),
                            'made_in': item[4].strip()
                        })
    except FileNotFoundError:
        print("product.txt not found.")
    return inventory

def display():
    print("\nWelcome to the SaimonCare Stock System!")
    print("The following products are currently available:\n")
    print("-----------------------------------------------------------------------------------------------")
    print("|        Name        |     Brand           |    Stocks    |     Price    |     Made in        |")
    print("-----------------------------------------------------------------------------------------------")

    stockList = readFile()

    for product in stockList:
        name = product['name']
        model = product['model']
        quantity = product['quantity']
        price = calculateSellingPrice(product['price'])
        origin = product['made_in']

        print(f"| {name:<18} | {model:<19} | {quantity:<12} | {price:<12} | {origin:<18} |")
        print("-----------------------------------------------------------------------------------------------")
