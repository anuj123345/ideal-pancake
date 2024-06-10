import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def generate_flipkart_url(product_name):
    base_url = "https://www.flipkart.com/search?q="
    product_name = "+".join(product_name.split())
    return base_url + product_name

def generate_amazon_url(product_name):
    base_url = "https://www.amazon.com/s?k="
    product_name = "+".join(product_name.split())
    return base_url + product_name

def generate_tatacliq_url(product_name):
    base_url = "https://www.tatacliq.com/search/?searchCategory=all&text="
    product_name = "+".join(product_name.split())
    return base_url + product_name

def get_flipkart_details(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(5)  # Wait for the page to load
    
    try:
        product = driver.find_element(By.CLASS_NAME, '_1fQZEK')
        name = product.find_element(By.CLASS_NAME, '_4rR01T').text
        price = product.find_element(By.CLASS_NAME, '_30jeq3._1_WHN1').text
        price = price.replace('₹', '').replace(',', '').strip()
        driver.quit()
        return name, float(price)
    except Exception as e:
        driver.quit()
        return None, None

def get_amazon_details(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(5)  # Wait for the page to load
    
    try:
        product = driver.find_element(By.CSS_SELECTOR, 'span.a-size-medium.a-color-base.a-text-normal')
        name = product.text
        price = driver.find_element(By.CSS_SELECTOR, 'span.a-price-whole').text
        price = price.replace(',', '').strip()
        driver.quit()
        return name, float(price)
    except Exception as e:
        driver.quit()
        return None, None

def get_tatacliq_details(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(5)  # Wait for the page to load
    
    try:
        product = driver.find_element(By.CLASS_NAME, 'ProductModule__productName')
        name = product.text
        price = driver.find_element(By.CLASS_NAME, 'ProductPrice__price').text
        price = price.replace('₹', '').replace(',', '').strip()
        driver.quit()
        return name, float(price)
    except Exception as e:
        driver.quit()
        return None, None

def compare_prices(flipkart_details, amazon_details, tatacliq_details):
    prices = []
    if flipkart_details[1]:
        prices.append(('Flipkart', flipkart_details[0], flipkart_details[1]))
    if amazon_details[1]:
        prices.append(('Amazon', amazon_details[0], amazon_details[1]))
    if tatacliq_details[1]:
        prices.append(('TataCliq', tatacliq_details[0], tatacliq_details[1]))

    prices.sort(key=lambda x: x[2])  # Sort by price
    return prices

def main():
    product_name = input("Enter the name of the product: ")

    flipkart_url = generate_flipkart_url(product_name)
    amazon_url = generate_amazon_url(product_name)
    tatacliq_url = generate_tatacliq_url(product_name)

    flipkart_details = get_flipkart_details(flipkart_url)
    amazon_details = get_amazon_details(amazon_url)
    tatacliq_details = get_tatacliq_details(tatacliq_url)

    if flipkart_details[1] or amazon_details[1] or tatacliq_details[1]:
        best_deal = compare_prices(flipkart_details, amazon_details, tatacliq_details)
        print("Best deal found:")
        for deal in best_deal:
            print(f"{deal[0]}: {deal[1]} - ₹{deal[2]}")
    else:
        print("No details found for the given product.")

if __name__ == "__main__":
    main()
