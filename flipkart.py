import os
import requests
from bs4 import BeautifulSoup
import webbrowser

def generate_flipkart_url(product_name):
    base_url = "https://www.flipkart.com/"
    query = "search?q="
    product_name = "+".join(product_name.split())
    return base_url + query + product_name

def fetch_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the product title
    product_title_elem = soup.find("span", {"class": "B_NuCI"})
    product_title = product_title_elem.get_text() if product_title_elem else "Title not found"

    # Find the category
    category_elem = soup.find("a", {"class": "_2whKao"})
    category = category_elem.get_text() if category_elem else "Category not found"

    # Find the item specifications
    specs = soup.find_all("div", {"class": "_3Rrcbo"})
    item_specs = {}
    for spec in specs:
        key_elem = spec.find("div", {"class": "_2lzn0o"})
        value_elem = spec.find("div", {"class": "_1qKb_B"})
        if key_elem and value_elem:
            key = key_elem.get_text()
            value = value_elem.get_text()
            item_specs[key] = value

    return product_title, category, item_specs

def open_url_in_terminal(url):
    if os.name == 'nt':  # For Windows
        os.system(f"start {url}")
    elif os.name == 'posix':  # For Linux/MacOS
        os.system(f"xdg-open {url}")

def main():
    product_name = input("Enter the name of the product: ")
    url = generate_flipkart_url(product_name)
    print("Generated Flipkart URL:", url)

    try:
        # Fetch product details if the URL is for a specific product
        if 'search' not in url:
            product_title, category, item_specs = fetch_product_details(url)
            print("\nProduct Title:", product_title)
            print("Category:", category)
            print("Item Specifications:")
            for key, value in item_specs.items():
                print(key + ":", value)
        else:
            print("This is a search URL. Opening in browser...")
            open_url_in_terminal(url)
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
