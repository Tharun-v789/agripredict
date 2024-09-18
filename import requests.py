

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import Select  

# Path to ChromeDriver
driver_path = "C:\Program Files (x86)\chromedriver.exe" 

# Setup Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless") # Run Chrome in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the driver
service1 = Service(driver_path)
driver = webdriver.Chrome(service=service1, options=chrome_options)

# Function to interact with date picker and commodity dropdown
def scrape_krama_reports():
    url = "https://krama.karnataka.gov.in/reports/DateWiseReport.aspx"
    driver.get(url)

    # Wait for the page to load completely
    wait = WebDriverWait(driver, 20)

    # Wait until the start date input is visible
    month_element = wait.until(EC.presence_of_element_located((By.ID, "_ctl0_content5_ddlmonth")))
    
    # Set the start date (modify the format based on what the input expects, e.g., "dd-mm-yyyy")
    
    select = Select(month_element)
    select.select_by_visible_text("SEPTEMBER")
    year_element = wait.until(EC.presence_of_element_located((By.ID, "_ctl0_content5_ddlyear")))
    select = Select(year_element)
    select.select_by_visible_text("2024")
 

    market_element = wait.until(EC.presence_of_element_located((By.ID, "_ctl0_content5_ddlmarket")))
    select = Select(market_element)
    select.select_by_visible_text("AllMarkets")
    # Select the commodity from the dropdown
    commodity_dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "_ctl0_content5_ddlcommodity"))))
    commodity_dropdown.select_by_visible_text("ONION")  # Example commodity

    # Submit the form to generate the report
    submit_button = driver.find_element(By.ID, "_ctl0_content5_viewreport")
    submit_button.click()

    # Wait for the table or report data to load
    wait.until(EC.presence_of_element_located((By.ID, "_ctl0_content5_gv")))  # Example table ID

    # Extract data from the table
    rows = driver.find_elements(By.XPATH, "//table[@id='_ctl0_content5_gv']/tbody/tr")
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        data = [column.text for column in columns]
        print(data)

# Run the scraping function
scrape_krama_reports()

# Close the browser after scraping
end = input("Press any key to exit")
driver.quit()
