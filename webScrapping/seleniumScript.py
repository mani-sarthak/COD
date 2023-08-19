from selenium import webdriver

# Set the path to your ChromeDriver executable
chromedriver_path = '/Users/manisarthak/Downloads/chromedriver-mac-arm64/chromedriver'

# Create a new Chrome browser instance
driver = webdriver.Chrome(executable_path=chromedriver_path)


url = "https://indiawris.gov.in/wris/#/groundWater"  # Replace with the actual URL
driver.get(url)


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Wait for an element with a specific ID to be present (adjust as needed)
element = WebDriverWait(driver, 100).until(
    EC.presence_of_element_located((By.ID, "element-id"))
)


data = element.text
print(data)


driver.quit()
