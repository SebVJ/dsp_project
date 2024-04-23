import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from pathlib import Path

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

# Get base URL to be scraped
base_url = 'https://www.edc.dk/soeg/?pageNr=1&kommune=Aarhus&edc=1'

# Initialize driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Open the first page
driver.get(base_url.format(1))

# Click accept to cookies
wait_cookie = WebDriverWait(driver, 5)
cookie_button = wait_cookie.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="OK"]')))
cookie_button.click()

# Switch off map
wait_map = WebDriverWait(driver, 10)
map_button = wait_map.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-checked="true"]')))
map_button.click()

# Initialize variables
addresses = []
postCodes = []
rooms_and_m2 = []
price = []
link = []
type = []
year_built = []
energy_rating = []
monthly_ownership_costs = []
technical_price = []
price_change = []
list_time = []
description = []

# Function to extract data from the current page
def extract_data_from_page():

    house_path = driver.find_elements(By.XPATH, '//address[@class="contents not-italic"]//h2 | //address[@class="contents not-italic"]//h3')

    # Iterate through each address and click
    for _ in range(len(house_path)):
        house_path = driver.find_elements(By.XPATH, '//address[@class="contents not-italic"]//h2 | //address[@class="contents not-italic"]//h3')
        address = house_path[_]
        driver.execute_script("arguments[0].click();", address)

        # Extract year built
        built_elements = driver.find_elements(By.XPATH,'//dt[@class="break-all" and text()="Byggeår"]/following-sibling::dd[1]')
        if built_elements:
            year_built.extend([built.text for built in built_elements])
        else:
            year_built.append("N/A")

        # Extract addresses
        address_elements = driver.find_elements(By.XPATH, '(//h1[contains(@class, "font-bold") and contains(@class, "md:style-h3")])[1]')
        if address_elements:
            addresses.extend([address.text for address in address_elements])
        else:
            addresses.append("N/A")

        # Extract post codes
        postCode_elements = driver.find_elements(By.XPATH, '(//span[@class="block md:text-primary-dusty"])[position() = 1]')
        if postCode_elements:
            postCodes.extend([postCode.text for postCode in postCode_elements])
        else:
            postCodes.append("N/A")

        # Extract rooms and m2
        rooms_and_m2_elements = driver.find_elements(By.XPATH, '(//span[@class="block md:text-primary-dusty  order-first md:order-last"]/span[2])[1]')
        if rooms_and_m2_elements:
            rooms_and_m2.extend([rooms_m2.text for rooms_m2 in rooms_and_m2_elements])
        else:
            rooms_and_m2.append("N/A")

        # Extract price
        price_elements = driver.find_elements(By.XPATH, '(//h2[contains(@class, "font-bold") and contains(@class, "md:style-h3")])[1]')
        if price_elements:
            price.extend([prices.text for prices in price_elements])
        else:
            price.append("N/A")

        # Extract Type 
        type_elements = driver.find_elements(By.XPATH, '(//span[@class="block md:text-primary-dusty  order-first md:order-last"])[1]')
        if type_elements:
            type.extend([types.text for types in type_elements])
        else:
            type.append("N/A")

        # Extract Energy rating
        energy_elements = driver.find_elements(By.XPATH, '//dt[@class="break-all" and text()="Energimærke"]/following-sibling::dd[1]')
        if energy_elements:
            energy_rating.extend([rating.text for rating in energy_elements])
        else:
            energy_rating.append("N/A")
            
        # Extract monthly ownership costs
        monthlyCosts_elements = driver.find_elements(By.XPATH, '//dt[text()="Ejerudgifter pr. md."]/following-sibling::*')
        if monthlyCosts_elements:
            monthly_ownership_costs.extend([rating.text for rating in monthlyCosts_elements])
        else:
            monthly_ownership_costs.append("N/A")

        # Extract technical price
        technicalPrice_elements = driver.find_elements(By.XPATH, '//dt[text()="Teknisk pris"]/following-sibling::*')
        if technicalPrice_elements:
            technical_price.extend([tech.text for tech in technicalPrice_elements])
        else:
            technical_price.append("N/A")

        # Extract price change
        priceChange_elements = driver.find_elements(By.XPATH, '//dt[@class="break-all" and text()="Prisudvikling"]/following-sibling::dd[1]')
        if priceChange_elements:
            price_change.extend([change.text for change in priceChange_elements])
        else:
            price_change.append("N/A")

        # Extract list time
        listTime_elements = driver.find_elements(By.XPATH, '//dt[@class="break-all" and text()="Liggetid"]/following-sibling::dd')
        if listTime_elements:
            list_time.extend([time.text for time in listTime_elements])
        else:
            list_time.append("N/A")

        description_element = driver.find_element(By.XPATH, '//div[@class="prose no-mb col-span-7 whitespace-pre-line lg:col-span-7"]')
        description_text = description_element.text
        description.append(description_text)


        driver.back()
        # Add wait time
        time.sleep(0.5)

