import statistics
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from assertpy import assert_that
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import pysnooper

# options = Options()
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--start-maximized')
options.add_argument('--disable-notifications')
options.add_argument('--disable-infobars')
DRIVER_PATH = "C:/Users/USER/PycharmProjects/PythonSelenium/drivers/chromedriver.exe"
# create a Service object
service = Service(executable_path=DRIVER_PATH)
# create a driver object
# driver = webdriver.Chrome(service=service, options=options)
# driver = webdriver.Edge(EdgeChromiumDriverManager().install())
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
driver.get("https://www.saucedemo.com/")
# driver.maximize_window()



# Login
@pysnooper.snoop()
def test_login_sauce_labs():
    # Login page
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user-name")))
    username = driver.find_element(By.ID, "user-name")
    username.send_keys("standard_user")
    password = driver.find_element(By.ID, "password")
    password.send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    assert driver.current_url == "https://www.saucedemo.com/inventory.html"


# Add to cart
def test_add_cart_sauce_labs():
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    assert_that(driver.find_element(By.ID, "remove-sauce-labs-backpack").text).is_equal_to("Remove")
    EC.text_to_be_present_in_element((By.ID, "remove-sauce-labs-backpack"), "Remove")
    price = driver.find_element(By.CLASS_NAME, "inventory_item_price").text.replace("$", "").strip()
    assert_that(price).is_equal_to_ignoring_case("29.99")
    print(price)


# count inventory items
def test_count_inventory_items():
    inventory_items = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert_that(len(inventory_items)).is_equal_to(6)


# select last inventory item
def test_select_last_inventory_item():
    inventory_items = driver.find_elements(By.CLASS_NAME, "inventory_item")
    last_iterm = inventory_items[-1]
    last_iterm.click()
    print(last_iterm.text)
    assert_that(driver.page_source).contains("Test.allTheThings() T-Shirt (Red)")


# add last item to cart
def test_add_last_item_to_cart():
    """add last item to cart"""
    add_button = driver.find_element(By.XPATH, "//*[@id='add-to-cart-test.allthethings()-t-shirt-(red)']")
    assert_that(add_button.text).is_equal_to("Add to cart")
    add_button.click()
    remove_button = driver.find_element(By.XPATH, "//*[@id='remove-test.allthethings()-t-shirt-(red)']")
    assert_that(remove_button.text).is_equal_to("Remove")


# remove last item from cart
def test_count_all_inventory_items():
    """count all items"""
    inventory_items = driver.find_element(By.CSS_SELECTOR, "div[class='inventory_list']")
    assert_that(len(inventory_items.find_elements(By.CLASS_NAME, "inventory_item"))).is_equal_to(6)


# print all items text
def test_print_all_items_text():
    """list of items"""
    item_desc = driver.find_elements(By.CLASS_NAME, "inventory_item_description")
    for item in item_desc:
        print(item.text.replace("Add to cart", " ").replace("Remove", " ") + "\n\n")
        assert_that(item.text).is_not_empty()


# print all prices
def test_print_all_price():
    """list of prices"""
    prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    for price in prices:
        print(price.text.replace("$", "").strip() + "\n\n")
        assert_that(price.text).is_not_empty()


# print min price
# @pysnooper.snoop()
def test_print_min_price():
    """min of prices"""
    try:
        all_prices = driver.find_elements(By.CLASS_NAME, "pricebar")
        prices = [float(price.text.strip("$Add to cartRemove").strip()) for price in all_prices]
        min_price = min(prices)
        print("The min price is {}: ".format(min_price))
    except Exception as e:
        print("Error: {}".format(e))


def test_print_max_price():
    """max of prices"""
    try:
        max_prices_list = driver.find_elements(By.CLASS_NAME, "pricebar")
        prices = [float(price.text.strip("$Add to cartRemove").strip()) for price in max_prices_list]
        print("The maximum price is: {}".format(max(prices)))
    except Exception as ex_ceptions:
        print("Error: {}".format(ex_ceptions))


# print average price
def test_print_average_price():
    """average of prices"""
    try:
        average_prices_list = driver.find_elements(By.CLASS_NAME, "pricebar")
        prices = [float(price.text.strip("$Add to cartRemove").strip()) for price in average_prices_list]
        print("The average price is: {}".format(sum(prices) / len(prices)))
    except Exception as ex_ceptions:
        print("Error: {}".format(ex_ceptions))


# print sum price
def test_print_sum_price():
    """sum of prices"""
    try:
        sum_prices_list = driver.find_elements(By.CLASS_NAME, "pricebar")
        prices = [float(price.text.strip("$Add to cartRemove").strip()) for price in sum_prices_list]
        print("The sum of prices is: {}".format(sum(prices)))
    except Exception as ex_ceptions:
        print("Error: {}".format(ex_ceptions))


def test_median_price():
    """median of prices"""
    try:
        median_prices_list = driver.find_elements(By.CLASS_NAME, "pricebar")
        prices = [float(price.text.strip("$Add to cartRemove").strip()) for price in median_prices_list]
        print("The median of prices is: {}".format(statistics.median(prices)))
    except Exception as ex_ceptions:
        print("Error: {}".format(ex_ceptions))