import csv
from datetime import datetime


# ============================================================
# SMART STOCK PORTFOLIO TRACKER
# ============================================================

stock_prices = {
    "AAPL": 180,
    "TSLA": 250,
    "MSFT": 420,
    "GOOGL": 175,
    "AMZN": 190,
    "NVDA": 145,
    "META": 560,
    "NFLX": 700,
    "AMD": 160,
    "INTC": 25
}

# ============================================================
# CURRENT MARKET PRICES
# ============================================================

current_prices = {
    "AAPL": 195,
    "TSLA": 270,
    "MSFT": 440,
    "GOOGL": 185,
    "AMZN": 205,
    "NVDA": 155,
    "META": 590,
    "NFLX": 730,
    "AMD": 175,
    "INTC": 28
}

portfolio = []
transactions = []


# ============================================================
# SHOW AVAILABLE STOCKS
# ============================================================

def show_stocks():

    print("\n========================================")
    print("           AVAILABLE STOCKS")
    print("========================================")

    print(f"{'Stock':<10}{'Price':<10}")
    print("----------------------------------------")

    for stock, price in stock_prices.items():
        print(f"{stock:<10}₹{price}")


# ============================================================
# BUY STOCK
# ============================================================

def buy_stock():

    print("\n========================================")
    print("               BUY STOCK")
    print("========================================")

    stock = input("Enter stock symbol: ").upper()

    if stock not in stock_prices:
        print("\n❌ Stock not available.")
        return

    try:
        quantity = int(input("Enter quantity to buy: "))

        if quantity <= 0:
            print("\n❌ Quantity must be greater than 0.")
            return

    except ValueError:
        print("\n❌ Please enter a valid number.")
        return

    price = stock_prices[stock]
    investment = price * quantity

    # Check if stock already exists
    for item in portfolio:

        if item[0] == stock:

            old_quantity = item[1]
            new_quantity = old_quantity + quantity
            new_investment = price * new_quantity

            item[1] = new_quantity
            item[3] = new_investment

            print("\n✅ Stock purchased successfully!")
            print(f"Stock: {stock}")
            print(f"Previous Quantity: {old_quantity}")
            print(f"Bought Quantity: {quantity}")
            print(f"New Quantity: {new_quantity}")
            print(f"Price: ₹{price}")
            print(f"Purchase Value: ₹{investment}")

            transactions.append([
                datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "BUY",
                stock,
                quantity,
                price,
                investment
            ])
            
            save_transactions()

            return

    # Add new stock
    portfolio.append([
        stock,
        quantity,
        price,
        investment
    ])

    transactions.append([
        datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "BUY",
        stock,
        quantity,
        price,
        investment
    ])
    
    save_transactions()

    print("\n✅ Stock purchased successfully!")
    print(f"Stock: {stock}")
    print(f"Quantity: {quantity}")
    print(f"Price: ₹{price}")
    print(f"Purchase Value: ₹{investment}")


# ============================================================
# SELL STOCK
# ============================================================

def sell_stock():

    print("\n========================================")
    print("              SELL STOCK")
    print("========================================")

    if not portfolio:

        print("\n❌ Your portfolio is empty.")
        return

    stock = input("Enter stock symbol: ").upper()

    for item in portfolio:

        if item[0] == stock:

            current_quantity = item[1]
            buy_price = item[2]

            print(f"\nCurrent Quantity: {current_quantity}")

            try:

                quantity = int(
                    input("Enter quantity to sell: ")
                )

                if quantity <= 0:

                    print(
                        "\n❌ Quantity must be greater than 0."
                    )

                    return

            except ValueError:

                print(
                    "\n❌ Please enter a valid number."
                )

                return

            if quantity > current_quantity:

                print("\n❌ Not enough shares.")

                print(
                    f"You currently have {current_quantity} shares."
                )

                return

            # Current market price
            sale_price = current_prices[stock]

            # Calculate sale value
            sale_value = sale_price * quantity

            # Calculate original cost
            original_cost = buy_price * quantity

            # Calculate realized profit/loss
            realized_profit_loss = (
                sale_value - original_cost
            )

            # Calculate remaining quantity
            remaining_quantity = (
                current_quantity - quantity
            )

            if remaining_quantity == 0:

                portfolio.remove(item)

            else:

                item[1] = remaining_quantity
                item[3] = buy_price * remaining_quantity

            print("\n✅ Stock sold successfully!")

            print(
                f"Previous Quantity : {current_quantity}"
            )

            print(
                f"Sold Quantity     : {quantity}"
            )

            print(
                f"Remaining Quantity: {remaining_quantity}"
            )

            print(f"Stock             : {stock}")
            print(f"Buy Price         : ₹{buy_price}")
            print(f"Sale Price        : ₹{sale_price}")
            print(f"Sale Value        : ₹{sale_value}")
            print(f"Original Cost     : ₹{original_cost}")

            if realized_profit_loss > 0:

                print(
                    f"Realized Profit   : ₹{realized_profit_loss}"
                )

            elif realized_profit_loss < 0:

                print(
                    f"Realized Loss     : ₹{abs(realized_profit_loss)}"
                )

            else:

                print(
                    "Realized Profit/Loss: ₹0"
                )

            # Record SELL transaction
            transactions.append([
                datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                ),
                "SELL",
                stock,
                quantity,
                sale_price,
                sale_value
            ])

            # Automatically save transaction
            save_transactions()

            # Automatically save portfolio
            save_portfolio()

            print(
                "\n✅ SELL transaction saved successfully!"
            )

            return

    print("\n❌ Stock not found in your portfolio.")