# Iterate through each address and click
current_page = 1
max_pages = 1 # Set the maximum number of pages you want to scrape when testing

while True: # Set to 'True' when scraping all available pages
    # Extract data from the current page
    extract_data_from_page()

    try:
        next_page_button = driver.find_element(By.XPATH, '//button[@aria-label="Næste" and @aria-disabled="false"]')
        next_page_button.click()
        # Delay of 1.5 seconds
        time.sleep(3)
        current_page += 1
        print(current_page)
    except NoSuchElementException:
        # No more pages, break the loop
        break

driver.quit()

# Print the length of each list
'''
print("addresses list:", addresses)
print("postCodes list:", postCodes)
print("rooms_and_m2 list:", rooms_and_m2)
print("price list:", price)
print("link list:", link)
print("type list:", type)
print("year_built list:", year_built)
print("energy_rating list:", energy_rating)
print("monthly_ownership_costs list:", monthly_ownership_costs)
print("technical_price list:", technical_price)
print("price_change list:", price_change)
print("list_time list:", list_time)
print("Length of addresses list:", len(addresses))
print("Length of postCodes list:", len(postCodes))
print("Length of rooms_and_m2 list:", len(rooms_and_m2))
print("Length of price list:", len(price))
print("Length of link list:", len(link))
print("Length of type list:", len(type))
print("Length of year_built list:", len(year_built))
print("Length of energy_rating list:", len(energy_rating))
print("Length of monthly_ownership_costs list:", len(monthly_ownership_costs))
print("Length of technical_price list:", len(technical_price))
print("Length of price_change list:", len(price_change))
print("Length of list_time list:", len(list_time))
'''

df = pd.DataFrame({"Address": addresses, 
                   "Post Code": postCodes,
                   "Type": type, 
                   "Rooms & m2": rooms_and_m2, 
                   "Price": price,
                   "Year Built": year_built,
                   "Energy Rating": energy_rating,
                   "Monthly Ownership Costs": monthly_ownership_costs,
                   "Price Change": price_change,
                   "List Time": list_time,
                   "Description": description})


# Split post code into post code and city and drop original column
df[['Post Code', 'City']] = df['Post Code'].str.split(n=1, expand=True)

df = df.drop("Post Code", axis=1)

# Split rooms and m2 into room and m2 collumns and drop original column

df[['Rooms', 'm2']] = df['Rooms & m2'].str.extract(r'(\d+)\s*rum.*?(\d+)\s*m²', expand=True)

df = df.drop("Rooms & m2", axis=1)

# Alter type to drop room and m2 info

df["Type"] = df["Type"].str.split(' ').str[0]

# Split price into numeric and currency

df[["Price", "Currency"]] = df["Price"].str.split(' ', expand=True)

## Convert kr to dkk

df["Currency"] = df["Currency"].str.replace("kr.", "DKK")

# Remove currency from ownership costs

df["Monthly Ownership Costs"] =df["Monthly Ownership Costs"].str.replace(' kr.', '')

# Extract % change from price change

df["Price Change %"] = df["Price Change"].str.split(' ', n=1).str[0]

df = df.drop("Price Change", axis=1)

# Create derived columns
## Price per m2
df["Price"] = pd.to_numeric(df["Price"].str.replace('.', '',))
df["m2"] = pd.to_numeric(df["m2"])
df["Price per. m2"] = (df["Price"]/df["m2"]).round(0)

# Discretize price

# Define custom bin edges
bin_edges = [100000, 500000, 1000000, 1500000, 2000000, 2500000, 3000000, 3500000, 4000000, 30000000]

# Define bin labels
bin_labels = ['100000-500000', '500000-1000000', '1000000-1500000', '1500000-2000000', '2000000-2500000', 
              '2500000-3000000', '3000000-3500000', '3500000-4000000', '4000000<']

# Convert remaning numeric column to numeric

df["Monthly Ownership Costs"] = pd.to_numeric(df["Monthly Ownership Costs"].str.replace('.', ''))

# Create column

df["Price Category"] = pd.cut(df["Price"], bins=bin_edges, labels=bin_labels, include_lowest=True).str.replace('.', '')


print(df)

filePath = Path("/Users/sebastian/Documents/Selenium Project/Aarhus Kommune Real Estate data - Scraped from EDC.csv")
df.to_csv(filePath, encoding="utf-8", index=False, sep="\t")

