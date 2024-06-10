import requests
from bs4 import BeautifulSoup
import re

def get_details(product_name, url, headers, cls_product, cls_name, cls_price):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        product = soup.find(cls_product)
        if not product:
            raise ValueError("Product container not found")
        name = product.find(cls_name).get_text()
        price = product.find(cls_price).get_text()
        price = re.sub(r'[^\d]', '', price)
        return name, float(price), url
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None

def compare_prices(flipkart_details, amazon_details, tatacliq_details):
    prices = []
    if flipkart_details[1]:
        prices.append((flipkart_details[0], flipkart_details[1], flipkart_details[2]))
    if amazon_details[1]:
        prices.append((amazon_details[0], amazon_details[1], amazon_details[2]))
    if tatacliq_details[1]:
        prices.append((tatacliq_details[0], tatacliq_details[1], tatacliq_details[2]))

    prices.sort(key=lambda x: x[1])  # Sort by price
    return prices

def main():
    product_name = input("Enter the name of the product: ")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    flipkart_url = f"https://www.flipkart.com/search?q={'+'.join(product_name.split())}"
    amazon_url = f"https://www.amazon.com/s?k={'+'.join(product_name.split())}"
    tatacliq_url = f"https://www.tatacliq.com/search/?searchCategory=all&text={'+'.join(product_name.split())}"

    flipkart_details = get_details(product_name, flipkart_url, headers, '_1AtVbE', 'IRpwTa', '_30jeq3')
    amazon_details = get_details(product_name, amazon_url, headers, 's-search-result', 'a-size-base-plus', 'a-price')
    tatacliq_details = get_details(product_name, tatacliq_url, headers, None, 'product-title', 'value')

    best_deal = compare_prices(flipkart_details, amazon_details, tatacliq_details)

    if best_deal:
        print("Best deal found:")
        best = best_deal[0]
        print(f"{best[0]}: {best[1]} - ₹{best[2]}")
        if best[0] == 'Flipkart':
            print(f"Link: {flipkart_details[2]}")
        elif best[0] == 'Amazon':
            print(f"Link: {amazon_details[2]}")
        elif best[0] == 'TataCliq':
            print(f"Link: {tatacliq_details[2]}")
    else:
        print("No details found for the given product.")

if __name__ == "__main__":
    main()