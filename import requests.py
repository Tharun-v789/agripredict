

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import Select  

COLUMN_NAMES = "Market	Date	Variety	Grade	Arrivals	Unit	Min	Max	Modal	District".split()
MARKETS = ["BENGALURU", "HUBBALI", "MYSURU", "DODDABALLAPUR"]
MONTHS = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]
YEARS = [2002, 2024]

# Function to interact with date picker and commodity dropdown
def scrape_krama_report(month, year, market, commodity):
    print(f"Scraping data for {month} {year} in {market} market for {commodity}...")
    ALL_DATA = []

    url = "https://krama.karnataka.gov.in/reports/DateWiseReport.aspx"
    driver.get(url)

    # Wait for the page to load completely
    wait = WebDriverWait(driver, 20)

    # Wait until the start date input is visible
    month_element = wait.until(EC.presence_of_element_located((By.ID, "_ctl0_content5_ddlmonth")))
    
    # Set the start date (modify the format based on what the input expects, e.g., "dd-mm-yyyy")
    select = Select(month_element)
    select.select_by_visible_text(month)
    year_element = wait.until(EC.presence_of_element_located((By.ID, "_ctl0_content5_ddlyear")))
    select = Select(year_element)
    select.select_by_visible_text(year)

    market_element = wait.until(EC.presence_of_element_located((By.ID, "_ctl0_content5_ddlmarket")))
    select = Select(market_element)
    select.select_by_visible_text(market)
    
    # Select the commodity from the dropdown
    commodity_dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "_ctl0_content5_ddlcommodity"))))
    commodity_dropdown.select_by_visible_text(commodity)  # Example commodity

    # Submit the form to generate the report
    submit_button = driver.find_element(By.ID, "_ctl0_content5_viewreport")
    submit_button.click()

    # Wait for the table or report data to load
    wait.until(EC.presence_of_element_located((By.ID, "_ctl0_content5_gv")))  # Example table ID

    # Extract data from the table
    rows = driver.find_elements(By.XPATH, "//table[@id='_ctl0_content5_gv']/tbody/tr")
    prev = ""
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        data = [column.text for column in columns]
        if len(data) != 10 or len(data[1]) != 10:
            continue
        if data[0]:
            prev = data[0]
        else:
            data[0] = prev
        ALL_DATA.append(data)

    # Add ALL_DATA to csv file
    with open("krama_report.csv", "a") as f:
        for data in ALL_DATA:
            f.write(",".join(data) + "\n")
    

# Run the scraping function
# scrape_krama_report("SEPTEMBER", "2023", "BENGALURU", "ONION")

def get_all_reports():
    print(COLUMN_NAMES)
    for market in MARKETS:
        for year in range(YEARS[0], YEARS[1] + 1):
            for month in MONTHS:
                scrape_krama_report(month, str(year), market, "ONION")



if __name__ == "__main__":

    with open("krama_report.csv", "w") as f:
        f.write(",".join(COLUMN_NAMES) + "\n")

    # Path to ChromeDriver
    driver_path = "C:\Program Files (x86)\chromedriver.exe" 

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the driver
    service1 = Service(driver_path)
    driver = webdriver.Chrome(service=service1, options=chrome_options)

    # Get all the reports pertaining to Onions
    get_all_reports()

    # Close the browser after scraping
    end = input("Press any key to exit")
    driver.quit()