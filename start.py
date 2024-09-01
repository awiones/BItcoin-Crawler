import random
import string
import time
import sys
import os

from colorama import Fore, Style, init

# Initialize colorama
init()

# Directory and file for storing data
DATA_DIR = 'data'
DATA_FILE = os.path.join(DATA_DIR, 'total_money.txt')

# Conversion rates
BTC_TO_USD = 58247.89  # Updated rate
ETH_TO_USD = 2477.85   # Updated rate

# Global variables to track total BTC and ETH
total_btc = 0.0
total_eth = 0.0

# List of fake websites for the crawling
WEBSITES = [
    "Blockchain.com",
    "Kraken.com",
    "BitPay.com",
    "Binance.com",
    "Coinbase.com"
]

def load_total_money():
    """Load the total money from the file."""
    global total_btc, total_eth
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            try:
                data = file.read().strip().split(',')
                total_btc = float(data[0])
                total_eth = float(data[1])
                print(f"DEBUG: Loaded total BTC: {total_btc}, total ETH: {total_eth}")
            except (ValueError, IndexError):
                total_btc = 0.0
                total_eth = 0.0
                print(f"DEBUG: Failed to load total_money from file. Set to BTC: 0.0, ETH: 0.0")

def save_total_money():
    """Save the total money to the file."""
    with open(DATA_FILE, 'w') as file:
        file.write(f"{total_btc:.2f},{total_eth:.2f}")
    print(f"DEBUG: Saved total_money to file: BTC {total_btc:.2f}, ETH {total_eth:.2f}")

def generate_random_bitcoin_address(length=34):
    """Generate a random fake Bitcoin address."""
    chars = string.ascii_letters + string.digits
    address = '1' + ''.join(random.choice(chars) for _ in range(length - 1))
    return address

def generate_random_ethereum_address(length=42):
    """Generate a random fake Ethereum address."""
    chars = string.hexdigits.lower()
    address = '0x' + ''.join(random.choice(chars) for _ in range(length - 2))
    return address

def generate_random_btc_amount():
    """Generate a random fake BTC amount."""
    return round(random.uniform(0.0001, 10.0), 4)

def generate_random_eth_amount():
    """Generate a random fake ETH amount."""
    return round(random.uniform(0.001, 100.0), 4)

def convert_to_usd(amount, crypto_type):
    """Convert cryptocurrency amount to USD."""
    if crypto_type == "BTC":
        return amount * BTC_TO_USD
    elif crypto_type == "ETH":
        return amount * ETH_TO_USD
    return 0.0

def generate_fake_btc_crawl_info():
    """Generate a fake Bitcoin address crawl info message with a rare valid address."""
    global total_btc
    website_name = random.choice(WEBSITES)
    bitcoin_address = generate_random_bitcoin_address()
    btc_amount = generate_random_btc_amount()
    
    # Rare chance to generate a 'valid' address
    is_valid = random.random() < 0.05  # 5% chance of being valid
    if is_valid:
        bitcoin_address = generate_random_bitcoin_address()
        btc_amount = generate_random_btc_amount()
        total_btc += btc_amount  # Add to total BTC
        save_total_money()  # Save total money to file
        result_message = f"{Fore.GREEN}From {website_name} | {bitcoin_address} Found {btc_amount} BTC{Style.RESET_ALL}"
    else:
        result_message = f"{Fore.RED}From {website_name} | {bitcoin_address} Not valid | No funds found.{Style.RESET_ALL}"
    
    return result_message

def generate_fake_eth_crawl_info():
    """Generate a fake Ethereum address crawl info message with a rare valid address."""
    global total_eth
    website_name = random.choice(WEBSITES)
    ethereum_address = generate_random_ethereum_address()
    eth_amount = generate_random_eth_amount()
    
    # Rare chance to generate a 'valid' address
    is_valid = random.random() < 0.05  # 5% chance of being valid
    if is_valid:
        ethereum_address = generate_random_ethereum_address()
        eth_amount = generate_random_eth_amount()
        total_eth += eth_amount  # Add to total ETH
        save_total_money()  # Save total money to file
        result_message = f"{Fore.CYAN}From {website_name} | {ethereum_address} Found {eth_amount} ETH{Style.RESET_ALL}"
    else:
        result_message = f"{Fore.RED}From {website_name} | {ethereum_address} Not valid | No funds found.{Style.RESET_ALL}"
    
    return result_message