# ============================================================
# VIEW PORTFOLIO
# ============================================================

def view_portfolio():

    print("\n============================================================")
    print("                    YOUR PORTFOLIO")
    print("============================================================")

    if not portfolio:

        print("\n❌ Your portfolio is empty.")
        return

    print(
        f"{'Stock':<8}"
        f"{'Qty':<7}"
        f"{'Buy Price':<12}"
        f"{'Current':<12}"
        f"{'Value':<14}"
        f"{'P/L':<12}"
    )

    print("-" * 65)

    total_investment = 0
    total_current_value = 0

    for item in portfolio:

        stock = item[0]
        quantity = item[1]
        buy_price = item[2]
        investment = item[3]

        current_price = current_prices[stock]

        current_value = current_price * quantity

        profit_loss = current_value - investment

        total_investment += investment
        total_current_value += current_value

        print(
            f"{stock:<8}"
            f"{quantity:<7}"
            f"₹{buy_price:<11.2f}"
            f"₹{current_price:<11.2f}"
            f"₹{current_value:<13.2f}"
            f"₹{profit_loss:<11.2f}"
        )

    overall_profit_loss = (
        total_current_value - total_investment
    )

    print("-" * 65)

    print(
        f"Total Investment : ₹{total_investment:.2f}"
    )

    print(
        f"Current Value    : ₹{total_current_value:.2f}"
    )

    if overall_profit_loss > 0:

        print(
            f"Overall Profit   : ₹{overall_profit_loss:.2f}"
        )

    elif overall_profit_loss < 0:

        print(
            f"Overall Loss     : ₹{abs(overall_profit_loss):.2f}"
        )

    else:

        print(
            "Overall Profit/Loss : ₹0.00"
        )

    print("============================================================")


# ============================================================
# CALCULATE TOTAL INVESTMENT
# ============================================================

def calculate_total():

    if not portfolio:
        print("\n❌ Your portfolio is empty.")
        return

    total = 0

    for item in portfolio:
        total += item[3]

    print("\n========================================")
    print("          TOTAL INVESTMENT")
    print("========================================")

    print(f"Total Investment: ₹{total:.2f}")


# ============================================================
# REMOVE STOCK
# ============================================================

def remove_stock():

    if not portfolio:
        print("\n❌ Portfolio is empty.")
        return

    stock = input(
        "\nEnter stock symbol to remove: "
    ).upper()

    for item in portfolio:

        if item[0] == stock:

            portfolio.remove(item)

            print(
                f"\n✅ {stock} removed successfully!"
            )

            return

    print("\n❌ Stock not found in portfolio.")


# ============================================================
# UPDATE STOCK QUANTITY
# ============================================================

def update_stock():

    if not portfolio:
        print("\n❌ Portfolio is empty.")
        return

    stock = input(
        "\nEnter stock symbol to update: "
    ).upper()

    for item in portfolio:

        if item[0] == stock:

            try:

                new_quantity = int(
                    input("Enter new quantity: ")
                )

                if new_quantity <= 0:

                    print(
                        "\n❌ Quantity must be greater than 0."
                    )

                    return

            except ValueError:

                print(
                    "\n❌ Please enter a valid number."
                )

                return

            price = item[2]

            new_investment = (
                price * new_quantity
            )

            item[1] = new_quantity
            item[3] = new_investment

            print("\n✅ Stock updated successfully!")

            print(f"Stock: {stock}")
            print(f"New Quantity: {new_quantity}")
            print(f"Price: ₹{price}")
            print(
                f"New Investment Value: ₹{new_investment}"
            )

            return

    print("\n❌ Stock not found in portfolio.")


