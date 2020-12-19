# from bs4 import BeautifulSoup
import requests
import json
import csv
from utils import convert_epoch, hash_file, check_duplicate

# Must use API becuse we cannot extract data through HTMl
source = requests.get("https://www.nyse.com/api/ipo-center/calendar").text

# Open a CSV file to save the entries
csv_file = open('IPO_Filings.csv', 'w')
csv_output = csv.writer(csv_file)
csv_output.writerow(["Date Filed", "Company", "Ticker", "Industry", "Price"])

# Traverse JSON payload to get information
data_dict = json.loads(source)
companies_list = data_dict['calendarList']
for company in companies_list:
    # Get useful information from the filings
    issuer = company['issuer_nm']
    ticker = company['symbol']
    industry = company['custom_group_industry_nm']
    price_range = company['current_file_price_range_usd']
    date_filed = convert_epoch(company['init_file_dt']) # Change this to expected?

    if company['deal_status_desc'] == 'Filed': # This will need to be 'Expected' I think
        csv_output.writerow([date_filed, issuer, ticker, industry, price_range])

# Close the file
csv_file.close()

# Call function to hash current file
hash_number = hash_file()

# Call function to check if this hash already exists
check_duplicate(hash_number)
