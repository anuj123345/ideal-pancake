import webbrowser

def generate_tatacliq_url(product_name):
    base_url = "https://www.tatacliq.com/search/?searchCategory=all&text="
    product_name = "+".join(product_name.split())
    return base_url + product_name

def main():
    product_name = input("Enter the name of the product: ")
    url = generate_tatacliq_url(product_name)
    print("Generated TataCliq URL:", url)

    # Open the generated URL in the default web browser
    try:
        webbrowser.open_new_tab(url)
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