# ============================================================
# SEARCH STOCK
# ============================================================

def search_stock():

    if not portfolio:
        print("\n❌ Portfolio is empty.")
        return

    stock = input(
        "\nEnter stock symbol to search: "
    ).upper()

    for item in portfolio:

        if item[0] == stock:

            print("\n✅ Stock found!")

            print(f"Stock: {item[0]}")
            print(f"Quantity: {item[1]}")
            print(f"Price: ₹{item[2]}")
            print(f"Investment: ₹{item[3]}")

            return

    print("\n❌ Stock not found in portfolio.")
    
    
    # ============================================================
# UPDATE MARKET PRICE
# ============================================================

def update_market_price():

    print("\n========================================")
    print("          UPDATE MARKET PRICE")
    print("========================================")

    stock = input("Enter stock symbol: ").upper()

    if stock not in current_prices:

        print("\n❌ Stock not found.")
        return

    print(
        f"\nCurrent Price of {stock}: ₹{current_prices[stock]}"
    )

    try:

        new_price = float(
            input("Enter new market price: ₹")
        )

        if new_price <= 0:

            print("\n❌ Price must be greater than 0.")
            return

    except ValueError:

        print("\n❌ Please enter a valid price.")
        return

    current_prices[stock] = new_price
    
    save_market_prices()

    print("\n✅ Market price updated successfully!")

    print(f"Stock: {stock}")
    print(f"New Market Price: ₹{new_price:.2f}")
    
    
    # ============================================================
    # PORTFOLIO DASHBOARD
    # ============================================================

def portfolio_dashboard():

    print("\n========================================")
    print("          📊 PORTFOLIO DASHBOARD")
    print("========================================")

    if not portfolio:

        print("\n❌ Portfolio is empty.")
        print("Please buy some stocks first.")
        return

    # Number of different stocks
    different_stocks = len(portfolio)

    # Starting values
    total_shares = 0
    total_investment = 0
    total_current_value = 0

    # Calculate portfolio values
    for item in portfolio:

        stock = item[0]
        quantity = item[1]
        investment = item[3]

        total_shares += quantity
        total_investment += investment

        # Use current market price
        current_price = current_prices[stock]

        current_value = current_price * quantity

        total_current_value += current_value

    # Calculate profit/loss
    profit_loss = (
        total_current_value - total_investment
    )
    
    profit_percentage = (
    profit_loss / total_investment
) * 100

    # Display dashboard
    print(f"\nDifferent Stocks : {different_stocks}")
    print(f"Total Shares     : {total_shares}")
    print(f"Investment       : ₹{total_investment:.2f}")
    print(f"Current Value    : ₹{total_current_value:.2f}")
    
    print(f"Profit %         : {profit_percentage:.2f}%")

    if profit_loss > 0:

        print(
            f"Profit/Loss      : Profit ₹{profit_loss:.2f}"
        )

    elif profit_loss < 0:

        print(
            f"Profit/Loss      : Loss ₹{abs(profit_loss):.2f}"
        )

    else:

        print("Profit/Loss      : ₹0.00")

    print(f"Transactions     : {len(transactions)}")

    print("\n========================================")


# ============================================================
# PORTFOLIO ALLOCATION
# ============================================================

def portfolio_allocation():

    if not portfolio:

        print("\n❌ Portfolio is empty.")
        return

    total_investment = 0

    # Calculate total investment
    for item in portfolio:

        total_investment += item[3]

    print("\n========================================")
    print("          PORTFOLIO ALLOCATION")
    print("========================================")

    print(
        f"{'Stock':<10}"
        f"{'Investment':<15}"
        f"{'Allocation':<12}"
    )

    print("----------------------------------------")

    for item in portfolio:

        stock = item[0]
        investment = item[3]

        percentage = (
            investment / total_investment
        ) * 100

        print(
            f"{stock:<10}"
            f"₹{investment:<14.2f}"
            f"{percentage:.2f}%"
        )

    print("----------------------------------------")

    print(
        f"Total Portfolio: ₹{total_investment:.2f}"
    )


# ============================================================
# PORTFOLIO SUMMARY
# ============================================================

