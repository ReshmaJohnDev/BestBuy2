import sys
import products
import store
import promotions


# ANSI color codes for styling
BRIGHT_CYAN = '\033[96m'
BRIGHT_GREEN = '\033[92m'
RED = '\033[31m'
RESET = '\033[0m'


def start(best_buy):
    """Displays Store menu and process orders"""
    menus = {1: "List all products in store ",
             2: "Show total amount in store",
             3: "Make an order",
             4: "Quit"
             }
    while True:
        print(f"Store Menu\n{'_' * 10}")
        for option, menu in menus.items():
            print(f"{BRIGHT_GREEN}{option}{RESET}.{menu}")
        print()
        try:
            user_choice = int(input("Please choose a number: "))
            if user_choice == 1:
                    list_products(best_buy)
            elif user_choice == 2:
                    get_total_products(best_buy)
            elif user_choice == 3:
                store_available_product_list = best_buy.get_all_products()
                process_order(best_buy, store_available_product_list)
            elif user_choice == 4:
                sys.exit()
            else:
                print(f"{RED}Invalid input. Please enter valid number.{RESET}\n")
                continue
        except ValueError:
            print(f"{RED}Please enter a valid choice{RESET}\n")

        except products.InvalidQuantityError as error_message:
            print(f"{RED}{error_message}{RESET}\n")

        except products.InsufficientStockError as error_message:
            print(f"{RED}{error_message}{RESET}\n")


def process_order(best_buy, store_available_product_list):
    """Handles the order process, allowing users to purchase products."""
    list_products(best_buy)
    print("When you want to finish order, enter empty text.")
    buy_list = []
    while True:
        product_number = input("Which product # do you want? ").strip()
        if not product_number: # Exit product when Enter is pressed
            break
        try:
            product_number = int(product_number)
            if  not 0<= product_number <= len(store_available_product_list)  :
                print(f"{RED}Invalid product number {product_number}."
                      f"Please enter valid product number{RESET}\n")
                continue
            product_amount = input("What amount do you want? ").strip()
            if not product_amount.isdigit() or int(product_amount) <= 0:
                print(f"{RED}Invalid quantity. Please enter a positive number.{RESET}\n")
                continue
            product_amount = int(product_amount)
            buy_list.append((product_number -1, product_amount))
            print(f"{BRIGHT_GREEN}Product added to list!{RESET}")

        except ValueError:
            print(f"{RED}Invalid input. Please enter numbers for product"
                  f" and amount.{RESET}\n")
    make_order(best_buy, buy_list)


def list_products(best_buy):
    """Displays all available products in the store"""
    product_list = best_buy.get_all_products()
    print('_' * 10)
    for index, product in enumerate(product_list):
        print(f"{BRIGHT_GREEN}{index + 1}{RESET}. {product.show()}")
    print('_' * 10)
    print()


def get_total_products(best_buy):
    """Displays the total available products in store"""
    total_quantity = best_buy.get_total_quantity()
    print(f"Total of {BRIGHT_GREEN}{total_quantity}{RESET} items in the store ")
    print()


def make_order(best_buy, buy_list):
    """Processes the order and displays the total price."""
    total_price = best_buy.order(buy_list)
    if total_price > 0:
        print(f"Order made! Total payment: {BRIGHT_GREEN}${total_price}{RESET}")
    else:
        print(f"{RED}Order failed. No payment was processed due to above error.{RESET}")


def main():
    """Initializes store products and handles user choices """
    #setup initial stock of inventory
    try:
        # setup initial stock of inventory

        product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                        products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                        products.Product("Google Pixel 7", price=500, quantity=250),
                        products.NonStockedProduct("Windows License", price=125),
                        products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
                        ]

        best_buy = store.Store([])
        for product in product_list:
            #checks for duplicates and adds products
            best_buy.add_product(product)

        # Create promotion catalog
        second_half_price = promotions.SecondHalfPrice("Second Half price!")
        third_one_free = promotions.ThirdOneFree("Third One Free!")
        thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

        # Add promotions to products
        product_list[0].promotion = second_half_price
        product_list[1].promotion = third_one_free
        product_list[3].promotion = thirty_percent

        #invoke start method
        start(best_buy)
    except ValueError as error_message:
        print(f"{RED}{error_message}{RESET}")


if __name__ == "__main__":
    main()