def print_menu():
    """Print the menu with a fixed border."""
    global total_btc, total_eth
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    load_total_money()
    
    menu_border = "+------------------------------------------------+"
    content_width = 48
    print(f"{Fore.CYAN}{menu_border}")
    print(f"{Fore.CYAN}|{' ' * content_width}|")
    print(f"{Fore.CYAN}|  Welcome to Crawling Bitcoin!{' ' * (content_width - 30)}|")
    print(f"{Fore.CYAN}|  Made By: Awiones{' ' * (content_width - 18)}|")
    print(f"{Fore.CYAN}|  Your current Total BTC: {total_btc:9.2f} BTC{' ' * (content_width - 39)}|")
    print(f"{Fore.CYAN}|  Your current Total ETH: {total_eth:9.2f} ETH{' ' * (content_width - 39)}|")
    print(f"{Fore.CYAN}|{' ' * content_width}|")
    print(f"{Fore.CYAN}{menu_border}")
    print(f"{Fore.MAGENTA}1. Crawl Bitcoin Addresses{Style.RESET_ALL}")
    print(f"{Fore.BLUE}2. Crawl Ethereum Addresses{Style.RESET_ALL}")
    print(f"{Fore.RED}3. Exit{Style.RESET_ALL}")


def display_menu():
    """Display the menu and handle user choice."""
    print_menu()
    choice = input("\nPlease choose an option (1/2/3): ")
    if choice in ['1', '2']:
        num_crawls = input(f"\nHow many times do you want to crawl? (Enter a number): ")
        if num_crawls.isdigit() and int(num_crawls) > 0:
            start_crawling(choice, int(num_crawls))
        else:
            print(f"{Fore.RED}Invalid number of crawls. Please enter a positive integer.{Style.RESET_ALL}")
            display_menu()
    elif choice == '3':
        print(f"{Fore.GREEN}Exiting...{Style.RESET_ALL}")
        sys.exit(0)
    else:
        print(f"{Fore.RED}Invalid choice, please try again.{Style.RESET_ALL}")
        display_menu()

def start_crawling(crypto_choice, num_crawls):
    """Start the crawling process."""
    global total_btc, total_eth
    if crypto_choice == '1':
        crypto_type = "BTC"
        crypto_name = "Bitcoin"
        generate_fake_info = generate_fake_btc_crawl_info
    elif crypto_choice == '2':
        crypto_type = "ETH"
        crypto_name = "Ethereum"
        generate_fake_info = generate_fake_eth_crawl_info

    print(f"\n{Fore.GREEN}Starting {crypto_name} crawling...{Style.RESET_ALL}")

    # Simulate crawling
    try:
        for _ in range(num_crawls):
            print(generate_fake_info())
            time.sleep(1)  # Simulate crawl time
    except KeyboardInterrupt:
        pass

    # Clear the line before printing final result
    sys.stdout.write('\r' + ' ' * 80 + '\r')
    sys.stdout.flush()
    print(f"{Fore.GREEN}Crawling finished!{Style.RESET_ALL}")
    
    # Compute total money in USD
    total_btc_usd = total_btc * BTC_TO_USD
    total_eth_usd = total_eth * ETH_TO_USD
    total_money_usd = total_btc_usd + total_eth_usd

    # Print the results
    if crypto_choice == '1':
        print(f"Total BTC collected: {total_btc:.2f} BTC")
        print(f"Total money collected: BTC {total_btc:.2f} (${total_btc_usd:,.2f} USD)")
    elif crypto_choice == '2':
        print(f"Total ETH collected: {total_eth:.2f} ETH")
        print(f"Total money collected: ETH {total_eth:.2f} (${total_eth_usd:,.2f} USD)")

    # Return to the menu
    input("\nPress Enter to return to the menu.")
    display_menu()

if __name__ == "__main__":
    display_menu()