def portfolio_summary():

    if not portfolio:

        print("\n❌ Portfolio is empty.")
        return

    total_stocks = len(portfolio)

    total_shares = 0
    total_investment = 0

    for item in portfolio:

        total_shares += item[1]
        total_investment += item[3]

    average_investment = (
        total_investment / total_stocks
    )

    print("\n========================================")
    print("          PORTFOLIO SUMMARY")
    print("========================================")

    print(
        f"Different Stocks  : {total_stocks}"
    )

    print(
        f"Total Shares      : {total_shares}"
    )

    print(
        f"Total Investment  : ₹{total_investment:.2f}"
    )

    print(
        f"Average Investment: ₹{average_investment:.2f}"
    )
    
    
    
   # ============================================================
# GENERATE PORTFOLIO REPORT
# ============================================================

def generate_portfolio_report():

    print("\n========================================")
    print("          PORTFOLIO REPORT")
    print("========================================")

    if not portfolio:
        print("\n❌ Portfolio is empty.")
        return

    total_investment = 0
    total_current_value = 0

    print(
        f"\n{'Stock':<8}"
        f"{'Qty':<6}"
        f"{'Buy Price':<12}"
        f"{'Current':<12}"
        f"{'Investment':<14}"
        f"{'Current Value':<16}"
        f"{'P/L':<12}"
    )

    print("-" * 90)

    for item in portfolio:

        stock = item[0]
        quantity = item[1]
        buy_price = item[2]
        investment = item[3]

        current_price = current_prices.get(
            stock,
            buy_price
        )

        current_value = current_price * quantity

        profit_loss = (
            current_value - investment
        )

        total_investment += investment
        total_current_value += current_value

        print(
            f"{stock:<8}"
            f"{quantity:<6}"
            f"₹{buy_price:<11.2f}"
            f"₹{current_price:<11.2f}"
            f"₹{investment:<13.2f}"
            f"₹{current_value:<15.2f}"
            f"₹{profit_loss:<11.2f}"
        )

    overall_profit_loss = (
        total_current_value - total_investment
    )

    print("-" * 90)

    print(
        f"\nTotal Investment : "
        f"₹{total_investment:.2f}"
    )

    print(
        f"Current Value    : "
        f"₹{total_current_value:.2f}"
    )

    if overall_profit_loss > 0:

        print(
            f"Overall P/L      : "
            f"Profit ₹{overall_profit_loss:.2f}"
        )

    elif overall_profit_loss < 0:

        print(
            f"Overall P/L      : "
            f"Loss ₹{abs(overall_profit_loss):.2f}"
        )

    else:

        print(
            "Overall P/L      : ₹0.00"
        )

    print("\n========================================")
    
        # Save report to a text file
    with open("portfolio_report.txt", "w", encoding="utf-8") as file:

        file.write("PORTFOLIO REPORT\n")
        file.write("=" * 50 + "\n\n")

        for item in portfolio:

            stock = item[0]
            quantity = item[1]
            buy_price = item[2]
            investment = item[3]

            current_price = current_prices.get(
                stock,
                buy_price
            )

            current_value = current_price * quantity
            profit_loss = current_value - investment

            file.write(
                f"Stock: {stock}\n"
            )

            file.write(
                f"Quantity: {quantity}\n"
            )

            file.write(
                f"Buy Price: ₹{buy_price:.2f}\n"
            )

            file.write(
                f"Current Price: ₹{current_price:.2f}\n"
            )

            file.write(
                f"Investment: ₹{investment:.2f}\n"
            )

            file.write(
                f"Current Value: ₹{current_value:.2f}\n"
            )

            file.write(
                f"Profit/Loss: ₹{profit_loss:.2f}\n"
            )

            file.write("-" * 50 + "\n")

        file.write(
            f"\nTotal Investment: ₹{total_investment:.2f}\n"
        )

        file.write(
            f"Current Value: ₹{total_current_value:.2f}\n"
        )

        file.write(
            f"Overall Profit/Loss: ₹{overall_profit_loss:.2f}\n"
        )

    print("\n✅ Portfolio report saved successfully!")
    print("File: portfolio_report.txt")


# ============================================================
# PROFIT / LOSS
# ============================================================

