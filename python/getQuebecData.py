import requests 
from contextlib import closing
import csv
import sqlite3
from bs4 import BeautifulSoup
import mysql.connector

url = "https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/"

# get the csv
response = requests.get(url, stream=True)
# Throw an error for bad status codes
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')
row = soup.find(class_="contenttable")

mydb = mysql.connector.connect(
  host="localhost",
  user="covicivy_sql",
  passwd="8bMpNo862hl{",
  database="covicivy_covidCasesInCanada"
)

mycursor = mydb.cursor()

for p in row.find_all("p"):
    print(p.getText())
  