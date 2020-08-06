from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.lazada.vn/products/711886096.html")
element = driver.find_element_by_class_name('pdp-mod-product-badge-title')
print(element.text)
driver.close()