def calculate_profit_loss():

    if not portfolio:

        print("\n❌ Portfolio is empty.")
        return

    print("\n========================================")
    print("            PROFIT / LOSS")
    print("========================================")

    total_invested = 0
    total_current_value = 0

    for item in portfolio:

        stock = item[0]
        quantity = item[1]
        buy_price = item[2]
        invested = item[3]

        current_price = current_prices[stock]

        current_value = (
            current_price * quantity
        )

        profit_loss = (
            current_value - invested
        )

        total_invested += invested
        total_current_value += current_value

        print(f"\nStock: {stock}")
        print(f"Quantity: {quantity}")
        print(f"Buy Price: ₹{buy_price}")
        print(f"Current Price: ₹{current_price}")
        print(f"Invested: ₹{invested}")
        print(f"Current Value: ₹{current_value}")

        if profit_loss > 0:

            print(
                f"Profit: ₹{profit_loss}"
            )

        elif profit_loss < 0:

            print(
                f"Loss: ₹{abs(profit_loss)}"
            )

        else:

            print("Profit/Loss: ₹0")

    overall_profit_loss = (
        total_current_value
        - total_invested
    )

    print("\n----------------------------------------")

    print(
        f"Total Invested: ₹{total_invested}"
    )

    print(
        f"Current Value: ₹{total_current_value}"
    )

    if overall_profit_loss > 0:

        print(
            f"Overall Profit: ₹{overall_profit_loss}"
        )

    elif overall_profit_loss < 0:

        print(
            f"Overall Loss: ₹{abs(overall_profit_loss)}"
        )

    else:

        print("Overall Profit/Loss: ₹0")


# ============================================================
# TRANSACTION HISTORY
# ============================================================

def transaction_history():

    print("\n========================================")
    print("          TRANSACTION HISTORY")
    print("========================================")

    if not transactions:

        print("\n❌ No transactions found.")
        return

    print(
        f"{'Date & Time':<20}"
        f"{'Action':<8}"
        f"{'Stock':<8}"
        f"{'Qty':<6}"
        f"{'Price':<10}"
        f"{'Value':<10}"
    )

    print("-" * 72)

    for transaction in transactions:

        date_time = transaction[0]
        action = transaction[1]
        stock = transaction[2]
        quantity = transaction[3]
        price = transaction[4]
        value = transaction[5]

        print(
            f"{date_time:<20}"
            f"{action:<8}"
            f"{stock:<8}"
            f"{quantity:<6}"
            f"₹{price:<9}"
            f"₹{value}"
        )
        
        
        # ============================================================
# TRANSACTION SUMMARY
# ============================================================

def transaction_summary():

    print("\n========================================")
    print("          TRANSACTION SUMMARY")
    print("========================================")

    if not transactions:

        print("\n❌ No transactions found.")
        return

    total_transactions = len(transactions)

    buy_count = 0
    sell_count = 0

    total_buy_value = 0
    total_sell_value = 0

    for transaction in transactions:

        action = transaction[1]
        value = transaction[5]

        if action == "BUY":

            buy_count += 1
            total_buy_value += value

        elif action == "SELL":

            sell_count += 1
            total_sell_value += value

    print(f"\nTotal Transactions : {total_transactions}")
    print(f"BUY Transactions   : {buy_count}")
    print(f"SELL Transactions  : {sell_count}")

    print(f"\nTotal Buy Value    : ₹{total_buy_value:.2f}")
    print(f"Total Sell Value   : ₹{total_sell_value:.2f}")

    print("\n========================================")
    
    
    
    # ============================================================
    # SAVE MARKET PRICES
    # ============================================================

def save_market_prices():

    try:

        with open(
            "market_prices.csv",
            "w",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Stock",
                "Current Price"
            ])

            for stock, price in current_prices.items():

                writer.writerow([
                    stock,
                    price
                ])

    except Exception as error:

        print("\n❌ Error saving market prices.")
        print(error)
        
        
        # ============================================================
# LOAD MARKET PRICES
# ============================================================

def load_market_prices():

    try:

        with open(
            "market_prices.csv",
            "r"
        ) as file:

            reader = csv.reader(file)

            next(reader, None)

            for row in reader:

                if len(row) == 2:

                    stock = row[0]
                    price = float(row[1])

                    if stock in current_prices:

                        current_prices[stock] = price

        print(
            "✅ Previous market prices loaded!"
        )

    except FileNotFoundError:

        pass

    except Exception as error:

        print("\n❌ Error loading market prices.")
        print(error)


# ============================================================
# SAVE PORTFOLIO
# ============================================================

def save_portfolio():

    try:

        with open(
            "portfolio.csv",
            "w",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Stock",
                "Quantity",
                "Price",
                "Investment"
            ])

            for item in portfolio:

                writer.writerow(item)

        print(
            "\n✅ Portfolio saved successfully!"
        )

    except Exception as error:

        print(
            "\n❌ Error while saving portfolio."
        )

        print(error)


