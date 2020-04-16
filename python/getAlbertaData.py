
import requests 
from contextlib import closing
import csv
import sqlite3
from bs4 import BeautifulSoup
import pandas as pd
import pymysql
from sshtunnel import SSHTunnelForwarder


#csv file download link
url = "https://www.alberta.ca/covid-19-alberta-data.aspx"

# get the csv
response = requests.get(url, stream=True)

# Throw an error for bad status codes
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

rows = soup.find("tbody").find_all("tr")

parsedData = []


for row in rows:

    parsedData.append(row.get_text())

sql_hostname = '127.0.0.1'
sql_username = 'covicivy'
sql_password = 'e#3(f$vL1MRq'
sql_main_database = 'covicivy_covidCasesInCanada'
sql_port = 3306
ssh_host = 'server178.web-hosting.com'
ssh_user = 'covicivy'
ssh_port = 21098
sql_ip = '127.0.0.1'


with SSHTunnelForwarder(
    (ssh_host, ssh_port),
    ssh_username=ssh_user,
    ssh_password= sql_password,
    remote_bind_address=(sql_hostname, sql_port)) as tunnel:
        conn = pymysql.connect(host='127.0.0.1', user=sql_username,
        passwd=sql_password, db=sql_main_database,
        port=tunnel.local_bind_port)
    
    
        try:


            with conn.cursor() as cursor:
    
                i=2

                while i < len(parsedData):
                    row = parsedData[i].strip('-').split('\n')

                    print(row)
                    dataIn = (row[2].strip('In '), row[1].strip())

                    i += 1
                                    
                    sql = """UPDATE CovidCasesAlberta SET `NumberOfCases` =  %s WHERE (`RegionName` = %s);"""
                    cursor.execute(sql, dataIn )

                    conn.commit()
        finally:
            conn.close()

