import requests 
from contextlib import closing
import csv
import sqlite3
from bs4 import BeautifulSoup

url = "https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/"

# get the csv
response = requests.get(url, stream=True)
# Throw an error for bad status codes
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')
row = soup.find(class_="contenttable")

for p in row.find_all("p"):
    print(p.getText())
  