# ============================================================
# SAVE TRANSACTIONS
# ============================================================

def save_transactions():

    try:

        with open(
            "transactions.csv",
            "w",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Date & Time",
                "Action",
                "Stock",
                "Quantity",
                "Price",
                "Value"
            ])

            for transaction in transactions:

                writer.writerow(transaction)

        print(
            "✅ Transactions saved successfully!"
        )

    except Exception as error:

        print(
            "\n❌ Error while saving transactions."
        )

        print(error)


# ============================================================
# LOAD PORTFOLIO
# ============================================================

def load_portfolio():

    try:

        with open(
            "portfolio.csv",
            "r"
        ) as file:

            reader = csv.reader(file)

            next(reader, None)

            for row in reader:

                if len(row) == 4:

                    stock = row[0]
                    quantity = int(row[1])
                    price = float(row[2])
                    investment = float(row[3])

                    existing_stock = False

                    for item in portfolio:

                        if item[0] == stock:

                            item[1] += quantity
                            item[3] += investment

                            existing_stock = True
                            break

                    if not existing_stock:

                        portfolio.append([
                            stock,
                            quantity,
                            price,
                            investment
                        ])

        if portfolio:

            print(
                "✅ Previous portfolio loaded successfully!"
            )

    except FileNotFoundError:

        pass

    except Exception as error:

        print(
            "\n❌ Error loading portfolio."
        )

        print(error)


# ============================================================
# LOAD TRANSACTIONS
# ============================================================

def load_transactions():

    try:

        with open(
            "transactions.csv",
            "r"
        ) as file:

            reader = csv.reader(file)

            next(reader, None)

            for row in reader:

                if len(row) == 6:

                    date_time = row[0]
                    action = row[1]
                    stock = row[2]
                    quantity = int(row[3])
                    price = float(row[4])
                    value = float(row[5])

                    transactions.append([
                        date_time,
                        action,
                        stock,
                        quantity,
                        price,
                        value
                    ])

        if transactions:

            print(
                "✅ Previous transaction history loaded!"
            )

    except FileNotFoundError:

        pass

    except Exception as error:

        print(
            "\n❌ Error loading transactions."
        )

        print(error)


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    while True:

        print("\n")

        print("========================================")
        print("       SMART STOCK PORTFOLIO TRACKER")
        print("========================================")
        
        print("0. Portfolio Dashboard")
        print("1. View Available Stocks")
        print("2. Buy Stock")
        print("3. Sell Stock")
        print("4. View Portfolio")
        print("5. Calculate Total Investment")
        print("6. Remove Stock")
        print("7. Update Stock Quantity")
        print("8. Search Stock")
        print("9. Portfolio Allocation")
        print("10. Portfolio Summary")
        print("11. Profit / Loss")
        print("12. Transaction History")
        print("13. Transaction Summary")
        print("14. Update Market Price")
        print("15. Save Portfolio")
        print("16. Save Transactions")
        print("17. Exit")
        print("18. Generate Portfolio Report")

        choice = input(
            "\nEnter your choice: "
        )

        if choice == "0":

            portfolio_dashboard()
               

        elif choice == "1":

            show_stocks()

        elif choice == "2":

            buy_stock()

        elif choice == "3":

            sell_stock()

        elif choice == "4":

            view_portfolio()

        elif choice == "5":

            calculate_total()

        elif choice == "6":

            remove_stock()

        elif choice == "7":

            update_stock()

        elif choice == "8":

            search_stock()

        elif choice == "9":

            portfolio_allocation()

        elif choice == "10":

            portfolio_summary()

        elif choice == "11":

            calculate_profit_loss()

        elif choice == "12":

            transaction_history()
            
        elif choice == "13":

            transaction_summary()
         
        elif choice == "14":

            update_market_price()

        elif choice == "15":

            save_portfolio()

        elif choice == "16":

            save_transactions()

        elif choice == "17":
                print("\nThank you for using Smart Stock Portfolio Tracker!")
                break

        elif choice == "18":
                generate_portfolio_report()
        else:
                print("\n❌ Invalid choice.")

        print(
            "Please select a number from 1 to 18."
        )
        
        
        
        # ============================================================
        # START APPLICATION
        # ============================================================

if __name__ == "__main__":

    load_portfolio()
    load_transactions()
    load_market_prices()

    main()