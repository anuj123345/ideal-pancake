import os
import webbrowser

def generate_amazon_url(product_name):
    base_url = "https://www.amazon.com/s?k="
    product_name = "+".join(product_name.split())
    return base_url + product_name

def open_url_in_terminal(url):
    if os.name == 'nt':  # For Windows
        os.system(f"start {url}")
    elif os.name == 'posix':  # For Linux/MacOS
        os.system(f"xdg-open {url}")

def main():
    product_name = input("Enter the name of the product: ")
    url = generate_amazon_url(product_name)
    print("Generated Amazon URL:", url)

    # Open the generated URL in the default web browser
    webbrowser.open_new_tab(url)

    try:
        open_url_in_terminal(url)
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
